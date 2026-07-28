"""
디퓨전/업스케일 생성 이미지의 2D FFT 고주파 패턴 확인 실습
-----------------------------------------------------
주의: 샌드박스에 외부 인터넷 이미지 다운로드가 막혀 있어 실제 디퓨전 모델
생성 이미지를 받아올 수 없었습니다. 대신 업스케일링 계열 생성모델에서
보고되는 대표적 아티팩트(격자형 체커보드 패턴 - transposed convolution/
GAN 업샘플링에서 흔함)를 합성한 프록시 이미지로 방법론을 검증합니다.
실제 회의 때는 이 스크립트에 실제 디퓨전 이미지 파일 경로만 바꿔 넣으면
동일하게 재사용 가능합니다.
"""
import numpy as np
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

rng = np.random.default_rng(42)

def fractal_noise(size=256, octaves=6):
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

def make_ai_upscaled(size=256, low=24):
    small = rng.normal(size=(low, low)) * 40 + 128
    up = cv2.resize(small, (size, size), interpolation=cv2.INTER_CUBIC)
    yy, xx = np.mgrid[0:size, 0:size]
    checker = 6 * np.sign(np.sin(xx*np.pi/4) * np.sin(yy*np.pi/4))
    up = up + checker
    up = np.clip(up, 0, 255)
    return up.astype(np.uint8)

def radial_profile(magnitude):
    """중심으로부터 거리별 평균 스펙트럼 에너지(방사형 프로파일)"""
    h, w = magnitude.shape
    cy, cx = h//2, w//2
    y, x = np.indices((h, w))
    r = np.sqrt((x-cx)**2 + (y-cy)**2).astype(int)
    tbin = np.bincount(r.ravel(), magnitude.ravel())
    nr = np.bincount(r.ravel())
    return tbin / np.maximum(nr, 1)

if __name__ == "__main__":
    outdir = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice"
    photo = fractal_noise()
    ai_img = make_ai_upscaled()

    fig, axes = plt.subplots(2, 3, figsize=(14,8))
    profiles = {}
    for i, (name, img) in enumerate([("실사진 프록시(자연 텍스처)", photo), ("AI 업스케일 프록시(체커보드 아티팩트)", ai_img)]):
        f = np.fft.fftshift(np.fft.fft2(img.astype(np.float64)))
        mag = 20*np.log(np.abs(f)+1)
        axes[0,i].imshow(img, cmap="gray"); axes[0,i].set_title(name); axes[0,i].axis("off")
        axes[1,i].imshow(mag, cmap="inferno"); axes[1,i].set_title("FFT magnitude spectrum"); axes[1,i].axis("off")
        profiles[name] = radial_profile(mag)

    ax = axes[0,2]
    for name, prof in profiles.items():
        ax.plot(prof, label=name)
    ax.set_title("방사형 주파수 프로파일\n(중심=저주파 -> 바깥=고주파)")
    ax.set_xlabel("주파수 반경(픽셀)")
    ax.set_ylabel("평균 log-magnitude")
    ax.legend(fontsize=8)
    axes[1,2].axis("off")

    plt.tight_layout()
    path = f"{outdir}/diffusion_fft_pattern.png"
    plt.savefig(path, dpi=130)
    plt.close()
    print("saved:", path)

    # 고주파 영역(반경 100~128) 평균 에너지 비교
    for name, prof in profiles.items():
        hf_energy = np.mean(prof[100:128])
        print(f"{name}: 고주파(반경100-128) 평균 에너지 = {hf_energy:.2f}")
