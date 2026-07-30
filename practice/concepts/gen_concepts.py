import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SIZE = 256

def make_square_corners(h):
    img = np.zeros((SIZE, SIZE))
    c = SIZE // 2
    pts = [(c-h, c-h), (c-h, c+h), (c+h, c-h), (c+h, c+h)]
    for (y, x) in pts:
        img[y, x] = 1.0
    return img

def make_sine():
    x = np.linspace(0, 2*np.pi, SIZE)
    row = np.sin(2*x)
    img = np.tile(row, (SIZE, 1))
    return img

def spectrum(img):
    f = np.fft.fftshift(np.fft.fft2(img))
    mag = np.log(np.abs(f) + 1)
    return mag

plt.rcParams['font.family'] = 'DejaVu Sans'

# ---------- Concept 1: high/low frequency ----------
sq = make_square_corners(50)
mag = spectrum(sq)
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(mag, cmap='gray')
c = SIZE // 2
ax.annotate('DC (center)\nlow frequency', xy=(c, c), xytext=(c-90, c-90),
            arrowprops=dict(arrowstyle='->', color='yellow', lw=2), color='yellow', fontsize=12,
            ha='center')
ax.annotate('far from center\nhigh frequency', xy=(c+70, c+70), xytext=(c+40, c+110),
            arrowprops=dict(arrowstyle='->', color='cyan', lw=2), color='cyan', fontsize=12,
            ha='center')
ax.set_title('High freq vs Low freq (spectrum of square-corner case)')
ax.axis('off')
plt.tight_layout()
plt.savefig('concept1_freq.png', dpi=130)
plt.close()

# ---------- Concept 2: conjugate symmetry (sine wave case) ----------
sine = make_sine()
mag2 = spectrum(sine)
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(mag2, cmap='gray')
c = SIZE // 2
# find the two bright points on the horizontal center line
row = mag2[c, :]
idx = np.argsort(row)[-3:]  # top brightest incl. DC
idx = sorted(idx)
for i in idx:
    if abs(i - c) > 2:  # skip DC
        ax.scatter([i], [c], s=200, facecolors='none', edgecolors='red', linewidths=2)
ax.annotate('symmetric pair\n(conjugate symmetry)', xy=(idx[0], c), xytext=(idx[0]-60, c-70),
            arrowprops=dict(arrowstyle='->', color='red', lw=2), color='red', fontsize=12, ha='center')
ax.annotate('', xy=(idx[-1], c), xytext=(idx[-1]+40, c-50),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.set_title('Conjugate symmetry (spectrum of sine-wave case)')
ax.axis('off')
plt.tight_layout()
plt.savefig('concept2_symmetry.png', dpi=130)
plt.close()

# ---------- Concept 3: sinc pattern ----------
mag3 = spectrum(sq)
fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
axes[0].imshow(mag3, cmap='gray')
axes[0].set_title('Spectrum (square-corner case)')
axes[0].axis('off')
# 1D cross-section through the center row to show ringing
row = mag3[c, :]
axes[1].plot(row, color='black')
axes[1].set_title('Brightness along center row (sinc-like ringing)')
axes[1].set_xlabel('pixel position')
axes[1].set_ylabel('log magnitude')
plt.tight_layout()
plt.savefig('concept3_sinc.png', dpi=130)
plt.close()

# ---------- Concept 4: cross pattern (horizontal/vertical concentration) ----------
mag4 = spectrum(sq)
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(mag4, cmap='gray')
ax.axhline(c, color='cyan', lw=1, alpha=0.5)
ax.axvline(c, color='cyan', lw=1, alpha=0.5)
ax.annotate('energy concentrated along\nhorizontal & vertical axes\n(cross shape)', xy=(c+15, c-90),
            xytext=(c+15, c-90), color='yellow', fontsize=12, ha='left')
ax.set_title('Cross-shaped concentration (square edges = horizontal+vertical lines)')
ax.axis('off')
plt.tight_layout()
plt.savefig('concept4_cross.png', dpi=130)
plt.close()

# ---------- Concept 5: h=50 vs h=20 comparison ----------
sq50 = make_square_corners(50)
sq20 = make_square_corners(20)
mag50 = spectrum(sq50)
mag20 = spectrum(sq20)
fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
axes[0].imshow(mag50, cmap='gray')
axes[0].set_title('h = 50 (wider spacing in space domain)')
axes[0].axis('off')
axes[1].imshow(mag20, cmap='gray')
axes[1].set_title('h = 20 (narrower spacing in space domain)')
axes[1].axis('off')
fig.suptitle('Reciprocal relationship: smaller h -> wider spectrum spacing', fontsize=13)
plt.tight_layout()
plt.savefig('concept5_reciprocal.png', dpi=130)
plt.close()

print("done")
