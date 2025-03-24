# Codyssey 2주차 - 문제3 인화 물질을 찾아라
# 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력

log_file = 'Mars_Base_Inventory_List.csv'
danger_file = 'Mars_Base_Inventory_danger.csv'
binary_file = 'Mars_Base_Inventory_List.bin'

def read_csv_file(filename):
    """CSV 파일을 읽어 리스트로 변환"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]  # 첫 줄(헤더) 제외
        
        data = []
        for line in lines:
            values = [v.strip() for v in line.split(',')]
            
            # 인화성 값 변환
            try:
                flammability = float(values[-1])
            except ValueError:
                flammability = 0.0  # 변환 실패 시 기본값
            
            data.append({
                'Substance': values[0],
                'Flammability': flammability
            })
        
        return data
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {filename}')
        return []
    except PermissionError:
        print(f'파일 권한이 없습니다: {filename}')
        return []
    except Exception as e:
        print(f'오류가 발생했습니다: {e}')
        return []

def sort_by_flammability(data):
    """인화성 기준으로 내림차순 정렬"""
    return sorted(data, key=lambda x: x['Flammability'], reverse=True)

def filter_high_flammability(data, threshold=0.7):
    """인화성이 threshold 이상인 항목 필터링"""
    return [item for item in data if item['Flammability'] >= threshold]

def save_to_csv(data, filename):
    """데이터를 CSV 파일로 저장"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('Substance,Flammability\n')
            for item in data:
                file.write(f"{item['Substance']},{item['Flammability']}\n")
        print(f'✅ 위험 화물 목록 저장 완료: {filename}')
    except Exception as e:
        print(f'❌ CSV 파일 저장 중 오류 발생: {e}')

def save_to_binary(data, filename):
    """데이터를 이진 파일로 저장"""
    try:
        with open(filename, 'wb') as file:
            for item in data:
                line = f"{item['Substance']}|{item['Flammability']}".encode('utf-8')
                file.write(line + b'\n')
        print(f'✅ 이진 파일 저장 완료: {filename}')
    except Exception as e:
        print(f'❌ 이진 파일 저장 중 오류 발생: {e}')

def read_from_binary(filename):
    """이진 파일을 읽고 출력"""
    try:
        with open(filename, 'rb') as file:
            content = file.readlines()
            print('✅ 저장된 이진 파일 내용:')
            for line in content:
                print(line.decode('utf-8').strip())
    except Exception as e:
        print(f'❌ 이진 파일 읽기 중 오류 발생: {e}')

def main():
    """메인 실행 함수"""
    data_list = read_csv_file(log_file)
    data_list = sort_by_flammability(data_list)
    dangerous_items = filter_high_flammability(data_list)
    
    save_to_csv(dangerous_items, danger_file)
    save_to_binary(data_list, binary_file)
    read_from_binary(binary_file)

if __name__ == "__main__":
    main()