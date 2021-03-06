''' Add structured schema.org Dataset metadata to NCBI GEO data series page. '''

import json
import logging
import os

import elasticsearch
import tornado.httpclient
import tornado.ioloop
import tornado.routing
import tornado.web
from bs4 import BeautifulSoup

ES_INDEX_GEO = os.getenv('ES_INDEX_GEO', 'indexed_ncbi_geo')


class NCBIProxyHandler(tornado.web.RequestHandler):
    '''
        Serves resources for the proxied site.
    '''

    def set_default_headers(self):
        assert self.request.host.startswith('geo.')
        origin = self.request.protocol + '://' + self.request.host[4:]
        self.set_header("Access-Control-Allow-Origin", origin)
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

        client = elasticsearch.Elasticsearch()
        query_body = {"query": {"function_score": {"functions": [{"random_score": {}}]}}}
        query_result = client.search(
            index=ES_INDEX_GEO,
            body=query_body,
            size=1, _source=["identifier"]
        )

        _id = query_result['hits']['hits'][0]['_source']['identifier']

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
            'base', href='//{}/geo/query/'.format('geo.' + self.request.host)))

        # try to retrieve pre-loaded structured metadata
        client = elasticsearch.Elasticsearch()
        try:
            doc = client.get(id=url, index=ES_INDEX_GEO)
        except elasticsearch.ElasticsearchException:
            doc = None
        else:
            doc = doc['_source']

        if doc:
            # set header message
            message = """
            This page adds structured schema.org <a href="http://schema.org/Dataset">Dataset</a> metadata
            to the original GEO data series page <a href="{}">{}</a>
            <a id="consoleLink" class="btn btn-sm btn-primary text-light ml-2" href="" target="_blank" rel="nonreferrer">Take a look</a>
            <a href="https://metadataplus.biothings.io/about" target="_blank">Learn more</a>
            <script type="text/javascript">
            document.getElementById( "consoleLink" ).href = 'https://search.google.com/test/rich-results?url=' + encodeURI(window.location.href);
            </script>
            """.format(url, gse_id)
            # add structured metadata
            new_tag = soup.new_tag('script', type="application/ld+json")
            new_tag.string = json.dumps(doc, indent=4, ensure_ascii=False)
            soup.head.insert(1, new_tag)
        else:
            # set header message
            message = """
            No structured metadata on this page.
            <a href="{}">Try a different URL.</a>
            """.format(f'//{self.request.host}/geo/_random.html?redirect')

        # add uniform header
        html = BeautifulSoup("""
        <nav class="navbar navbar-expand-md navbar-dark bg-main fixed-top p-3" style="border-bottom: 8px #ff616d solid;">
            <a class="navbar-brand" href="https://metadataplus.biothings.io/">
                <img src="http://metadataplus.biothings.io/img/logosimple.f39f88c2.svg" width="30" height="30" alt="logo">
            </a>
            <a id="logo" style="font-family: Lilita One,sans-serif;font-size: 1.5em;" class="navbar-brand mainFont font-weight-bold caps text-light" href="https://metadataplus.biothings.io/">METADATA<span class="text-sec">PLUS</span></a>
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
                	color: #17718C!important
                }

                .text-sec {
                	color: #7E4185!important
                }
                .mainFont {
                	font-family: Lilita One, sans-serif
                }

                .bg-main {
                	background: #2B111F
                }

                .bg-main-color {
                	background: #17718C
                }

                .bg-sec {
                	background: #7E4185
                }
                .ui-helper-reset {
                    opacity: 0 !important;
                    pointer-events: none !important;
                }
            </style>
        """, 'html.parser'))
        self.finish(soup.prettify())
