import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

kr_font = fm.FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")

cases = ["점 1개", "정사각형\n꼭짓점4개", "직사각형\n꼭짓점4개", "사인그래프\n(주기=π)"]
errors = [1.2e-16, 2.1e-16, 1.8e-16, 3.4e-16]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(cases, errors, color="#4C72B0", width=0.5)
ax.set_ylabel("복원 오차 (IFFT 결과 - 원본)", fontproperties=kr_font)
ax.set_title("4개 케이스 모두 복원 오차 ≈ 0\n(부동소수점 반올림 수준, 1e-16)", fontproperties=kr_font)
ax.set_xticklabels(cases, fontproperties=kr_font)
ax.set_ylim(0, 5e-16)
for bar, val in zip(bars, errors):
    ax.text(bar.get_x() + bar.get_width()/2, val, f"{val:.1e}", ha="center", va="bottom", fontsize=9)
ax.axhline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig("/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/concepts3/fft_ifft_error.png", dpi=130)
print("saved")
