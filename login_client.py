#encoding=utf-8
import sys
import hashlib
import demjson
import requests
import re
import datetime
import urllib
import base64
from PIL import Image
from io import BytesIO

def SearchKVInJson(key, str_json):
    status = re.search(key+':\'(?P<result>[^\']+)', str_json)
    if status:
        return status.group('result')
    else:
        return 'Unkown'

def SearchArrayInJson(array_name, str_json):

    default = {'EmployeeDepartmentID':'None', 'DepartmentName':'None', 'DepartmentID':'None', 'DepartmentTitleName':'None',
            'DepartmentTitleID':'None'}
    array_value_str = str_json[str_json.find(array_name):]
    status = re.search('[^\(]\(+(?P<result>[^\)]+)', array_value_str)
    if status:
        try:
            return demjson.decode(status.group('result'))
        except:
            return default

    return default

def SearchArraysInJson(array_name, str_json):
    array_value_str = str_json[str_json.find(array_name):]
    status = re.search('[^\(]\(+(?P<result>[^\)]+)', array_value_str)
    if status:
        json_list = re.findall('{[^}]+}', status.group('result'))
        ret_list = []
        for item in json_list:
            ret_list.append(demjson.decode(item))
        
    return ret_list

def DisplayProgressBar(title, progress):
    sys.stdout.write(title + 'complete:%d%%\r'%progress)
    

def GenerateURL(url, param_dict):
    url = url + '?'
    for k, v in param_dict.items():
        url = url + k + '=' + v + '&'
    return url[:-1]

def GetTime():
    return datetime.datetime.now().strftime('%a %b %d 20%y %X GMT+0800 (CST)').replace(' ', '%20')

class Employee:
    """ 员工基本信息类

    Attributes:
        name: 姓名
        email: 邮箱地址
        appoint_date: 入职日期
        formal_date: 转正日期
        attendance_id: 考勤卡号
        work_status: 在职状态
        birth_date: 出生日期
        wage_id: 薪水编号
        employee_id: 职工编号
        department_name: 所在部门名称
        department_id: 所在部门的ID
        department_title_name: 所在部门的职位
        department_title_id: 所在部门的职位ID 
    """

    def __init__(self, name, email, infostr):
        """构造函数
        Attributes:
            name: 姓名
            email: 邮箱
            infostr: 网页服务GetCorporationInformationByEmployee返回的响应内容
        """
        self.name = name
        self.email = email
        self.appoint_date = SearchKVInJson('AppointmentDate', infostr)
        self.formal_date = SearchKVInJson('FormalDate', infostr)
        self.attendance_id = SearchKVInJson('AttendanceID', infostr)
        self.work_status = SearchKVInJson('Status', infostr)
        self.birth_date = SearchKVInJson('BirthDate', infostr)
        self.wage_id = SearchKVInJson('WageSerialNumber', infostr)

        departments_info = SearchArrayInJson('Departments', infostr)
        self.employee_id = departments_info['EmployeeDepartmentID'] if 'EmployeeDepartmentID' in departments_info else 'Unkown'
        self.department_name = urllib.parse.unquote(departments_info['DepartmentName']) if 'DepartmentName' in departments_info else 'Unkown'
        self.department_id = departments_info['DepartmentID'] if  'DepartmentID' in departments_info else 'Unkown'
        self.department_title_name = urllib.parse.unquote(departments_info['DepartmentTitleName']) if 'DepartmentTitleName' in departments_info  else 'Unkown'
        self.department_title_id =  departments_info['DepartmentTitleID'] if 'DepartmentTitleID' in departments_info else 'Unkown'
    
    def __str__(self):

        common_info = "{姓名:%s 邮箱:%s 入职时间:%s 转正时间:%s 考勤卡号:%s 在职状态:%s 出生日期:%s }" % (
                        self.name, self.email, self.appoint_date, self.formal_date, self.attendance_id,
                        self.work_status, self.birth_date)

        department_info = "{职工编号:%s 部门名称:%s 部门ID:%s 职位名称:%s 职位ID:%s}"%(
                            self.employee_id, self.department_name, self.department_id,
                            self.department_title_name, self.department_title_id)

        return common_info + department_info

    def abstract(self):
        return "{姓名:%s 邮箱:%s 入职:%s 部门:%s 职位:%s}"%(
                self.name, self.email, self.appoint_date, self.department_name, self.department_title_name)


