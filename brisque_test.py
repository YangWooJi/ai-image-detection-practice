"""
BRISQUE(Blind/Referenceless Image Spatial Quality Evaluator) 6종 이미지 비교 테스트
5차 미팅 액션아이템 #2

brisque_images/ 폴더의 6종 이미지에 대해 BRISQUE 점수를 계산하고 표로 출력한다.
점수가 낮을수록 "자연 영상 통계에 가깝다(고품질)", 높을수록 "부자연스럽다(저품질/왜곡)"로 해석된다.

이미지 출처: Wikimedia Commons (전부 CC0 / Public Domain / CC BY-SA 4.0, 상세 출처는 README 참고)
"""
import os
import sys
import cv2
import numpy as np
from brisque import BRISQUE

# Windows 콘솔(cp949 등)에서 한글 출력이 깨지는 것을 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# brisque==0.2.0의 scale_features()가 numpy>=2.0에서 float(shape=(1,) ndarray)를
# 시도하다 TypeError를 내는 알려진 호환성 버그가 있어, 값 추출 방식만 안전하게 패치한다.
# (참고: https://github.com/rehanguha/brisque/blob/main/brisque/brisque.py)
def _patched_scale_features(self, features):
    def _safe_float(f):
        return float(np.ravel(f)[0])

    min_ = np.array(self.scale_params["min_"], dtype=object)
    max_ = np.array(self.scale_params["max_"], dtype=object)
    features_flat = np.array([_safe_float(f) for f in features], dtype=np.float64)
    min_flat = np.array([_safe_float(m) for m in min_], dtype=np.float64)
    max_flat = np.array([_safe_float(m) for m in max_], dtype=np.float64)
    return -1 + (2.0 / (max_flat - min_flat) * (features_flat - min_flat))


BRISQUE.scale_features = _patched_scale_features

IMAGE_DIR = "brisque_images"

# (파일명, 한글 라벨) - README/미팅 액션아이템의 6종 분류에 맞춘 순서
IMAGE_LABELS = {
    "square_plain.png": "사각형 이미지",
    "square_ai.png": "AI로 만든 사각형 이미지",
    "sketch_cartoon_bw.jpg": "만화로 만든 흑백 스케치",
    "sketch_ai_bw.jpg": "AI로 만든 흑백 스케치",
    "sketch_nonai_bw.jpg": "AI 없이 만든 흑백 스케치",
    "sketch_ai_color.png": "AI로 만든 컬러 스케치",
}


def main():
    scorer = BRISQUE(url=False)
    results = []

    for filename, label in IMAGE_LABELS.items():
        path = os.path.join(IMAGE_DIR, filename)
        if not os.path.exists(path):
            print(f"[경고] 파일 없음: {path}")
            continue

        img = cv2.imread(path)
        if img is None:
            print(f"[경고] 이미지를 읽을 수 없음: {path}")
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        score = scorer.score(img_rgb)
        results.append((label, filename, score))

    # 표 출력
    print(f"\n{'이미지 종류':22s} {'파일명':24s} {'BRISQUE 점수':>14s}")
    print("-" * 62)
    for label, filename, score in results:
        print(f"{label:22s} {filename:24s} {score:14.3f}")

    print("\n(참고) 점수가 낮을수록 자연 영상 통계에 가깝고(고품질),")
    print("       높을수록 부자연스러운/왜곡된 통계 특성을 보인다(저품질).")

    return results


if __name__ == "__main__":
    main()
