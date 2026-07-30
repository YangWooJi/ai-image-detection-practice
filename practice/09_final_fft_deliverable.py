"""
5차 미팅 최종 결과물 1: 2D FFT / 2D IFFT
- 점 가운데 1개
- 정사각형 꼭지점만(4개 점)
- 직사각형 꼭지점만(4개 점)
- 사인그래프 (이미지 폭을 0~2pi로 볼 때 주기=pi, 즉 폭 전체에 2주기)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

SIZE = 256

def make_images():
    imgs = {}

    # 1) 점 가운데 1개
    dot = np.zeros((SIZE, SIZE), np.float64)
    c = SIZE // 2
    dot[c, c] = 255
    imgs["점_1개(중앙)"] = dot

    # 2) 정사각형 꼭지점만 (4개 점)
    sq = np.zeros((SIZE, SIZE), np.float64)
    h = 50
    for dy, dx in [(-h, -h), (-h, h), (h, -h), (h, h)]:
        sq[c+dy, c+dx] = 255
    imgs["정사각형_꼭짓점만(4점)"] = sq

    # 3) 직사각형 꼭지점만 (4개 점, 가로/세로 비율 다름)
    rect = np.zeros((SIZE, SIZE), np.float64)
    hy, hx = 30, 80
    for dy, dx in [(-hy, -hx), (-hy, hx), (hy, -hx), (hy, hx)]:
        rect[c+dy, c+dx] = 255
    imgs["직사각형_꼭짓점만(4점)"] = rect

    # 4) 사인그래프: 이미지 폭을 0~2pi로 볼 때, 주기=pi (=> 폭 전체에 2주기)
    x = np.linspace(0, 2*np.pi, SIZE, endpoint=False)
    signal = np.sin(2*x)  # sin(k*x)에서 k=2 => 주기 = 2pi/k = pi
    sine_row = 127 + 127*signal
    sine = np.tile(sine_row, (SIZE, 1))
    imgs["사인그래프_주기pi"] = sine

    return imgs

def fft_ifft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude = 20*np.log(np.abs(fshift)+1)
    img_back = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift)))
    recon_error = np.mean(np.abs(img - img_back))
    return magnitude, img_back, recon_error

if __name__ == "__main__":
    outdir = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice"
    imgs = make_images()

    fig, axes = plt.subplots(len(imgs), 3, figsize=(12, 4*len(imgs)))
    for i, (name, img) in enumerate(imgs.items()):
        mag, recon, err = fft_ifft(img)
        axes[i,0].imshow(img, cmap="gray"); axes[i,0].set_title(f"원본: {name}"); axes[i,0].axis("off")
        axes[i,1].imshow(mag, cmap="gray"); axes[i,1].set_title("2D FFT (magnitude, log)"); axes[i,1].axis("off")
        axes[i,2].imshow(recon, cmap="gray"); axes[i,2].set_title(f"2D IFFT 복원\n(오차={err:.6f})"); axes[i,2].axis("off")
        print(f"{name}: 복원 오차 = {err:.6f}")

    plt.tight_layout()
    path = f"{outdir}/09_final_fft_deliverable.png"
    plt.savefig(path, dpi=130)
    plt.close()
    print("saved:", path)