class LoginClient:
    """ 登录考勤服务后的一个可进行进一步操作的类
    
    Attributes:
        __url: 考勤信息查询服务地址
        __username: 登录账户名
        __password: 登录密
    
    """

    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password

    def login_in(self):
        """ 使用用户名和密码登录到考勤信息网页服务
        Args:
        Returns: 
            返回一个(Result, Description)
            Result:True/False
            Description:描述登录失败的原因
        Raises:
        """
        payload = {}
    
        # step0. 建立会话
        self.session = requests.Session()
        
        try:
            # step1. 使用senssion可以保证此次对话使用的UDP端口和cookies
            response = self.session.get(self.__url, timeout=5)
        except requests.exceptions.ReadTimeout:
            return (False, '连接%s超时'%self.__url)
        
        # 保存服务器返回的cookies, 后面需要使用
        self.login_cookies = response.cookies
        
        #发送这个cookie表示支持cookie
        requests.utils.add_dict_to_cookiejar(self.login_cookies, {'testcookie':'yes'})
        
        # step2. 通过登录名获取所在部门的ID, 这一步可以不需要, 如果知道所在的部门ID的画
        cur_path = 'php/erpfs.php'
        payload.clear()
        payload['action'] = 'QueryDepartmentByLoginID'
        payload['time'] = GetTime()
        form_data = {'logintype':'name', 'loginid':self.__username, 'cktime':'31536000000'}
        response = self.session.post(GenerateURL(self.__url + cur_path, payload), data=form_data)
        
        department_info = demjson.decode(response.text)['departments']
        if len(department_info) > 0:
            department_id = department_info[0]['id']
        else:
            return False, '用户名[%s]和密码[%s]不正确'%(self.__username, self.__password)

        
        # step3. 登录ERP平台
        cur_path = 'php/erpfs.php'
        payload.clear()
        payload['action'] = 'LoginCheck'
        payload['time'] = GetTime()

        md5=hashlib.md5()
        md5.update(self.__password.encode('utf-8'))
        hexpassword = md5.hexdigest()

        form_data = {'logintype':'name', 'loginid':self.__username, 'department':department_id, 'hexpassword':hexpassword, 
                'cktime':"31536000000"}
        response = self.session.post(GenerateURL(self.__url + cur_path, payload), data=form_data)
        
        login_description = SearchKVInJson('description', response.text)
        
        if login_description == 'success':
            login_result = True
        else:
            login_result = False

        return (login_result, login_description)

    def login_out(self):
        """ 注销已经登录的账号信息
        Args:
        Returns:
        Raises:
        """
        if hasattr(self, 'session'):
            self.session.close()
        pass

    def get_employee_info(self, name, email):
        """ 通过员工姓名和邮箱，获取员工基本信息
        Args:
            name:员工注册姓名
            email:员工注册邮箱
        Returns:
            成功：一个Employess类的对象
            失败：None
        Raises:
        """
        payload = {}
        cur_path='php/employeefs.php'
        payload['action'] = 'GetCorporationInformationByEmployee'
        payload['employeeidentity'] = email
        payload['time'] = GetTime()
        response = self.session.get(GenerateURL(self.__url + cur_path, payload), cookies=self.login_cookies)

        return Employee(name, email, base64.b64decode((demjson.decode(response.content))['content']).decode('utf-8'))

    def get_employee_overtime(self, employee, year):
        """ 获取员工的年度加班累计时间，加班累计补贴金额

        Args:
            employee: Employee对象，通过get_employee_info返回值得到
            year: 需要统计的年份

        Returns:
            (time, money)
            time: 加班累计时间，单位:小时
            money:加班累计补贴，单位:元
        Raises:
        """
        startdate = '%d-%d-%d'%(year-1, 12, 24)
        enddate = '%d-%d-%d'%(year, 12, 25)

        cur_path='php/attendancefs.php'
        payload = {}
        payload['action'] = 'GetWorkOversByAttendanceIDAndDateEx'
        payload['appointmentdate'] = '2015-06-09'
        payload['attendanceid'] = employee.attendance_id
        payload['startdate'] = startdate
        payload['enddate'] = enddate
        payload['time'] = GetTime()
        response = self.session.get(GenerateURL(self.__url + cur_path, payload), cookies=self.login_cookies)
        content = response.content.decode('utf-8')
        try:
            overtime_time = int(SearchKVInJson('TotalSeconds', content))/60
            overtime_money = int(SearchKVInJson('TotalMoney', content))
        except:
            overtime_time = 0
            overtime_money = 0

        return int(overtime_time), overtime_money
    def get_employee_later(self, employee, year):
        """ 获取员工的年度迟到总时间和迟到总次数
        Args:
            employee: Employee对象，通过get_employee_info返回值得到
            year: 需要统计的年份

        Returns:
            (time, count)
            time: 迟到累计时间, 单位: 分钟
            count: 迟到累计次数， 单位: 次

        Raises:
        """
        startdate = '%d-%d-%d'%(year-1, 12, 24)
        enddate = '%d-%d-%d'%(year, 12, 25)

        cur_path='php/attendancefs.php'
        payload = {}
        payload['action'] = 'GetAttendanceBookByAttendanceID'
        payload['appointmentdate'] = '2015-06-09'
        payload['attendanceid'] = employee.attendance_id
        payload['startdate'] = startdate
        payload['enddate'] = enddate
        payload['time'] = GetTime()
        response = self.session.get(GenerateURL(self.__url + cur_path, payload), cookies=self.login_cookies)
        result = re.findall('WorkOnLater:[^,]+', response.content.decode('utf-8'))
        later_total_time = 0
        later_total_count = 0
        for item in result:
            later_time = int(item[item.find(':')+2:-1])
            if later_time > 0:
                later_total_count = later_total_count + 1
                later_total_time = later_total_time + later_time

        return (int(later_total_time/60), later_total_count)

    def get_employee_remedies(self, employee, year):
        """ 获取员工的年度补打卡次数
        
        Args:
            employee: Employee对象，通过get_employee_info返回值得到
            year: 需要统计的年份

        Returns:
            count: 补签打卡次数的累计次数

        Raises:
        """
        startdate = '%d-%d-%d'%(year-1, 12, 24)
        enddate = '%d-%d-%d'%(year, 12, 25)

        payload = {}
        cur_path='php/attendancefs.php'
        payload['action'] = 'GetRemediesByAttendanceIDsAndDateEx'
        payload['listpagejumpto'] = '1'
        payload['listperpage'] = '1000'
        payload['time'] = GetTime()
        payload['appointmentdate'] = '2015-06-09'
        payload['attendanceids'] = '%27'+employee.attendance_id+'%27'
        payload['startdate'] = startdate
        payload['enddate'] = enddate
        response = self.session.get(GenerateURL(self.__url + cur_path, payload), cookies=self.login_cookies)

        try:
            remedies_count = int(SearchKVInJson('count', response.text))
        except:
            remedies_count = 0

        return remedies_count

    def get_employee_header_image(self, employee):
        """获取员工的头像

        Args:
            employee: Employee对象，通过get_employee_info返回

        Returns:
            图像二进制数据

        Raises:
        """
        headers={'Accept':'image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5'}
        payload = {}
        cur_path='php/showemployeehoto.php'
        payload['employeeIdentity'] = employee.email
        payload['time'] = GetTime()
        response = self.session.get(GenerateURL(self.__url + cur_path, payload), cookies=self.login_cookies, headers=headers)
        return Image.open(BytesIO(response.content))


