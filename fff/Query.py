import requests


class Query:
    query_objs = []
    bus_cat_names = []
    bus_cat_names_no_dups = []



class QueryTextOutputBlock:
    query_item = None
    bus_name = ''
    addr1 = ''
    addr2 = ''
    addr3 = ''
    city = ''
    state = ''
    zip_code = ''
    phone = ''

    def __init__(self, query_item):
        self.query_item = query_item
        self.bus_name = '' if query_item['Name'] is None else query_item['Name']
        self.addr1 = '' if query_item['Address']['address1'] is None else query_item['Address']['address1']
        self.addr2 = '' if query_item['Address']['address2'] is None else query_item['Address']['address2']
        self.addr3 = '' if query_item['Address']['address3'] is None else query_item['Address']['address3']
        self.city = '' if query_item['Address']['city'] is None else query_item['Address']['city']
        self.state = '' if query_item['Address']['state'] is None else query_item['Address']['state']
        self.zip_code = '' if query_item['Address']['zip_code'] is None else query_item['Address']['zip_code']
        self.phone = '' if query_item['Phone'] is None else query_item['Phone']

    def the_name(self):
        return self.bus_name

    def the_address_lines(self):
        # address: line 1 and 2
        addrlines = []
        if self.addr1 != '':
            addrlines.append(self.addr1)
        if self.addr2 != '':
            addrlines.append(self.addr2)
        if self.addr3 != '':
            addrlines.append(self.addr3)

        # address: line 3
        addr_line3 = "%s, %s %s" % (self.city, self.state, self.zip_code)
        addrlines.append(addr_line3)

        return addrlines

    def the_phone_number(self):
        return self.phone

    def lines(self):
        if self.the_name() == '':
            raise Exception('self.bus_name is empty string')
        if self.the_phone_number() == '':
            raise Exception('self.phone is empty string')

        lines = []

        # business name
        lines.append(self.the_name())

        # address block
        addrlns = self.the_address_lines()
        if len(addrlns) > 0:
            lines.extend(addrlns)

        # phone number
        lines.append(self.the_phone_number())
        
        return lines