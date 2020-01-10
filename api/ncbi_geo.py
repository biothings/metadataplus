''' Add structured schema.org Dataset metadata to NCBI GEO data series page. '''

import json
import logging
import os
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.routing
import tornado.web
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from tornado.options import options
import api.config
import elasticsearch
# from crawler.spiders import NCBIGeoSpider

client = elasticsearch.Elasticsearch(api.config.ES_HOST)


async def transform(doc, url, identifier):

    mappings = {
        "Title": "name",
        "Organism": "organism",
        "Experiment type": "measurementTechnique",
        "Summary": "description",
        "Contributor(s)": lambda value: {
            "creator": [{
                "@type": "Person",
                "name": individual
            } for individual in value.split(', ')]
        },
        "Submission date": "datePublished",
        "Last update date": "dateModified",
        "Organization": lambda value: {
            "publisher": {
                "@type": "Organization",
                "name": value
            }
        },
    }
    _doc = {
        "@context": "http://schema.org/",
        "@type": "Dataset",
        "identifier": identifier,
        "distribution": {
            "@type": "dataDownload",
            "contentUrl": url
        },
        "includedInDataCatalog": {
            "@type": "DataCatalog",
            "name": "NCBI GEO",
            "url": "https://www.ncbi.nlm.nih.gov/geo/"
        }
    }
    pmids = doc.get("Citation(s)")
    if pmids:
        _doc['citation'] = []
        for pmid in pmids.split(', '):

            # funders
            http_client = tornado.httpclient.AsyncHTTPClient()
            url = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
            response = await http_client.fetch(url)
            title_xpath = '//*[@id="maincontent"]/div/div[5]/div/div[6]/div[1]/div/h4[4]/text()'
            # grant support section exists
            if Selector(text=response.body.decode()).xpath(title_xpath).get() == 'Grant support':
                xpath = '//*[@id="maincontent"]/div/div[5]/div/div[6]/div[1]/div/ul[4]/li/a/text()'
                supporters = Selector(text=response.body.decode()).xpath(xpath).getall()
                if supporters:
                    identifiers, funders = [], []
                    for supporter in supporters:
                        terms = supporter.split('/')[:-1]
                        identifiers.append(terms[0])
                        funders.append('/'.join(terms[1:]))
                    _doc['funding'] = [
                        {
                            'funder': {
                                '@type': 'Organization',
                                'name': funder
                            },
                            'identifier': identifier.strip(),
                        } for funder, identifier in zip(funders, identifiers)
                    ]

            # citation
            http_client = tornado.httpclient.AsyncHTTPClient()
            citation_url = 'https://www.ncbi.nlm.nih.gov/sites/PubmedCitation?id=' + pmid
            citation_response = await http_client.fetch(citation_url)
            citation_text = Selector(text=citation_response.body.decode()).xpath('string(/)').get()
            _doc['citation'].append(citation_text.replace(u'\xa0', u' '))

    for key, value in doc.items():
        if key in mappings:
            if isinstance(mappings[key], str):
                _doc[mappings[key]] = value
            elif callable(mappings[key]):
                _doc.update(mappings[key](value))
            else:
                raise RuntimeError()

    return dict(sorted(_doc.items()))


class NCBIProxyHandler(tornado.web.RequestHandler):
    '''
        Serves resources for the proxied site.
    '''

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", options.server_host)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    async def get(self):

        root = 'https://www.ncbi.nlm.nih.gov'
        url = root + self.request.uri
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url, raise_error=False)

        self.set_status(response.code)
        self.set_header('Content-Type', response.headers.get('Content-Type'))
        self.finish(response.body)


class NCBIRandomDatasetExplorer(tornado.web.RequestHandler):

    async def get(self):

        query_body = {"query": {"function_score": {"functions": [{"random_score": {}}]}}}
        query_result = client.search(
            index=api.config.ES_INDEX_GEO,
            body=query_body,
            size=1,
            _source=["_id"])

        _id = query_result['hits']['hits'][0]['_id']

        if self.get_argument('redirect', False) is not False:
            self.redirect('/geo/{}'.format(_id))
        else:
            await NCBIGeoDatasetWrapper.get(self, _id)


