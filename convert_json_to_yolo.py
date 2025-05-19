import os
import json

# 입력 및 출력 경로 (본인 로컬 환경 맞게 수정)
INPUT_JSON_DIR = "D:/reusable-trash-images/reusable-trash-images/selectstar-reusable-trash-json"
OUTPUT_LABEL_DIR = "D:/reusable-trash-images/reusable-trash-images/yolo-labels"

classes = ['paper', 'pack', 'can', 'glass', 'pet', 'plastic', 'vinyl']
class_to_id = {name: idx for idx, name in enumerate(classes)}

os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

total_files = 0
converted_files = 0
skipped_files = 0
unknown_labels = 0

for filename in os.listdir(INPUT_JSON_DIR):
    if not filename.endswith(".json"):
        continue

    total_files += 1
    json_path = os.path.join(INPUT_JSON_DIR, filename)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except UnicodeDecodeError:
        try:
            with open(json_path, 'r', encoding='cp949') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ {filename} 디코딩 실패: {e}")
            skipped_files += 1
            continue
    except Exception as e:
        print(f"❌ {filename} 처리 중 오류 발생: {e}")
        skipped_files += 1
        continue

    image_width = data['imageWidth']
    image_height = data['imageHeight']
    shapes = data['shapes']
    yolo_lines = []

    for shape in shapes:
        if shape['shape_type'] != 'rectangle':
            continue

        label = shape['label']
        if label not in class_to_id:
            print(f"⚠️ 알 수 없는 라벨입니다: {label}")
            unknown_labels += 1
            continue

        (x1, y1), (x2, y2) = shape['points']
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)

        x_center = ((x_min + x_max) / 2) / image_width
        y_center = ((y_min + y_max) / 2) / image_height
        w = (x_max - x_min) / image_width
        h = (y_max - y_min) / image_height

        class_id = class_to_id[label]
        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    if yolo_lines:
        label_filename = os.path.splitext(data['imagePath'])[0] + '.txt'
        label_path = os.path.join(OUTPUT_LABEL_DIR, label_filename)
        with open(label_path, 'w') as f:
            f.write('\n'.join(yolo_lines))
        converted_files += 1
        print(f"✅ 변환 완료!!: {filename} → {label_filename}")
    else:
        skipped_files += 1
        print(f"⚠️ 라벨이 없습니다. 건너뜁니다: {filename}")

print("\n===== 변환 요약 =====")
print(f"총 JSON 파일 수: {total_files}")
print(f"성공적으로 변환된 파일: {converted_files}")
print(f"라벨 없음으로 건너뛴 파일: {skipped_files}")
print(f"알 수 없는 라벨 수: {unknown_labels}")
