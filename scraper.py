import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests

# GitHub Secrets에서 텔레그램 정보 불러오기
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

def check_megabox_event():
    # 클라우드 백그라운드 환경(Headless)에 맞춘 크롬 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = 'https://www.megabox.co.kr/event'
        driver.get(url)
        time.sleep(5) # 페이지 렌더링 대기
        
        titles = driver.find_elements(By.CSS_SELECTOR, 'div.event-list a.tit')
        target_keyword = '메가박스 아트그라피'
        
        for title in titles:
            if target_keyword in title.text:
                send_telegram_message(f"🚨 [알림] '{target_keyword}' 이벤트 등록 감지!\n링크: {url}")
                return # 발견 즉시 알림을 보내고 스크립트 종료
                
    except Exception as e:
        print(f"오류 발생: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    check_megabox_event()
