"""
테스트 케이스 확장: 대각선 하나 / 완전 무작위 노이즈
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIZE = 256
c = SIZE // 2

# 1) 대각선 하나 (좌상단->우하단, 45도 방향 직선)
diag = np.zeros((SIZE, SIZE))
for i in range(SIZE):
    diag[i, i] = 255
    if i+1 < SIZE: diag[i, i+1] = 255  # 살짝 두껍게

# 2) 완전 무작위 노이즈
rng = np.random.default_rng(0)
noise = rng.uniform(0, 255, size=(SIZE, SIZE))

def fft_ifft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude = 20*np.log(np.abs(fshift)+1)
    img_back = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift)))
    recon_error = np.mean(np.abs(img - img_back))
    return magnitude, img_back, recon_error

fig, axes = plt.subplots(2, 3, figsize=(13, 9))
for row, (name, img) in enumerate([("diagonal line", diag), ("random noise", noise)]):
    mag, recon, err = fft_ifft(img)
    axes[row,0].imshow(img, cmap="gray"); axes[row,0].set_title(f"original: {name}"); axes[row,0].axis("off")
    axes[row,1].imshow(mag, cmap="gray"); axes[row,1].set_title("2D FFT spectrum"); axes[row,1].axis("off")
    axes[row,2].imshow(recon, cmap="gray"); axes[row,2].set_title(f"IFFT recon (err={err:.6f})"); axes[row,2].axis("off")
    print(f"{name}: recon error = {err:.6f}")

plt.tight_layout()
plt.savefig("fft_diagonal_noise_test.png", dpi=130)
plt.close()
print("saved fft_diagonal_noise_test.png")
