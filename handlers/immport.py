''' Add structured schema.org Dataset metadata to ImmPort page. '''

import json
import logging
import os

import elasticsearch
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.routing
import tornado.web
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tornado.options import options

ES_INDEX_IMMPORT = os.getenv('ES_INDEX_IMMPORT', 'indexed_immport')


class ImmPortProxyHandler(tornado.web.RequestHandler):
    '''
        Serves resources for the proxied site.
    '''

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    async def get(self):

        if self.request.uri.endswith('js'):
            self.set_status(404)
            return

        root = 'https://www.immport.org'
        url = root + self.request.uri
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url, raise_error=False)

        self.set_status(response.code)
        self.set_header('Content-Type', response.headers.get('Content-Type'))
        self.finish(response.body)


WAIT_CONDITION = '//*[@id="ui-accordiontab-0-content"]/div/table/tbody/tr[1]/td[2]'


def server_side_render(url):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, WAIT_CONDITION)))

    return driver.page_source


class ImmPortDatasetWrapper(tornado.web.RequestHandler):

    async def get(self, _id):

        url = 'https://www.immport.org/shared/study/' + _id

        ioloop = tornado.ioloop.IOLoop.current()
        text = await ioloop.run_in_executor(None, server_side_render, url)

        soup = BeautifulSoup(text, 'html.parser')

        # modify resource path redirection
        soup.base['href'] = '//{}/shared/'.format('immport.' + self.request.host)

        # try to retrieve pre-loaded structured metadata
        client = elasticsearch.Elasticsearch()
        try:
            doc = client.get(id=url, index=ES_INDEX_IMMPORT)
        except elasticsearch.ElasticsearchException:
            doc = None
        else:
            doc = doc['_source']

        if doc:
            # add structured metadata
            new_tag = soup.new_tag('script', type="application/ld+json")
            new_tag.string = json.dumps(doc, indent=4, ensure_ascii=False)
            soup.head.insert(1, new_tag)

        self.finish(soup.prettify())
