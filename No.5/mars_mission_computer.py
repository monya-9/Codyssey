# Codyssey No.5 - 문제8 불안정한 미션 컴퓨터…
# 미션 컴퓨터 정보를 가져오는 코드 작성해서 상태를 파악

import platform
import json
import psutil  # 시스템 정보를 가져오기 위한 라이브러리


class MissionComputer:
    """미션 컴퓨터 클래스"""
    
    def __init__(self):
        """MissionComputer 클래스 초기화"""
        pass
        
    def get_mission_computer_info(self):
        """
        미션 컴퓨터의 시스템 정보를 가져오는 메소드
        
        Returns:
            dict: 시스템 정보를 담은 딕셔너리
        """
        try:
            system_info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU의 타입': platform.processor(),
                'CPU의 코어 수': psutil.cpu_count(logical=False),
                '메모리의 크기': f'{round(psutil.virtual_memory().total / (1024**3), 2)} GB'
            }
            
            # JSON 형식으로 출력
            print(json.dumps(system_info, ensure_ascii=False, indent=4))
            
            return system_info
        except Exception as e:
            print(f'시스템 정보를 가져오는 중 오류 발생: {e}')
            return {}
    
    def get_mission_computer_load(self):
        """
        미션 컴퓨터의 부하 정보를 가져오는 메소드
        
        Returns:
            dict: 시스템 부하 정보를 담은 딕셔너리
        """
        try:
            load_info = {
                'CPU 실시간 사용량': f'{psutil.cpu_percent()}%',
                '메모리 실시간 사용량': f'{psutil.virtual_memory().percent}%'
            }
            
            # JSON 형식으로 출력
            print(json.dumps(load_info, ensure_ascii=False, indent=4))
            
            return load_info
        except Exception as e:
            print(f'시스템 부하 정보를 가져오는 중 오류 발생: {e}')
            return {}


def main():
    # MissionComputer 클래스 인스턴스화
    runComputer = MissionComputer()

    # 시스템 정보 출력
    print('시스템 정보:')
    runComputer.get_mission_computer_info()

    # 시스템 부하 정보 출력
    print('\n시스템 부하 정보:')
    runComputer.get_mission_computer_load()


if __name__ == '__main__':
    main()