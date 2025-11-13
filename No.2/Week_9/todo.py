import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import sys
import os

# --- SMTP 설정 상수 ---
# [Gmail 설정]
GMAIL_SMTP_SERVER = 'smtp.gmail.com'
GMAIL_SMTP_PORT = 587 
# [Naver 설정] (주의: 네이버는 일반 비밀번호와 2단계 인증 미사용 시에만 작동 가능성이 높음)
NAVER_SMTP_SERVER = 'smtp.naver.com'
NAVER_SMTP_PORT = 587 

def get_target_list(file_path):
    """
    CSV 파일에서 이름과 이메일 주소 목록을 읽어옵니다.
    """
    target_list = []
    try:
        # 인코딩 오류 방지를 위해 'utf-8-sig' 사용
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # CSV 헤더가 '이름'과 '이메일'인지 확인
                if '이름' in row and '이메일' in row:
                    target_list.append({'name': row['이름'], 'email': row['이메일']})
        print(f'총 {len(target_list)}명의 수신 명단을 CSV 파일에서 불러왔습니다.')
        return target_list
    except FileNotFoundError:
        print(f'오류: 수신 명단 파일 "{file_path}"을 찾을 수 없습니다.')
        sys.exit(1)
    except Exception as e:
        print(f'CSV 파일 처리 중 오류 발생: {e}')
        sys.exit(1)

def get_html_body(recipient_name):
    """
    받는 사람 이름에 맞춰 개인화된 HTML 메일 본문을 생성합니다.
    """
    html_content = f"""\
<html>
  <head></head>
  <body>
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ccc; border-radius: 10px;">
      <h3 style="color: #007bff;">안녕하세요, {recipient_name}님!</h3>
      <p>이 메일은 Python의 SMTP 라이브러리를 사용하여 발송된 HTML 형식의 테스트 메일입니다.</p>
      <p>첨부 파일 및 명단 발송 기능이 모두 정상 작동함을 확인합니다.</p>
      <hr style="border-top: 1px solid #eee;">
      <p style="font-size: 12px; color: #666;">자동 발송 시스템 - 회신 불가</p>
    </div>
  </body>
</html>
"""
    return html_content

def create_mime_message(sender, receivers, subject, body_html, attachment_path=None):
    """
    HTML 본문과 첨부 파일을 포함하는 MIMEMultipart 메시지 객체를 생성합니다.
    """
    # 1. MIMEMultipart 객체 생성
    message = MIMEMultipart('mixed')
    message['From'] = sender
    # 받는 사람이 여러 명일 경우 쉼표로 구분하여 문자열로 설정
    message['To'] = ', '.join(receivers)
    message['Subject'] = subject

    # 2. HTML 본문 추가 (MIMEText)
    # _subtype을 'html'로 설정하여 HTML 형식임을 명시
    html_part = MIMEText(body_html, 'html', 'utf-8')
    message.attach(html_part)

    # 3. 첨부 파일 처리 (선택 사항)
    if attachment_path and os.path.exists(attachment_path):
        try:
            filename = os.path.basename(attachment_path)
            
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Base64 인코딩
            encoders.encode_base64(part)
            
            # 첨부 파일 이름 설정
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= "{filename}"',
            )
            
            # 메시지에 첨부 파일 추가
            message.attach(part)
            print(f'   -> 첨부 파일 "{filename}" 추가됨.')
            
        except Exception as e:
            print(f'   -> 경고: 첨부 파일 처리 중 오류 발생 - {e}')

    return message

def send_mail(server_host, server_port, sender_email, app_password, message, all_recipients):
    """
    SMTP 서버에 접속하여 메일을 전송하는 핵심 함수.
    """
    try:
        # 1. 서버 연결 설정
        server = smtplib.SMTP(server_host, server_port)
        server.ehlo()
        server.starttls() 
        server.ehlo()
        
        # 2. 로그인
        server.login(sender_email, app_password)
        print(f'SMTP 서버 로그인 성공 ({server_host}).')
        
        # 3. 메일 전송
        server.sendmail(sender_email, all_recipients, message.as_string())
        print('메일이 성공적으로 전송되었습니다.')
        
    except smtplib.SMTPAuthenticationError:
        print('오류: SMTP 인증에 실패했습니다. 앱 비밀번호/설정을 확인하십시오.')
        sys.exit(1)
    except smtplib.SMTPConnectError:
        print(f'오류: SMTP 서버 연결에 실패했습니다. 호스트/포트({server_host}:{server_port}) 확인 필요.')
        sys.exit(1)
    except Exception as e:
        print(f'메일 전송 중 예상치 못한 오류 발생: {e}')
    finally:
        # server 변수가 생성되었는지 확인 후 종료
        if 'server' in locals() and server:
            server.quit() 

