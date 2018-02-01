#!/usr/bin/env python

#encoding=utf-8

import sys
import login_client
import argparse
import xlrd, xlwt

parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='the website address of erp')
parser.add_argument('username', type=str, help='the username login with')
parser.add_argument('password', type=str, help='the password login with')
parser.add_argument('inputfile', type=str, help='the employee need static')
parser.add_argument('outputfile', type=str, help='the statics datasheet')
parser.add_argument('year', type=int, help='the year of the statics')
parser.add_argument('--later-statics', help='include later time & count statics, default no', action="store_true")
parser.add_argument('--save-header', help='save the header image of employee', action='store_true')
args = parser.parse_args()

employees_list = []

input_sheet = xlrd.open_workbook(args.inputfile).sheets()[0]
output_workbook = xlwt.Workbook(encoding='utf-8')
output_sheet = output_workbook.add_sheet('2017-statics')

# 写入明目信息

SHEET_NAME_INDEX = 0
SHEET_EMAIL_INDEX = 1
SHEET_OVERTIME_TIME_INDEX = 2
SHEET_OVERTIME_MONEY_INDEX = 3
SHEET_REMEDIES_COUNT_INDEX = 4
SHEET_LATER_TIME_INDEX = 5
SHEET_LATER_COUNT_INDEX = 6
SHEET_DEPARTMENT_COUNT_INDEX = 7

output_sheet.write(0, SHEET_NAME_INDEX, '姓名')
output_sheet.write(0, SHEET_EMAIL_INDEX, '邮箱')
output_sheet.write(0, SHEET_OVERTIME_TIME_INDEX, '加班时间/分钟')
output_sheet.write(0, SHEET_OVERTIME_MONEY_INDEX, '加班补贴/元')
output_sheet.write(0, SHEET_REMEDIES_COUNT_INDEX, '补签次数/次')
output_sheet.write(0, SHEET_LATER_TIME_INDEX, '迟到时间/分钟')
output_sheet.write(0, SHEET_LATER_COUNT_INDEX, '迟到次数/次')
output_sheet.write(0, SHEET_DEPARTMENT_COUNT_INDEX, '部门')


for index in range(0, input_sheet.nrows):
    items = input_sheet.row(index)
    name = items[0].value
    email = items[1].value
    employees_list.append([name, email])

client = login_client.LoginClient(args.url, args.username, args.password)

login_result, login_description = client.login_in()

if login_result:
    print('登录成功')
else:
    print('登录失败:', login_description)
    sys.exit(-1)

output_row_index = 1

statics_count = 0

for employee in employees_list:
    name = employee[0]
    email = employee[1]

    employee_info = client.get_employee_info(name, email)
    overtime_time, overtime_money = client.get_employee_overtime(employee_info, args.year)
    remedies_count = client.get_employee_remedies(employee_info, args.year)

    output_sheet.write(output_row_index, SHEET_NAME_INDEX, name)
    output_sheet.write(output_row_index, SHEET_EMAIL_INDEX, email)
    output_sheet.write(output_row_index, SHEET_OVERTIME_TIME_INDEX, overtime_time)
    output_sheet.write(output_row_index, SHEET_OVERTIME_MONEY_INDEX, overtime_money)
    output_sheet.write(output_row_index, SHEET_REMEDIES_COUNT_INDEX, remedies_count)
    output_sheet.write(output_row_index, SHEET_DEPARTMENT_COUNT_INDEX, employee_info.department_name)

    if args.save_header:
        header_img = client.get_employee_header_image(employee_info)
        header_img.save('images/%s.gif'%name)
    
    if args.later_statics:
        later_time, later_count = client.get_employee_later(employee_info, args.year)
        output_sheet.write(output_row_index, SHEET_LATER_TIME_INDEX, later_time)
        output_sheet.write(output_row_index, SHEET_LATER_COUNT_INDEX, later_count)
        later_info_str = '迟到时间:%s分钟  迟到次数:%s'%(later_time, later_count)
    else:
        later_info_str = ''
    
    output_row_index = output_row_index + 1
    print(employee_info.abstract(), '加班:%s分钟 补贴:%s元 补签:%s次'%(overtime_time, overtime_money, remedies_count), 
            later_info_str)

    statics_count = statics_count + 1

output_workbook.save(args.outputfile) 
