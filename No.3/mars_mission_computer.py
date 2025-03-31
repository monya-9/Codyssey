# Codyssey No.3 - 문제6 미션 컴퓨터 리턴즈
# 더미 센서(dummy sensor) 생성 및 테스트

import random
import datetime

class DummySensor:
    """화성 기지 환경 센서를 시뮬레이션하는 클래스"""
    
    def __init__(self):
        """초기 환경 값 설정"""
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
    
    def set_env(self):
        """랜덤 값으로 환경 데이터 설정"""
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 0)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 0)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 0)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 0)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 0)
    
    def get_env(self):
        """환경 값을 반환하고 로그 파일에 기록"""
        log_entry = f"{datetime.datetime.now()}, {self.env_values}\n"
        
        try:
            with open('mars_env_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(f'로그 저장 중 오류 발생: {e}')
        
        return self.env_values

# 인스턴스 생성 및 테스트
def main():
    ds = DummySensor()
    ds.set_env()
    print(ds.get_env())

if __name__ == "__main__":
    main()