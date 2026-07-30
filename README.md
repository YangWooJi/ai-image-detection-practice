# AI 생성 이미지 판별 서비스 — 5차 미팅 준비 실습

4차 미팅(2026-07-26) 액션 아이템 4개를 중심으로 정리한 실습 코드입니다.

| # | 항목 | 우선순위 | 상태 |
|---|------|---------|------|
| 1 | 2D FFT/IFFT 실습 (점 1개 / 정사각형 꼭짓점 / 직사각형 꼭짓점 / 사인그래프 주기=π) | 최상 | 완료 |
| 2 | BRISQUE 테스트 (사각형/AI사각형/만화흑백스케치/AI흑백스케치/비AI흑백스케치/AI컬러스케치) | 최상 | 완료 |
| 3 | OpenCV 기초 학습 | 상 | 진행 중 (방학 내내) |
| 4 | 클라이언트(JS) 이미지 필터링 구조 설계 | 중 | 완료 |

## 파일

- `fft_ifft.py` — 점 1개(중앙) / 정사각형 꼭짓점 4개 / 직사각형 꼭짓점 4개 / 사인그래프(주기=π)를 각각 2D FFT 변환 → 스펙트럼 확인 → 2D IFFT로 역변환. 4개 케이스 모두 복원 오차 0.000000.
- `fft_ifft_result.png` — 위 실습 결과 이미지 (원본 / FFT 스펙트럼 / IFFT 복원)
- `client_js_flow.py` — 클라이언트(JS) 이미지 필터링 파이프라인 흐름도 생성 스크립트
- `client_js_flow.png` — 흐름도 결과 이미지
- `brisque_test.py` — BRISQUE 6종 이미지 테스트 스크립트
- `brisque_images/` — BRISQUE 테스트에 사용한 6종 이미지 (출처는 아래 표 참고)

### 심화 실습 (FFT 개념 보강)

- `concept1_freq.png` ~ `concept5_reciprocal.png` — 주파수, 대칭성, sinc 함수, 십자 패턴, 역수 관계 등 FFT 핵심 개념을 하나씩 시각화한 설명 이미지 5종
- `fft_concept_walkthrough.py` — 1D FFT(사인파 합성 신호 역추적) → 2D FFT(줄무늬 격자에 방향 개념 추가) 확장 데모 스크립트
- `fft_1d_demo.png` / `fft_2d_demo.png` — 위 스크립트의 1D / 2D 데모 결과 이미지
- `fft_diamond_test.py` / `fft_diamond_test.png` — 정사각형 꼭짓점(축 정렬, 분리 가능) vs 마름모(45도 회전, 분리 불가능) 스펙트럼 비교
- `fft_filled_box.py` / `fft_filled_box.png` — 테두리만이 아닌 실제로 채워진 정사각형(box 함수)의 2D FFT 스펙트럼
- `fft_circle_test.py` — 원(회전 대칭 신호) 테스트 스크립트, 결과 이미지는 `concepts/fft_circle_test.png`
- `fft_diagonal_noise_test.py` — 대각선 / 완전 무작위 노이즈 테스트 스크립트, 결과 이미지는 `concepts/fft_diagonal_noise_test.png`
- `fft_ifft_error.png` — `fft_ifft.py`의 4개 케이스(점/정사각형/직사각형/사인그래프) 복원 오차를 막대그래프로 비교 (모두 1e-16 수준)

## BRISQUE 테스트 결과

`pip install brisque`(내부적으로 opencv-contrib 기반)로 6종 이미지의 BRISQUE 점수를 계산했다.
점수가 낮을수록 자연 영상 통계에 가깝고(고품질), 높을수록 부자연스러운/왜곡된 통계 특성을 보인다(저품질).

| 이미지 종류 | 파일명 | BRISQUE 점수 | 출처 (라이선스) |
|---|---|---:|---|
| 사각형 이미지 | `square_plain.png` | 121.988 | [Square - black simple.svg](https://commons.wikimedia.org/wiki/File:Square_-_black_simple.svg) (Public Domain) |
| AI로 만든 사각형 이미지 | `square_ai.png` | 103.072 | [Cuboids.png](https://commons.wikimedia.org/wiki/File:Cuboids.png) (CC0, Craiyon 생성) |
| 만화로 만든 흑백 스케치 | `sketch_cartoon_bw.jpg` | 21.357 | [Felix 1919.jpg](https://commons.wikimedia.org/wiki/File:Felix_1919.jpg) (Public Domain, 1919년作) |
| AI로 만든 흑백 스케치 | `sketch_ai_bw.jpg` | 8.259 | [Invisible Religion Drawing AI.jpg](https://commons.wikimedia.org/wiki/File:Invisible_Religion_Drawing_AI.jpg) (CC0, AI 생성) |
| AI 없이 만든 흑백 스케치 | `sketch_nonai_bw.jpg` | 71.610 | [Carl Spitzweg 연필 스케치](https://commons.wikimedia.org/wiki/File:Carl_Spitzweg_-_H%C3%A4nde_und_Arme_eines_M%C3%A4dchens.jpg) (Public Domain) |
| AI로 만든 컬러 스케치 | `sketch_ai_color.png` | 27.352 | [Midjourney - Comic Dinosaur.png](https://commons.wikimedia.org/wiki/File:Midjourney_-_Comic_Dinosaur.png) (CC BY-SA 4.0, Midjourney 생성) |

**관찰**
- 단순 기하학적 도형(사각형 계열)은 AI/비AI 구분과 무관하게 점수가 매우 높게(가장 부자연스럽게) 나왔다. BRISQUE는 자연 사진 통계를 기준으로 학습된 모델이라, 벡터 그래픽처럼 통계적 분산이 거의 없는 이미지에는 점수가 학습 범위를 벗어나 극단적으로 나오는 것으로 보인다.
- 스케치 계열에서는 AI로 만든 흑백 스케치(8.259)가 오히려 비AI 스케치(71.610)나 만화 스케치(21.357)보다 훨씬 낮은(자연스러운) 점수를 받았다. 즉 BRISQUE 점수만으로는 "AI 생성 여부"를 직접 판별하기 어렵고, 오히려 이미지의 세부 질감·노이즈·해상도 특성에 더 민감하게 반응하는 것으로 보인다.

## 실행 방법

```
pip install numpy matplotlib
python3 fft_ifft.py
python3 client_js_flow.py

pip install brisque opencv-contrib-python-headless
python3 brisque_test.py
```

## 참고

실습 중 정리한 개념 설명과 깨달은 점은 노션 페이지에 있습니다.
[5차 미팅 결과물 (FFT/IFFT, BRISQUE, 클라이언트 흐름도)](https://app.notion.com/p/3ac942a2f054812bba76d499b2f8b0be)
