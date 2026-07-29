import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

SIZE = 256
freqs = [2, 4, 8, 16]  # 이미지 폭 안에 줄무늬가 반복되는 횟수

fig, axes = plt.subplots(1, len(freqs), figsize=(16,4.5))
for i, f in enumerate(freqs):
    x = np.arange(SIZE)
    row = 127 + 127*np.sin(2*np.pi*f*x/SIZE)
    img = np.tile(row, (SIZE,1))
    axes[i].imshow(img, cmap="gray")
    label = "저주파(굵음)" if f==min(freqs) else ("고주파(촘촘함)" if f==max(freqs) else "")
    axes[i].set_title(f"반복 {f}번\n{label}", fontsize=12)
    axes[i].axis("off")

plt.suptitle("주파수가 커질수록(반복 횟수가 많아질수록) 줄무늬는 더 가늘고 촘촘해진다", fontsize=13)
plt.tight_layout()
path = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/12_stripe_frequency_examples.png"
plt.savefig(path, dpi=130)
plt.close()
print("saved:", path)
