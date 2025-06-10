import unittest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YouTubeSearchScrollVideo(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.app_package = "com.google.android.youtube"
        options.app_activity = "com.google.android.apps.youtube.app.WatchWhileActivity"
        options.no_reset = True
        options.automation_name = "UiAutomator2"

        self.driver = webdriver.Remote("http://localhost:4723", options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def tearDown(self):
        self.driver.quit()

    def test_scroll_past_reels_to_video(self):
        try:
            print("🔍 Поиск 'music 2024'")
            # Открываем поиск
            search_btn = self.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//*[@content-desc="Search"]'))
            )
            search_btn.click()

            # Вводим запрос
            search_field = self.wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, "com.google.android.youtube:id/search_edit_text"))
            )
            search_field.clear()
            search_field.send_keys("music 2024")
            self.driver.press_keycode(66)  # ENTER
            time.sleep(3)  # Ожидаем загрузки результатов

            print("🔽 Ищем обычное видео (пропускаем Shorts)")
            found_video = False
            attempts = 0
            max_attempts = 15  # Увеличил количество попыток
            
            while not found_video and attempts < max_attempts:
                # Ищем все элементы, которые могут быть видео
                video_elements = self.driver.find_elements(
                    AppiumBy.XPATH, '//android.view.ViewGroup[contains(@content-desc, "video")]'
                )
                
                for video in video_elements:
                    try:
                        # Проверяем, что это не Shorts
                        if "shorts" not in video.get_attribute("content-desc").lower():
                            video.click()
                            print("▶ Найдено обычное видео - начинаем воспроизведение")
                            
                            # Проверяем, что видео запустилось
                            self.wait.until(
                                EC.presence_of_element_located(
                                    (AppiumBy.ID, "com.google.android.youtube:id/player_view")
                                )
                            )
                            found_video = True
                            time.sleep(10)  # Смотрим видео 10 секунд
                            self.driver.back()  # Возвращаемся к результатам поиска
                            break
                    except:
                        continue
                
                if not found_video:
                    # Скроллим вниз
                    window_size = self.driver.get_window_size()
                    start_x = window_size['width'] // 2
                    start_y = window_size['height'] * 0.7
                    end_y = window_size['height'] * 0.3
                    
                    self.driver.swipe(start_x, start_y, start_x, end_y, 500)
                    attempts += 1
                    print(f"⏬ Скролл вниз (попытка {attempts}/{max_attempts})")
                    time.sleep(2)  # Ожидаем загрузки нового контента

            if not found_video:
                self.driver.save_screenshot("no_video_found.png")
                self.fail("❌ Не удалось найти обычное видео после скролла")

            print("✅ Тест успешно завершен")

        except Exception as e:
            self.driver.save_screenshot("test_error.png")
            self.fail(f"❌ Тест завершился с ошибкой: {str(e)}")


if __name__ == "__main__":
    unittest.main()
    