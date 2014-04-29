# - * - coding: UTF-8 - * -

import urllib2
from DBWraper import *
import csv

class CSVMaker:
    def __init__(self):
        self.db = DBWraper()

    def start_processing(self):
        cred_list = self.db.get_cred_list_all()
        for cred in cred_list:
            info_details = self.db.read_info_details(cred[0])
            details_list = [
                ['Business Name','Category Name','Rating', 'Number Of Reviews', 'Coupon', 'Buy It Now', 'Address One', 'City', 'State', 'Zip', 'Phone', 'Website']
            ]
            for each_details in info_details:
                try:

                    #print each_details
                    category_info = self.db.read_category_details(each_details[2])
                    #print  each_details[2]
                    category_name = ''
                    if category_info:
                        category_name = category_info[3]
                    else:
                        category_page_link = each_details[16]
                        unquoted_cat_page_link = urllib2.unquote(category_page_link)
                        ss = unquoted_cat_page_link[unquoted_cat_page_link.index('&st=')+1:]
                        sss = ss[:ss.index('&')]
                        category_name = sss.replace('st=','')

                    details_list += [[u''+each_details[3].decode('ascii', 'ignore').encode('utf8'),category_name,each_details[4],each_details[5],
                    each_details[6],each_details[7],u''+each_details[8].decode('ascii', 'ignore').encode('utf8'),u''+each_details[10].decode('ascii', 'ignore').encode('utf8'),
                    u''+each_details[11].decode('ascii', 'ignore').encode('utf8'),u''+each_details[12].decode('ascii', 'ignore').encode('utf8'),each_details[13],each_details[14]]]
                except Exception,msg:
                    print each_details

            login_tuple = self.db.read_login_cred(each_details[1])

            file_name = login_tuple[1]+'.csv' if login_tuple else str(each_details[1])+'.csv'

            with open('Output/'+file_name, 'w') as fp:
                a = csv.writer(fp, delimiter=',')
                a.writerows(details_list)

CSVMaker().start_processing()