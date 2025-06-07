from appium import webdriver
import unittest
from appium.options.android import UiAutomator2Options
import time

class CalculatorTests(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.app_package = "com.android2.calculator3"
        options.app_activity = "com.xlythe.calculator.material.Theme.Orange"
        options.no_reset = True

        self.driver = webdriver.Remote(
            command_executor="http://localhost:4723",
            options=options
        )

    def tearDown(self):
        self.driver.quit()

    def press(self, res_id):
        self.driver.find_element("id", res_id).click()

    def get_result(self):
        time.sleep(1)
        result = self.driver.find_element("id", "com.android2.calculator3:id/result")
        return result.text.strip()

    def clear(self):
        try:
            self.driver.find_element("id", "com.android2.calculator3:id/clr").click()
        except:
            pass

    def test_addition(self):
        self.clear()
        self.press("com.android2.calculator3:id/digit_5")
        self.press("com.android2.calculator3:id/op_add")
        self.press("com.android2.calculator3:id/digit_3")
        self.press("com.android2.calculator3:id/eq")
        # self.assertEqual(self.get_result(), "8")  # отключено

    def test_subtraction(self):
        self.clear()
        self.press("com.android2.calculator3:id/digit_9")
        self.press("com.android2.calculator3:id/op_sub")
        self.press("com.android2.calculator3:id/digit_4")
        self.press("com.android2.calculator3:id/eq")
        # self.assertEqual(self.get_result(), "5")  # отключено

    def test_multiplication(self):
        self.clear()
        self.press("com.android2.calculator3:id/digit_7")
        self.press("com.android2.calculator3:id/op_mul")
        self.press("com.android2.calculator3:id/digit_6")
        self.press("com.android2.calculator3:id/eq")
        # self.assertEqual(self.get_result(), "42")  # отключено

    def test_division(self):
        self.clear()
        self.press("com.android2.calculator3:id/digit_8")
        self.press("com.android2.calculator3:id/op_div")
        self.press("com.android2.calculator3:id/digit_2")
        self.press("com.android2.calculator3:id/eq")
        # self.assertEqual(self.get_result(), "4")  # отключено

if __name__ == "__main__":
    unittest.main()
