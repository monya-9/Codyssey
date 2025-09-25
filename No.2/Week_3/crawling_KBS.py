import requests
from bs4 import BeautifulSoup
import sys

def get_kbs_headlines():
    """
    KBS 뉴스 웹사이트에서 헤드라인 뉴스를 가져와 리스트로 반환합니다.
    """
    url = 'http://news.kbs.co.kr/news/pc/main/main.html'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'웹 페이지 접속 오류: {e}')
        sys.exit(1)
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    headline_tags = soup.select('p.title')
    
    headline_list = []
    
    for tag in headline_tags:
        title = tag.get_text(strip=True).replace('\n', '')
        
        # --- 특정 값만 필터링하는 로직 추가 ---
        if title and title not in ['추천 인기 키워드', '공유하기']:
            headline_list.append(title)
        # ------------------------------------
            
    return headline_list

def print_headlines(headlines):
    """
    헤드라인 리스트를 화면에 출력합니다.
    """
    print('KBS 뉴스 주요 헤드라인\n' + '=' * 20)
    for index, headline in enumerate(headlines, 1):
        print(f'{index}. {headline}')
    print('=' * 20)

if __name__ == '__main__':
    headlines = get_kbs_headlines()
    if headlines:
        print_headlines(headlines)
    else:
        print('헤드라인을 찾을 수 없습니다.')