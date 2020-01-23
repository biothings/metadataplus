from biothings.web.api.es.query_builder import ESQueryBuilder


class MPQueryBuilder(ESQueryBuilder):

    def _extra_query_types(self, q):
        return {
            "query": {
                "dis_max": {
                    "queries": [
                        {
                            "query_string": {
                                "query": q,
                                "fields": ["name^6", "description^3"]
                            }
                        },
                        {
                            "query_string": {
                                "query": q
                            }
                        }
                    ]
                }
            }
        }
