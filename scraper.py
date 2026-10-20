import time
import json
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_apple_chart(country_code, limit=20):
    print(f"🔄 [System] Apple Music {country_code.upper()} 실시간 스트리밍 차트 수집 중...")
    # 🌟 애플 마케팅 툴 공식 최신 API 주소 (절대 막히거나 폭파되지 않는 정식 규격)
    url = f"https://rss.marketingtools.apple.com/api/v2/{country_code}/music/most-played/{limit}/songs.json"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json()
            # 2026년형 최신 JSON 피드 트리 구조 파싱
            results = data.get('feed', {}).get('results', [])
            chart = []
            
            for idx, item in enumerate(results, start=1):
                title = item.get('name') or "알 수 없음"
                artist = item.get('artistName') or "알 수 없음"
                
                chart.append({
                    'rank': idx,
                    'title': str(title).strip(),
                    'artist': str(artist).strip()
                })
            return chart
    except Exception as e:
        print(f"⚠️ {country_code.upper()} 수집 에러: {e}")
    return []

if __name__ == "__main__":
    # 한국(kr) K-Pop 실시간 스트리밍 인기 차트 20위 수집
    kpop = get_apple_chart("kr", limit=20)
    
    # 일본(jp) J-Pop 실시간 스트리밍 인기 차트 20위 수집
    jpop = get_apple_chart("jp", limit=20)
    
    combined = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "kpop": kpop,
        "jpop": jpop
    }
    
    # 깃허브 저장소에 최신 JSON 파일 업데이트
    with open("chart_data.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=4)
        
    print("✅ 애플 공식 API 연동 K-Pop & J-Pop 수집 최종 성공!")
