import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

def make_images(size=256):
    imgs = {}

    dot = np.zeros((size, size), np.uint8)
    dot[size//2, size//2] = 255
    imgs["dot"] = dot

    sq = np.zeros((size, size), np.uint8)
    c = size//2
    h = 30
    sq[c-h:c+h, c-h:c+h] = 255
    imgs["square"] = sq

    rect = np.zeros((size, size), np.uint8)
    rect[c-15:c+15, c-70:c+70] = 255
    imgs["rectangle"] = rect

    x = np.arange(size)
    freq = 8
    sine_1d = (127 + 127*np.sin(2*np.pi*freq*x/size)).astype(np.uint8)
    sine = np.tile(sine_1d, (size, 1))
    imgs["sine_wave"] = sine

    return imgs

def fft_ifft_demo(img, name, outdir):
    f = np.fft.fft2(img.astype(np.float64))
    fshift = np.fft.fftshift(f)
    magnitude = 20*np.log(np.abs(fshift)+1)

    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    fig, axes = plt.subplots(1, 3, figsize=(12,4))
    axes[0].imshow(img, cmap="gray"); axes[0].set_title(f"원본: {name}"); axes[0].axis("off")
    axes[1].imshow(magnitude, cmap="gray"); axes[1].set_title("FFT 주파수 스펙트럼\n(magnitude, log scale)"); axes[1].axis("off")
    axes[2].imshow(img_back, cmap="gray"); axes[2].set_title("IFFT 복원 결과"); axes[2].axis("off")
    plt.tight_layout()
    outpath = f"{outdir}/fft_{name}.png"
    plt.savefig(outpath, dpi=130)
    plt.close()

    recon_error = np.mean(np.abs(img.astype(np.float64) - img_back))
    return outpath, recon_error

if __name__ == "__main__":
    outdir = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice"
    imgs = make_images()
    for name, img in imgs.items():
        path, err = fft_ifft_demo(img, name, outdir)
        print(f"{name}: 복원 오차(평균 절대오차) = {err:.6f} -> {path}")
