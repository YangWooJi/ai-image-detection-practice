import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIZE = 256
c = SIZE // 2

# 진짜로 색칠된(채워진) 정사각형 - 경계선이 있는 box 함수
box = np.zeros((SIZE, SIZE))
h = 40
box[c-h:c+h, c-h:c+h] = 255

F = np.fft.fft2(box)
Fs = np.fft.fftshift(F)
mag = np.log(np.abs(Fs)+1)

fig, axes = plt.subplots(1, 2, figsize=(10,5))
axes[0].imshow(box, cmap="gray"); axes[0].set_title("filled square (real box)"); axes[0].axis("off")
axes[1].imshow(mag, cmap="gray"); axes[1].set_title("2D FFT spectrum (log magnitude)"); axes[1].axis("off")
plt.tight_layout()
plt.savefig("fft_filled_box.png", dpi=130)
plt.close()
print("saved fft_filled_box.png")
