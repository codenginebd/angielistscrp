# - * - coding: UTF-8 - * -

from bs4 import BeautifulSoup
from DBWraper import *
from Browser import *

###Read all account credentials.
db = DBWraper()
cred_list = db.get_cred_list_one()

login_url = 'https://my.angieslist.com/AngiesList/login.aspx'
logout_url = 'http://search.angieslist.com/logout/'

category_domains = []
file = open('angieslist_categories.csv','r')
content_list = file.read().split('\n')
for each_category in content_list:
    category_domains += [each_category.strip()]
file.close()

for each_cred in cred_list:
    browser = Browser()
    uname = each_cred[1]
    password = each_cred[2]
    browser.OpenURL(login_url)

    ##Do Login
    uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
    if not uNameElement:
        print 'Email element not found!'
    browser.TypeInto(each_cred[1],uNameElement)

    passElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserPasswordTextbox')
    if not passElement:
        print 'Password element not found!'
    browser.TypeInto(each_cred[2],passElement)

    signInButton = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$LoginButton')
    if not signInButton:
        print 'Sign In button not found!'

    browser.ClickElement(signInButton)

    ###Login is done.
    page = browser.GetPage()

    soup = BeautifulSoup(page)

    category_urls = soup.find_all('a',{'class':'serviceCategoryUrl'})

    data = []

    for each_url in category_urls:
        cat_name = each_url.text.strip()
        cat_url = each_url['href']
        if cat_name in category_domains:
            data.append((each_cred[0],'',cat_name,cat_url))

    db.save_category_info(data)

    db.mark_login_info_as_cat_crawled(each_cred[0])

    ###Finally do logout
    #browser.OpenURL(logout_url)
    browser.Close()