def main():
    """
    사용자 입력을 받고 메일 전송 방식을 결정하여 전송을 실행하는 메인 함수입니다.
    """
    print('*** CSV 명단을 이용한 HTML 메일 발송을 시작합니다. ***')

    # 사용자 입력 받기
    sender_email = input('보내는 사람 이메일 주소: ')
    app_password = input('Gmail/Naver 앱 비밀번호: ')
    
    # 서버 선택 (보너스 과제 포함)
    server_choice = input('사용할 SMTP 서버를 선택하세요 (1: Gmail, 2: Naver): ')
    if server_choice == '1':
        server_host = GMAIL_SMTP_SERVER
        server_port = GMAIL_SMTP_PORT
    elif server_choice == '2':
        server_host = NAVER_SMTP_SERVER
        server_port = NAVER_SMTP_PORT
    else:
        print('잘못된 선택입니다. Gmail을 기본값으로 사용합니다.')
        server_host = GMAIL_SMTP_SERVER
        server_port = GMAIL_SMTP_PORT
        
    # 명단 가져오기
    csv_file_path = 'mail_target_list.csv'
    target_list = get_target_list(csv_file_path)
    if not target_list:
        return

    # ----------------------------------------------------
    # [과제 요구사항] 받는 사람에게 메일 보내는 두 가지 방법 시도 및 선택
    # ----------------------------------------------------
    
    # 1. 개별 전송 (Individual Send): 명단 수만큼 반복하여 개별적으로 메일 전송 (권장: 개인화 용이)
    print('\n[1. 개별 전송 방식 시작 (권장)]')
    
    for target in target_list:
        recipient_name = target['name']
        receiver_email = target['email']
        
        print(f'-> {recipient_name}님 ({receiver_email})에게 전송 시도...')
        
        # 개인화된 HTML 본문 생성
        html_body = get_html_body(recipient_name)
        
        # 메시지 생성 (받는 사람: 1명)
        message = create_mime_message(
            sender_email, 
            [receiver_email], 
            f'개별 발송 테스트 - {recipient_name}님께', 
            html_body, 
            'attachment.txt'
        )
        
        # send_mail 호출 시 서버 호스트와 포트 전달
        send_mail(server_host, server_port, sender_email, app_password, message, [receiver_email])
        print('-' * 40)
        
    # 2. 그룹 전송 (Group Send): 명단을 'To' 필드에 모두 넣어 한 번에 전송 (개인화 어려움)
    print('\n[2. 그룹 전송 방식 (CC/BCC 효과) - 시뮬레이션]')
    
    all_emails = [t['email'] for t in target_list]
    
    # 그룹 전송용 HTML 본문 (개인화 불가)
    group_html_body = get_html_body("수신자 여러분") 
    
    # 메시지 생성 (받는 사람: 명단 전체)
    group_message = create_mime_message(
        sender_email, 
        all_emails, 
        '그룹 일괄 발송 테스트 - 수신자 여러분께', 
        group_html_body, 
        'attachment.txt'
    )
    
    print(f'-> 총 {len(all_emails)}명에게 그룹 전송 시도...')
    # send_mail(server_host, server_port, sender_email, app_password, group_message, all_emails)
    print('   (그룹 전송은 실제 서비스에서 보안 문제로 인해 권장되지 않으므로, 시뮬레이션만 합니다.)')
    
    # 결론 도출: 개인화된 내용과 오류 처리가 명확한 개별 전송 방식이 더 좋은 방법입니다.
    print('\n[결론] 명단 기반 발송에는 오류 처리가 명확하고 개인화가 가능한 개별 전송 방식이 더 좋은 방법입니다.')

if __name__ == '__main__':
    main()
