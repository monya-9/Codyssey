# Codyssey No.4 - 문제7 살아난 미션 컴퓨터
# 직접 센서 데이터의 결과를 출력하고 내용을 확인

import random
import time
import json
from datetime import datetime


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.ds = DummySensor()
        self.history = []

    def get_sensor_data(self):
        print("시스템 시작. 종료하려면 'q'를 입력하세요.")
        start_time = time.time()
        while True:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            self.history.append(self.env_values.copy())

            print(json.dumps(self.env_values, indent=2))

            if len(self.history) >= 60:
                avg = {}
                for key in self.env_values:
                    avg[key] = round(sum(d[key] for d in self.history[-60:]) / 60, 2)
                print('[5분 평균]')
                print(json.dumps(avg, indent=2))

            print("5초 대기 중... 종료하려면 'q'를 누르세요.")
            for _ in range(5):
                time.sleep(1)
                try:
                    import msvcrt
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8')
                        if key == 'q':
                            print('System stopped...')
                            return
                except ImportError:
                    pass


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()