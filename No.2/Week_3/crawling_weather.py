import requests
from bs4 import BeautifulSoup
import sys

def get_naver_weather():
    """
    네이버 날씨 웹 페이지에서 현재 기온을 가져와 출력합니다.
    """
    url = 'https://search.naver.com/search.naver?query=날씨'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'네이버 날씨 페이지 접속 오류: {e}')
        sys.exit(1)
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 개발자 도구로 찾은 현재 기온의 클래스 값
    current_temp_tag = soup.find('div', class_ = 'temperature_text')
    
    if current_temp_tag:
        temperature = current_temp_tag.get_text(strip = True).replace('현재 온도', '')
        print(f'네이버 날씨 정보')
        print(f'현재 기온: {temperature}')
    else:
        print('날씨 정보를 찾을 수 없습니다.')

if __name__ == '__main__':
    get_naver_weather()