"""
테스트 케이스 확장: 원(circle) - 회전 대칭 신호의 스펙트럼도 회전 대칭인지 확인
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIZE = 256
c = SIZE // 2
y, x = np.ogrid[:SIZE, :SIZE]
dist = np.sqrt((x - c)**2 + (y - c)**2)

# 원 테두리 (얇은 링)
r = 60
ring_width = 2
circle = np.where(np.abs(dist - r) < ring_width, 255.0, 0.0)

def fft_ifft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude = 20*np.log(np.abs(fshift)+1)
    img_back = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift)))
    recon_error = np.mean(np.abs(img - img_back))
    return magnitude, img_back, recon_error

mag, recon, err = fft_ifft(circle)
print(f"circle: recon error = {err:.6f}")

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
axes[0].imshow(circle, cmap="gray"); axes[0].set_title("original: circle outline"); axes[0].axis("off")
axes[1].imshow(mag, cmap="gray"); axes[1].set_title("2D FFT spectrum (magnitude, log)"); axes[1].axis("off")
axes[2].imshow(recon, cmap="gray"); axes[2].set_title(f"IFFT recon (err={err:.6f})"); axes[2].axis("off")
plt.tight_layout()
plt.savefig("fft_circle_test.png", dpi=130)
plt.close()
print("saved fft_circle_test.png")
