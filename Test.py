# - * - coding: UTF-8 - * -

from Browser import *

proxy_ip = ''

browser = Browser(proxy_ip)
b = browser.OpenURL('https://my.angieslist.com/Angieslist/Login.aspx')
if not b:
    print 'Failed!'
##Do Login
uNameElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserNameTextbox')
if not uNameElement:
    print 'Email element not found!'
browser.TypeInto('RhytmbluFunnyfigar@gmail.com',uNameElement)

passElement = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$UserPasswordTextbox')
if not passElement:
    print 'Password element not found!'
browser.TypeInto('import',passElement)

signInButton = browser.FindElementByName('ctl00$ContentPlaceHolderMainContent$LoginControl$LoginButton')
if not signInButton:
    print 'Sign In button not found!'

browser.ClickElement(signInButton)

print "Logged In..."

browser.OpenURL('http://search.angieslist.com/spCategorySearch/?stc=&st=Electrical&loc=Yellow%2520road%25202-30%2520%2520Chicago%252C%2520IL%252060601&p=6&zipcode=60601&mzid=529&mid=7&s=0&v=list&mmid=&catid=54&spn=&spid=&loggingRS=0&showReviewedIn=0&showStats=0&cf=0&df=0&gf=0&pohf=0&ssaf=0&qqf=0&nfc=&mrf=0&ecof=0&mmh=0&pp=website1&flibby=0&af=0&ebw=1&cif=0&cgtif=0')

page = browser.GetPage()

f = open('ppage.html','w')

f.write(page)

f.close()

from Parser import *

f = open('ppage.html','r')

c = f.read()

address = Parser.parse_address(c)

print address


