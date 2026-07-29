# Vitamin ME · 멜론차트 트래커

fromis_9 「Vitamin ME」(song_no `602540014`)의 멜론 실시간 TOP100 순위를
매시 수집해서 **주식 캔들 차트**처럼 보는 프로젝트. (번장 앨범 트래커와 동일 아키텍처)

## 구조
```
track.py                     # 실시간 TOP100 스크레이퍼 (stdlib only)
docs/index.html              # GitHub Pages 대시보드 (lightweight-charts 캔들)
docs/data/vitamin_me.json    # 수집 데이터 [{ts, rank, freeze}, ...]
.github/workflows/track.yml  # 매시 cron → 스크레이프 → 커밋
```

## 세팅
1. 이 폴더를 새 repo로 push.
2. **Settings → Pages → Source: `Deploy from a branch`, 브랜치 `main` / 폴더 `/docs`**.
3. **Settings → Actions → General → Workflow permissions: `Read and write`** 체크.
4. Actions 탭에서 `track-melon-chart` → `Run workflow`로 한 번 수동 실행(첫 데이터).
5. `https://<아이디>.github.io/<repo>/` 접속.

이후 매시 자동으로 순위가 쌓이고, KST 1시 스냅샷은 `freeze:true`로 태깅돼
차트에 🧊 마커로 표시됨.

## 캔들 읽는 법
하루치 시간별 순위를 캔들 1개로 집계:
- **시가/종가** = 그날 첫/마지막 순위
- **고가** = 그날 최고 순위(제일 높은 위치), **저가** = 최저
- **초록** = 하루 동안 순위 상승 / **빨강** = 하락
- y축은 순위 반전(위=1위)이라 주식처럼 "위로 = 좋음"

## 초반 백필 (완료)
발매일(20260721)~20260729 시간별 순위는 수기 기록표로 이미 채워둠
(`docs/data/vitamin_me.json`, 181포인트). 멜론이 과거 실시간 차트를
공개 조회로 안 주기 때문에 이 수기 데이터가 초반 구간의 유일한 소스.
이후 구간은 cron이 매시 이어붙임. 데이터는 발매일 진입 87위부터 시작.

재생성: `python gen_backfill.py` (표 원본이 스크립트에 박혀 있음).

## 곡 바꾸기
`track.yml`의 `SONG_NO`와 파일명만 바꾸면 다른 곡도 추적 가능.
song_no는 멜론 곡 페이지 URL 끝 숫자, 또는:
`https://www.melon.com/search/keyword/index.json?jscallback=x&query=<검색어>`
