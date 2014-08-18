__author__ = 'Codengine'

from DBWraper import *

db = DBWraper()

cred_list = db.get_cred_list()

""" This script is responsible to init categories in the categories table. """

category_domains = []
file = open('angieslist_categories.csv','r')
content_list = file.read().split('\n')
for each_category in content_list:
    category_domains += [each_category.strip()]
file.close()

for cred in cred_list:
    db.save_categories_foracategory(category_domains,cred[0])


