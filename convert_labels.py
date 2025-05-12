# 이 스크립트는 TACO.v2-versao-2.yolov5pytorch 데이터셋의 세부 클래스(class ID 0~57)를
# 총 6개의 대분류 클래스로 변환하여 YOLO 형식의 라벨 파일을 재구성합니다.
#
# 각 라벨 파일의 클래스 ID를 대분류 기준으로 재정의하여 라벨을 간소화합니다.
#
# ⭐️ 데이터셋은 본 레포지토리에 포함되어 있지 않습니다.
#     아래 링크에서 직접 다운로드해 주세요:
#     https://universe.roboflow.com/antonio-raimundo/taco/dataset/2/download/yolov5pytorch
#
# 📁 이 파일은 TACO.v2-versao-2.yolov5pytorch 디렉토리 안에서 실행하세요.

import os

fine_to_coarse = {
    0: 0, 1: 0, 11: 0, 16: 0, 24: 0, 25: 0, 44: 0, 46: 0,  # Metal
    6: 1, 9: 1, 10: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1, 42: 1, 43: 1, 48: 1, 49: 1,  # Plastic
    2: 2, 14: 2, 15: 2, 50: 2, 51: 2, 52: 2, 55: 2,  # Special Waste
    3: 3, 19: 3, 20: 3, 21: 3,  # Glass
    4: 4, 7: 4, 8: 4, 12: 4, 13: 4, 22: 4, 23: 4, 26: 4, 27: 4, 33: 4, 34: 4, 35: 4, 36: 4, 54: 4, 57: 4,  # Paper
    5: 5, 17: 5, 18: 5, 45: 5, 47: 5, 53: 5, 56: 5  # General Waste
}

base_path = os.path.dirname(os.path.abspath(__file__))
splits = ['train', 'valid', 'test']

for split in splits:
    label_dir = os.path.join(base_path, split, "labels")
    if not os.path.exists(label_dir):
        print(f"{split}/labels 디렉토리를 찾을 수 없습니다. 건너뜁니다.")
        continue

    for file_name in os.listdir(label_dir):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(label_dir, file_name)

        with open(file_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue

            try:
                original_class = int(parts[0])
                if original_class not in fine_to_coarse:
                    continue
                new_class = fine_to_coarse[original_class]
                new_line = " ".join([str(new_class)] + parts[1:])
                new_lines.append(new_line)
            except ValueError:
                continue

        with open(file_path, 'w') as f:
            f.write("\n".join(new_lines))

    print(f"{split} 변환 완료!!")