# Codyssey No.11 - 문제8 음성에서 문자로
# 음성 파일 텍스트 변환

import os
import csv
import speech_recognition as sr


def transcribe_audio_to_csv(audio_file):
    """
    음성 파일을 받아 텍스트로 변환하고, 타임스탬프와 함께 CSV로 저장
    파일명은 원본 이름과 같고 확장자는 .csv로 저장됨
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, show_all=False)

            csv_filename = os.path.splitext(audio_file)[0] + '.csv'
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Time', 'Text'])
                writer.writerow(['00:00', text])

            print(f'{csv_filename} 저장 완료.')

    except sr.UnknownValueError:
        print(f'음성을 이해할 수 없습니다: {audio_file}')
    except sr.RequestError as e:
        print(f'STT 서비스 요청 실패: {e}')
    except Exception as e:
        print(f'오류 발생: {e}')


def process_audio_directory(directory):
    """
    지정된 디렉토리 내의 모든 .wav 파일에 대해 STT 변환 수행
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith('.wav'):
            full_path = os.path.join(directory, filename)
            transcribe_audio_to_csv(full_path)


def search_keyword_in_csv(directory, keyword):
    """
    보너스 과제: 키워드를 포함하는 행을 찾아 출력
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith('.csv'):
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # 헤더 스킵
                for row in reader:
                    if keyword.lower() in row[1].lower():
                        print(f'{filename} >> {row[0]}: {row[1]}')


if __name__ == '__main__':
    audio_folder = 'records'  # 음성 파일이 저장된 폴더 경로
    process_audio_directory(audio_folder)

    # 보너스 과제: 키워드 검색
    key = input('찾을 키워드를 입력하세요 (없으면 Enter): ').strip()
    if key:
        search_keyword_in_csv(audio_folder, key)