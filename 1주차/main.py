# Codyssey 1주차차
# 로그 분석 프로그램

print('Hello Mars')

log_file = 'mission_computer_main.log'

def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {filename}')
        return []
    except PermissionError:
        print(f'파일 권한이 없습니다: {filename}')
        return []
    except Exception as e:
        print(f'오류가 발생했습니다: {e}')
        return []

log_lines = read_log_file(log_file)

print('로그 파일 내용:')
for line in log_lines:
    print(line, end='')

log_lines.reverse()


def analyze_logs(log_lines):
    error_keywords = [
        '[ERROR]',
        '[CRITICAL]',
        'Exception:',
        'Traceback (most recent call last):',
        'mission failure',
        'shutdown',
        'connection lost',
        'unstable',
        'explosion'
    ]

    error_messages = []
    
    for line in log_lines:
        if any(keyword in line for keyword in error_keywords):
            error_messages.append(line.strip())
    
    return error_messages

error_logs = analyze_logs(log_lines)


def save_error_logs(error_logs, output_file='error_logs.txt'):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for log in error_logs:
                file.write(log + '\n')
        print(f'✅ 오류 로그 저장 완료: {output_file}')
    except Exception as e:
        print(f'❌ 오류 로그 저장 중 오류 발생: {e}')

save_error_logs(error_logs)


def generate_markdown_report(error_logs, output_file='log_analysis.md'):
    try:
        with open(output_file, 'w', encoding='utf-8') as md_file:
            md_file.write('# 🚀 로그 분석 보고서\n\n')
            md_file.write('## 1. 개요\n')
            md_file.write('- 본 보고서는 `mission_computer_main.log`의 로그를 분석하여 사고 원인을 조사한 결과입니다.\n')
            md_file.write('- 주요 오류 메시지를 검토하여 시스템 장애의 원인을 분석하였습니다.\n\n')

            md_file.write('## 2. 주요 발견 사항\n')
            if error_logs:
                md_file.write('- 다음과 같은 오류가 발견되었습니다:\n')
                for log in error_logs:
                    md_file.write(f'  - `{log}`\n')
            else:
                md_file.write('- 분석된 주요 오류가 없습니다.\n')

            md_file.write('\n## 3. 사고 원인 및 분석\n')
            md_file.write('- 로그에서 추출된 오류 메시지를 기반으로 시스템 장애 원인을 분석합니다.\n')
            md_file.write('- 필요 시, 추가적인 로그 분석이 필요할 수 있습니다.\n\n')

            md_file.write('## 4. 결론 및 조치 사항\n')
            md_file.write('- 발견된 오류를 기반으로 후속 조치를 결정해야 합니다.\n')
            md_file.write('- 향후 로그 모니터링을 자동화하여 실시간 감지를 강화할 수 있습니다.\n')

        print(f'✅ Markdown 보고서 생성 완료: {output_file}')
    except Exception as e:
        print(f'❌ Markdown 파일 생성 중 오류 발생: {e}')

generate_markdown_report(error_logs)