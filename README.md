# cr-statics

> A python tools for generating annual statistics

## Introduction
公司对于每年的考勤数据只有数据，没有趋势图，所以编写这个小工具[cr-statics](https://github.com/bryant81/cr-statics)，通过使用[requests](http://python-requests.org)和[pyecharts](http://pyecharts.org/)两个模块来统计分析一年的考勤的各项指标性数据，然后进行图形化展示。

## Installtation

### Python Compatibility

cr-statics works on for Python3.4+

cr-statics handles all strings and files with unicode encoding

## Basic Usage

### 获取给定的人员名单的年度各项统计

 ./cr-statics.py --url <考勤ERP网址> --login_name <登录用户名> --login_password <登录密码> --input_file <人员名单> --year <统计的年份>

* 人员名单需要符合json格式，如下:
> {'Name':'张三', 'Email':'ZhangSan@qq.com'}

