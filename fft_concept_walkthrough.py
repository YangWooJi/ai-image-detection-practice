"""
FFT 개념 처음부터: 1D -> 2D 확장 데모
1) 1D: 숫자 나열이 실제로 몇 개의 사인파 합으로 이루어졌는지 FFT로 "역추적"
2) 2D: 사진(픽셀 격자)도 같은 원리 -- 단, 사인파에 '방향'까지 붙는다 (2D 줄무늬 = grating)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1) 1D demo ----------
def demo_1d():
    N = 64
    t = np.arange(N)
    # 진짜 신호: 주파수 3짜리 파동(진폭1) + 주파수 7짜리 파동(진폭0.5)을 섞어서 하나의 숫자 나열을 만듦
    signal = 1.0*np.sin(2*np.pi*3*t/N) + 0.5*np.sin(2*np.pi*7*t/N)

    F = np.fft.fft(signal)
    mag = np.abs(F) / (N/2)   # 진폭 스케일로 정규화
    freqs = np.fft.fftfreq(N, d=1) * N  # 정수 주파수 라벨

    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    axes[0].stem(t, signal)
    axes[0].set_title("1D signal (just a list of 64 numbers)")
    axes[0].set_xlabel("sample index"); axes[0].set_ylabel("value")

    axes[1].stem(freqs[:N//2], mag[:N//2])
    axes[1].set_title("FFT result: which frequencies are hiding inside, and how strong")
    axes[1].set_xlabel("frequency (cycles per 64 samples)"); axes[1].set_ylabel("amplitude")
    axes[1].set_xlim(0, 20)

    plt.tight_layout()
    plt.savefig("fft_1d_demo.png", dpi=130)
    plt.close()

    peak_idx = np.argsort(mag[:N//2])[::-1][:2]
    print("1D demo: 원래 신호에 넣은 건 freq=3(진폭1), freq=7(진폭0.5)")
    print("FFT가 찾아낸 상위 2개 피크:", [(freqs[i], round(mag[i],2)) for i in peak_idx])


# ---------- 2) 2D demo: gratings (방향+주파수를 가진 줄무늬) ----------
def make_grating(size, fx, fy, amp=1.0):
    """fx, fy: 가로/세로 방향 주파수 성분. 이 값으로 줄무늬의 방향과 간격이 정해진다."""
    x = np.arange(size)
    y = np.arange(size)
    X, Y = np.meshgrid(x, y)
    return amp * np.sin(2*np.pi*(fx*X/size + fy*Y/size))

def demo_2d():
    SIZE = 256
    # grating A: 가로로만 변하는 저주파 줄무늬 (세로선 형태, fy=0)
    gA = make_grating(SIZE, fx=6, fy=0, amp=1.0)
    # grating B: 대각선 방향의 고주파 줄무늬 (fx=fy=20, 45도 방향)
    gB = make_grating(SIZE, fx=20, fy=20, amp=0.5)
    img = gA + gB  # 사진 한 장 = 이 두 줄무늬 패턴이 섞여있는 것 (실제 사진은 이런 줄무늬가 수천 개 섞인 것)

    F = np.fft.fft2(img)
    Fs = np.fft.fftshift(F)
    mag = np.abs(Fs)
    center = SIZE // 2

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    axes[0].imshow(gA, cmap="gray"); axes[0].set_title("grating A only\n(fx=6, fy=0 -> vertical stripes)"); axes[0].axis("off")
    axes[1].imshow(gB, cmap="gray"); axes[1].set_title("grating B only\n(fx=20, fy=20 -> diagonal stripes)"); axes[1].axis("off")
    axes[2].imshow(img, cmap="gray"); axes[2].set_title("img = A + B\n(this is our 'photo')"); axes[2].axis("off")

    zoom = 40  # 중심에서 +-40픽셀만 확대해서 보기 (점들이 중심 근처에 몰려있음)
    axes[3].imshow(np.log(mag+1), cmap="gray",
                    extent=[-center, center, center, -center])
    axes[3].set_xlim(-zoom, zoom); axes[3].set_ylim(zoom, -zoom)
    axes[3].axhline(0, color="red", lw=0.5); axes[3].axvline(0, color="red", lw=0.5)
    axes[3].set_title("2D FFT spectrum of (A+B), zoomed near center\n(0,0)=DC, red lines=axes, each dot=one grating")
    axes[3].set_xlabel("fx"); axes[3].set_ylabel("fy")

    plt.tight_layout()
    plt.savefig("fft_2d_demo.png", dpi=130)
    plt.close()

    # 실제로 스펙트럼에서 밝은 점(피크)들의 좌표를 코드로 직접 찾아서 확인
    thresh = mag.max() * 0.05
    ys, xs = np.where(mag > thresh)
    coords = sorted(set(zip((xs-center).tolist(), (ys-center).tolist())))
    print("2D demo saved. 스펙트럼에서 밝기 임계값을 넘는 (fx,fy) 좌표들:")
    for cxy in coords:
        print("  ", cxy)
    print("예상: grating A -> (+-6, 0), grating B -> (+-20, +-20)")

if __name__ == "__main__":
    demo_1d()
    demo_2d()
