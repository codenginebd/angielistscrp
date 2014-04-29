# - * - coding: UTF-8 - * -

import math
import time
from random import randint

from Browser import *
from Parser import *
from DBWraper import *
from collections import defaultdict

db = DBWraper()
login_url = 'https://my.angieslist.com/AngiesList/login.aspx'
logout_url = 'http://search.angieslist.com/logout/'

cred_list = db.get_cred_list()
if not cred_list:
    print "Cred List %s" % str(last_saved_cred_id)

for each_cred in cred_list:
    browser = Browser()
    datarows = db.read_missing_address_rows(each_cred[0])
    if len(datarows) > 0:
        b = browser.OpenURL(login_url)
        if not b:
            continue

        uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
        if not uNameElement:
            print 'Email element not found!'
            continue
        browser.TypeInto(each_cred[1],uNameElement)

        passElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserPasswordTextbox')
        if not passElement:
            print 'Password element not found!'
            continue
        browser.TypeInto(each_cred[2],passElement)

        signInButton = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$LoginButton')
        if not signInButton:
            print 'Sign In button not found!'
            continue

        browser.ClickElement(signInButton)

        print "Logged In..."
    groups= defaultdict( list )
    for each_data_row in datarows:
        groups[each_data_row[16]] += [each_data_row]

    for key in groups.keys():
        updated_addresses = []
        browser.OpenURL(key)
        page = browser.GetPage()
        basic_info_list,next_button_available = Parser.parse_basic_info(page)
        tuples = groups.get(key)
        for each_basic_info in basic_info_list:
            for t in tuples:
                if t[3] == each_basic_info['business_name']:
                    browser.OpenURL(each_basic_info['link'])
                    page = browser.GetPage()
                    address = Parser.parse_address(page)
                    address['info_id'] = t[0]
                    updated_addresses += [address]

        db.update_missing_info(updated_addresses)
    browser.Close()
    print 'End'

