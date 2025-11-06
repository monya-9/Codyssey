import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys
import os

# --- 전역 상수 및 설정 ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587 # STARTTLS (TLS) 보안 포트

def send_email_with_attachment(sender_email, app_password, receiver_email, subject, body, attachment_path=None):
    """
    Gmail SMTP 서버를 통해 이메일을 전송하는 함수입니다.
    첨부 파일을 포함할 수 있으며, 발생 가능한 예외를 처리합니다.
    """
    
    # 1. MIME 멀티파트 메시지 생성
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # 2. 본문 첨부 (MIMEText)
    message.attach(MIMEText(body, 'plain'))

    # 3. 첨부 파일 처리 (보너스 과제)
    if attachment_path:
        try:
            # 파일 이름과 확장자 분리
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
            print(f'첨부 파일 "{filename}"을 성공적으로 추가했습니다.')
            
        except FileNotFoundError:
            print(f'경고: 첨부 파일 "{attachment_path}"을 찾을 수 없습니다. 파일 없이 메일을 전송합니다.')
        except Exception as e:
            print(f'첨부 파일 처리 중 예상치 못한 오류 발생: {e}')

    # 4. SMTP 서버 연결 및 전송
    try:
        # TLS 암호화를 위해 587 포트로 연결
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo() # 서버 응답 확인
        server.starttls() # TLS 보안 연결 시작
        server.ehlo() # TLS 보안 연결 후 서버 응답 다시 확인
        
        # 로그인 (사용자 이메일과 앱 비밀번호 사용)
        server.login(sender_email, app_password)
        print('SMTP 서버 로그인 성공.')
        
        # 메일 전송
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('메일이 성공적으로 전송되었습니다.')
        
    except smtplib.SMTPAuthenticationError:
        print('오류: SMTP 인증에 실패했습니다.')
        print('앱 비밀번호(App Password)를 정확히 입력했는지 확인하십시오.')
        sys.exit(1)
    except smtplib.SMTPConnectError:
        print(f'오류: {SMTP_SERVER} 서버 연결에 실패했습니다. 포트 {SMTP_PORT} 확인 필요.')
        sys.exit(1)
    except Exception as e:
        print(f'메일 전송 중 예상치 못한 오류 발생: {e}')
    finally:
        if 'server' in locals():
            server.quit() # 연결 종료

def main():
    """
    사용자 입력을 받고 메일 전송 함수를 호출하는 메인 함수입니다.
    """
    print('*** Gmail SMTP를 이용한 이메일 전송을 시작합니다. ***')
    print('*** 참고: Gmail에서는 보안을 위해 "앱 비밀번호"를 사용해야 합니다. ***')

    # 사용자 입력 받기
    sender_email = input('보내는 사람 (Gmail 주소): ')
    # 보안상 일반 비밀번호 대신 앱 비밀번호를 사용해야 함
    app_password = input('Gmail 앱 비밀번호: ')
    receiver_email = input('받는 사람 이메일 주소: ')
    
    # 메일 내용 설정
    subject = '파이썬 SMTP 테스트 메일입니다.'
    body = '안녕하세요. 파이썬 기본 패키지를 사용하여 전송한 테스트 메일입니다.'

    # 보너스 과제: 첨부 파일 경로 설정 (예시: 같은 폴더에 'attachment.txt' 파일이 있다고 가정)
    # 첨부 파일이 없다면 None으로 두거나, 실제 파일 경로로 수정하십시오.
    attachment_to_send = 'attachment.txt' 

    # 메일 전송 함수 호출
    send_email_with_attachment(sender_email, app_password, receiver_email, subject, body, attachment_to_send)

if __name__ == '__main__':
    main()