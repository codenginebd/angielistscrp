# - * - coding: UTF-8 - * -

import math
import time
from random import randint

from Browser import *
from Parser import *
from DBWraper import *

category_domains = []
file = open('angieslist_categories.csv','r')
content_list = file.read().split('\n')
for each_category in content_list:
    category_domains += [each_category.strip()]
file.close()

print "Domain Read Done!"

db = DBWraper()
login_url = 'https://my.angieslist.com/AngiesList/login.aspx'
logout_url = 'http://search.angieslist.com/logout/'

proxy_ip_addressess = [
    '72.93.108.40:21104',
    '65.188.183.22:27603',
    '67.136.153.130:3128',
    '198.98.102.38:3128',
    '130.94.148.99:80',
    '205.213.195.180:8080',
    '130.14.29.120:80',
    '205.213.195.80:8080',
    '206.174.39.13:3128',
    '66.35.68.145:7808',
    '192.210.217.135:21',
    '66.171.16.253:3128',
    '198.23.143.4:8080',
    '76.97.85.76:8080',
    '74.221.211.12:7808',
    '74.221.211.12:3128',
    '66.35.68.146:7808'
]

while True:
    #last_saved_state = db.read_last_saved_state()
    last_saved_cred_id = 0
    #last_current_state = db.read_last_row_current_states()
    #last_login_cred_id_current_state = last_current_state[5]
    #if last_saved_state:
    #    if last_saved_state[1] == 13:
    #        last_saved_cred_id = 0
    #    else:
    #        last_saved_cred_id = last_saved_state[1] - 1

    browser = Browser()
    browser.OpenURL('http://www.ip-adress.com/proxy_list/?k=time&d=desc')
    page = browser.GetPage()
    proxy_ip_list = Parser.parse_proxy_ip_address(page)

    proxy_ip_list = proxy_ip_addressess

    print "Proxy IP Found: "
    print len(proxy_ip_list)
    cred_list = db.get_cred_list(start=45,limit=1000)
    if not cred_list:
        print "Cred List %s" % str(last_saved_cred_id)
        break
    for each_cred in cred_list:
        try:
            print 'Entered %s' % each_cred[1]
            ###Get a random proxy ip address
            proxy_index = randint(0,len(proxy_ip_list) - 1)
            proxy_ip = proxy_ip_list[proxy_index]
            print "Requesting using proxy ip"
            print proxy_ip
            browser = Browser(proxy_ip)
            uname = each_cred[1]
            password = each_cred[2]
            b = browser.OpenURL(login_url)
            if not b:
                continue
            ##Do Login
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

            ###Get the first unread cat link.
            cat_record = db.get_first_unread_cat_record(each_cred[0])

            if not cat_record:
                login_cred_record = (each_cred[0],each_cred[1],each_cred[2],0,1)
                db.update_login_cred(login_cred_record)
                continue

            cat_id = cat_record[0]
            zip_code = cat_record[2]
            cat_name = cat_record[3]
            cat_link = cat_record[4]

            print 'First unread found %s' % str(cat_record[0])

            ###Login is done.
            current_state = db.read_current_state(each_cred[0])
            if current_state:
                print 'Current state found.'
                #cat_id = current_state[1]
                page_index = current_state[2]
                total_page = current_state[3]
                status = current_state[4]
                login_cred_id = current_state[5]
                link1 = current_state[6]
                link2 = current_state[7]

                page_url = link1+'&p='+str(page_index)+link2

                bb = browser.OpenURL(page_url)
                if not bb:
                    continue

                uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
                if uNameElement:
                    print 'May be the account is blocked!'
                    db.mark_login_as_blocked(each_cred[0])
                    continue

                result = []

                ###Get info from the page.
                page = browser.GetPage()
                basic_info_list,next_button_available = Parser.parse_basic_info(page)
                for each_basic_info in basic_info_list:
                    nor = 0
                    try:
                        nor = int(each_basic_info['num_of_reviews'])
                    except Exception,msg:
                        pass
                    if nor >= 3 and each_basic_info['link']:
                        b = browser.OpenURL(each_basic_info['link'])
                        if not b:
                            continue

                        uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
                        if uNameElement:
                            print 'May be the account is blocked!'
                            db.mark_login_as_blocked(each_cred[0])
                            continue

                        timetosleep = randint(1,3)
                        time.sleep(timetosleep)
                        details_page = browser.GetPage()
                        address_info = Parser.parse_address(details_page)

                        dataset = dict(each_basic_info.items()+address_info.items())


                        result.append(dataset)

                        ###Now put a sleep.
                        timetosleep = randint(1,5)
                        time.sleep(timetosleep)


                ###Now save info details.
                db.save_info_details(result,each_cred[0],cat_id,total_page,page_url)

                if int(page_index) >= int(total_page):
                    ###Crawling is done.
                    #record = (_,cat_id,page_index,total_page,1,each_cred[0],link1,link2)
                    ###Update the current state.
                    #db.update_current_state(record)

                    db.delete_current_record(each_cred[0],cat_id)

                    db.update_cat_as_read(cat_id)

                    #login_cred_record = (each_cred[0],each_cred[1],each_cred[2],0,1)

                    #db.update_login_cred(login_cred_record)

                else:
                    page_index = int(page_index) + 1
                    record = (0,cat_id,page_index,total_page,0,each_cred[0],link1,link2)
                    ###Update the current state.
                    db.update_current_state(record)

            else:
                ###Visit the link.
                print 'Current state not found.'
                bb = browser.OpenURL(cat_link)
                if not bb:
                    continue

                uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
                if uNameElement:
                    print 'May be the account is blocked!'
                    db.mark_login_as_blocked(each_cred[0])
                    continue

                result = []

                ###Get info from the page.
                page = browser.GetPage()
                basic_info_list,next_button_available = Parser.parse_basic_info(page)

                total_records = Parser.parse_page_count_total(page)
                page_count_total = math.ceil(float(total_records)/20)

                url_first_part,url_second_part = '',''

                page_url = browser.GetPageURL()

                ###Now save tyhe record state as current if next button is available and also get the next page link for the subsequent links.
                if next_button_available and page_count_total > 1:
                    browser.scroll_to_pager_link()
                    time.sleep(3)
                    elem = browser.FindElementByClassName('.next')
                    if elem:
                        browser.ClickElement(elem)
                        page_url = browser.GetPageURL()

                        url_first_part = page_url[:page_url.index('&p=')]
                        url_second_part = page_url[page_url.index('&zipcode'):]

                for each_basic_info in basic_info_list:
                    nor = 0
                    try:
                        nor = int(each_basic_info['num_of_reviews'])
                    except Exception,msg:
                        pass
                    if nor >= 3 and each_basic_info['link']:
                        b = browser.OpenURL(each_basic_info['link'])
                        if not b:
                            continue

                        uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
                        if uNameElement:
                            print 'May be the account is blocked!'
                            db.mark_login_as_blocked(each_cred[0])
                            continue

                        timetosleep = randint(1,3)
                        time.sleep(timetosleep)

                        details_page = browser.GetPage()
                        address_info = Parser.parse_address(details_page)

                        dataset = dict(each_basic_info.items()+address_info.items())

                        result.append(dataset)

                        ###Now put a sleep.
                        timetosleep = randint(1,5)
                        time.sleep(timetosleep)


                #page = browser.GetPage()
                sstatus = 0
                if not url_first_part or not url_second_part:
                    sstatus = 1
                record = (0,cat_id,0,page_count_total,sstatus,each_cred[0],url_first_part,url_second_part)
                ###Update the current state.
                db.update_current_state(record)

                ###Now save info details.
                db.save_info_details(result,each_cred[0],cat_id,page_count_total,page_url)

                record = (0,cat_id,1,page_count_total,0,each_cred[0],url_first_part,url_second_part)
                ###Update the current state.
                db.update_current_state(record)

            db.save_last_state(each_cred[0])
            browser.Close()

            timetosleep = randint(3,7)
            time.sleep(timetosleep)

        except Exception,msg:
            print "Exception occured."
            print msg
            continue
        finally:
            browser.Close()




















