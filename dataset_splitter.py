import os
import shutil
import random
from pathlib import Path

# 본인 로컬 환경에 맞게 데이터 경로를 수정해야 합니다.
IMAGE_DIR = Path("D:/reusable-trash-images/reusable-trash-images/selectstar-reusable-trash-image")
LABEL_DIR = Path("D:/reusable-trash-images/reusable-trash-images/yolo-labels")

OUTPUT_DIR = Path("D:/reusable-trash-images/reusable-trash-images/dataset")
OUTPUT_IMAGES = OUTPUT_DIR / "images"
OUTPUT_LABELS = OUTPUT_DIR / "labels"

train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

image_files = list(IMAGE_DIR.glob("*"))
image_files = [f for f in image_files if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]

print(f"총 이미지 수: {len(image_files)}")
random.shuffle(image_files)

total = len(image_files)
train_count = int(total * train_ratio)
val_count = int(total * val_ratio)
test_count = total - train_count - val_count

splits = {
    "train": image_files[:train_count],
    "val": image_files[train_count:train_count + val_count],
    "test": image_files[train_count + val_count:]
}

for split in splits:
    (OUTPUT_IMAGES / split).mkdir(parents=True, exist_ok=True)
    (OUTPUT_LABELS / split).mkdir(parents=True, exist_ok=True)

valid_image_count = 0
for split, files in splits.items():
    for img_path in files:
        label_path = LABEL_DIR / (img_path.stem + ".txt")
        if not label_path.exists():
            print(f"❌ 라벨 없음: {label_path.name} → 이미지 {img_path.name} 건너뜁니다")
            continue

        shutil.copy(img_path, OUTPUT_IMAGES / split / img_path.name)
        shutil.copy(label_path, OUTPUT_LABELS / split / label_path.name)
        valid_image_count += 1

print(f"✅ 데이터셋 분할 완료!! (라벨 있는 이미지 수: {valid_image_count})")
