import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

size = 256
h = 30

def spectrum(img):
    f = np.fft.fftshift(np.fft.fft2(img.astype(np.float64)))
    return 20*np.log(np.abs(f)+1)

# 1) 정중앙 정사각형
center_sq = np.zeros((size,size), np.uint8)
c = size//2
center_sq[c-h:c+h, c-h:c+h] = 255

# 2) 왼쪽 위 구석 정사각형 (같은 크기, 위치만 다름)
corner_sq = np.zeros((size,size), np.uint8)
corner_sq[20:20+2*h, 20:20+2*h] = 255

fig, axes = plt.subplots(2, 2, figsize=(10,10))
axes[0,0].imshow(center_sq, cmap="gray"); axes[0,0].set_title("정사각형: 이미지 정중앙"); axes[0,0].axis("off")
axes[0,1].imshow(corner_sq, cmap="gray"); axes[0,1].set_title("정사각형: 왼쪽 위 구석\n(크기·모양은 동일, 위치만 다름)"); axes[0,1].axis("off")
axes[1,0].imshow(spectrum(center_sq), cmap="inferno"); axes[1,0].set_title("스펙트럼 (정중앙 사각형)"); axes[1,0].axis("off")
axes[1,1].imshow(spectrum(corner_sq), cmap="inferno"); axes[1,1].set_title("스펙트럼 (구석 사각형)\n-- 거의 똑같이 생김!"); axes[1,1].axis("off")
plt.tight_layout()
path = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/08_position_invariance.png"
plt.savefig(path, dpi=130)
plt.close()
print("saved:", path)
