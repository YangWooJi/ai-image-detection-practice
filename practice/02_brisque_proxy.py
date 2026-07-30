"""
BRISQUE 스타일 무기준 화질 특징(MSCN + AGGD) 실습
------------------------------------------------
주의: 실제 BRISQUE는 사전 학습된 SVR 회귀 모델(brisque_model_live.yml 등)로
0~100 점수를 산출하지만, 오프라인 샌드박스 환경이라 모델 파일을 내려받을 수 없습니다.
따라서 BRISQUE의 핵심 특징 추출 단계(MSCN 계수 + AGGD 분포 적합, 18차원 특징)까지
직접 구현하고, "자연 영상 기준으로부터의 통계적 이탈도"를 비교 지표로 사용합니다.
실제 배포 시에는 opencv-contrib(cv2.quality.QualityBRISQUE)나 pip brisque 패키지+
사전학습 모델을 이용해 정식 0~100 점수를 내야 합니다.
"""
import numpy as np
import cv2
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

rng = np.random.default_rng(42)

# ---------- 1. 실험용 이미지 생성 ----------
def fractal_noise(size=256, octaves=6):
    """자연 영상과 유사한 1/f 주파수 특성을 가진 합성 텍스처(실사진 프록시)"""
    img = np.zeros((size, size))
    amp = 1.0
    for o in range(octaves):
        scale = 2 ** o
        small = rng.normal(size=(max(size//scale,2), max(size//scale,2)))
        big = cv2.resize(small, (size, size), interpolation=cv2.INTER_CUBIC)
        img += amp * big
        amp *= 0.55
    img = (img - img.min()) / (img.max() - img.min()) * 255
    return img.astype(np.uint8)

def make_sketch(photo):
    """실사진 프록시로부터 엣지 기반 스케치 생성"""
    edges = cv2.Canny(photo, 60, 150)
    sketch = 255 - edges
    return sketch

def make_ai_upscaled(size=256, low=24):
    """저해상도 노이즈를 bicubic 업샘플링 + 체커보드 아티팩트 추가
    (디퓨전/GAN 업샘플링 계열에서 흔히 보고되는 고주파 격자 아티팩트의 프록시)"""
    small = rng.normal(size=(low, low)) * 40 + 128
    up = cv2.resize(small, (size, size), interpolation=cv2.INTER_CUBIC)
    yy, xx = np.mgrid[0:size, 0:size]
    checker = 6 * np.sign(np.sin(xx*np.pi/4) * np.sin(yy*np.pi/4))
    up = up + checker
    up = np.clip(up, 0, 255)
    return up.astype(np.uint8)

# ---------- 2. MSCN + AGGD 기반 BRISQUE 특징 ----------
_gamma_range = np.arange(0.2, 10.001, 0.001)
_gamma_vals = np.array([math.gamma(1.0/g) for g in _gamma_range])
_gamma_vals2 = np.array([math.gamma(2.0/g) for g in _gamma_range])
_gamma_vals3 = np.array([math.gamma(3.0/g) for g in _gamma_range])
_r_gam = (_gamma_vals2**2) / (_gamma_vals * _gamma_vals3)

def mscn_coeff(img, C=1.0):
    img = img.astype(np.float64)
    mu = cv2.GaussianBlur(img, (7,7), 7/6)
    mu_sq = cv2.GaussianBlur(img*img, (7,7), 7/6)
    sigma = np.sqrt(np.abs(mu_sq - mu*mu))
    return (img - mu) / (sigma + C)

def aggd_fit(vec):
    vec = vec.flatten()
    left = vec[vec < 0]
    right = vec[vec >= 0]
    left_std = math.sqrt(np.mean(left**2)) if left.size else 1e-8
    right_std = math.sqrt(np.mean(right**2)) if right.size else 1e-8
    gamma_hat = left_std / right_std
    mean_abs = np.mean(np.abs(vec))
    rhat = (mean_abs**2) / np.mean(vec**2) if np.mean(vec**2) > 0 else 0
    rhat_norm = rhat * (gamma_hat**3 + 1) * (gamma_hat + 1) / ((gamma_hat**2 + 1)**2 + 1e-12)
    idx = np.argmin(np.abs(_r_gam - rhat_norm))
    alpha = _gamma_range[idx]
    return alpha, left_std, right_std

def brisque_like_features(img):
    m = mscn_coeff(img)
    alpha0, l0, r0 = aggd_fit(m)
    feats = [alpha0, (l0**2 + r0**2)/2]
    shifts = {"H": (0,1), "V": (1,0), "D1": (1,1), "D2": (1,-1)}
    for name, (dy, dx) in shifts.items():
        shifted = np.roll(np.roll(m, dy, axis=0), dx, axis=1)
        prod = m * shifted
        a, l, r = aggd_fit(prod)
        feats += [a, l**2, r**2]
    return np.array(feats), m  # 18차원

# ---------- 3. 실행 ----------
if __name__ == "__main__":
    outdir = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice"
    photo = fractal_noise()
    sketch = make_sketch(photo)
    ai_img = make_ai_upscaled()

    images = {"실사진(프록시: 자연 텍스처)": photo,
              "스케치(엣지 변환)": sketch,
              "AI생성/업스케일 프록시": ai_img}

    feats_all = {}
    mscn_all = {}
    for name, img in images.items():
        feats, m = brisque_like_features(img)
        feats_all[name] = feats
        mscn_all[name] = m

    ref_name = "실사진(프록시: 자연 텍스처)"
    ref = feats_all[ref_name]

    print(f"{'이미지 종류':30s}  {'MSCN alpha':>10s}  {'자연기준 대비 특징거리':>20s}")
    dists = {}
    for name, feats in feats_all.items():
        dist = np.linalg.norm(feats - ref)
        dists[name] = dist
        print(f"{name:30s}  {feats[0]:10.3f}  {dist:20.3f}")

    # 시각화: 이미지 + MSCN 히스토그램
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    for i, (name, img) in enumerate(images.items()):
        axes[0, i].imshow(img, cmap="gray")
        axes[0, i].set_title(name)
        axes[0, i].axis("off")
        axes[1, i].hist(mscn_all[name].flatten(), bins=100, color="steelblue")
        axes[1, i].set_title(f"MSCN 계수 분포\nalpha={feats_all[name][0]:.2f}, 자연기준거리={dists[name]:.2f}")
    plt.tight_layout()
    path = f"{outdir}/brisque_comparison.png"
    plt.savefig(path, dpi=130)
    plt.close()
    print("saved:", path)
