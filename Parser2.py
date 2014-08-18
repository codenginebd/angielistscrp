# - * - coding: UTF-8 - * -

from bs4 import BeautifulSoup
import re

class Parser2:
    def __init__(self):
        pass

    @staticmethod
    def parse_address_from_searchbar(page):
        soup = BeautifulSoup(page)
        primary_address,primary_location,zipcode,address,city,state,laddress,lcity,lstate,lzip = '','','','','','','','','',''
        try:
            primary_address = soup.find('input',{'name':'primaryAddress'})['value']
            primary_location = soup.find('input',{'name':'primaryLoc'})['value']
            zipcode = soup.find('input',{'name':'zipcode'})['value']
            searchbox = soup.find('input',{'id':'locationBox'})
            if searchbox:
                laddress = searchbox['value']
                laddress_list = laddress.split(',')
                lcity = laddress_list[0]
                lstate = laddress_list[1]
                lzip = laddress_list[2]
        except Exception,msg:
            print 'Exception occured inside parse_address_from_searchbar() method.'
            pass

        if primary_address:
            pa = primary_address.split(',')
            if len(pa) == 4:
                address = pa[0]
                city = pa[1]
                state = pa[2]


        return primary_address,primary_location,address,city,state,zipcode,laddress,lcity,lstate,lzip

#f = open('page.htm','r')
#c = f.read()
#f.close()

#print Parser2.parse_address_from_searchbar(c)
