class QueryDatum:
    filename = ''
    data = None

    def __init__(self, filename_, data_):
        self.filename = filename_
        self.data = data_

class BusinessFinderEventSubscriber:

    #
    # OPERATIONS: Polymorphic
    #
    def ExecQuery_OnComplete(self, query_data_filename, query_data):
        pass

    def ExecQuery_Before(self, http_req_url, term):
        pass

class BusinessFinderEventPrinter(BusinessFinderEventSubscriber):
    #
    # FIELDS
    #
    http_request_url = ""
    is_first = True
    queryDataFilenames = []
    queryDataItems = []

    #
    # OVERRIDES: BusinessFinderEventSubscriber
    #
    def ExecQuery_OnComplete(self, query_data_filename, query_data):
        #print(query_data)
        #new_query_filename = f"output/{query_data_filename}"
        self.queryDataFilenames.append(query_data_filename)
        self.queryDataItems.append(QueryDatum(query_data_filename, query_data))

        msg = "\n*** ExecQuery (AFTER) ***\n"
        msg += f"\n   Just processed file: {query_data_filename}"
        print(msg)

    def ExecQuery_Before(self, http_req_url, term):
        msg = ""
        if self.is_first:
            #msg = f"Term: {term}{self.http_request_url}"
            self.is_first = False

        msg = "\n*** ExecQuery (BEFORE) ***\n\n"
        msg += f"   Term: {term}\n"
        msg += f"   HTTP GET: {http_req_url}"
        print(msg)
        return msg