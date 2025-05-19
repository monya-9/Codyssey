# Codyssey No.8 - 문제1 비밀번호 XXXXXX
# 암호 해독

"""
ZIP 파일 암호 해제 프로그램
조건: 6자리 숫자와 소문자 알파벳으로 구성
"""

import zipfile
import itertools
import string
import time
import os
import sys


def unlock_zip(zip_filename='emergency_storage_key.zip'):
    """
    ZIP 파일의 암호를 찾아 해제하는 함수
    
    Args:
        zip_filename (str): 해제할 ZIP 파일 경로
    
    Returns:
        str: 찾은 암호 (실패 시 None)
    """
    # 파일 존재 여부 확인
    if not os.path.exists(zip_filename):
        print(f'오류: {zip_filename} 파일을 찾을 수 없습니다.')
        return None
    
    try:
        zip_file = zipfile.ZipFile(zip_filename)
    except zipfile.BadZipFile:
        print(f'오류: {zip_filename}은 유효한 ZIP 파일이 아닙니다.')
        return None
    
    # 파일 목록 확인
    file_list = zip_file.namelist()
    if not file_list:
        print('ZIP 파일이 비어 있습니다.')
        zip_file.close()
        return None
    
    print(f'ZIP 파일 내용: {file_list}')
    
    # 테스트 파일 선택 (첫 번째 파일)
    test_file = file_list[0]
    
    # 가능한 문자 집합 정의 (숫자와 소문자 알파벳)
    chars = string.digits + string.ascii_lowercase
    
    # 시작 시간 기록
    start_time = time.time()
    count = 0
    last_report_time = start_time
    
    print('암호 해제 시작...')
    print(f'시작 시간: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')
    print('6자리 암호 시도 중...')
    
    # 표준 오류 출력 비활성화 (오류 메시지 숨기기)
    original_stderr = sys.stderr
    null_stderr = open(os.devnull, 'w')
    
    try:
        # 정확히 6자리 조합만 시도 (최적화)
        for combo in itertools.product(chars, repeat=6):
            password = ''.join(combo)
            count += 1
            
            # 100,000번 시도마다 진행 상황 출력
            if count % 100000 == 0:
                current_time = time.time()
                elapsed = current_time - start_time
                interval = current_time - last_report_time
                speed = 100000 / interval if interval > 0 else 0
                
                print(f'시도 횟수: {count:,}회, 진행 시간: {elapsed:.2f}초, '
                      f'현재 암호: {password}, 시도 속도: {speed:.2f}회/초')
                
                last_report_time = current_time
            
            try:
                # 오류 메시지 숨기기
                sys.stderr = null_stderr
                
                # 테스트용으로 단일 파일을 메모리로 추출 시도
                zip_file.read(test_file, pwd=password.encode())
                
                # 오류 메시지 복원
                sys.stderr = original_stderr
                
                # 성공 시 결과 출력
                end_time = time.time()
                elapsed = end_time - start_time
                
                print('\n암호 해제 성공!')
                print(f'암호: {password}')
                print(f'시도 횟수: {count:,}회')
                print(f'소요 시간: {elapsed:.2f}초')
                
                # 파일 실제 추출 테스트
                try:
                    temp_dir = 'temp_extract'
                    if not os.path.exists(temp_dir):
                        os.mkdir(temp_dir)
                    
                    # 추출 테스트
                    zip_file.extractall(path=temp_dir, pwd=password.encode())
                    print(f'ZIP 파일 내용을 {temp_dir} 폴더에 성공적으로 추출했습니다.')
                except Exception as e:
                    print(f'파일 추출 중 오류 발생: {str(e)}')
                
                # 암호를 파일로 저장
                try:
                    with open('password.txt', 'w') as f:
                        f.write(password)
                    print(f'암호가 password.txt 파일에 저장되었습니다.')
                except Exception as e:
                    print(f'암호 저장 중 오류 발생: {str(e)}')
                
                # 안전하게 ZIP 파일 닫기
                zip_file.close()
                
                # 임시 stderr 파일 닫기
                null_stderr.close()
                
                return password
                
            except (RuntimeError, zipfile.BadZipFile):
                # 오류 메시지 복원
                sys.stderr = original_stderr
                # 잘못된 암호인 경우 다음 시도
                continue
            except Exception:
                # 오류 메시지 복원
                sys.stderr = original_stderr
                # 다른 오류 발생 시 조용히 다음 시도로 넘어감
                continue
    
    finally:
        # 오류 메시지 복원 및 자원 정리
        sys.stderr = original_stderr
        null_stderr.close()
        
        try:
            zip_file.close()
        except:
            pass
    
    print('\n암호 해제 실패: 모든 조합 시도 후 실패')
    return None


if __name__ == '__main__':
    try:
        result = unlock_zip()
        if result:
            print(f'프로그램 종료 - 암호 찾음: {result}')
        else:
            print('프로그램 종료 - 암호를 찾지 못했습니다.')
    except KeyboardInterrupt:
        print('\n사용자에 의해 프로그램이 중단되었습니다.')
    except Exception as e:
        print(f'프로그램 실행 중 오류 발생: {str(e)}')