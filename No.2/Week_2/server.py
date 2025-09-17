import http.server
import socketserver
import time

# --- 제약조건: 클래스 이름은 CapWord 방식으로 작성합니다.
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    # --- 제약조건: 함수 이름은 소문자_언더라인으로 작성합니다.
    def do_GET(self):
        """
        GET 요청을 처리하는 메서드.
        """
        self.log_request_info()
        self.send_response_and_file()
    
    def log_request_info(self):
        """
        접속 정보를 서버 콘솔에 출력합니다.
        """
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        client_ip = self.client_address[0]
        
        print(f'접속 시간: {current_time}')
        print(f'접속한 클라이언트의 IP address: {client_ip}\n')
        
    def send_response_and_file(self):
        """
        index.html 파일을 읽어 클라이언트에 전송합니다.
        """
        try:
            with open('index.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, 'File Not Found: index.html')

def run_server():
    """
    HTTP 서버를 실행하는 함수.
    """
    host = '0.0.0.0'
    port = 8080
    
    # 서버 객체 생성
    server_address = (host, port)
    httpd = socketserver.TCPServer(server_address, MyHTTPRequestHandler)
    
    print(f'서버가 http://{host}:{port}에서 실행 중입니다.')
    
    try:
        # 서버 시작
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n서버를 종료합니다.')
        httpd.server_close()

if __name__ == '__main__':
    run_server()