"""
FFT/IFFT 심화 실습: 정사각형 꼭짓점(축 정렬) vs 마름모(45도 회전) 비교
- 분리 가능(separable) 구조 여부에 따라 스펙트럼이 달라지는지 직접 확인
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams['axes.unicode_minus'] = False

SIZE = 256
c = SIZE // 2

def make_images():
    imgs = {}

    # 1) 정사각형 꼭짓점 4개 (축 정렬, 기존 실습과 동일) - 분리 가능(separable) 구조
    sq = np.zeros((SIZE, SIZE), np.float64)
    h = 50
    for dy, dx in [(-h, -h), (-h, h), (h, -h), (h, h)]:
        sq[c+dy, c+dx] = 255
    imgs["square_corners_axis_aligned"] = sq

    # 2) 마름모 (위/아래/좌/우 점 4개) - 정사각형을 45도 돌린 배치, 분리 불가능 구조
    dm = np.zeros((SIZE, SIZE), np.float64)
    r = 70  # 원점에서 거리 (h*sqrt(2)와 비슷한 스케일로 맞춤)
    for dy, dx in [(-r, 0), (r, 0), (0, -r), (0, r)]:
        dm[c+dy, c+dx] = 255
    imgs["diamond_4points_45deg"] = dm

    return imgs

def fft_ifft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude = 20*np.log(np.abs(fshift)+1)
    img_back = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift)))
    recon_error = np.mean(np.abs(img - img_back))
    return magnitude, img_back, recon_error

if __name__ == "__main__":
    imgs = make_images()
    fig, axes = plt.subplots(len(imgs), 3, figsize=(12, 4*len(imgs)))
    for i, (name, img) in enumerate(imgs.items()):
        mag, recon, err = fft_ifft(img)
        axes[i,0].imshow(img, cmap="gray"); axes[i,0].set_title(f"original: {name}"); axes[i,0].axis("off")
        axes[i,1].imshow(mag, cmap="gray"); axes[i,1].set_title("2D FFT (magnitude, log)"); axes[i,1].axis("off")
        axes[i,2].imshow(recon, cmap="gray"); axes[i,2].set_title(f"IFFT recon (err={err:.6f})"); axes[i,2].axis("off")
        print(f"{name}: recon error = {err:.6f}")

    plt.tight_layout()
    path = "fft_diamond_test.png"
    plt.savefig(path, dpi=130)
    plt.close()
    print("saved:", path)
