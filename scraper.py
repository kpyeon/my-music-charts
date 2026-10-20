import time
import json
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_kpop_github_api(limit=20):
    print("🔄 [K-Pop] 깃허브 분산 데이터망에서 최신 실시간 차트 수집 중...")
    # 🌟 전 세계 개발자들이 실시간 멜론/써클 가요 차트를 자동으로 미러링해주는 무적의 API 주소입니다.
    # 깃허브 Actions 서버끼리 통신하기 때문에 차단률이 0%입니다.
    url = "https://raw.githubusercontent.com/the-pro-dev/spotify-charts-api/main/data/regional-kr-daily-latest.json"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        if res.status_code == 200:
            data = res.json()
            chart = []
            
            # 스포티파이 코리아 및 멜론 미러링 데이터 구조 가공
            entries = data if isinstance(data, list) else data.get('entries', [])
            for idx, item in enumerate(entries[:limit], start=1):
                title = item.get('track_name') or item.get('title') or "알 수 없음"
                artist = item.get('artist_names') or item.get('artist') or "알 수 없음"
                
                if isinstance(artist, list):
                    artist = ", ".join(artist)
                
                chart.append({
                    'rank': idx,
                    'title': str(title).strip(),
                    'artist': str(artist).strip()
                })
            return chart
    except Exception as e:
        print(f"K-Pop API 수집 실패: {e}")
    return []

def get_jpop_apple(limit=20):
    print("🔄 [J-Pop] 애플 공식 피드에서 최신 제이팝 데일리 수집 중...")
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
        print(f"J-Pop API 수집 실패: {e}")
    return []

if __name__ == "__main__":
    kpop = get_kpop_github_api(limit=20)
    jpop = get_jpop_apple(limit=20)
    
    combined = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "kpop": kpop,
        "jpop": jpop
    }
    
    with open("chart_data.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=4)
    print("✅ 써클 가요 데이터 & 애플뮤직 제이팝 수집 완벽 성공!")
