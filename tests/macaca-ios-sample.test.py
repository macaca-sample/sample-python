#coding:utf-8

import unittest
import os
import time
from macaca import WebDriver
from retrying import retry

desired_caps = {
    'platformName': 'iOS',
    'deviceName': 'iPhone 6s',
    'app': 'https://npmcdn.com/ios-app-bootstrap@latest/build/ios-app-bootstrap.zip',
}

server_url = {
    'hostname': 'localhost',
    'port': 3456
}

def switch_to_webview(driver):
    contexts = driver.contexts
    driver.context = contexts[-1]
    return driver

def switch_to_native(driver):
    contexts = driver.contexts
    driver.context = contexts[0]
    return driver

class MacacaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver(desired_caps, server_url)
        cls.initDriver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @classmethod
    @retry
    def initDriver(cls):
        print("Retry connecting server...")
        cls.driver.init()

    def test_01_login(self):
        self.driver \
            .element_by_xpath('//XCUIElementTypeTextField[1]') \
            .send_keys('中文+Test+12345678')   \

        self.driver \
            .element_by_xpath('//XCUIElementTypeSecureTextField[1]') \
            .send_keys('111111') \

        self.driver \
            .element_by_name('Done') \
            .click()

        self.driver \
            .element_by_name('Login') \
            .click()

    def test_02_scroll_tableview(self):
        self.driver              \
            .element_by_name('HOME') \
            .click()

        self.driver             \
            .element_by_name('list') \
            .click()

    def test_03_gesture(self):
        self.driver \
            .touch('drag', {
              'fromX': 200,
              'fromY': 400,
              'toX': 200,
              'toY': 100,
              'duration': 2
            })

        time.sleep(1)

        self.driver \
            .touch('drag', {
              'fromX': 100,
              'fromY': 100,
              'toX': 100,
              'toY': 400,
              'duration': 2
            })

        time.sleep(1)

        self.driver \
            .element_by_name('Gesture') \
            .click()

        self.driver \
            .touch('tap', {
              'x': 100,
              'y': 100
            })

        time.sleep(1)

        self.driver \
            .touch('press', {
              'x': 100,
              'y': 100,
              'duration': 1
            })

        time.sleep(1)

        self.driver \
            .element_by_id('info') \
            .touch('pinch', {
              'scale': 2,
              'velocity': 1
            })

        time.sleep(1)

        self.driver \
            .touch('drag', {
              'fromX': 100,
              'fromY': 100,
              'toX': 100,
              'toY': 600,
              'steps': 100
            })

    def test_04_webview(self):
        self.driver \
            .element_by_name('Webview') \
            .click()

        time.sleep(3)
        self.driver.save_screenshot('./webView.png') # save screen shot

        switch_to_webview(self.driver) \
            .element_by_id('pushView') \
            .touch('tap')

        switch_to_webview(self.driver) \
            .element_by_id('popView') \
            .touch('tap')

    def test_05_web(self):
        switch_to_native(self.driver) \
            .element_by_name('Baidu') \
            .touch('tap')

        time.sleep(3)
        self.driver.save_screenshot("./baidu.png")

        switch_to_webview(self.driver) \
            .element_by_id('index-kw') \
            .send_keys('macaca') \
            .element_by_id('index-bn') \
            .touch('tap')

    def test_06_logout(self):
        switch_to_native(self.driver) \
            .element_by_name('PERSONAL') \
            .click()

        self.driver.element_by_name('Logout') \
            .click()

if __name__ == '__main__':
    unittest.main()
