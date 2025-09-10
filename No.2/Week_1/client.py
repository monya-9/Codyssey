import socket
import threading
import sys

def recv_message(client_socket):
    """
    서버로부터 메시지를 수신하는 스레드 함수
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print('서버와 연결이 끊어졌습니다.')
                break
            print(message)
        except (ConnectionAbortedError, ConnectionResetError):
            print('서버와 연결이 끊어졌습니다.')
            break
        except Exception as e:
            print(f'에러 발생: {e}')
            break

def start_client():
    """
    클라이언트를 시작하고 서버에 접속
    """
    host = '127.0.0.1'
    port = 50000
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print('서버에 접속했습니다. 메시지를 입력하세요. (/종료로 나가기)')
        
        # 메시지 수신 스레드 시작
        recv_thread = threading.Thread(target=recv_message, args=(client_socket,))
        recv_thread.daemon = True
        recv_thread.start()
        
        # 메시지 전송
        while True:
            message = input()
            try:
                client_socket.send(message.encode('utf-8'))
                if message == '/종료':
                    break
            except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                print('서버와 연결이 끊어져 메시지를 보낼 수 없습니다.')
                break
                
    except ConnectionRefusedError:
        print('서버에 연결할 수 없습니다.')
    finally:
        client_socket.close()

if __name__ == '__main__':
    start_client()