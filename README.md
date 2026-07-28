# AI 생성 이미지 판별 서비스 — 5차 미팅 준비 실습

4차 미팅(2026-07-26) 실행 항목 1~6에 대한 실습/실험 코드 모음입니다.

- `01_fft_basic.py` : 2D FFT/IFFT 단순 이미지 실습 (점/정사각형/직사각형/사인파)
- `02_brisque_proxy.py` : BRISQUE 스타일 MSCN/AGGD 특징 비교 (실사진 프록시 vs 스케치 vs AI생성 프록시)
- `03_diffusion_fft.py` : 업스케일 생성 이미지의 2D FFT 패턴(체커보드 아티팩트) 확인
- `04_watermark_analoghole.py` : 저오퍼시티 고주파 워터마크 + 아날로그 홀(재촬영) 시뮬레이션
- `05_flowchart.py` : 클라이언트(JS) 이미지 필터링 구조 흐름도 생성

## 실행 방법
```
pip install opencv-python-headless numpy matplotlib
python3 01_fft_basic.py
python3 02_brisque_proxy.py
python3 03_diffusion_fft.py
python3 04_watermark_analoghole.py
python3 05_flowchart.py
```

## 참고
샌드박스 환경에 외부 인터넷(이미지 다운로드)이 막혀 있어 실제 사진/실제 디퓨전 생성 이미지 대신
동일한 통계적 성질을 갖는 합성(synthetic) 프록시 이미지로 방법론을 검증했습니다.
실제 이미지 파일 경로로 교체하면 동일하게 재사용 가능합니다.
