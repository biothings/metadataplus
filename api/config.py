import os

from biothings.web.api.es.handlers import QueryHandler
from biothings.web.settings.default import *

# from api.ncbi_geo import APP_LIST as GEO_APP
from api.query_builder import MPQueryBuilder
from api.query_transformer import MPResultTransformer

# *****************************************************************************
# Elasticsearch
# *****************************************************************************
ES_DOC_TYPE = '_doc'
ES_HOST = os.getenv("ES_HOST", 'localhost:9200')
ES_INDEX = os.getenv('ES_INDEX', '_all')  # query endpoint
ES_INDEX_GEO = os.getenv('ES_INDEX_GEO', 'indexed_ncbi_geo')  # get endpoint

# *****************************************************************************
# Tornado URL Patterns
# *****************************************************************************
# UNINITIALIZED_APP_LIST = GEO_APP TODO
APP_LIST = [
    (r"/api/query/?", QueryHandler),
]

# *****************************************************************************
# Biothings SDK Settings
# *****************************************************************************
ES_QUERY_BUILDER = MPQueryBuilder
ES_RESULT_TRANSFORMER = MPResultTransformer
ACCESS_CONTROL_ALLOW_METHODS = 'HEAD,GET,POST,DELETE,PUT,OPTIONS'
DISABLE_CACHING = True
ALLOW_RANDOM_QUERY = True
