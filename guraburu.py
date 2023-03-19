import time
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# Chromeドライバーのパス
DRIVER_PATH = 'C:/Users/cococ/OneDrive/デスクトップ/chromedriver_win32/chromedriver.exe'

# イベントページのURL
EVENT_URL = 'https://game.granbluefantasy.jp/#quest/supporter/902281/1/0/10471'

# HPバーのテンプレート画像のパス
HP_BAR_TEMPLATE_PATH = 'hp_bar_template.png'

def login(driver, username, password):
    # グラブルのログインページにアクセス
    driver.get('https://game.granbluefantasy.jp/#mypage')

    # ログイン情報を入力してログイン
    username_input = driver.find_element_by_id("subject-id")
    password_input = driver.find_element_by_name('subject_password')
    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element_by_css_selector('button[type="submit"]').click()

    # ログイン後、ジータの部屋に移動
    driver.get('https://game.granbluefantasy.jp/#mypage')

def use_elixir(driver):
    # エリクシールを使用する
    driver.find_element_by_css_selector('div[data-reactid=".0.0.2.1.1.1.1.0"]').click()
    driver.find_element_by_css_selector('div[data-reactid=".0.0.2.1.1.1.1.2.0.0"]').click()
    time.sleep(5)
    driver.find_element_by_css_selector('button[data-reactid=".0.0.2.1.1.1.1.2.2.0"]').click()
    time.sleep(5)

def summon_friend(driver):
    # フレンド召喚を行う
    driver.find_element_by_css_selector('div[data-reactid=".0.0.1.1.1.1.2.0"]').click()
    time.sleep(5)
    driver.find_element_by_css_selector('div[data-reactid=".0.0.1.1.1.1.3.1.1.0"]').click()
    time.sleep(5)

def start_battle(driver):
    # 戦闘を始める
    driver.find_element_by_css_selector('div[data-reactid=".0.0.1.1.1.1.1.0"]').click()
    time.sleep(5)

# 敵を攻撃する
def attack_enemy(driver, enemy_info, image):
    # 敵を攻撃する
    for info in enemy_info:
        # 敵の位置を取得
        position = info['location']

        # スクリーンショットから敵の画像を切り抜く
        enemy_image = image[position['y']:position['y']+info['size']['height'], position['x']:position['x']+info['size']['width']]

# Selenium WebDriverを使用してChromeを開く
driver = webdriver.Chrome(DRIVER_PATH)

# ログインする
driver.get('https://game.granbluefantasy.jp/#mypage')

#login(driver, 'your_username', 'your_password')
time.sleep(60)

# イベントページにアクセスする
driver.get(EVENT_URL)

# フレンド召喚を行う
summon_friend(driver)

# 戦闘を始める
start_battle(driver)

# 敵を攻撃する
enemy_info = []
for i in range(1, 7):
    selector = f'div[data-reactid=".0.0.1.1.1.1.2.2.1.{i}.0.0"]'
    element = driver.find_element_by_css_selector(selector)
    location = element.location
    size = element.size
    enemy_info.append({'location': location, 'size': size})

screenshot = driver.get_screenshot_as_png()
image = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR)

attack_enemy(driver, enemy_info, image)

# 戦闘が終了するまで待つ
time.sleep(20)

# 結果を確認する
result = driver.find_element_by_css_selector('div[data-reactid=".0.0.1.1.2.0.2"]')
if '敗北' in result.text:
    print('敗北しました')
else:
    print('勝利しました')

# ブラウザを閉じる
driver.quit()


#メイン関数
#if name == 'main':
# Chromeドライバーを起動する
#driver = webdriver.Chrome(DRIVER_PATH)


# イベントバトルを行う
#event_battle(driver, 'username', 'password')

# ブラウザを閉じる
#driver.quit()