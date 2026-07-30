import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fm.fontManager.addfont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(9, 12))
ax.set_xlim(0, 11)
ax.set_ylim(0, 26)
ax.axis("off")

boxes = [
    (5, 24.5, "① 사용자 이미지 업로드 시도\n(모바일 웹뷰 / PC 브라우저)", "#cfe8ff"),
    (5, 21.5, "② 클라이언트(JS) 1차 필터링\n- 해상도 체크\n- BRISQUE-류 화질 프록시 점수\n- 매직바이트 검증(파일 위장 방지)", "#d9f2d9"),
    (2.3, 18, "미달\n(Tier C)", "#ffd6d6"),
    (7.4, 18, "통과", "#d9f2d9"),
    (2.3, 15.3, "업로드 차단 +\n사용자에게 재촬영/\n원본 이미지 요청", "#ffd6d6"),
    (7.4, 15, "③ 클라이언트 측 압축/리사이즈\n(서버 부하 절감)", "#d9f2d9"),
    (7.4, 12, "④ 서버 업로드\n(원본은 임시 저장)", "#cfe8ff"),
    (7.4, 9, "⑤ 비동기 큐 등록\n(백그라운드 작업, 즉시 응답 X)", "#fff2cc"),
    (7.4, 6, "⑥ 핵심 판별 알고리즘\n- 2D FFT 주파수 분석\n- BRISQUE 무기준 화질\n- 워터마크(있는 경우) 검출", "#fff2cc"),
    (7.4, 3, "⑦ 등급/확률 산출 후 저장\n원본 이미지는 즉시 삭제,\n등급·추출 특징만 DB 보관", "#cfe8ff"),
    (7.4, 0.7, "⑧ 사용자에게 신뢰도 등급 표시", "#e0d4f7"),
]

for x, y, text, color in boxes:
    w = 4.0 if x != 2.3 else 3.4
    rect = patches.FancyBboxPatch((x-w/2, y-1.1), w, 2.2, boxstyle="round,pad=0.1",
                                    linewidth=1.2, edgecolor="#333333", facecolor=color)
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=10)

arrows = [
    (5,23.4,5,22.7),
    (5,20.4,2.3,19.1),
    (5,20.4,7.4,19.1),
    (2.3,16.9,2.3,16.4),
    (7.4,16.9,7.4,16.1),
    (7.4,13.9,7.4,13.1),
    (7.4,10.9,7.4,10.1),
    (7.4,7.9,7.4,7.1),
    (7.4,4.9,7.4,4.1),
    (7.4,1.9,7.4,1.8),
]
for x1,y1,x2,y2 in arrows:
    ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle="->", lw=1.4, color="#333333"))

ax.set_title("클라이언트(JS) 기반 이미지 전처리 · 서버 파이프라인 흐름도", fontsize=13, pad=15)
plt.tight_layout()
path = "/sessions/awesome-dazzling-mccarthy/mnt/outputs/practice/client_js_flow.png"
plt.savefig(path, dpi=140)
plt.close()
print("saved:", path)
