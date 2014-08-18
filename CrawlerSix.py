__author__ = 'Codengine'

import math
import time
from random import randint

from Browser import *
from Parser import *
from DBWraper import *

login_url = 'https://my.angieslist.com/AngiesList/login.aspx'
logout_url = 'http://search.angieslist.com/logout/'

class CrawlerSix:
    def __init__(self):
        self.w1 = True

    def start_processing(self):
        while True:
            self.db = DBWraper(self.w1)
            cred_list = self.db.get_cred_list()
            if not cred_list:
                print "Cred List Not Found."
                break
            for each_cred in cred_list:

                basic_info = self.db.read_basic_info_address_unfetched(each_cred[0])
                if not basic_info:
                    print 'No basic info found! for account %s' % str(each_cred[0])
                    continue

                browser = Browser()

                b = browser.OpenURL(login_url)
                if not b:
                    print 'Login URL open failed.'
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

                for info in basic_info:
                    url = info[18]
                    b = browser.OpenURL(url)
                    if not b:
                        continue

                    uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
                    if uNameElement:
                        print 'May be the account is blocked!'
                        self.db.mark_login_as_blocked(each_cred[0])
                        continue
                    timetosleep = randint(10,25)
                    time.sleep(timetosleep)

                    details_page = browser.GetPage()
                    address_info = Parser.parse_address(details_page)

                    self.db.update_basic_info_with_address(info[0],address_info)

                browser.Close()

                sleep_time_10mins = randint(90,140)
                print 'Sleeping now %s minutes' % str(sleep_time_10mins/60)
                time.sleep(sleep_time_10mins)
                print 'Sleeping done.'
            sleep_time_10mins = randint(200,300)
            print 'Sleeping %s minutes' % str(sleep_time_10mins/60)
            time.sleep(sleep_time_10mins)
            print 'Sleeping done.'
            self.w1 = not self.w1
            self.db.close()

CrawlerSix().start_processing()


