# - * - coding: UTF-8 - * -

import MySQLdb

db_name = 'spiderbot'
uname = 'root'
password = 'root'
host = '127.0.0.1'

class DBWraper:
    def __init__(self):
        try:
            self.dbconn = MySQLdb.connect(charset='utf8', init_command='SET NAMES UTF8',host=host,user=uname,passwd=password,db=db_name)
            self.dbconn.set_character_set('utf8') #cur = self.dbconn.cursor()
            #cur.execute('SET NAMES utf8;')
        except Exception,msg:
            self.dbconn = None

    def get_cred_list(self,start=0,limit=1234567890):
        cred_list = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            cur.execute('select * from login_cred where blocked=0 and done=0 order by id limit %s,%s' % (str(start),str(limit)))
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

    def read_info_details(self,login_cred_id):
        results = []
        if self.dbconn:
            cur = self.dbconn.cursor()
            query = "select * from info_details where login_cred_id=%s" % str(login_cred_id)
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


    def close(self):
        if self.dbconn:
            self.dbconn.close()

#db = DBWraper()
#db.update_current_state((1,1,1,'LINK',1,1,1))
#db.save_category_info([(1,'','cat_name','http://stackoverflow.com/questions/5687718/python-mysql-insert-data')])
#print len('http://stackoverflow.com/questions/5687718/python-mysql-insert-data')



