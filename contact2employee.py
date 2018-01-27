#!/usr/bin/env python3
# encoding=utf-8

import sys
import xlrd, xlwt
import re

xl_input_name = sys.argv[1]
xl_output_name = sys.argv[2]

input_sheet = xlrd.open_workbook(xl_input_name).sheets()[0]

workbook_output = xlwt.Workbook(encoding='utf-8')
output_sheet = workbook_output.add_sheet('employees')

output_row_index = 0
for row_index in range(2, input_sheet.nrows):
    row_item = input_sheet.row(row_index)
    if(len(row_item[3].value) > 0 and -1 != row_item[6].value.find('@')):
        name = row_item[3].value
        email = row_item[6].value.lstrip().rstrip()
        print('[%s][%s]'%(name, email))
        email = re.match('[^\n]+', email).group()
        if(email.find(' ') != -1):
            email = email[:email.find(' ')]
        output_sheet.write(output_row_index, 0, name)
        output_sheet.write(output_row_index, 1, email)
        output_row_index = output_row_index + 1

workbook_output.save(xl_output_name)
