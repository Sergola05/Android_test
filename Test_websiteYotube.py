import unittest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YouTubeSearchScrollVideo(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "browserName": "Chrome",
            "automationName": "UiAutomator2",
            "chromedriverExecutableDir": "/path/to/chromedriver"  # Укажите путь к chromedriver, если требуется
        }
        self.driver = webdriver.Remote("http://localhost:4723", desired_caps)
        self.wait = WebDriverWait(self.driver, 20)

        # Открываем мобильную версию YouTube
        self.driver.get("https://m.youtube.com")
        time.sleep(3)  # Даем странице загрузиться

        self.search_query = "music 2024"
        self.base_url = "https://m.youtube.com"

    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def test_scroll_past_reels_to_video(self):
        try:
            print("🔍 Поиск 'music 2024'")
            # Находим и кликаем на иконку поиска (лупа)
            search_btn = self.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//button[@aria-label="Search YouTube"]'))
            )
            search_btn.click()

            # Находим поле поиска и вводим запрос
            search_field = self.wait.until(
                EC.visibility_of_element_located((AppiumBy.XPATH, '//input[@id="search"]'))
            )
            search_field.clear()
            search_field.send_keys("music 2024")
            search_field.submit()
            time.sleep(3)

            print("🔽 Ищем обычное видео (пропускаем Shorts)")
            found_video = False
            attempts = 0
            max_attempts = 15

            while not found_video and attempts < max_attempts:
                # Ищем все элементы, которые могут быть видео (исключая Shorts)
                video_elements = self.driver.find_elements(
                    AppiumBy.XPATH, '//a[contains(@href, "/watch")]'
                )
                for video in video_elements:
                    try:
                        # Пропускаем элементы, относящиеся к Shorts
                        if "/shorts/" not in video.get_attribute("href"):
                            video.click()
                            print("▶ Найдено обычное видео - начинаем воспроизведение")
                            self.wait.until(
                                EC.presence_of_element_located((AppiumBy.XPATH, '//video'))
                            )
                            found_video = True
                            time.sleep(10)
                            self.driver.back()
                            break
                    except Exception:
                        continue
            self.test_3_play_video()
            
            # Прокручиваем к блоку связанных видео
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2)")
            
            # Проверяем наличие связанных видео
            related_videos = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "related-item")]'))
            )
            
            self.assertGreater(len(related_videos), 0, "Связанные видео не найдены")
            print(f"✅ Найдено {len(related_videos)} связанных видео")
        except Exception as e:
            self.driver.save_screenshot("related_error.png")
            self.fail(f"❌ Ошибка проверки связанных видео: {str(e)}")

    def test_5_navigate_to_home(self):
        """5. Возврат на главную страницу"""
        print("\n=== 5. Тест возврата на главную ===")
        try:
            # Находимся на странице видео (из предыдущего теста)
            self.test_4_check_related_videos()
            
            # Нажимаем логотип YouTube для возврата на главную
            home_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="YouTube"]'))
            )
            home_btn.click()
            
            # Проверяем, что вернулись на главную
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "shelf")]'))
            )
            print("✅ Успешный возврат на главную страницу")
        except Exception as e:
            self.driver.save_screenshot("home_error.png")
            self.fail(f"❌ Ошибка возврата на главную: {str(e)}")


if __name__ == "__main__":
    unittest.main()