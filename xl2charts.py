#!/usr/bin/env python


from pyecharts import Scatter, Bar, Page
import xlrd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', type=str, help='the statics file from cr-statics')
parser.add_argument('--only-rd', help='only report R&D Center department', action='store_true')
args = parser.parse_args()

rd_departments_list = ['嵌入部', '系统部', '软件部', '项目管理部', '硬件部', '结构部', '测试部', '研发中心']

page=Page()

if args.only_rd:
    subtitle = '创世科技研发中心2017年度(2016.12.25-2017.12.24)统计数据'
else:
    subtitle = '创世科技2017年度(2016.12.25-2017.12.24)统计数据'

later_charts = Scatter(title='迟到', subtitle=subtitle, width=1920, height=1080)
overtime_charts = Scatter(title='加班', subtitle=subtitle, width=1920, height=1080)
remedies_bar = Bar(title='补签', subtitle=subtitle, width=1920, height=1080)

sheet = xlrd.open_workbook(args.inputfile).sheets()[0]

name_list = []
remedies_count_list = []


for index in range(1, sheet.nrows):
    items = sheet.row(index) 
    
    name = items[0].value
    overtime_time = items[2].value
    overtime_money = items[3].value
    remedies_count = items[4].value
    later_time = items[5].value
    later_count = items[6].value
    department_name = items[7].value

    if (args.only_rd and department_name in rd_departments_list) or not args.only_rd:
        later_charts.add([name], [later_time], [later_count], xaxis_name='迟到累计时间(分钟)', yaxis_name='迟到累计次数', yaxis_name_gap=40)
        overtime_charts.add([name], [overtime_time], [overtime_money], xaxis_name='加班累计时间(分钟)', yaxis_name='加班累计餐补(元)', yaxis_name_gap=40)

        remedies_count_list.append(remedies_count+0.5)
        name_list.append(name)

remedies_bar.add('', name_list, remedies_count_list, is_xaxis_show=False, yaxis_name='累计补签次数', xaxis_pos='top', tooltip_formatter='{b}:{c}次')

page.add(remedies_bar)
page.add(later_charts)
page.add(overtime_charts)

page.render()
