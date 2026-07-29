import json
from datetime import datetime, timezone, timedelta
KST = timezone(timedelta(hours=9))
N = None
# 표 그대로: 날짜 -> 시(0~23) 순위, N=차트아웃/미기록(검정칸)
TABLE = {
"20260721":[N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,87,83,86,90,68],
"20260722":[56,N,N,N,N,N,N,N,44,55,62,79,87,86,90,95,94,94,86,86,89,85,79,57],
"20260723":[53,94,94,94,94,94,94,95,60,76,90,97,99,99,96,100,100,100,99,98,95,95,91,75],
"20260724":[63,99,99,99,99,99,99,99,69,78,92,96,100,96,96,96,99,96,97,96,96,96,95,81],
"20260725":[67,100,100,100,100,100,100,100,73,80,86,98,98,97,97,97,96,97,95,97,97,97,95,82],
"20260726":[69,98,98,98,97,97,97,97,67,69,76,83,89,89,88,90,92,91,89,91,84,82,71,57],
"20260727":[53,93,93,93,93,93,93,93,54,57,68,79,82,80,86,91,93,89,86,84,87,91,84,72],
"20260728":[71,93,93,93,93,93,93,93,67,73,88,99,98,92,87,95,89,89,86,84,86,85,83,77],
"20260729":[72,93,93,93,93,93,93,93,59,61,75,79,81,79,83,87,90,87,78,82,82,79,76,N],
}
data=[]
for d,hrs in TABLE.items():
    assert len(hrs)==24, (d,len(hrs))
    for h,r in enumerate(hrs):
        if r is None: continue
        ts=datetime(int(d[:4]),int(d[4:6]),int(d[6:8]),h,tzinfo=KST)
        data.append({"ts":ts.isoformat(timespec="minutes"),"rank":r,"freeze":h==1})
with open("docs/data/vitamin_me.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=0)
# 검증
ranks=[p["rank"] for p in data]
best=min(ranks); worst=max(ranks)
bp=[p for p in data if p["rank"]==best][0]
print(f"총 {len(data)}개 포인트")
print(f"최고 #{best} @ {bp['ts']}   최저 #{worst}   변동폭 {worst-best}")
print(f"현재(마지막) #{data[-1]['rank']} @ {data[-1]['ts']}")
print("프리징(1시)태그:", sum(1 for p in data if p['freeze']),"일")
