import json
import requests

from fff.Query import Query
from fff.events import BusinessFinderEventSubscriber
from fff.events import BusinessFinderEventPrinter

# =================================================================================================
# Usage:
#   // Create and register BusinessFinderEventSubscriber
#   
#   app.LoadZipCodes()
#   
#   app.ExecAllQueries()
# =================================================================================================
class App:

    #
    # CONSTANTS
    #
    API_KEY = '36tLgH1xQsATRJFYzudnHZjiWKB8iK85RC2oDUYF16UDy1pADvt-2AtZMViGNoRNsFlKymNjPS5eYqGnDs1bba41b7a0L5dKWr00LRzTcnZ8lG8K7AHttbBHl4PdY3Yx'

    #
    # LAMBDAS
    #
    the_bearer = lambda access_token: "Bearer %s" % access_token

    headers = {
        "accept": "application/json",
        'Authorization': the_bearer(API_KEY)
        }
    
    #
    # Fields
    #
    categories = 'masonry'
    term = 'tax'
    queries = []
    zip_codes = []
    event_subs = []

    #
    # CTOR(s)
    #
    def __init__(self, def_printer=BusinessFinderEventPrinter()):
        if not def_printer is None:
            self.event_subs.append(def_printer)

    #n
    # Methods
    #
    def LoadZipCodes(self, zip_codes_filename='fff/zipcodes/zip_codes.json'):
        #new_zip_codes_filename = f"output/json/{zip_codes_filename}"
        with open(zip_codes_filename, 'r') as f:
            data = json.load(f)

            for z in data:
                #print('Zip code: ', z)
                self.zip_codes.append(z)

        return self.zip_codes

    def ExecQueries(self, stop=5):
        if not self.zip_codes:
            self.LoadZipCodes()

        output = ''
        i = 0
        for z in self.zip_codes:
            try:
                if i == stop:
                    break

                output += self.ExecQueryByZipCode(z)
                query_data_filename = "output/json/%s.json" % z['zip_code']
                self.fire_execquery_oncomplete(query_data_filename, output)
                i += 1
            except Exception as ex:
                print(ex)
                continue

        return output

    def ExecQuery(self, payload, filename='response.json'):
        
        #////////////////////////////////////////////////
        # API CALL

            res = requests.get('https://api.yelp.com/v3/businesses/search', params=payload, headers=self.headers)
            #res = requests.get('https://api.yelp.com/v3/businesses/business_id_or_alias/service_offerings', params=payload, headers=self.headers)
            if res.status_code != 200:
                raise Exception("App.ExecQuery: response.status_code == 200")

            q = Query()
            q.obj = json.loads(res.text)

            # dump json to output.json
            #new_fname = f"/output/json/{filename}"
            with open(filename, 'w') as f:
                json.dump(q.obj, f, indent=3)


        #////////////////////////////////////////////////
        # Simplify json

        # extract fields:
        # - name: q.obj['businesses'][0]['name']
        # - address: q.obj['businesses'][0]['location']
        # - phone: q.obj['businesses'][0]['display_phone']
        # - categories
            output = ''
            try:
                q.query_objs = list(map(self.exec_q, q.obj['businesses']))

            #////////////////////////////////////////////////
            # Get sorted, no-dups list of business names

                # get all business category names
                q.bus_cat_names = self.get_bus_cat_names(q.obj)

                # remove duplicate names
                q.bus_cat_names_no_dups =  list(dict.fromkeys(q.bus_cat_names))

                # add to app query collection
                self.queries.append(q)

                # convert python object list (query) into list of pretty printed strings
                # pretty_query_strs = list(map(lambda query_obj: json.dumps(query_obj, indent=3), q.query_objs))
                # print(pretty_query_strs[0])
                for query_str in map(lambda query_obj: json.dumps(query_obj, indent=3), q.query_objs):
                    output += "%s\n" % query_str
                    #print(query_str)
            except Exception as ex:
                print(ex)
            finally:
                return output


    def ExecQueryByZipCode(self, zip_code):
        payload = self.make_payload(zip_code=zip_code)

        filename = "output/json/%s.json" % zip_code['zip_code']
        return self.ExecQuery(payload, filename)

    def ExecQueryByCoords(self, coord):

    #////////////////////////////////////////////////
    # Set up API payload

        payload = self.make_payload(coord['lat'], coord['lon'])

        return self.ExecQuery(payload)

    def ExecAllQueries(self):
        if not self.zip_codes:
            self.LoadZipCodes()

        output = ''
        for z in self.zip_codes:
            output += self.ExecQueryByZipCode(z)
            self.fire_execquery_oncomplete(output)

        return output

    #
    # Utilities
    #
    def get_bus_cat_names(self, json_obj):
        categories = []
        for business in json_obj['businesses']:
            #print(business['name'])
            for category in business['categories']:
                categories.append(category['title'])

        return categories

    def print_section(self, ra, title):
        ra.sort()
        print('')
        print("%s (%d)" % (title, len(ra)))
        print('')
        for elem in ra:
            print(elem)
        print('')

    def exec_q(qself, query_obj):
        query_result_obj = {}
        query_result_obj['name'] = query_obj['name']
        query_result_obj['address'] = query_obj['location']
        query_result_obj['phone_number'] = query_obj['display_phone']
        query_result_obj['categories'] = query_obj['categories']
        return query_result_obj

    def make_payload(self, lat, lon, limit="50"):
        payload = {
            'locale':'en_US',
            'limit':limit,
            'term': self.term,
            'categories':self.categories,
            'latitude': lat,
            'longitude': lon,
            'radius': '40000'
            }
        return payload

    def make_payload(self, zip_code, limit=50):
        payload = {
            'locale':'en_US',
            'limit': limit,
            'term': self.term,
            'categories':self.categories,
            'location':str(zip_code['zip_code']),
            'radius': '40000'
            }
        return payload

    def fire_execquery_oncomplete(self, query_data_filename, output):
        if not self.event_subs is None:
            for sub in self.event_subs:
                if isinstance(sub, BusinessFinderEventSubscriber):
                        sub.ExecQuery_OnComplete(query_data_filename, output)
            