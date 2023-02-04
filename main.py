from lib2to3.pytree import convert
from fff.App import App
from fff.events import BusinessFinderEventPrinter
from fff.filters import JmesPathFilter
from functools import cmp_to_key
from fff.Query import Query, QueryTextOutputBlock

import json
import requests
import jmespath
import os

#================================================================================
# LAMBDAS/FUNCTIONS
#================================================================================
def entry_point():
    
    # set up subscriber
    printer = BusinessFinderEventPrinter()
    app = App(printer)

    # TEST
    #zips = app.LoadZipCodes()
    #for z in zips:
    #    print(z)

    # TEST
    #result = app.ExecAllQueries()
    #print(result)

    result = app.ExecQueries(2)
    print('QUERY RESULT')
    print('')
    print(result)

    # apply filter to query data filenames
    q_filter = JmesPathFilter()
    filtered_query_results = q_filter.Apply(printer.queryDataItems, 'businesses[].{Name: name, Phone: display_phone, Address: location}')

    def cmp_items_name(a, b):
        name_a = a['Name']
        name_b = b['Name']
        if name_a > name_b:
            return 1
        elif name_a == name_b:
            return 0
        else:
            return -1

    # sort results
    pred = cmp_to_key(cmp_items_name)
    filtered_query_results.sort(key=pred)

    # remove duplicates
    res = []
    [res.append(x) for x in filtered_query_results if x not in res]

    # filter: get resulting company details for companies that have a business name and phone number
    final_results = [x for x in res if x['Phone'] != '' and x['Phone'] is not None]

    #
    # create formatted text output
    #
    def convert_query_item_to_text(query_item):
        result = QueryTextOutputBlock(query_item)
        lns = result.lines()
        lines = list(map(lambda l: "\n%s" % l, lns[1:]))
        newlines = [lns[0]]
        newlines.extend(lines)
        text_output = ''
        for l in newlines:
            text_output += l
        
        return "%s\n\n" % text_output

    #
    # send text to file
    #

    # delete last output file
    if os.path.exists('businesses.txt'):
        os.remove('businesses.txt')

    text_output = list(map(convert_query_item_to_text, final_results))

    # sort text output before sending to file
    text_output.sort()
    for text_output_item in text_output:
        with open("output/businesses.txt", "a") as f:
            f.write(text_output_item)
            #f.write(f"output/{text_output_item}")

#================================================================================
# ENTRY-POINT
#================================================================================

coords = [
    {
        'lat': '41.20978328532493',
        'lon': '-111.9679557116452'
    },
    {
        'lat': '41.22292208977511',
        'lon': '-111.96428644991106'
    },
    { # Treehouse Museum
        'lat':'41.22676312486201',
        'lon':'-111.97321065851749'
    },
    { # Walmart Supercenter
        'lat': '41.272564212568646', 
        'lon': '-111.97303223476604'
    },
    { # Smith's Marketplace
        'lat': '41.304421916482916', 
        'lon': '-111.96698669072345'
    }
]

entry_point()
