# -*- coding: utf-8 -*-
import unittest

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException


class TestChrome(unittest.TestCase):
    def setUp(self):
        self.display = Display(visible=0, size=(800, 800))
        self.display.start()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://github.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_python1(self):
        driver = self.driver
        driver.get(
            self.base_url + "/SeleniumHQ/selenium/wiki/SeIDEReleaseNotes")
        driver.find_element_by_link_text(
            "https://github.com/SeleniumHQ/selenium/wiki/SeIDE-Release-Notes").click()
        driver.find_element_by_link_text(
            "https://github.com/SeleniumHQ/selenium/issues/396").click()
        try:
            self.assertEqual("I-needs investigation",
                             driver.find_element_by_xpath(
                                 "//a[contains(text(),'I-needs investigation')]").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.display.stop()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
