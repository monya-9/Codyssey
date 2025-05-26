# Codyssey No.8 - 문제2 카이사르의 암호
# 암호 해독

def caesar_cipher_decode(target_text):
    """
    주어진 문자열을 카이사르 암호 방식으로 해독한다.
    알파벳의 각 문자를 0~25만큼 왼쪽으로 이동시키는 해독 결과를 모두 출력한다.

    Args:
        target_text (str): 암호화된 문자열
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for shift in range(26):
        decoded = ''
        for ch in target_text:
            if ch.islower():
                # 소문자인 경우 시프트된 위치 계산 후 해독
                index = (alphabet.index(ch) - shift) % 26
                decoded += alphabet[index]
            elif ch.isupper():
                # 대문자인 경우도 소문자로 인덱싱한 후 대문자로 변환
                index = (alphabet.index(ch.lower()) - shift) % 26
                decoded += alphabet[index].upper()
            else:
                # 알파벳이 아닌 문자는 그대로 유지
                decoded += ch
        print(f'[{shift}] {decoded}')


def read_password_file():
    """
    암호 문자열이 저장된 password.txt 파일을 읽는다.

    Returns:
        str: 파일에서 읽은 암호 문자열 (공백 제거)
    """
    try:
        with open('password.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print('파일을 찾을 수 없습니다.')
        return ''
    except PermissionError:
        print('파일에 접근할 권한이 없습니다.')
        return ''
    except Exception as e:
        print(f'오류 발생: {e}')
        return ''


def save_result(text):
    """
    최종적으로 선택한 해독 결과를 result.txt 파일에 저장한다.

    Args:
        text (str): 저장할 해독 문자열
    """
    try:
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print('결과가 result.txt에 저장되었습니다.')
    except Exception as e:
        print(f'결과 저장 중 오류 발생: {e}')


def main():
    """
    프로그램 실행의 시작점이며 전체 해독 과정을 진행한다:
    - 암호 파일 읽기
    - 모든 시프트 해독 결과 출력
    - 사용자로부터 해독 시프트 번호를 입력받아 결과 저장
    """
    cipher_text = read_password_file()
    if cipher_text:
        caesar_cipher_decode(cipher_text)
        try:
            selected = int(input('\n정상적으로 해독된 번호를 입력하세요: '))
            if 0 <= selected < 26:
                alphabet = 'abcdefghijklmnopqrstuvwxyz'
                result = ''
                for ch in cipher_text:
                    if ch.islower():
                        index = (alphabet.index(ch) - selected) % 26
                        result += alphabet[index]
                    elif ch.isupper():
                        index = (alphabet.index(ch.lower()) - selected) % 26
                        result += alphabet[index].upper()
                    else:
                        result += ch
                save_result(result)
            else:
                print('유효하지 않은 번호입니다.')
        except ValueError:
            print('숫자를 입력하세요.')


if __name__ == '__main__':
    main()