# - * - coding: UTF-8 - * -

import csv
import re, os,sys

class CSVWritter:
	def __init__(self,fileName):
		self.fileName = fileName
		csvFile = open(self.fileName,"wb")
		csvFile.close()
	def AppendToCSV(self,data):
		csvAllDataRows = []
		for each_row in data:
			csvDataRow = []
			csvDataRow.append(each_row["zip_code"].encode('utf-8').strip())
			csvDataRow.append(each_row["category"].encode('utf-8').strip())
			csvDataRow.append(each_row["business_name"].encode('utf-8').strip())
			csvDataRow.append(each_row["rating"].encode('utf-8').strip())
			csvDataRow.append(each_row["num_of_reviews"].encode('utf-8').strip())
			csvDataRow.append(each_row["coupon"].encode('utf-8').strip())
			csvDataRow.append(each_row["buy_itnow"].encode('utf-8').strip())
			csvDataRow.append(each_row["a1"].encode('utf-8').strip())
			csvDataRow.append(each_row["a2"].encode('utf-8').strip())
			csvDataRow.append(each_row["phone"].encode('utf-8').strip())
			csvDataRow.append(each_row["website"].encode('utf-8').strip())
			csvAllDataRows.append(csvDataRow)
		csvFile = open(self.fileName,"ab")
		csvWritter = csv.writer(csvFile)
		#counter = 1
		for eachDataRow in csvAllDataRows:
			try:
				print str(eachDataRow)
				csvWritter.writerow(eachDataRow)
				#counter += 1
				#if counter >= 3:
					#break
			except Exception,e:
				print str(e)
		csvFile.close()