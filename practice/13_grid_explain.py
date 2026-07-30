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
h = 50

def spectrum(img):
    f = np.fft.fftshift(np.fft.fft2(img))
    return 20*np.log(np.abs(f)+1)

# (a) 좌우 쌍만 (왼쪽-오른쪽 점 2개, 위아래 변화 없음)
lr = np.zeros((SIZE,SIZE))
lr[c, c-h] = 255
lr[c, c+h] = 255

# (b) 위아래 쌍만 (위-아래 점 2개, 좌우 변화 없음)
tb = np.zeros((SIZE,SIZE))
tb[c-h, c] = 255
tb[c+h, c] = 255

# (c) 4개 다 (좌우+위아래 합쳐짐)
four = np.zeros((SIZE,SIZE))
for dy,dx in [(-h,-h),(-h,h),(h,-h),(h,h)]:
    four[c+dy,c+dx] = 255

fig, axes = plt.subplots(2,3, figsize=(15,10))
titles = ["좌우 점 2개만\n(위아래 변화 없음)", "위아래 점 2개만\n(좌우 변화 없음)", "4개 점 전부\n(좌우+위아래 동시)"]
for i, img in enumerate([lr, tb, four]):
    axes[0,i].imshow(img, cmap="gray"); axes[0,i].set_title(titles[i]); axes[0,i].axis("off")
    axes[1,i].imshow(spectrum(img), cmap="gray"); axes[1,i].axis("off")

axes[1,0].set_title("스펙트럼: 세로줄무늬만\n(가로축 방향으로만 변화)")
axes[1,1].set_title("스펙트럼: 가로줄무늬만\n(세로축 방향으로만 변화)")
axes[1,2].set_title("스펙트럼: 두 무늬가 겹쳐짐\n= 격자(체크)무늬")

plt.tight_layout()
path = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/13_grid_explain.png"
plt.savefig(path, dpi=130)
plt.close()
print("saved:", path)
