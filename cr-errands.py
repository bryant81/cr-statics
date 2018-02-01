#!/usr/bin/env python

#encoding=utf-8

import sys
import login_client
import argparse
import xlrd, xlwt
from pyecharts import Pie, Page

rd_departments_list = ['嵌入部', '系统部', '软件部', '项目管理部', '硬件部', '结构部', '测试部', '研发中心']

cities = ("阿坝","阿拉善","阿里","安康","安庆","鞍山","安顺","安阳","澳门","北京","白银",
            "保定","宝鸡","保山","包头","巴中","北海","蚌埠","本溪","毕节","滨州","百色","亳州",
            "重庆","成都","长沙","长春","沧州","常德","昌都","长治","常州","巢湖","潮州","承德",
            "郴州","赤峰","池州","崇左","楚雄","滁州","朝阳","大连","东莞","大理","丹东","大庆",
            "大同","大兴安岭","德宏","德阳","德州","定西","迪庆","东营","鄂尔多斯","恩施","鄂州",
            "福州","防城港","佛山","抚顺","抚州","阜新","阜阳","广州","桂林","贵阳","甘南",
            "赣州","甘孜","广安","广元","贵港","果洛","杭州","哈尔滨","合肥","海口","呼和浩特",
            "海北","海东","海南","海西","邯郸","汉中","鹤壁","河池","鹤岗","黑河","衡水","衡阳",
            "河源","贺州","红河","淮安","淮北","怀化","淮南","黄冈","黄南","黄山","黄石","惠州",
            "葫芦岛","呼伦贝尔","湖州","菏泽","济南","佳木斯","吉安","江门","焦作","嘉兴","嘉峪关",
            "揭阳","吉林","金昌","晋城","景德镇","荆门","荆州","金华","济宁","晋中","锦州","九江",
            "酒泉","昆明","开封","兰州","拉萨","来宾","莱芜","廊坊","乐山","凉山","连云港",
            "聊城","辽阳","辽源","丽江","临沧","临汾","临夏","临沂","林芝","丽水","六安","六盘水",
            "柳州","陇南","龙岩","娄底","漯河","洛阳","泸州","吕梁","马鞍山","茂名","眉山","梅州",
            "绵阳","牡丹江","南京","南昌","南宁","宁波","南充","南平","南通","南阳","那曲","内江",
            "宁德","怒江","盘锦","攀枝花","平顶山","平凉","萍乡","莆田","濮阳","青岛","黔东南",
            "黔南","黔西南","庆阳","清远","秦皇岛","钦州","齐齐哈尔","泉州","曲靖","衢州","日喀则",
            "日照","上海","深圳","苏州","沈阳","石家庄","三门峡","三明","三亚","商洛","商丘","上饶",
            "山南","汕头","汕尾","韶关","绍兴","邵阳","十堰","朔州","四平","绥化","遂宁","随州","宿迁",
            "宿州","天津","太原","泰安","泰州","台州","唐山","天水","铁岭","铜川","通化","通辽",
            "铜陵","铜仁","台湾","武汉","乌鲁木齐","无锡","威海","潍坊","文山","温州","乌海","芜湖",
            "乌兰察布","武威","梧州","厦门","西安","西宁","襄樊","湘潭","湘西","咸宁","咸阳","孝感",
            "邢台","新乡","信阳","新余","忻州","西双版纳","宣城","许昌","徐州","香港","锡林郭勒","兴安",
            "银川","雅安","延安","延边","盐城","阳江","阳泉","扬州","烟台","宜宾","宜昌","宜春",
            "营口","益阳","永州","岳阳","榆林","运城","云浮","玉树","玉溪","玉林","杂多县","赞皇县",
            "枣强县","枣阳市","枣庄","泽库县","增城市","曾都区","泽普县","泽州县","札达县","扎赉特旗",
            "扎兰屯市","扎鲁特旗","扎囊县","张北县","张店区","章贡区","张家港","张家界","张家口","漳平市",
            "漳浦县","章丘市","樟树市","张湾区","彰武县","漳县","张掖","漳州","长子县","湛河区","湛江",
            "站前区","沾益县","诏安县","召陵区","昭平县","肇庆","昭通","赵县","昭阳区","招远市","肇源县",
            "肇州县","柞水县","柘城县","浙江","镇安县","振安区","镇巴县","正安县","正定县","正定新区",
            "正蓝旗","正宁县","蒸湘区","正镶白旗","正阳县","郑州","镇海区","镇江","浈江区","镇康县",
            "镇赉县","镇平县","振兴区","镇雄县","镇原县","志丹县","治多县","芝罘区","枝江市",
            "芷江侗族自治县","织金县","中方县","中江县","钟楼区","中牟县","中宁县","中山","中山区",
            "钟山区","钟山县","中卫","钟祥市","中阳县","中原区","周村区","周口","周宁县","舟曲县","舟山",
            "周至县","庄河市","诸城市","珠海","珠晖区","诸暨市","驻马店","准格尔旗","涿鹿县","卓尼",
            "涿州市","卓资县","珠山区","竹山县","竹溪县","株洲","株洲县","淄博","子长县","淄川区","自贡",
            "秭归县","紫金县","自流井区","资溪县","资兴市","资阳")

