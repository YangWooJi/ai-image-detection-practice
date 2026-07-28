"""
저(低)오퍼시티 고주파 워터마크 합성 + '아날로그 홀'(재촬영) 공격 시뮬레이션
--------------------------------------------------------------------
교수님 아이디어: 사람 눈에는 거의 안 보이지만(저오퍼시티) 카메라로 재촬영해도
살아남는 "고주파" 패턴을 이미지에 합성 -> 재촬영(블러+압축+리사이즈+노이즈)
후에도 FFT 상에서 패턴이 검출되는지 확인.

개선점: 워터마크 유무 두 조건에 "동일한" 열화(블러/압축/리사이즈/노이즈) 시드를
사용해 순수하게 워터마크 신호만의 생존율을 비교(차분 스펙트럼 분석).
자연 영상은 저주파에 에너지가 집중되고 고주파로 갈수록 에너지가 급격히
줄어들기 때문에, 워터마크를 Nyquist에 가까운 고주파(freq=100/128)에 배치.
"""
import numpy as np
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

def base_photo(size=256, seed=1):
    rng = np.random.default_rng(seed)
    img = np.zeros((size, size))
    amp = 1.0
    for o in range(6):
        scale = 2 ** o
        small = rng.normal(size=(max(size//scale,2), max(size//scale,2)))
        big = cv2.resize(small, (size, size), interpolation=cv2.INTER_CUBIC)
        img += amp * big
        amp *= 0.55
    img = (img - img.min()) / (img.max() - img.min()) * 220 + 20
    return img

def make_watermark_pattern(size=256, freq=100):
    x = np.arange(size)
    xx, yy = np.meshgrid(x, x)
    pattern = np.sin(2*np.pi*freq*xx/size) * np.sin(2*np.pi*freq*yy/size)
    return pattern

def simulate_analog_hole(img, noise_seed=99):
    """화면 재촬영 근사: 블러 -> JPEG 압축 -> 다운/업 리사이즈 -> 동일 시드 노이즈"""
    rng = np.random.default_rng(noise_seed)
    blurred = cv2.GaussianBlur(img, (3,3), 0.6)
    ok, enc = cv2.imencode(".jpg", np.clip(blurred,0,255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 55])
    jpeg = cv2.imdecode(enc, cv2.IMREAD_GRAYSCALE).astype(np.float64)
    small = cv2.resize(jpeg, (jpeg.shape[1]//2, jpeg.shape[0]//2), interpolation=cv2.INTER_AREA)
    back = cv2.resize(small, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
    noisy = back + rng.normal(0, 3.0, back.shape)  # 동일 seed -> 동일 노이즈 패턴
    return np.clip(noisy, 0, 255)

def spectrum(img):
    f = np.fft.fftshift(np.fft.fft2(img.astype(np.float64)))
    return f, 20*np.log(np.abs(f)+1)

def peak_and_floor(mag, freq, size=256):
    c = size//2
    coords = [(c+freq, c+freq), (c+freq, c-freq), (c-freq, c+freq), (c-freq, c-freq)]
    peak = np.mean([mag[py, px] for py, px in coords])
    yy, xx = np.indices((size,size))
    r = np.sqrt((xx-c)**2 + (yy-c)**2)
    donut = mag[(r>freq-5)&(r<freq+5)]
    # 정확히 피크 좌표 근방(반경3) 제외한 도넛 평균을 노이즈 플로어로 사용
    floor = np.median(donut)
    return peak, floor

if __name__ == "__main__":
    outdir = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice"
    size = 256
    FREQ = 45
    photo = base_photo(size)
    pattern = make_watermark_pattern(size, freq=FREQ)

    opacity = 0.03
    watermarked = np.clip(photo + opacity*255*pattern, 0, 255)
    psnr = 10*np.log10((255**2)/np.mean((watermarked-photo)**2))

    # 동일한 열화 시드로 두 조건 처리 (순수 워터마크 생존력 비교를 위해)
    recap_wm = simulate_analog_hole(watermarked, noise_seed=99)
    recap_plain = simulate_analog_hole(photo, noise_seed=99)

    _, mag_orig_wm = spectrum(watermarked)
    _, mag_orig_plain = spectrum(photo)
    _, mag_recap_wm = spectrum(recap_wm)
    _, mag_recap_plain = spectrum(recap_plain)

    # 차분 이미지: 재촬영 후 "워터마크 있음 - 워터마크 없음" => 순수 워터마크 잔존 신호
    diff_recap = recap_wm - recap_plain
    f_diff, mag_diff = spectrum(diff_recap)

    p1, fl1 = peak_and_floor(mag_orig_wm, FREQ, size)
    p2, fl2 = peak_and_floor(mag_recap_wm, FREQ, size)
    p3, fl3 = peak_and_floor(mag_diff, FREQ, size)

    print(f"PSNR(원본 vs 워터마크 삽입) = {psnr:.2f} dB  (30dB 이상이면 육안상 거의 구분 불가)")
    print(f"[삽입 직후]            peak={p1:.1f} floor={fl1:.1f}  peak/floor={p1/fl1:.2f}")
    print(f"[재촬영 후 - 워터마크 포함 이미지 자체] peak={p2:.1f} floor={fl2:.1f}  peak/floor={p2/fl2:.2f}")
    print(f"[재촬영 후 - 차분(워터마크 순수 잔존신호)] peak={p3:.1f} floor={fl3:.1f}  peak/floor={p3/fl3:.2f}")

    fig, axes = plt.subplots(2, 4, figsize=(18,9))
    panels = [("원본", photo, mag_orig_plain),
              ("워터마크 삽입\n(육안상 거의 동일, PSNR %.1fdB)"%psnr, watermarked, mag_orig_wm),
              ("재촬영 시뮬레이션\n(워터마크 O)", recap_wm, mag_recap_wm),
              ("재촬영 후 차분\n(WM있음 - WM없음)", diff_recap+128, mag_diff)]
    for i,(name,im,mag) in enumerate(panels):
        axes[0,i].imshow(im, cmap="gray", vmin=0, vmax=255); axes[0,i].set_title(name, fontsize=10); axes[0,i].axis("off")
        axes[1,i].imshow(mag, cmap="inferno"); axes[1,i].set_title("FFT magnitude"); axes[1,i].axis("off")
    plt.tight_layout()
    path = f"{outdir}/watermark_analoghole.png"
    plt.savefig(path, dpi=130)
    plt.close()
    print("saved:", path)
