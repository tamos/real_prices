
# usage: bash collect_urls.sh > file_list.txt
curl http://www.winnipegassessment.com/AsmtTax/English/SelfService/SalesBooks.stm  | grep -o  '/AsmtTax.*\.pdf' | awk '{print "http://www.winnipegassessment.com"$0 }'
