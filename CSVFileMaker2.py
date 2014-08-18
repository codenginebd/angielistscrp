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
                ['Business Name','Category Name','Rating', 'Number Of Reviews', 'Coupon', 'Buy It Now', 'Address One', 'City', 'State', 'Zip', 'Phone', 'Website','acc_address','acc_city','acc_state','acc_zip','detail_link']
            ]
            for each_details in info_details:
                try:

                    details_list += [[u''+urllib2.unquote(each_details[4]).decode('ascii', 'ignore').encode('utf8'),u''+urllib2.unquote(each_details[1]).decode('ascii', 'ignore').encode('utf8'),
                                      each_details[5],each_details[6],each_details[7],each_details[8],u''+urllib2.unquote(each_details[9]).decode('ascii', 'ignore').encode('utf8'),
                                      u''+each_details[11].decode('ascii', 'ignore').encode('utf8'),u''+each_details[12].decode('ascii', 'ignore').encode('utf8'),
                                      u''+each_details[13].decode('ascii', 'ignore').encode('utf8'),each_details[14],each_details[15],u''+urllib2.unquote(each_details[25]).decode('ascii', 'ignore').encode('utf8'),
                                      u''+each_details[26].decode('ascii', 'ignore').encode('utf8'),each_details[27],each_details[28],each_details[18]]]
                except Exception,msg:
                    print each_details

                login_tuple = self.db.read_login_cred(each_details[2])

                file_name = login_tuple[1]+'.csv' if login_tuple else str(each_details[1])+'.csv'

                with open('Output/'+file_name, 'w') as fp:
                    a = csv.writer(fp, delimiter=',')
                    a.writerows(details_list)

CSVMaker().start_processing()