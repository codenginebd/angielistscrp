# - * - coding: UTF-8 - * -

from bs4 import BeautifulSoup
import re


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def parse_basic_info(page):
        soup = BeautifulSoup(page)
        sr_info_tds = soup.findAll('td', {'class': 'sr_info'})
        basic_info_list = []
        for each_td in sr_info_tds:
            basic_info = {
                'business_name': '',
                'rating': '',
                'num_of_reviews': '',
                'coupon': 'No',
                'buy_itnow': 'No',
                'dlink': ''
            }
            name_anchor = each_td.find('a', {'class': 'spNameLink ala'})
            if name_anchor:
                href = name_anchor['href']
                name = name_anchor.text
                if href:
                    basic_info['dlink'] = href
                if name:
                    basic_info['business_name'] = name
            coupon_div = each_td.find('div', {'class': 'grade-coupon'})
            if coupon_div:
                coupon_text = coupon_div['title']
                if coupon_text:
                    basic_info['coupon'] = 'Yes'
            grade_span = each_td.find('span', {'class': 'search-result-grade'})
            if grade_span:
                grade_text = grade_span.text
                if grade_text:
                    basic_info['rating'] = grade_text
            review_div = each_td.find('div', {'class': 'search-result-review'})
            if review_div:
                review_text = review_div.text
                if review_text:
                    basic_info['num_of_reviews'] = review_text
            buy_itnow_button = each_td.find('div', {'class': 'deal-buyitnow-button'})
            if buy_itnow_button:
                basic_info['buy_itnow'] = 'Yes'

            if basic_info['rating'] == 'A' or basic_info['rating'] == 'B' or buy_itnow_button or basic_info['coupon'] =='Yes':
                basic_info_list.append(basic_info)

        _next_button_available = False

        next_button = soup.find('div', {'class': 'search-results-next'})
        if next_button:
            _next_button_available = True

        return (basic_info_list, _next_button_available, len(sr_info_tds))

    @staticmethod
    def parse_page_count_total(page):
        soup = BeautifulSoup(page)
        search_result_count_div = soup.find('div', {'id': 'searchResultsCount'})
        if search_result_count_div:
            try:
                result_count_text = search_result_count_div.text.replace('Search Results', '').strip()
                return int(result_count_text)
            except Exception, msg:
                return 0
        return 0

    @staticmethod
    def extract_address(s):
        rs = s[::-1]

        rssplit = rs.split(' ')

        if rssplit:

            try:

                zip = rssplit[0]

                state = rssplit[1]

                city = rs.replace(zip, '').replace(state, '').strip()

                zip = zip[::-1]

                state = state[::-1]

                city = city[::-1]

                return (city, state, zip)
            except Exception, msg:
                return ('', '', '')
        return ('', '', '')

    @staticmethod
    def parse_address(page):
        soup = BeautifulSoup(page)
        address_element_span = soup.find('span',
                                         {'id': 'ctl00_ContentPlaceHolderMainContent_SPSideBar1_ContactAddress'})
        address_info = {
            'a1': '',
            'a2': '',
            'city': '',
            'state': '',
            'zip': '',
            'phone': '',
            'website': ''
        }
        if address_element_span:
            address_element_content1 = address_element_span.contents[0].string if len(
                address_element_span.contents) > 0 else ''
            if address_element_content1:
                address_info['a1'] = address_element_content1

            address_element_content2 = ''
            try:
                address_element_content2 = re.sub('<(.+?)>', '', address_element_span.contents[1].string) if len(
                    address_element_span.contents) > 1 else ''
                if address_element_content2:
                    address_info['a2'] = address_element_content2
                    address_info['city'], address_info['state'], address_info['zip'] = Parser.extract_address(
                        address_element_content2)
            except Exception, msg:
                print 'Exception Inside...'
                address_element_content2 = re.sub('<(.+?)>', '', address_element_span.contents[2].string) if len(
                    address_element_span.contents) > 1 else ''
                if address_element_content2:
                    address_info['a2'] = address_element_content2
                    address_info['city'], address_info['state'], address_info['zip'] = Parser.extract_address(
                        address_element_content2)

        phone_number_span_element = soup.find('span',
                                              {'id': 'ctl00_ContentPlaceHolderMainContent_SPSideBar1_PhoneNumbers'})
        if phone_number_span_element:
            phone_number_strong_elem = phone_number_span_element.find('strong')
            if phone_number_strong_elem:
                phone_number = phone_number_strong_elem.text
                if phone_number:
                    address_info['phone'] = phone_number
        web_link_anchor = soup.find('a', {'class': 'contact-right-link ala'})
        if web_link_anchor:
            web_link = web_link_anchor['href']
            if web_link:
                address_info['website'] = web_link

        return address_info


@staticmethod
def parse_all_search_category_links(page):
    soup = BeautifulSoup(page)
    category_anchors = soup.findAll('a', {'class': 'serviceCategoryUrl'})
    urls = []
    for each_anchor in category_anchors:
        urls.append(each_anchor['href'])
    return urls


@staticmethod
def find_if_nextbutton_available(page):
    soup = BeautifulSoup(page)
    return False


@staticmethod
def parse_proxy_ip_address(page):
    proxy_list = []
    soup = BeautifulSoup(page)
    oddtrs = soup.findAll('tr', {'class': 'odd'})
    eventrs = soup.findAll('tr', {'class': 'even'})
    for each_oddtr in oddtrs:
        try:
            ip = each_oddtr.findAll('td')[0].text.strip()
            proxy_list.append(ip)
        except Exception, msg:
            print 'Hmm Exception1 Occured '
            print msg
    for each_eventr in eventrs:
        try:
            ip = each_eventr.findAll('td')[0].text.strip()
            proxy_list.append(ip)
        except Exception, msg:
            print 'Hmm Exception2 Occured '
            print msg
    return proxy_list






