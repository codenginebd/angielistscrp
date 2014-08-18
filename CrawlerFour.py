__author__ = 'Codengine'

import math
import time
from random import randint

from Browser import *
from Parser import *
from DBWraper import *
from Parser2 import *

login_url = 'https://my.angieslist.com/AngiesList/login.aspx'
logout_url = 'http://search.angieslist.com/logout/'

class CrawlerFour:
    def __init__(self):
        self.w1 = True

    def crawl_category(self):
        pass

    def start_processing(self):
        while True:
            self.db = DBWraper(self.w1)

            cred_list = self.db.get_cred_list_crawler_one()
            if not cred_list:
                print "Cred List Not Found."
                break
            for each_cred in cred_list:

                last_unread_cat_ = self.db.read_last_unread_category(each_cred[0])
                if not last_unread_cat_:
                    print 'No unread category found!'
                    continue

                browser = Browser()
                #uname = each_cred[1]
                #password = each_cred[2]
                b = browser.OpenURL(login_url)
                if not b:
                    print 'Login URL open failed.'
                    continue
                    ##Do Login
                uNameElement = browser.FindElementById('UserNameTextbox')
                if not uNameElement:
                    print 'Email element not found!'
                    continue
                browser.TypeInto(each_cred[1],uNameElement)

                passElement = browser.FindElementById('UserPasswordTextbox')
                if not passElement:
                    print 'Password element not found!'
                    continue
                browser.TypeInto(each_cred[2],passElement)

                signInButton = browser.FindElementById('ctl00_ContentPlaceHolderMainContent_LoginControl_LoginButton')
                if not signInButton:
                    print 'Sign In button not found!'
                    continue

                browser.ClickElement(signInButton)

                uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
                if uNameElement:
                    print 'May be the account is blocked!'
                    self.db.mark_login_as_blocked(each_cred[0])
                    continue

                print "Logged In..."

                ###Login is done.
                page = browser.GetPage()

                soup = BeautifulSoup(page)

                category_urls = soup.find_all('a',{'class':'serviceCategoryUrl'})

                url_to_go = None

                for each_url in category_urls:
                    cat_name = each_url.text.strip()
                    cat_url = each_url['href']
                    url_to_go = cat_url
                    break
                if not url_to_go:
                    login_cred_record = (each_cred[0],each_cred[1],each_cred[2],0,1)
                    self.db.update_login_cred(login_cred_record)
                    continue

                for i in range(3):
                    ###Read the last non-visited category for this login.
                    category_name = None
                    last_unread_cat = self.db.read_last_unread_category(each_cred[0])
                    if not last_unread_cat:
                        login_cred_record = (each_cred[0],each_cred[1],each_cred[2],0,0,1)
                        self.db.update_login_cred_basic_info_fetched(login_cred_record)
                        browser.Close()
                        continue
                    category_name = last_unread_cat[2]

                    b = browser.OpenURL(url_to_go)
                    if not b:
                        print 'Category URL open failed.'
                        print 'Url: '
                        print url_to_go
                        continue

                    search_box = browser.FindElementById('searchBox')
                    if not search_box:
                        print 'Searchbox Element Not Found!'
                        continue
                    browser.ClearText(search_box)
                    browser.TypeInto(category_name,search_box)
                    search_submit_button = browser.FindElementById('searchSubmit')
                    browser.ClickElement(search_submit_button)

                    ##Now collect page untill page is over.
                    result = []
                    page_index = 0
                    while True:
                        page_index += 1
                        page_url = browser.GetPageURL()
                        page = browser.GetPage()
                        basic_info_list,next_button_available,total_records_count = Parser.parse_basic_info(page)

                        page_count = Parser.parse_page_count_total(page)

                        print 'Total Records Count %s' % str(total_records_count)

                        address_tuple = Parser2.parse_address_from_searchbar(page)

                        #basicinfolist = basic_info_list

                        t = []

                        for i in basic_info_list:
                            i['s_primaryaddress'] = address_tuple[0]
                            i['s_primarylocation'] = address_tuple[1]
                            i['s_address'] = address_tuple[2]
                            i['s_city'] = address_tuple[3]
                            i['s_state'] = address_tuple[4]
                            i['s_zip'] = address_tuple[5]
                            i['l_address'] = address_tuple[6]
                            i['l_city'] = address_tuple[7]
                            i['l_state'] = address_tuple[8]
                            i['l_zip'] = address_tuple[9]
                            i['link'] = page_url
                            t += [i]

                        basic_info_list = t

                        result += basic_info_list
                        if total_records_count < 20:
                            break
                        browser.scroll_to_pager_link()
                        time.sleep(3)
                        elem = browser.FindElementByClassName('.next')
                        if elem:
                            browser.ClickElement(elem)
                            time.sleep(3)

                        import math

                        if math.ceil(float(page_count)/20 <= page_index):
                            break

                    temp_results = []
                    for each in result:
                        if not each in temp_results:
                            temp_results += [each]

                    result = temp_results

                    filtered_results = []

                    for each_basic_info in result:
                        nor = 0
                        try:
                            nor = int(each_basic_info['num_of_reviews'])
                        except Exception,msg:
                            pass
                        if each_basic_info['buy_itnow'] == 'Yes' or each_basic_info['coupon'] == 'Yes':
                            filtered_results += [each_basic_info]
                        else:
                            if each_basic_info['rating'] == 'A':
                                if nor >= 4 and each_basic_info['link']:
                                    filtered_results += [each_basic_info]
                            elif each_basic_info['rating'] == 'B':
                                if nor >= 15 and each_basic_info['link']:
                                    filtered_results += [each_basic_info]

                    self.db.save_basic_info(filtered_results,each_cred[0],category_name)
                    self.db.mark_category_read(last_unread_cat[0])

                    sleep_time_1min = randint(10,25)
                    print 'Sleeping %s minutes' % str(sleep_time_1min/60)
                    time.sleep(sleep_time_1min)
                    print 'Sleeping done.'

                browser.Close()
                sleep_time_1min = randint(100,200)
                print 'Sleeping %s minutes' % str(sleep_time_1min/60)
                time.sleep(sleep_time_1min)
                print 'Sleeping done.'

            sleep_time_10mins = randint(100,200)
            print 'Sleeping %s minutes' % str(sleep_time_10mins/60)
            time.sleep(sleep_time_10mins)
            print 'Sleeping done.'
            self.w1 = not self.w1
            self.db.close()

CrawlerFour().start_processing()




