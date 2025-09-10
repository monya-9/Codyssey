import socket
import threading
import sys

# 접속된 클라이언트 소켓과 주소를 저장할 딕셔너리
clients = {}
# 락(lock) 객체, 여러 스레드가 clients 딕셔너리에 동시에 접근하는 것을 방지
lock = threading.Lock()
# 서버 종료를 위한 이벤트 객체
shutdown_event = threading.Event()

def handle_client(client_socket, client_address):
    """
    클라이언트와의 통신을 처리하는 스레드 함수
    """
    print(f'새로운 접속: {client_address[0]}:{client_address[1]}')
    
    with lock:
        client_name = f'사용자{len(clients)}'
        clients[client_socket] = client_name
        
    broadcast_message(f'{client_name}님이 입장하셨습니다.', client_socket)
    
    try:
        while not shutdown_event.is_set():
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            # 서버 전체 종료 명령어
            if message.strip() == '/서버종료':
                print('클라이언트의 요청으로 서버를 종료합니다.')
                shutdown_event.set() # 이벤트 설정
                break
                
            # 클라이언트 개별 종료 명령어
            if message.strip() == '/종료':
                break
            
            if message.startswith('/귓속말 '):
                parts = message.split(' ', 2)
                if len(parts) >= 3:
                    target_name = parts[1]
                    whisper_message = parts[2]
                    send_whisper(client_socket, target_name, whisper_message, client_name)
                    continue
            
            broadcast_message(f'{client_name}> {message}', client_socket)
            
    except (ConnectionAbortedError, ConnectionResetError):
        print(f'클라이언트 {client_address}와의 연결이 끊어졌습니다.')
    except Exception as e:
        print(f'예상치 못한 에러 발생: {e}')
    finally:
        with lock:
            if client_socket in clients:
                del clients[client_socket]
            
            if not shutdown_event.is_set():
                broadcast_message(f'{client_name}님이 퇴장하셨습니다.', None)
            
        client_socket.close()
        print(f'연결 종료: {client_address[0]}:{client_address[1]}')

def broadcast_message(message, sender_socket):
    """
    특정 클라이언트를 제외하고 모든 접속자에게 메시지를 전송
    """
    with lock:
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception as e:
                    print(f'메시지 전송 실패: {e}')
                    
def send_whisper(sender_socket, target_name, whisper_message, sender_name):
    """
    특정 클라이언트에게만 귓속말 메시지를 전송
    """
    with lock:
        # 자신에게 귓속말을 보내는 것을 방지
        if sender_name == target_name:
            sender_socket.send(f'**{sender_name}님, 자신에게 귓속말을 보낼 수 없습니다.**'.encode('utf-8'))
            return

        found_target = False
        for client_socket, name in clients.items():
            if name == target_name:
                try:
                    client_socket.send(f'**{sender_name}님의 귓속말: {whisper_message}**'.encode('utf-8'))
                    sender_socket.send(f'**{target_name}님에게 귓속말을 보냈습니다.**'.encode('utf-8'))
                    found_target = True
                except Exception as e:
                    print(f'귓속말 전송 실패: {e}')
                break
        
        if not found_target:
            sender_socket.send(f'**{target_name}님을 찾을 수 없습니다.**'.encode('utf-8'))

def start_server():
    """
    서버를 시작하고 클라이언트 접속을 대기
    """
    host = '0.0.0.0'
    port = 50000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    
    print(f'서버가 {host}:{port}에서 시작되었습니다. 클라이언트 접속을 기다리는 중...')
    
    try:
        while not shutdown_event.is_set():
            server_socket.settimeout(1.0)
            try:
                client_socket, client_address = server_socket.accept()
                
                client_thread = threading.Thread(target=handle_client, 
                                                 args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
            except socket.timeout:
                continue
            
    except KeyboardInterrupt:
        print('서버 종료 중...')
    except Exception as e:
        if not shutdown_event.is_set():
            print(f'예상치 못한 서버 에러: {e}')
    finally:
        server_socket.close()
        print('서버가 성공적으로 종료되었습니다.')

if __name__ == '__main__':
    start_server()