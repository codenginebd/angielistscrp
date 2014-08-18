# - * - coding: UTF-8 - * -

import urllib2

from datetime import datetime

import pymysql

db_name = 'spiderbot'
uname = 'root'
password = 'root'
host = '127.0.0.1'

db_name2 = 'spiderbot_w2'

class DBWraper:
    def __init__(self,w1=True):
        try:
            if w1:
                print 'Connecting database %s' % db_name
                self.dbconn = pymysql.connect(charset='utf8', init_command='SET NAMES UTF8',host=host,user=uname,passwd=password,db=db_name)
            else:
                print 'Connecting database %s' % db_name2
                self.dbconn = pymysql.connect(charset='utf8', init_command='SET NAMES UTF8',host=host,user=uname,passwd=password,db=db_name2)
            #self.dbconn.set_character_set('utf8') #cur = self.dbconn.cursor()
            #cur.execute('SET NAMES utf8;')
        except Exception,msg:
            self.dbconn = None

    def read_dates_by_group(self,login_cred_id):
        dates = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select last_updated_address from info_details where login_cred_id=%s and address1 != '' group by DATE(last_updated_address)" % str(login_cred_id))
            rows = cur.fetchall()
            for each_row in rows:
                dates += [each_row[0]]
            cur.close()
        return dates

    def get_cred_list(self,start=0,limit=1234567890):
        cred_list = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute('select * from login_cred where blocked=0 and done=0 order by id limit %s,%s' % (str(start),str(limit)))
            rows = cur.fetchall()
            for each_row in rows:
                cred_list.append(each_row)
        return cred_list

    def get_cred_list_crawler_one(self,start=0,limit=1234567890):
        cred_list = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute('select * from login_cred where blocked=0 and basic_info_crawled=0 order by id limit %s,%s' % (str(start),str(limit)))
            rows = cur.fetchall()
            for each_row in rows:
                cred_list.append(each_row)
        return cred_list

    def get_cred_list_all(self):
        cred_list = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute('select * from login_cred')
            rows = cur.fetchall()
            for each_row in rows:
                cred_list.append(each_row)
        return cred_list

    def get_cred_list_one(self):
        cred_list = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute('select * from login_cred where blocked=0 and done=0 and category_crawled=0')
            rows = cur.fetchall()
            for each_row in rows:
                cred_list.append(each_row)
        return cred_list

    def read_last_saved_state(self):
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute('select * from cat_last_state limit 1')
            row = cur.fetchone()
            return row

    def save_last_state(self,login_cred_id):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                cur.execute('delete from cat_last_state')
                cur.execute('insert into cat_last_state(login_cred_id) values(%s)' % str(login_cred_id))

    def read_last_row_current_states(self):
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute('select * from current_state order by id desc limit 1')
            row = cur.fetchone()
            return row

    def mark_login_info_as_cat_crawled(self,login_cred_id):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                cur.execute('update login_cred set category_crawled=1 where id=%s' % str(login_cred_id))

    def mark_login_as_blocked(self,login_cred_id):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                cur.execute('update login_cred set blocked=1 where id=%s' % str(login_cred_id))

    def update_login_cred(self,record):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                cur.execute('update login_cred set blocked=%s,done=%s where id=%s' % (str(record[3]),str(record[4]),str(record[0])))

    def update_login_cred_basic_info_fetched(self,record):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                cur.execute('update login_cred set blocked=%s,basic_info_crawled=%s where id=%s' % (str(record[3]),str(record[5]),str(record[0])))

    def update_cat_as_read(self,cat_id):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                cur.execute('update tbl_category set visited=1 where id=%s' % str(cat_id))

    def delete_current_record(self,login_cred_id,cat_id):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                query = 'delete from current_state where cat_id=%s and login_cred_id=%s' % (str(cat_id),str(login_cred_id))
                print query
                cur.execute(query)

    def get_login_cred(self,uname,password):
        if self.dbconn:
            try:
                cur = self.dbconn.cursor()
                cur.execute("select * from login_cred where email='%s' and password='%s'" % (uname,password))
                record = cur.fetchone()
                return record
            except Exception,msg:
                pass

    def save_category_info(self,data):
        if self.dbconn:
            with self.dbconn:
                for each_data in data:
                    try:
                        cursor = self.dbconn.cursor()
                        query = "insert into tbl_category(login_cred_id,zip_code,cat_name,cat_link) values(%s,'%s','%s','%s')" % (each_data[0],each_data[1],each_data[2],each_data[3])
                        print query
                        cursor.execute(query)
                        print 'Done!'
                    except Exception,msg:
                        print msg

    def read_current_state(self,login_cred_id):
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select * from current_state where login_cred_id=%s" % str(login_cred_id))
            record = cur.fetchone()
            return record

    def read_last_state(self):
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select * from cat_last_state limit 1")
            record = cur.fetchone()
            return record

    def read_first_row_cat(self):
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select * from tbl_category limit 0,1")
            record = cur.fetchone()
            return record

    def read_cat_offset_all(self,offset):
        data = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select * from tbl_category limit %s,18446744073709551615" % str(offset))
            rows = cur.fetchall()
            for each_row in rows:
                data.append(each_row)
        return data

    def read_cat_list(self,login_cred_id):
        data = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select * from tbl_category where login_cred_id=%s" % str(login_cred_id))
            rows = cur.fetchall()
            for each_row in rows:
                data.append(each_row)
        return data

    def delete_cat(self,cat_id):
        with self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("delete from tbl_category where id=%s" % str(cat_id))

    def read_cat_list_all(self):
        data = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select * from tbl_category")
            rows = cur.fetchall()
            for each_row in rows:
                data.append(each_row)
        return data

    def get_first_unread_cat_record(self,login_cred_id):
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute("select * from tbl_category where login_cred_id=%s and visited=0 limit 1" % str(login_cred_id))
            record = cur.fetchone()
            return record

    def update_current_state(self,record):
        if self.dbconn:
            with self.dbconn:
                cur = self.dbconn.cursor()
                cur.execute('select * from current_state where cat_id=%s and login_cred_id=%s limit 1' % (str(record[1]),str(record[5])))
                _record = cur.fetchone()
                if _record:
                    cur.execute("update current_state set page_index=%s,link1='%s',link2='%s',status=%s where cat_id=%s and login_cred_id=%s limit 1" % (str(record[2]),record[6],record[7],str(record[4]),str(record[1]),str(record[5])))
                else:
                    q = "insert into current_state(cat_id,page_index,total_page,status,login_cred_id,link1,link2) values(%s,%s,%s,%s,%s,'%s','%s')" % (str(record[1]),str(record[2]),str(record[3]),str(record[4]),str(record[5]),record[6],record[7])
                    cur.execute(q)

    def save_info_details(self,data,login_cred_id,category_id,page_count,page_link):
        if self.dbconn:
            with self.dbconn:
                for each_record in data:
                    try:

                        query = "insert into info_details(login_cred_id,tb_category_id,business_name,rating,number_of_reviews,coupon,buy_itnow,address1,address2,city,state,zip,phone,website,page_count,link) values(%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,'%s')" % (u''+str(login_cred_id),u''+str(category_id),u''+each_record['business_name'].replace("'",r"\'").encode('ascii', 'ignore'),u''+each_record['rating'],u''+each_record['num_of_reviews'],
                                                                                                                                                                                                                                                                                                     u''+each_record['coupon'],u''+each_record['buy_itnow'],u''+each_record['a1'].encode('ascii', 'ignore'),u''+each_record['a2'].encode('ascii', 'ignore'),u''+each_record['city'].encode('ascii', 'ignore'),
                                                                                                                                                                                                                                                                                                     u''+each_record['state'].encode('ascii', 'ignore'),u''+each_record['zip'],u''+each_record['phone'],u''+each_record['website'],u''+str(page_count),u''+str(page_link))


                        cur = self.dbconn.cursor()

                        cur.execute(query)
                    except Exception,msg:
                        print 'Exception Occured inside Save Info Details.'
                        print msg
                        print 'Data: '
                        print each_record
                        print 'StackTrace Ended.'
                        pass

    def save_basic_info(self,data,login_cred_id,category_name):
        if self.dbconn:
            with self.dbconn:
                for each_record in data:
                    try:
                        query = """insert into info_details(login_cred_id,category_name,business_name,rating,number_of_reviews,coupon,buy_itnow,details_link,s_primaryaddress,s_primary_location,s_address,s_city,s_state,s_zip,laddress,lcity,lstate,lzip,address_fetched,last_updated_basic,link)
                        values(%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',0,'%s','%s')""" % (str(login_cred_id),urllib2.quote(category_name),
                        urllib2.quote(each_record['business_name']),each_record['rating'],each_record['num_of_reviews'],each_record['coupon'],each_record['buy_itnow'],
                        each_record['dlink'],urllib2.quote(each_record['s_primaryaddress']),urllib2.quote(each_record['s_primarylocation']),urllib2.quote(each_record['s_address']),
                        urllib2.quote(each_record['s_city']),each_record['s_state'],each_record['s_zip'],urllib2.quote(each_record['l_address']),urllib2.quote(each_record['l_city']),each_record['l_state'],each_record['l_zip'],datetime.now(),each_record['link'])

                        cur = self.dbconn.cursor()
                        cur.execute(query)

                    except Exception,msg:
                        print 'Exception Occured inside save_basic_info'
                        print msg
                        print 'Data: '
                        print each_record
                        print 'StackTrace Ended.'
                        pass

    def read_info_details(self,login_cred_id,date):
        results = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            query = "select * from info_details where login_cred_id=%s and DATE(last_updated_address)>='%s' and address1 != ''" % (str(login_cred_id),date)
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                results.append(row)
        return results

    def read_login_cred(self,login_cred_id):
        if self.dbconn:
            cur = self.dbconn.cursor()
            query = "select * from login_cred where id=%s" % str(login_cred_id)
            cur.execute(query)
            return cur.fetchone()

    def read_category_details(self,cat_id):
        if self.dbconn:
            cur = self.dbconn.cursor()
            query = "select * from tbl_category where id=%s" % str(cat_id)
            cur.execute(query)
            return cur.fetchone()

    def read_missing_address_rows(self,login_cred_id):
        results = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            query = "select * from info_details where city='' and state='' and zip='' and address1!='' and cast(number_of_reviews as unsigned)>=3 and login_cred_id=%s" % str(login_cred_id)
            print query
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                results.append(row)
        return results

    def update_missing_info(self,data):
        if self.dbconn:
            with self.dbconn:
                for each_data in data:
                    query = "update info_details set address2='%s',city='%s',state='%s',zip='%s' where id=%s" % (each_data['a2'],each_data['city'],each_data['state'],each_data['zip'],str(each_data['info_id']))
                    cur = self.dbconn.cursor()
                    cur.execute(query)

    def read_last_unread_category(self,login_cred_id):
        if self.dbconn:
            query = 'select * from categories where login_cred_id=%s and visited=0 limit 1' % str(login_cred_id)
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result

    def save_categories_foracategory(self,category_list,login_cred_id):
        if self.dbconn:
            with self.dbconn:
                for category in category_list:
                    try:
                        query = "insert into categories(login_cred_id,category_name,visited) values(%s,'%s',0)" % (str(login_cred_id),category)
                        cursor = self.dbconn.cursor()
                        cursor.execute(query)
                        cursor.close()
                    except Exception,msg:
                        pass

    def mark_category_read(self,cat_id):
        if self.dbconn:
            with self.dbconn:
                query = 'update categories set visited=1 where id=%s' % str(cat_id)
                cursor = self.dbconn.cursor()
                cursor.execute(query)
                cursor.close()

    def read_basic_info_address_unfetched(self,login_cred_id,count=13):
        results = []
        if self.dbconn:
            query = "select * from info_details where login_cred_id=%s and address_fetched=0 and ((number_of_reviews >= '4' and rating ='A') or (number_of_reviews >= '15' and rating ='B')) limit %s" % (str(login_cred_id),str(count))
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                results.append(row)
            cursor.close()
        return results

    def mark_basic_info_address_fetched(self,id):
        if self.dbconn:
            with self.dbconn:
                query = 'update info_details set address_fetched=1 where id=%s' % str(id)
                cursor = self.dbconn.cursor()
                cursor.execute(query)
                cursor.close()

    def update_basic_info_with_address(self,id,address_info):
        if self.dbconn:
            with self.dbconn:
                query = ''
                try:
                    query = "update info_details set address1='%s',address2='%s',city='%s',state='%s',zip='%s',phone='%s',website='%s',address_fetched=1,last_updated_address='%s' where id=%s" % (urllib2.quote(address_info['a1']),urllib2.quote(address_info['a2']),urllib2.quote(address_info['city']),address_info['state'],address_info['zip'],address_info['phone'],address_info['website'],datetime.now(),str(id))
                    cursor = self.dbconn.cursor()
                    cursor.execute(query)
                    cursor.close()
                except Exception,msg:
                    print 'Exception Inside update basic info with address method.'
                    print msg
                    print query
                    print 'Msg Ended.'

    def close(self):
        if self.dbconn:
            self.dbconn.close()

#db = DBWraper()
#d = db.read_dates_by_group(1)
#for i in d:
#    print db.read_info_details(1,i.date())
#    break
#db.update_current_state((1,1,1,'LINK',1,1,1))
#db.save_category_info([(1,'','cat_name','http://stackoverflow.com/questions/5687718/python-mysql-insert-data')])
#print len('http://stackoverflow.com/questions/5687718/python-mysql-insert-data')



