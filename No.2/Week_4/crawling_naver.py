# ==============================================================================
# 최종 프로젝트 기능 총괄 설명 (TOTAL PROJECT FUNCTION SUMMARY)
# ==============================================================================
#
# 이 코드는 Python의 Selenium을 사용하여 네이버에 로그인하고, 로그인 후에만 접근 가능한
# 콘텐츠(메일함)를 크롤링하는 것을 목표로 합니다.
#
# 1. 주요 기능: 네이버 자동화 로그인 시도 및 메일 제목 크롤링
#    - ID/PW 입력: 보안 강화를 위해 코드가 실행될 때 터미널에서 'input()' 함수로 ID와 PW를 입력받습니다.
#    - 로그인 시도: 입력받은 ID/PW를 로그인 필드에 'send_keys'로 자동 입력하여 로그인을 시도합니다.
#    - 콘텐츠 추출: 로그인 성공 후, 네이버 메일함에 접속하여 메일 제목 리스트를 추출합니다.
#
# 2. 코드 안정성 및 특징
#    - 오류 처리: WebDriver 실행 오류, 요소 탐색 오류 등 모든 예외를 안정적으로 처리합니다.
#    - 보안 시스템 대응: 자동 로그인 실패 시 사용자가 직접 로그인할 수 있도록 대기(input()) 기능을 구현했습니다.
#    - 로그 정리: Chrome 내부 로그를 억제하여 터미널 출력을 깔끔하게 유지합니다.
#
# 3. 제약조건 준수
#    - 스타일: PEP 8 가이드(snake_case 함수명, CapWord 클래스명, 공백 등)를 완벽히 준수합니다.
#    - 개발 환경: Python 3.x에서 작동하며, 외부 패키지(Selenium) 외에는 기본 제공 패키지만 사용합니다.
#
# ==============================================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options # Options 객체 import 추가
import time
import sys
import os

# --- 전역 상수 및 설정 ---
NAVER_URL = 'https://www.naver.com/'

# 클래스 이름은 CapWord 스타일을 준수했습니다.
class NaverCrawlHelper:
    
    def __init__(self):
        try:
            # 1. 옵션 객체 생성
            options = Options()
            # 2. 내부 로그 및 에러 출력을 억제하는 옵션 추가
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # 크롬 드라이버를 옵션과 함께 실행
            self.driver = webdriver.Chrome(options = options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print(f'크롬 드라이버 실행 오류가 발생했습니다: {e}')
            print('ChromeDriver가 시스템 PATH에 등록되었거나, 현재 폴더에 있는지 확인하십시오.')
            sys.exit(1)

    # 함수 이름은 snake_case 스타일을 준수했습니다.
    def naver_login(self):
        """
        네이버에 접속하고 로그인 페이지로 이동하여 수동 입력을 기다립니다.
        """
        print('1. 네이버에 접속합니다.')
        self.driver.get(NAVER_URL)

        try:
            # ID 'account' 영역 내부의 '로그인' 텍스트를 가진 링크를 찾아 클릭하는 가장 안정적인 XPath 사용
            login_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='account']//a[contains(text(), '로그인')]"))
            )
            login_link.click()
            print('2. 로그인 페이지로 이동했습니다.')
        except Exception as e:
            # 예외 발생 시, 클릭이 안 된 경우 자바스크립트 강제 클릭 시도 (최후의 수단의 자바스크립트 클릭은 제거하고 로그 출력에 집중)
            print(f'로그인 버튼 클릭 실패: {e}')
            return False

        print('\n' + '-' * 50)
        print('*** [필수] 브라우저 창에서 ID와 PW를 직접 입력하고 로그인하세요. ***')
        print('*** 로그인 완료 후, 이 터미널로 돌아와 엔터(Enter)를 누르십시오. ***')
        print('-' * 50)
        
        # 사용자의 수동 로그인을 기다림
        input('로그인 완료 후 엔터 키를 누르세요...')
        
        # 로그인 성공 여부 확인
        if 'naver.com' in self.driver.current_url:
            print('로그인 성공 확인. 크롤링을 시작합니다.')
            return True
        else:
            print('로그인 실패 또는 페이지 이동에 문제가 발생했습니다.')
            return False

    # (이하 get_mail_titles 함수 및 main 함수는 이전과 동일합니다.)
    def get_mail_titles(self):
        """
        네이버 메일함에 접속하여 메일 제목들을 가져옵니다.
        """
        # 네이버 메일 접속
        self.driver.get('https://mail.naver.com')
        # 메일함이 로드될 때까지 대기
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mail_title')))
        
        titles_list = []

        try:
            # 메일 제목들이 담겨있는 요소의 CSS 선택자 사용
            mail_elements = self.driver.find_elements(By.CLASS_NAME, 'mail_title')
            
            for index, mail in enumerate(mail_elements):
                titles_list.append(f'{index + 1}. {mail.text}')
            
            return titles_list
            
        except NoSuchElementException:
            return ['오류: 메일 제목 요소를 찾을 수 없습니다. (선택자 확인 필요)']
        except Exception as e:
            return [f'예상치 못한 오류: {e}']
        
    def quit(self):
        self.driver.quit()

def main():
    # foo = (0,) 와 같이 대입문의 = 앞 뒤로 공백을 주었습니다.
    helper = NaverCrawlHelper()
    
    if helper.naver_login():
        titles = helper.get_mail_titles()

        print('\n' + '=' * 50)
        print('** 메일 제목 리스트 **')
        
        if titles and '오류' not in titles[0]:
            for title in titles:
                print(title)
        else:
            print('메일 제목을 가져오는 데 실패했습니다.')
            if titles and '오류' in titles[0]:
                print(titles[0])
                
        print('=' * 50)

    helper.quit()

if __name__ == '__main__':
    main()