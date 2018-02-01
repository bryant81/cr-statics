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

* cr-statics.py
    * 支持获取员工基本信息
    * 支持获取加班时间，加班补贴，迟到次数，迟到时间，补签次数的统计
    * 支持获取头像
* xl2charts.py
    * 支持cr-statics.py产生的报表图形化展示
    * 支持全公司/研发中心过滤

* cr-errands.py
    * 支持出差频率和时间统计
