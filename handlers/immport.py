''' Add structured schema.org Dataset metadata to ImmPort '''

import json
import os

import elasticsearch
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.routing
import tornado.web


ES_INDEX_IMMPORT = os.getenv('ES_INDEX_IMMPORT', 'indexed_immport')


class PlusWrapper(tornado.web.RequestHandler):

    async def get(self, _id):

        url = 'https://www.immport.org/shared/study/' + _id

        # try to retrieve pre-loaded structured metadata
        client = elasticsearch.Elasticsearch()
        try:
            doc = client.get(id=url, index=ES_INDEX_IMMPORT)
        except elasticsearch.ElasticsearchException:
            doc = None
        else:
            doc = doc['_source']

        if doc:
            # set header message
            message = """
            This page adds structured schema.org <a href="http://schema.org/Dataset">Dataset</a> metadata
            to the original source series page <a href="{}">{}</a>
            <a id="consoleLink" class="btn btn-sm btn-primary text-light ml-2" href="" target="_blank" rel="nonreferrer">Take a look</a>
            <a href="https://metadataplus.biothings.io/about" target="_blank">Learn more</a>
            <script type="text/javascript">
            document.getElementById( "consoleLink" ).href = 'https://search.google.com/test/rich-results?url=' + encodeURI(window.location.href);
            </script>
            """.format(url, _id)
            # add structured metadata
            metadata = """
            <script type="application/ld+json">
            {}
            </script>
            """.format(json.dumps(doc, indent=4, ensure_ascii=False))
        else:
            # set header message
            message = """
            No structured metadata on this page.
            <a href="{}">Try a different URL.</a>
            """.format(f'//{self.request.host}/geo/_random.html?redirect')

            # add structured metadata
            metadata = ''

        # MARCO
        page = """
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width,initial-scale=1.0">
            <meta name="HandheldFriendly" content="True">
            <meta property="og:locale" content="en_US">
            {}
            <link href="https://fonts.googleapis.com/css?family=Lilita+One&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
            <style>
                .text-main {{
                	color: #17718C!important
                }}

                .text-sec {{
                	color: #7E4185!important
                }}

                .mainFont {{
                	font-family: Lilita One, sans-serif
                }}

                .bg-main {{
                	background: #2B111F
                }}

                .bg-main-color {{
                	background: #17718C
                }}

                .bg-sec {{
                	background: #7E4185
                }}

                .ui-helper-reset {{
                	opacity: 0!important;
                	pointer-events: none!important
                }}
                .if{{
                    height:100vh;
                }}
            </style>
          </head>
          <body class="body-back row m-0">
              <nav class="navbar navbar-expand-md navbar-dark bg-main p-3 col-sm-12" style="border-bottom: 8px #ff616d solid;">
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
              <iframe src="{}" class="col-sm-12 if p-0">
            <noscript>
              <strong>We're sorry but METADATA PLUS site doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
            </noscript>
          </body>
        </html>
        """.format(metadata, message, url)

        self.finish(page)
