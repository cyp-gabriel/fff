import jmespath
import json
from os.path import exists
from pathlib import Path

class JmesPathFilter:

    def Apply(self, query_data_items, search_arg):
        # apply filter to query data filenames
        filtered_query_results = []
        for query_datum in query_data_items:

            path = Path(query_datum.filename)
            if not exists(path):
                continue

            # load json data from file
            with open(query_datum.filename, 'r') as f:
                query_json = json.load(f)

                # apply filter
                filtered_query = jmespath.search(search_arg, query_json)
                if not self.contains(filtered_query_results, filtered_query):
                    filtered_query_results.extend(filtered_query)

        return filtered_query_results

    def contains(self, queries, query):
        if not queries:
            return False

        # for q in queries:
        #     if q['Name'] == query['Name']:
        #         return True
        return False