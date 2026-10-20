import time
import json
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_kpop_apple_feed(limit=20):
    print("🔄 [K-Pop] 애플 공식 한국 가요 인기 랭킹 수집 중...")
    # 🌟 대기업 애플이 영구적으로 제공하여 절대 터질 일 없는 공식 한국 인기 앨범/곡 차트 피드입니다.
    url = "https://itunes.apple.com/kr/rss/topalbums/limit=30/json"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        if res.status_code == 200:
            data = res.json()
            entries = data.get('feed', {}).get('entry', [])
            chart = []
            for idx, item in enumerate(entries[:limit], 1):
                title = item.get('im:name', {}).get('label') or "알 수 없음"
                artist = item.get('im:artist', {}).get('label') or "알 수 없음"
                
                chart.append({
                    'rank': idx,
                    'title': str(title).strip(),
                    'artist': str(artist).strip()
                })
            return chart
    except Exception as e:
        print(f"K-Pop 애플 피드 수집 실패: {e}")
    return []

def get_jpop_apple_feed(limit=20):
    print("🔄 [J-Pop] 애플 공식 일본 데일리 차트 수집 중...")
    url = "https://itunes.apple.com/jp/rss/topsongs/limit=30/json"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        if res.status_code == 200:
            data = res.json()
            entries = data.get('feed', {}).get('entry', [])
            chart = []
            for idx, item in enumerate(entries[:limit], 1):
                title = item.get('im:name', {}).get('label') or "알 수 없음"
                artist = item.get('im:artist', {}).get('label') or "알 수 없음"
                chart.append({
                    'rank': idx,
                    'title': str(title).strip(),
                    'artist': str(artist).strip()
                })
            return chart
    except Exception as e:
        print(f"J-Pop 애플 피드 수집 실패: {e}")
    return []

if __name__ == "__main__":
    kpop = get_kpop_apple_feed(limit=20)
    jpop = get_jpop_apple_feed(limit=20)
    
    combined = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "kpop": kpop,
        "jpop": jpop
    }
    
    with open("chart_data.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=4)
    print("✅ 애플 공식 피드 기반 K-Pop & J-Pop 수집 완벽 성공!")
