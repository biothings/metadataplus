from biothings.web.api.es.transform import ESResultTransformer

DATASOURCES = (
    'harvard_dataverse',
    'ncbi_geo',
    'omicsdi',
    'zenodo')


class MPResultTransformer(ESResultTransformer):

    def _get_doc(self, doc):

        _doc = doc.get('_source', doc.get('fields', {}))

        # Map index name to generic datasource name

        for source in DATASOURCES:
            if source in doc['_index']:
                _doc['_index'] = source
                break

        return _doc