class NCBIGeoDatasetWrapper(tornado.web.RequestHandler):

    async def get(self, gse_id):

        root = 'https://www.ncbi.nlm.nih.gov'
        path = '/geo/query/acc.cgi?acc='
        url = root + path + gse_id
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url)
        text = response.body.decode()
        soup = BeautifulSoup(text, 'html.parser')

        # add resource path redirection
        soup.head.insert(0, soup.new_tag(
            'base', href='//{}/geo/query/'.format(options.geo_host)))

        # try to retrieve pre-loaded structured metadata
        try:
            doc = client.get(id=gse_id, index=api.config.ES_INDEX_GEO)
        except elasticsearch.ElasticsearchException:
            doc = None
        else:
            doc = doc['_source']

        # TODO parse raw metadata and do live transform
        if not doc:
            logging.warning('[%s] Cannot retrieve from es.', gse_id)
            # try:
            #     # capture raw metadata
            #     doc = NCBIGeoSpider().parse(Selector(text=text))
            #     # transform to structured metadata
            #     doc = await transform(doc, url, gse_id)
            # except Exception:
            #     logging.warning('[%s] Cannot parse raw metadata.', gse_id)
            self.send_error()
            return

        if doc:
            # set header message
            message = """
            This page adds structured schema.org <a href="http://schema.org/Dataset">Dataset</a> metadata
            to the original GEO data series page <a href="{}">{}</a>
            <a id="consoleLink" class="btn btn-sm btn-primary text-light ml-2" href="" target="_blank" rel="nonreferrer">Take a look</a>
            <script type="text/javascript">
            document.getElementById( "consoleLink" ).href = 'https://search.google.com/test/rich-results?url=' + encodeURI(window.location.href);
            </script>
            """.format(url, gse_id)
            # add structured metadata
            new_tag = soup.new_tag('script', type="application/ld+json")
            new_tag.string = json.dumps(doc, indent=4, ensure_ascii=False)
            soup.head.insert(1, new_tag)
            # # add js required by "Take a look" button
            # new_tag = soup.new_tag('script', type="text/javascript")
            # new_tag.string = """
            # document.getElementById( "consolelink" ).href = 'https://search.google.com/structured-data/testing-tool/u/0/#url=' + encodeURI(window.location.href); """
            # soup.head.insert(1, new_tag)
        else:
            # set header message
            message = """
            No structured metadata on this page.
            <a href="{}">Try a different URL.</a>
            """.format('/geo/_random.html?redirect')

        # add uniform header
        html = BeautifulSoup("""
        <nav class="navbar navbar-expand-md navbar-dark bg-main fixed-top p-3" style="border-bottom: 8px #ff616d solid;">
            <a class="navbar-brand" href="http://metadataplus.biothings.io/">
                <img src="http://metadataplus.biothings.io/img/logosimple.54090637.svg" width="30" height="30" alt="logo">
            </a>
            <a id="logo" style="font-family: Lilita One,sans-serif;font-size: 1.5em;" class="navbar-brand mainFont font-weight-bold caps text-light" href="http://metadataplus.biothings.io/">METADATA<span class="text-sec">PLUS</span></a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse justify-content-between" id="navbarSupportedContent">
                <small class="text-muted m-auto font-weight-bold alert alert-light">
                {}
                </small>
                <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link h-link" href="https://discovery.biothings.io/best-practices">Discovery Guide</a></li>
                <li class="nav-item"><a class="nav-link h-link" href="https://discovery.biothings.io/schema-playground">Schema Playground</a></li>
                </ul>
            </div>
        </nav>
        """.format(message), 'html.parser')
        soup.body.insert(2, html)
        soup.head.insert(2, BeautifulSoup("""
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        """, 'html.parser'))
        soup.head.insert(2, BeautifulSoup("""
            <link href="https://fonts.googleapis.com/css?family=Lilita+One&display=swap" rel="stylesheet">
        """, 'html.parser'))
        soup.head.insert(2, BeautifulSoup("""
            <style>
                body {
                    padding-top: 120px !important;
                }
                .text-main {
                	color: #7a7adc!important
                }

                .text-sec {
                	color: #ff616d!important
                }
                .mainFont {
                	font-family: Lilita One, sans-serif
                }

                .bg-main {
                	background: #333362
                }

                .bg-main-color {
                	background: #7a7adc
                }

                .bg-sec {
                	background: #ff616d
                }
                .ui-helper-reset {
                    opacity: 0 !important;
                    pointer-events: none !important;
                }
            </style>
        """, 'html.parser'))
        self.finish(soup.prettify())
