import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SIZE = 256
c = SIZE // 2

def spectrum(img):
    f = np.fft.fftshift(np.fft.fft2(img))
    return np.log(np.abs(f) + 1)

# ---------- fft_diamond_test.png ----------
def make_points(pts):
    img = np.zeros((SIZE, SIZE))
    for (y, x) in pts:
        img[int(round(y)), int(round(x))] = 1.0
    return img

h = 50
square_pts = [(c-h, c-h), (c-h, c+h), (c+h, c-h), (c+h, c+h)]
theta = np.radians(45)
R = h / np.cos(np.radians(45))  # distance so rotated points still land near integer grid nicely
diamond_pts = [(c - h*np.sqrt(2), c), (c, c - h*np.sqrt(2)), (c, c + h*np.sqrt(2)), (c + h*np.sqrt(2), c)]

sq_img = make_points(square_pts)
di_img = make_points(diamond_pts)
sq_spec = spectrum(sq_img)
di_spec = spectrum(di_img)

fig, axes = plt.subplots(2, 2, figsize=(9, 9))
axes[0,0].imshow(sq_img, cmap='gray'); axes[0,0].set_title('Square corners (axis-aligned)'); axes[0,0].axis('off')
axes[0,1].imshow(di_img, cmap='gray'); axes[0,1].set_title('Diamond (rotated 45°)'); axes[0,1].axis('off')
axes[1,0].imshow(sq_spec, cmap='gray'); axes[1,0].set_title('Spectrum: cross pattern'); axes[1,0].axis('off')
axes[1,1].imshow(di_spec, cmap='gray'); axes[1,1].set_title('Spectrum: rotated 45° too'); axes[1,1].axis('off')
fig.suptitle('Rotation property: rotating the image rotates the spectrum by the same angle', fontsize=12)
plt.tight_layout()
plt.savefig('fft_diamond_test.png', dpi=130)
plt.close()

# ---------- fft_1d_demo.png ----------
N = 64
x = np.arange(N)
signal = 1.0*np.sin(2*np.pi*3*x/N) + 0.5*np.sin(2*np.pi*7*x/N)
F = np.fft.fft(signal)
mag = np.abs(F)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].plot(x, signal, marker='o', markersize=3, color='black')
axes[0].set_title('1D signal (64 samples): freq=3 (amp 1) + freq=7 (amp 0.5)')
axes[0].set_xlabel('sample index')
axes[1].stem(np.arange(N), mag)
axes[1].set_title('FFT magnitude — peaks exactly at 3, 7 (and mirrors 61, 57)')
axes[1].set_xlabel('frequency bin')
plt.tight_layout()
plt.savefig('fft_1d_demo.png', dpi=130)
plt.close()

# ---------- fft_2d_demo.png ----------
yy, xx = np.mgrid[0:SIZE, 0:SIZE]

def grating(freq, angle_deg, phase=0):
    theta = np.radians(angle_deg)
    return np.sin(2*np.pi*freq*(xx*np.cos(theta) + yy*np.sin(theta))/SIZE + phase)

gratings = [
    ('horizontal, freq=8', grating(8, 0)),
    ('vertical, freq=8', grating(8, 90)),
    ('diagonal 45°, freq=12', grating(12, 45)),
]

fig, axes = plt.subplots(3, 2, figsize=(8, 11))
for i, (label, g) in enumerate(gratings):
    axes[i,0].imshow(g, cmap='gray'); axes[i,0].set_title(f'grating: {label}'); axes[i,0].axis('off')
    axes[i,1].imshow(spectrum(g), cmap='gray'); axes[i,1].set_title('spectrum: one point pair'); axes[i,1].axis('off')
fig.suptitle('Each 2D grating = one point pair in the spectrum (direction + spacing)', fontsize=12)
plt.tight_layout()
plt.savefig('fft_2d_demo.png', dpi=130)
plt.close()

# ---------- fft_filled_box.png ----------
box = np.zeros((SIZE, SIZE))
box[c-40:c+40, c-40:c+40] = 1.0
box_spec = spectrum(box)

fig, axes = plt.subplots(1, 2, figsize=(9, 4.8))
axes[0].imshow(box, cmap='gray'); axes[0].set_title('Filled square'); axes[0].axis('off')
axes[1].imshow(box_spec, cmap='gray'); axes[1].set_title('Spectrum: cross (+) pattern'); axes[1].axis('off')
fig.suptitle('Horizontal edges -> vertical-axis energy, vertical edges -> horizontal-axis energy', fontsize=11)
plt.tight_layout()
plt.savefig('fft_filled_box.png', dpi=130)
plt.close()

print("done")
