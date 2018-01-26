#!/usr/bin/env python
import sys

import unittest
import login_client

url = 'http://192.168.43.2/erp/'


class TestLoginIn(unittest.TestCase):
    
    # 正确的登录
    def test_login_in_normal(self):
        loginclient = login_client.LoginClient(url, '郑浩', 'zhenghao')
        login_result, login_description = loginclient.login_in()
        self.assertEqual(login_result, True)
        self.assertIsInstance(login_description, str)
        loginclient.login_out()
    
    # 错误的登录1
    def test_login_in_with_incorrect_username_password(self):
        loginclient = login_client.LoginClient(url, 'xx', 'oo')
        login_result, login_description = loginclient.login_in()
        self.assertEqual(login_result, False)
        self.assertIsInstance(login_description, str)
        loginclient.login_out()

    # 错误的登录2
    def test_login_in_with_incorrect_url(self):
        loginclient = login_client.LoginClient(url, 'xx', 'oo')
        login_result, login_description = loginclient.login_in()
        self.assertEqual(login_result, False)
        self.assertIsInstance(login_description, str)
        loginclient.login_out()

class TestLoginClientGet(unittest.TestCase):

    def setUp(self):
        self.login_client = login_client.LoginClient(url, '郑浩', 'zhenghao')
        self.login_client.login_in()

    def test_get_employee_info(self):
        
        employee = self.login_client.get_employee_info('郑浩', 'zhenghao@crearo.com')
        self.assertNotEqual(employee.attendance_id, 'Unkown')

        employee = self.login_client.get_employee_info('xx', 'xx@crearo.com')
        self.assertEqual(employee.attendance_id, 'Unkown')

    def test_get_employee_overtime(self):
        employee = self.login_client.get_employee_info('郑浩', 'zhenghao@crearo.com')
        overtime_time, overtime_money = self.login_client.get_employee_overtime(employee, 2017)
        self.assertIsInstance(overtime_time, int)
        self.assertIsInstance(overtime_money, int)

        employee = self.login_client.get_employee_info('xx', 'xx@crearo.com')
        overtime_time, overtime_money = self.login_client.get_employee_overtime(employee, 2017)
        self.assertEqual(overtime_time, 0)
        self.assertEqual(overtime_money, 0)

    def test_get_employee_remedies(self):
        employee = self.login_client.get_employee_info('郑浩', 'zhenghao@crearo.com')
        remedies_count = self.login_client.get_employee_remedies(employee, 2017)
        self.assertIsInstance(remedies_count, int)

        employee = self.login_client.get_employee_info('xx', 'xx@crearo.com')
        remedies_count = self.login_client.get_employee_remedies(employee, 2017)
        self.assertEqual(remedies_count, 0)

    def test_get_employee_later(self):
        employee = self.login_client.get_employee_info('郑浩', 'zhenghao@crearo.com')
        later_total_time, later_total_count = self.login_client.get_employee_later(employee, 2017)
        self.assertIsInstance(later_total_time, int)
        self.assertIsInstance(later_total_count, int)

    def tearDown(self):
        self.login_client.login_out()

if __name__ == '__main__':
    unittest.main(warnings='ignore')



