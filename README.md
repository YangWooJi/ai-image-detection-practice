# AI 생성 이미지 판별 서비스 — 5차 미팅 준비 실습

4차 미팅(2026-07-26) 액션 아이템 4개를 중심으로 정리한 실습 코드입니다.

| # | 항목 | 우선순위 | 상태 |
|---|------|---------|------|
| 1 | 2D FFT/IFFT 실습 (점 1개 / 정사각형 꼭짓점 / 직사각형 꼭짓점 / 사인그래프 주기=π) | 최상 | 완료 |
| 2 | BRISQUE 테스트 (사각형/AI사각형/만화흑백스케치/AI흑백스케치/비AI흑백스케치/AI컬러스케치) | 최상 | 진행 중 |
| 3 | OpenCV 기초 학습 | 상 | 진행 중 (방학 내내) |
| 4 | 클라이언트(JS) 이미지 필터링 구조 설계 | 중 | 완료 |

## 파일

- `fft_ifft.py` — 점 1개(중앙) / 정사각형 꼭짓점 4개 / 직사각형 꼭짓점 4개 / 사인그래프(주기=π)를 각각 2D FFT 변환 → 스펙트럼 확인 → 2D IFFT로 역변환. 4개 케이스 모두 복원 오차 0.000000.
- `fft_ifft_result.png` — 위 실습 결과 이미지 (원본 / FFT 스펙트럼 / IFFT 복원)
- `client_js_flow.py` — 클라이언트(JS) 이미지 필터링 파이프라인 흐름도 생성 스크립트
- `client_js_flow.png` — 흐름도 결과 이미지
- `brisque_test.py` — (진행 중) BRISQUE 6종 이미지 테스트 스크립트

## 실행 방법

```
pip install numpy matplotlib
python3 fft_ifft.py
python3 client_js_flow.py
```

## 참고

실습 중 정리한 개념 설명과 깨달은 점은 노션 페이지에 있습니다.
[5차 미팅 결과물 (FFT/IFFT, BRISQUE, 클라이언트 흐름도)](https://app.notion.com/p/3ac942a2f054812bba76d499b2f8b0be)
