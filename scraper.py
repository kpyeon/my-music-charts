import time
import json
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_kpop_circle(limit=20):
    url = "https://circlechart.kr/data/api/chart/global"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            raw_list = data.get('data', {}).get('list', []) or data.get('list', [])
            chart = []
            for idx, item in enumerate(raw_list[:limit], start=1):
                chart.append({
                    'rank': idx,
                    'title': item.get('SONG_NAME') or item.get('song_name'),
                    'artist': item.get('ARTIST_NAME') or item.get('artist_name')
                })
            return chart
    except Exception as e:
        print(f"K-Pop 수집 에러: {e}")
    return []

def get_jpop_apple(limit=20):
    url = "https://itunes.apple.com/jp/rss/topsongs/limit=30/json"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            entries = data.get('feed', {}).get('entry', [])
            chart = []
            for idx, item in enumerate(entries[:limit], 1):
                chart.append({
                    'rank': idx,
                    'title': item.get('im:name', {}).get('label'),
                    'artist': item.get('im:artist', {}).get('label')
                })
            return chart
    except Exception as e:
        print(f"J-Pop 수집 에러: {e}")
    return []

if __name__ == "__main__":
    kpop = get_kpop_circle(limit=20)
    jpop = get_jpop_apple(limit=20)
    
    combined = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "kpop": kpop,
        "jpop": jpop
    }
    
    with open("chart_data.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=4)
    print("수집 완료 및 파일 보존 완료!")
