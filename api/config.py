import os
from biothings.web.settings.default import *
from biothings.web.api.es.handlers import QueryHandler
# from api.ncbi_geo import APP_LIST as GEO_APP

# *****************************************************************************
# Elasticsearch
# *****************************************************************************
ES_INDEX = os.getenv('ES_INDEX', 'indexed_ncbi_geo')
ES_DOC_TYPE = '_doc'
ES_HOST = os.getenv("ES_HOST", 'localhost:9200')

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
ACCESS_CONTROL_ALLOW_METHODS = 'HEAD,GET,POST,DELETE,PUT,OPTIONS'
DISABLE_CACHING = True
ALLOW_RANDOM_QUERY = True
