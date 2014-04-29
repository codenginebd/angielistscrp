# - * - coding: UTF-8 - * -

from bs4 import BeautifulSoup
from Browser import *
from Parser import *
from FileWritter import *

import logging
logger = logging.getLogger('webdatacrawler')
hdlr = logging.FileHandler('C:\Python27\WebDataCrawler\webdatacrawler.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

logger.info('Starting program...')


login_url = 'https://my.angieslist.com/AngiesList/login.aspx'
login_cred = {
                'email':'riponow@mailblog.biz',
                'pass':'kolicecki'
              }

def crawl_zip(login_cred):
    browser = Browser()
    browser.OpenURL(login_url)
    uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
    if not uNameElement:
        print 'Email element not found!'
    browser.TypeInto(login_cred['email'],uNameElement)

    passElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserPasswordTextbox')
    if not passElement:
        print 'Password element not found!'
    browser.TypeInto(login_cred['pass'],passElement)

    signInButton = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$LoginButton')
    if not signInButton:
        print 'Sign In button not found!'

    page = browser.GetPage()

    soup = BeautifulSoup(page)

    category_urls = soup.find_all(attrs={'class':'serviceCategoryUrl'})

    for each_url in category_urls:
        print each_url

    browser.ClickElement(signInButton)

    page = browser.GetPage()

    category_links = Parser.parse_all_search_category_links(page)

    category_file = open('category_list.txt','w')

    for each_cat in category_links:
        category_file.write(each_cat+'\r\n')

    category_file.close()

    for each_category_link in category_links:
        result = []
        print 'Entering category: '+each_category_link
        browser.OpenURL(each_category_link)
        page = browser.GetPage()
        next_button_available = False
        next_button_clicked = False
        basic_info_list,next_button_available = Parser.parse_basic_info(page)
        for each_basic_info in basic_info_list:
            if each_basic_info['link']:
                browser.OpenURL(each_basic_info['link'])
                details_page = browser.GetPage()
                address_info = Parser.parse_address(details_page)

                dataset = dict(each_basic_info.items()+address_info.items())
                dataset['zip_code'] = ''
                dataset['category'] = ''

                result.append(dataset)

        if next_button_available:
            ###else click
            if not next_button_clicked:
                elem = browser.FindElementByClassName('.next')
                if elem:
                    browser.ClickElement(elem)
                    next_button_clicked = True
                    ###Get the url.
                    page_count = 1
                    page_url = browser.GetPageURL()

                    url_first_part = page_url[:page_url.index('&p=')]
                    url_second_part = page_url[page_url.index('&zipcode'):]

                    while True:
                        new_page_url = url_first_part+'&p='+str(page_count)+url_second_part
                        browser.OpenURL(new_page_url)
                        contents = browser.GetPage()
                        basic_info_list,next_button_available = Parser.parse_basic_info(contents)
                        if len(basic_info_list) == 0:
                            break
                        for each_basic_info in basic_info_list:
                            if each_basic_info['link']:
                                browser.OpenURL(each_basic_info['link'])
                                details_page = browser.GetPage()
                                address_info = Parser.parse_address(details_page)

                                dataset = dict(each_basic_info.items()+address_info.items())
                                dataset['zip_code'] = ''
                                dataset['category'] = ''

                                result.append(dataset)

                        page_count += 1

                        if not next_button_available:
                            break

                        #print 'Printing...'
                        #print result
                        #print 'End printing...'

        ###Save data here.
        csvwritter = CSVWritter('data.csv')
        csvwritter.AppendToCSV(result)


        ###Get all info list.
        ###for each info go to the detail link and scrape data.

        ###Find if div with class search-results-next exist inside a while loop. if so find a with class ala pagerLink next enabled and click else break the loop.


def main_entry():
    crawl_zip(login_cred)


main_entry()