def get_city_from_remark(remark):

    if remark.find('展') != -1:
        return '展会'
    
    if remark.find('训') != -1 or remark.find('招聘') != -1:
        return '培训'

    for city in cities:
        if remark.find(city) != -1:
            return city

    spec_city = [('一所', '北京'),('通广', '济南'), ('西藏', '拉萨'), ('鲁软', '济南'), ('5000','合肥'), ('天地伟业','天津'),
            ('东电','重庆'), ('南瑞','南京'), ('山东','济南')]
    for spec in spec_city:
        if remark.find(spec[0]) != -1:
            return spec[1]

    print(remark)
    return '未知'


parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='the website address of erp')
parser.add_argument('username', type=str, help='the username login with')
parser.add_argument('password', type=str, help='the password login with')
parser.add_argument('inputfile', type=str, help='the employee need static')
parser.add_argument('outputfile', type=str, help='the statics datasheet')
parser.add_argument('year', type=int, help='the year of the statics')
args = parser.parse_args()

input_sheet = xlrd.open_workbook(args.inputfile).sheets()[0]
output_workbook = xlwt.Workbook(encoding='utf-8')
output_sheet = output_workbook.add_sheet('2017-statics')


SHEET_NAME_INDEX = 0
SHEET_EMAIL_INDEX = 1
SHEET_ARRANDS_TIME = 2
SHEET_ARRANDS_CITY = 3
SHEET_ARRANDS_REMARK = 4

output_sheet.write(0, SHEET_NAME_INDEX, '姓名')
output_sheet.write(0, SHEET_EMAIL_INDEX, '邮箱')
output_sheet.write(0, SHEET_ARRANDS_TIME, '出差时间')
output_sheet.write(0, SHEET_ARRANDS_REMARK, '出差是由')

employees_list = []
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

sales_errands_list = []
tranning_errands_list = []
exhibition_errands_list = []

for employee in employees_list:
    name = employee[0]
    email = employee[1]

    employee_info = client.get_employee_info(name, email)
    department_name = employee_info.department_name
    if department_name in rd_departments_list:
        errands_list = client.get_employee_errands(employee_info, args.year)
        for errands in errands_list:
            city = get_city_from_remark(errands[1])
            if city == '展会':
                exhibition_errands_list.append(errands)
            elif city == '培训' or city == '招聘':
                tranning_errands_list.append(errands)
            else:
                sales_errands_list.append((errands[0], city, errands[1]))

            output_sheet.write(output_row_index, SHEET_NAME_INDEX, name)
            output_sheet.write(output_row_index, SHEET_EMAIL_INDEX, email)
            output_sheet.write(output_row_index, SHEET_ARRANDS_TIME, int(errands[0]))
            output_sheet.write(output_row_index, SHEET_ARRANDS_CITY, city)
            output_sheet.write(output_row_index, SHEET_ARRANDS_REMARK, errands[1])
            
            output_row_index = output_row_index + 1
            statics_count = statics_count + 1
        
            #print('姓名:%s 出差时间:%s 出差原因:%s'%(name, errands[0], errands[1]))
#print(exhibition_errands_list)
#print(tranning_errands_list)
#print(sales_errands_list)

city_errands_count = {}
errands_count = 0

city_errands_time = {}
errands_time = 0

for errands in sales_errands_list:
    city = errands[1]
    
    if city not in city_errands_count:
        city_errands_count[city] = 1
    else:
        city_errands_count[city] = city_errands_count[city] + 1
    
    errands_count = errands_count + 1

    if city not in city_errands_time:
        city_errands_time[city] = int(errands[0])
    else:
        city_errands_time[city] = city_errands_time[city] + int(errands[0])
    
    errands_time = errands_time + int(errands[0])

#print(city_errands_count)
#print(city_errands_time)

page = Page()

pie_errands_count = Pie('2017研发出差次数统计(单位：次) 累计：%d次'% errands_count, width=1280, height=720, title_top='bootom')
pie_errands_count.add('', city_errands_count.keys(), city_errands_count.values(), is_label_show=True, label_text_color='#F00', legend_top='bottom')

pie_errands_time = Pie('2017研发出差时间统计(单位：工作小时/每个工作日7.5小时) 累计: %d 小时'% errands_time, width=1280, height=720, title_top='bootom')
pie_errands_time.add('', city_errands_time.keys(), city_errands_time.values(), is_label_show=True, label_text_color='#F00', legend_top='bottom')

page.add(pie_errands_count)
page.add(pie_errands_time)

page.render('2017研发出差统计.html')

    
output_workbook.save(args.outputfile)
