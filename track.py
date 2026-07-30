#!/usr/bin/env python3
"""
멜론 실시간 TOP100에서 특정 곡의 순위를 찍어 data/vitamin_me.json에 append.
- KST 1시 스냅샷은 freeze=true 로 태깅 (프리징 진입 순위 마킹용)
- TOP100 밖이면 rank=null (차트아웃)
GitHub Actions cron(매시)에서 실행.
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone, timedelta

SONG_NO = os.environ.get("SONG_NO", "602540014")   # fromis_9 - Vitamin ME
OUT      = os.path.join(os.path.dirname(__file__), "docs", "data", "vitamin_me.json")
KST      = timezone(timedelta(hours=9))
CHART_URL = "https://www.melon.com/chart/index.htm"
HEADERS   = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Referer": "https://www.melon.com/",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

def fetch_rank(song_no: str):
    """실시간 TOP100 HTML을 받아 song_no의 순위를 리턴 (없으면 None)."""
    req = urllib.request.Request(CHART_URL, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    # 의존성 없이 파싱: 각 곡 행에 data-song-no="..." 와 <span class="rank ">N</span>
    import re
    # 행 단위로 자르기 (lst50/lst100 tr)
    rows = re.split(r'<tr[^>]*class="lst(?:50|100)"', html)[1:]
    for row in rows:
        m_id = re.search(r'data-song-no="(\d+)"', row)
        if not m_id or m_id.group(1) != song_no:
            continue
        m_rk = re.search(r'<span class="rank ">(\d+)</span>', row)
        if m_rk:
            return int(m_rk.group(1))
    return None

def main():
    now = datetime.now(KST).replace(minute=0, second=0, microsecond=0)  # 정각으로 정렬
    rank = fetch_rank(SONG_NO)
    point = {
        "ts": now.isoformat(timespec="minutes"),   # KST ISO
        "rank": rank,                               # 1~100 또는 null(차트아웃)
        "freeze": now.hour == 1,                    # 프리징 진입 스냅샷 태그
    }

    data = []
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            try: data = json.load(f)
            except json.JSONDecodeError: data = []

    # 같은 시(hour) 중복 방지: 마지막 포인트가 같은 시각대면 덮어씀
    if data and data[-1]["ts"][:13] == point["ts"][:13]:
        data[-1] = point
    else:
        data.append(point)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0)
    print(f"[{point['ts']}] rank={rank} freeze={point['freeze']}  (총 {len(data)}개)")

if __name__ == "__main__":
    main()
