import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(-10, 10, 1000)
freqs = [0.15, 0.3, 0.5, 0.7]  # 후보 주파수들 (점점 촘촘해짐)

d_small = 1.2   # 두 점이 가까움
d_large = 6.0   # 두 점이 멂

fig, axes = plt.subplots(len(freqs), 2, figsize=(12, 12))

for row, k in enumerate(freqs):
    for col, d in enumerate([d_small, d_large]):
        ax = axes[row, col]
        wave = np.cos(2*np.pi*k*x)
        ax.plot(x, wave, color="lightsteelblue", lw=1.5)
        p1, p2 = -d/2, d/2
        y1, y2 = np.cos(2*np.pi*k*p1), np.cos(2*np.pi*k*p2)
        aligned = (y1 > 0.7 and y2 > 0.7)
        color = "green" if aligned else "red"
        ax.plot([p1,p2],[y1,y2], "o", color=color, markersize=10, zorder=5)
        ax.axhline(0, color="gray", lw=0.5)
        status = "일치(★)" if aligned else "불일치"
        d_label = "가까운 두 점" if col==0 else "먼 두 점"
        ax.set_title(f"{d_label}, 후보주파수 k={k}  →  {status}", fontsize=10,
                     color=("darkgreen" if aligned else "darkred"))
        ax.set_ylim(-1.3, 1.3)
        ax.set_xticks([]); 

plt.tight_layout()
path = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/11_reciprocal_explain.png"
plt.savefig(path, dpi=120)
plt.close()
print("saved:", path)
