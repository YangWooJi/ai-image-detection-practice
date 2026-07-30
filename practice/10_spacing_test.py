import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

SIZE = 256
c = SIZE // 2

def make_corners(h):
    img = np.zeros((SIZE, SIZE), np.float64)
    for dy, dx in [(-h,-h),(-h,h),(h,-h),(h,h)]:
        img[c+dy, c+dx] = 255
    return img

def spectrum(img):
    f = np.fft.fftshift(np.fft.fft2(img))
    return 20*np.log(np.abs(f)+1)

small = make_corners(20)   # 점 4개를 가깝게(작은 정사각형)
big = make_corners(50)     # 점 4개를 멀게(큰 정사각형, 아까 그대로)

fig, axes = plt.subplots(2,2, figsize=(10,10))
axes[0,0].imshow(small, cmap="gray"); axes[0,0].set_title("점 4개를 가깝게 (작은 정사각형, h=20)"); axes[0,0].axis("off")
axes[0,1].imshow(big, cmap="gray"); axes[0,1].set_title("점 4개를 멀게 (큰 정사각형, h=50, 어제 것)"); axes[0,1].axis("off")
axes[1,0].imshow(spectrum(small), cmap="gray"); axes[1,0].set_title("스펙트럼 (가까운 점들)"); axes[1,0].axis("off")
axes[1,1].imshow(spectrum(big), cmap="gray"); axes[1,1].set_title("스펙트럼 (먼 점들)"); axes[1,1].axis("off")
plt.tight_layout()
path = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/10_spacing_test.png"
plt.savefig(path, dpi=130)
plt.close()
print("saved:", path)
