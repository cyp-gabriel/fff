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

class BusinessFinderEventPrinter(BusinessFinderEventSubscriber):
    #
    # FIELDS
    #
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