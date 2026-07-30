import numpy as np
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1])

# ---- (A) 세로줄무늬: 좌우로만 변함, 위아래로는 안변함 ----
ax1 = fig.add_subplot(gs[0, 0])
size = 200
x = np.arange(size)
stripe = (127 + 127*np.sin(2*np.pi*6*x/size))
img = np.tile(stripe, (size, 1))
ax1.imshow(img, cmap="gray", extent=[0, size, size, 0])
ax1.set_title("세로줄무늬: 좌우로만 변하고, 위아래로는 안 변함", fontsize=13)
ax1.annotate("", xy=(size*0.35, size*0.85), xytext=(size*0.35, size*0.15),
             arrowprops=dict(arrowstyle="<->", color="cyan", lw=2))
ax1.text(size*0.38, size*0.5, "위아래로 훑어도\n색이 안 바뀜\n(변화 없음)", color="cyan", fontsize=10, va="center")
ax1.annotate("", xy=(size*0.95, size*0.35), xytext=(size*0.55, size*0.35),
             arrowprops=dict(arrowstyle="->", color="yellow", lw=2))
ax1.text(size*0.6, size*0.28, "좌우로 훑으면\n밝다-어둡다 반복", color="yellow", fontsize=10)
ax1.set_xticks([]); ax1.set_yticks([])

# ---- (B) 연못 물결 비유 ----
ax2 = fig.add_subplot(gs[0, 1])
yy, xx = np.mgrid[-100:100, -100:100]
r = np.sqrt(xx**2 + yy**2) + 1e-6
ripple = np.sin(r/4) / (r/4)
ax2.imshow(ripple, cmap="gray")
ax2.set_title("연못 물결 비유: 중심에서 퍼지며\n커졌다 작아졌다 반복하며 잦아듦", fontsize=13)
ax2.set_xticks([]); ax2.set_yticks([])

# ---- (C) sinc 함수 1D 그래프 ----
ax3 = fig.add_subplot(gs[1, 0])
t = np.linspace(-15, 15, 1000)
sinc = np.sinc(t/np.pi)  # sin(x)/x 형태
ax3.plot(t, sinc, color="steelblue", lw=2)
ax3.axhline(0, color="gray", lw=0.5)
ax3.fill_between(t, sinc, 0, alpha=0.2)
ax3.set_title("sinc 함수 그래프\n(중심에서 크고, 오르내리며 잦아듦 = '물결모양 비율')", fontsize=13)
ax3.set_xlabel("중심으로부터 거리(=주파수)")
ax3.set_ylabel("그 주파수가 필요한 정도")
ax3.annotate("여기서 다시\n살짝 올라옴(물결)", xy=(6.2, 0.05), xytext=(8, 0.35),
             arrowprops=dict(arrowstyle="->", color="red"), color="red", fontsize=9)

# ---- (D) 실제 정사각형 스펙트럼의 가로 단면(실제 데이터로 검증) ----
ax4 = fig.add_subplot(gs[1, 1])
sq = np.zeros((256, 256), np.uint8)
c = 128
h = 30
sq[c-h:c+h, c-h:c+h] = 255
f = np.fft.fftshift(np.fft.fft2(sq.astype(np.float64)))
mag = 20*np.log(np.abs(f)+1)
center_row = mag[128, :]
ax4.plot(np.arange(256)-128, center_row, color="darkorange", lw=1.8)
ax4.set_title("실제 우리 데이터: 정사각형 스펙트럼의\n가로 중심선 단면 (진짜로 물결모양이 보임)", fontsize=13)
ax4.set_xlabel("중심으로부터 거리(픽셀)")
ax4.set_ylabel("밝기(그 주파수의 양)")

plt.tight_layout()
path = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/06_stripe_and_sinc_explained.png"
plt.savefig(path, dpi=130)
plt.close()
print("saved:", path)
