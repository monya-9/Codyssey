# Codyssey No.10 - 문제7 자비스가 필요해!
# 음성 녹화 및 저장

"""
시스템의 마이크를 인식하고 음성을 녹음하는 프로그램
녹음된 파일은 records 폴더에 '년월일-시간분초.wav' 형식으로 저장됩니다.
"""

import os
import time
import datetime
import pyaudio
import wave


class AudioRecorder:
    """
    시스템 마이크를 사용하여 음성을 녹음하는 클래스
    """
    
    def __init__(self):
        """
        오디오 레코더 초기화
        """
        self.format = pyaudio.paInt16  # 16비트 포맷
        self.channels = 1              # 모노 채널
        self.rate = 44100              # 샘플링 레이트 (Hz)
        self.chunk = 1024              # 프레임 버퍼 크기
        self.audio = pyaudio.PyAudio()
        self.recording_dir = 'records'
        
        # records 디렉토리 생성
        if not os.path.exists(self.recording_dir):
            os.makedirs(self.recording_dir)
    
    def list_audio_devices(self):
        """
        시스템에 연결된 모든 오디오 장치를 나열합니다.
        
        Returns:
            list: (인덱스, 장치 이름) 튜플의 목록
        """
        devices = []
        info = self.audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        for i in range(num_devices):
            device_info = self.audio.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                devices.append((i, device_info.get('name')))
        
        return devices
    
    def record_audio(self, seconds, device_index=None):
        """
        지정된 시간 동안 오디오를 녹음합니다.
        
        Args:
            seconds (int): 녹음 시간 (초)
            device_index (int, optional): 사용할 마이크 장치 인덱스
        
        Returns:
            str: 저장된 녹음 파일 경로
        """
        # 현재 날짜와 시간으로 파일 이름 생성
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f'{self.recording_dir}/{timestamp}.wav'
        
        # 녹음 스트림 열기
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.chunk
        )
        
        print(f'녹음 시작... {seconds}초 동안 녹음합니다.')
        
        # 녹음 시작
        frames = []
        for i in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)
            
            # 진행 상황 표시 (10% 단위)
            progress = (i + 1) / int(self.rate / self.chunk * seconds) * 100
            if progress % 10 < (self.chunk / self.rate * 100):
                print(f'진행 중: {int(progress)}%')
        
        # 스트림 종료
        stream.stop_stream()
        stream.close()
        
        # WAV 파일로 저장
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f'녹음 완료! 파일이 저장되었습니다: {filename}')
        
        return filename
    
    def close(self):
        """
        오디오 객체를 종료합니다.
        """
        self.audio.terminate()


def list_recordings_by_date(start_date=None, end_date=None):
    """
    지정된 날짜 범위 내의 모든 녹음 파일을 나열합니다.
    
    Args:
        start_date (str, optional): 시작 날짜 (YYYYMMDD 형식)
        end_date (str, optional): 종료 날짜 (YYYYMMDD 형식)
    
    Returns:
        list: 파일 경로 목록
    """
    recording_dir = 'records'
    if not os.path.exists(recording_dir):
        print(f'"{recording_dir}" 폴더가 존재하지 않습니다.')
        return []
    
    # 모든 WAV 파일 가져오기
    files = [f for f in os.listdir(recording_dir) if f.endswith('.wav')]
    
    # 날짜 범위가 제공되지 않으면 모든 파일 반환
    if start_date is None and end_date is None:
        return [os.path.join(recording_dir, f) for f in files]
    
    # 날짜 필터링
    filtered_files = []
    
    for file in files:
        try:
            # 파일 이름에서 날짜 부분 추출
            date_part = file.split('-')[0]
            
            # 날짜 범위 체크
            if start_date and date_part < start_date:
                continue
            if end_date and date_part > end_date:
                continue
                
            filtered_files.append(os.path.join(recording_dir, file))
        except:
            # 잘못된 형식의 파일 이름은 건너뛰기
            continue
    
    return filtered_files


def display_menu():
    """
    사용자 메뉴를 표시합니다.
    """
    print('\n===== JAVIS - 음성 녹음 시스템 =====')
    print('1. 마이크 장치 목록 보기')
    print('2. 음성 녹음하기')
    print('3. 날짜별 녹음 파일 목록 보기')
    print('4. 종료')
    print('===================================')


def main():
    """
    메인 함수 - 사용자 상호작용 처리
    """
    recorder = AudioRecorder()
    
    while True:
        display_menu()
        choice = input('\n메뉴를 선택하세요 (1-4): ')
        
        if choice == '1':
            # 마이크 장치 목록 표시
            devices = recorder.list_audio_devices()
            print('\n--- 사용 가능한 마이크 장치 ---')
            if not devices:
                print('마이크 장치를 찾을 수 없습니다.')
            else:
                for idx, name in devices:
                    print(f'인덱스 {idx}: {name}')
            
        elif choice == '2':
            # 음성 녹음
            devices = recorder.list_audio_devices()
            
            if not devices:
                print('마이크 장치를 찾을 수 없습니다.')
                continue
            
            # 장치 목록 표시
            print('\n--- 사용 가능한 마이크 장치 ---')
            for idx, name in devices:
                print(f'인덱스 {idx}: {name}')
            
            # 장치 선택
            device_idx = input('\n사용할 마이크 장치 인덱스를 입력하세요 (기본값: 시스템 기본 장치): ')
            if device_idx.strip() and device_idx.isdigit():
                device_idx = int(device_idx)
                # 유효한 장치 인덱스 검증
                if all(device_idx != idx for idx, _ in devices):
                    print('유효하지 않은 장치 인덱스입니다. 기본 장치를 사용합니다.')
                    device_idx = None
            else:
                device_idx = None
            
            # 녹음 시간 입력
            while True:
                try:
                    seconds = float(input('\n녹음 시간을 입력하세요 (초): '))
                    if seconds <= 0:
                        print('0보다 큰 값을 입력하세요.')
                        continue
                    break
                except ValueError:
                    print('유효한 숫자를 입력하세요.')
            
            # 녹음 실행
            try:
                recorder.record_audio(seconds, device_idx)
            except Exception as e:
                print(f'녹음 중 오류 발생: {str(e)}')
            
        elif choice == '3':
            # 날짜별 녹음 파일 목록
            print('\n--- 날짜별 녹음 파일 목록 ---')
            print('날짜 형식: YYYYMMDD (예: 20250602)')
            
            # 날짜 범위 입력 (선택 사항)
            start_date = input('시작 날짜 (모든 날짜: Enter): ')
            end_date = input('종료 날짜 (모든 날짜: Enter): ')
            
            if not start_date.strip():
                start_date = None
            if not end_date.strip():
                end_date = None
            
            # 파일 목록 표시
            files = list_recordings_by_date(start_date, end_date)
            
            if not files:
                print('해당 날짜 범위에 녹음 파일이 없습니다.')
            else:
                print('\n--- 녹음 파일 목록 ---')
                for file in files:
                    # 파일 크기 (KB)
                    size_kb = os.path.getsize(file) / 1024
                    # 파일 생성 시간
                    ctime = time.ctime(os.path.getctime(file))
                    print(f'{os.path.basename(file)} ({size_kb:.1f} KB) - {ctime}')
        
        elif choice == '4':
            # 종료
            print('프로그램을 종료합니다.')
            recorder.close()
            break
            
        else:
            print('올바른 메뉴 번호를 입력해주세요.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n사용자에 의해 프로그램이 중단되었습니다.')
    except Exception as e:
        print(f'프로그램 실행 중 오류 발생: {str(e)}')