import yfinance as yf
import pandas as pd
import numpy as np  # 추가
from datetime import datetime, timedelta
from pykrx import stock  # 수급 데이터 추출용
import os

def get_ticker_list():
    """실시간 지수 종목을 가져오되, 실패 시 백업 리스트 반환"""
    print("📡 실시간 우량주(KOSPI 200, KOSDAQ 150) 목록 수집 중...")
    try:
        # 코스피 200 (1028), 코스닥 150 (2034) 구성 종목 수집
        k200 = stock.get_index_portfolio_deposit_file("1028")
        kd150 = stock.get_index_portfolio_deposit_file("2034")
        
        all_tickers = list(set(k200 + kd150)) # 중복 제거
        
        # 야후 파이낸스 형식으로 변환
        formatted = []
        for t in all_tickers:
            # 코스피/코스닥 구분 (pykrx의 구체적인 시장 구분 함수 사용)
            market = stock.get_market_ticker_list(market="KOSPI")
            suffix = ".KS" if t in market else ".KQ"
            formatted.append(f"{t}{suffix}")
        
        print(f"✅ 실시간 수집 성공: {len(formatted)} 종목")
        return formatted

    except Exception as e:
        print(f"⚠️ 실시간 수집 실패({e}). 백업 우량주 리스트를 사용합니다.")
        # 실패 시 사용할 핵심 우량주 500선 예시 (일부 요약)
        backup_tickers = [
    # --- 코스피 대형주 (KOSPI 200 중심) ---
    "005930.KS", "000660.KS", "005380.KS", "000270.KS", "035420.KS", "005490.KS", "051910.KS", "006400.KS", 
    "105560.KS", "068270.KS", "035720.KS", "012330.KS", "028260.KS", "000810.KS", "055550.KS", "011780.KS", 
    "032830.KS", "003550.KS", "033780.KS", "000100.KS", "009150.KS", "010130.KS", "018260.KS", "010140.KS", 
    "086790.KS", "003670.KS", "017670.KS", "011070.KS", "010950.KS", "009540.KS", "030200.KS", "034220.KS",
    "011170.KS", "005830.KS", "004020.KS", "036570.KS", "000720.KS", "009830.KS", "024110.KS", "034020.KS",
    "029780.KS", "008770.KS", "002790.KS", "012450.KS", "005940.KS", "071050.KS", "267250.KS", "016360.KS",
    "004990.KS", "000210.KS", "011210.KS", "001040.KS", "078930.KS", "001450.KS", "006800.KS", "005385.KS",
    "000080.KS", "007070.KS", "014680.KS", "035250.KS", "001230.KS", "011790.KS", "271560.KS", "004800.KS",
    
    # --- 코스닥 대형주 (KOSDAQ 150 및 핵심 반도체/2차전지) ---
    "458870.KQ", "086520.KQ", "247540.KQ", "091990.KQ", "066970.KQ", "293490.KQ", "058470.KQ", "278280.KQ", 
    "035900.KQ", "067310.KQ", "112040.KQ", "034230.KQ", "041510.KQ", "028300.KQ", "036930.KQ", "064550.KQ", 
    "214150.KQ", "039030.KQ", "078600.KQ", "042700.KQ", "145020.KQ", "086280.KQ", "036830.KQ", "178920.KQ",
    "060250.KQ", "048410.KQ", "054090.KQ", "036490.KQ", "025900.KQ", "000250.KQ", "084370.KQ", "036200.KQ",
    "051900.KQ", "095700.KQ", "063170.KQ", "035600.KQ", "046890.KQ", "053030.KQ", "086900.KQ", "121600.KQ",
    "253450.KQ", "065680.KQ", "032190.KQ", "098460.KQ", "051370.KQ", "033640.KQ", "089030.KQ", "038500.KQ",
    "043060.KQ", "033530.KQ", "214450.KQ", "290670.KQ", "042000.KQ", "005290.KQ", "131970.KQ", "065350.KQ",
    
    # --- 주요 섹터별 테마주 및 중형주 (분석 가치가 높은 종목들) ---
    "001440.KS", "003090.KS", "011000.KS", "006260.KS", "000670.KS", "001740.KS", "001500.KS", "004170.KS",
    "005180.KS", "000990.KS", "003410.KS", "003490.KS", "005250.KS", "009420.KS", "010060.KS", "010620.KS",
    "011760.KS", "012750.KS", "015760.KS", "020150.KS", "021240.KS", "023530.KS", "028050.KS", "028670.KS",
    "032640.KS", "034730.KS", "036460.KS", "042660.KS", "047040.KS", "047810.KS", "051600.KS", "052690.KS",
    "069500.KS", "069620.KS", "071090.KS", "071840.KS", "078350.KS", "079160.KS", "081660.KS", "086280.KS",
    "088350.KS", "090430.KS", "092230.KS", "093050.KS", "096770.KS", "097950.KS", "103140.KS", "111770.KS",
    "120110.KS", "128940.KS", "137310.KS", "138040.KS", "138930.KS", "139130.KS", "139480.KS", "161390.KS",
    "161890.KS", "175330.KS", "180640.KS", "185750.KS", "192080.KS", "192820.KS", "204320.KS", "207940.KS",
    "214320.KS", "251270.KS", "267250.KS", "271560.KS", "272210.KS", "282330.KS", "285130.KS", "294630.KS",
    "298000.KS", "298020.KS", "298040.KS", "298050.KS", "302440.KS", "316140.KS", "326030.KS", "329180.KS",
    "336260.KS", "336330.KS", "352820.KS", "361610.KS", "373220.KS", "375500.KS", "377300.KS", "381970.KS",
    "383220.KS", "402340.KS", "448300.KS", "450080.KS"
    ]
        return backup_tickers

def get_investor_data(ticker_list, days=5):
    """최근 n거래일간의 외인/기관 순매수 합계를 가져옴"""
    print(f"📊 최근 {days}거래일 수급 데이터 수집 중...")
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=10)).strftime("%Y%m%d") # 여유있게 설정
    
    investor_results = {}
    for full_ticker in ticker_list:
        ticker = full_ticker.split('.')[0]
        try:
            # 기간 내 투자자별 순매수량 수집
            df = stock.get_market_net_purchase_of_equities_by_ticker(start_date, end_date, ticker)
            # 최근 n일치 합산 (데이터가 있을 경우)
            if not df.empty:
                # '전체' 행이 아닌 개별 날짜 데이터를 합산해야 함
                foreign_net = df['외국인'].tail(days).sum()
                inst_net = df['기관합계'].tail(days).sum()
                investor_results[ticker] = {
                    "외인순매수": int(foreign_net),
                    "기관순매수": int(inst_net),
                    "수급합계": int(foreign_net + inst_net)
                }
        except:
            investor_results[ticker] = {"외인순매수": 0, "기관순매수": 0, "수급합계": 0}
            
    return investor_results

def get_naver_supply(ticker):
    """네이버 금융에서 해당 종목의 최신 수급(외인/기관) 1일치를 긁어옴"""
    url = f"https://finance.naver.com/item/frgn.naver?code={ticker}"
    try:
        # 네이버 금융 페이지의 테이블 중 3번째(인덱스 2)가 수급 테이블임
        # 헤더가 중복되거나 빈 행이 있을 수 있어 처리가 필요함
        tables = pd.read_html(url, encoding='euc-kr')
        df = tables[2]
        
        # 유효한 데이터만 필터링 (날짜가 있는 행만)
        df = df.dropna(subset=['날짜'])
        if df.empty:
            return 0, 0
        
        # 가장 최근일(첫 번째 행)의 외인 순매매량과 기관 순매매량 추출
        # 네이버 테이블 구조상 '외국인'과 '기관' 컬럼의 순매매량 위치 확인
        foreign_net = df.iloc[0]['외국인.1'] 
        inst_net = df.iloc[0]['기관.1']
        
        return int(foreign_net), int(inst_net)
    except Exception as e:
        # print(f"⚠️ {ticker} 수급 수집 실패: {e}")
        return 0, 0

def get_quant_analysis():
    print("🔍 CCI, MFI 포함 정밀 분석 시작...")
    
    tickers = get_ticker_list()    
    results = []

    # 2. 수급 데이터 미리 수집
    # investor_map = get_investor_data(tickers, days=5)
    
    for raw_ticker in tickers:
        try:
            clean_ticker = raw_ticker.split('.')[0]
            symbol = f"{clean_ticker}.KS" if int(clean_ticker) < 900000 else f"{clean_ticker}.KQ"
            
            # MFI와 CCI 계산을 위해 고가(High), 저가(Low), 거래량(Volume)이 추가로 필요함
            df = yf.download(symbol, period="3mo", progress=False)
            
            if df.empty or len(df) < 20:
                continue

            # 데이터 추출 (Single/Multi 인덱스 대응)
            close = df['Close'].squeeze()
            high = df['High'].squeeze()
            low = df['Low'].squeeze()
            volume = df['Volume'].squeeze()

            # 1. RSI 계산 (기존 유지)
            delta = close.diff()
            up = delta.clip(lower=0).rolling(window=14).mean()
            down = -delta.clip(upper=0).rolling(window=14).mean()
            rsi = (100 - (100 / (1 + (up / down)))).iloc[-1]

            # 2. CCI 계산 (기초 자산의 가격 수준이 평균에서 얼마나 떨어져 있는가)
            tp = (high + low + close) / 3
            ma = tp.rolling(window=20).mean()
            mad = tp.rolling(window=20).apply(lambda x: np.abs(x - x.mean()).mean())
            cci = ((tp - ma) / (0.015 * mad)).iloc[-1]

            # 3. MFI 계산 (RSI에 거래량을 가중치로 준 지표)
            typical_price = (high + low + close) / 3
            money_flow = typical_price * volume
            positive_flow = (money_flow.where(typical_price > typical_price.shift(1), 0)).rolling(window=14).sum()
            negative_flow = (money_flow.where(typical_price < typical_price.shift(1), 0)).rolling(window=14).sum()
            mfr = positive_flow / negative_flow
            mfi = (100 - (100 / (1 + mfr))).iloc[-1]

            # 종합 점수 계산 (각 지표의 역발상 점수 평균)
            # RSI/MFI는 0~100 (낮을수록 저점), CCI는 보통 -100~+100 (낮을수록 저점)
            rsi_score = 100 - rsi
            mfi_score = 100 - mfi
            cci_score = ((-cci + 200) / 4) # -200~200 범위를 0~100 점수로 환산
            
            total_score = (rsi_score + mfi_score + cci_score) / 3

            # 3. 수급 데이터 매칭
            # supply = investor_map.get(clean_ticker, {"외인순매수": 0, "기관순매수": 0, "수급합계": 0})
            # 2. 네이버 금융 수급 데이터 가져오기
            f_net, i_net = get_naver_supply(clean_ticker)
            
            results.append({
                "티커": clean_ticker,
                "현재가": int(close.iloc[-1]),
                "RSI": round(float(rsi), 2),
                "MFI": round(float(mfi), 2),
                "CCI": round(float(cci), 2),
                "외인순매수": f_net,
                "기관순매수": i_net,
                "수급합계": f_net + i_net,
                "종합점수": round(float(total_score), 2)
            })
            print(f"✅ {symbol} 분석 완료 (수급: {f_net + i_net})")
            
            # 네이버 서버 부하 방지를 위한 미세한 지연 (선택사항)
            time.sleep(0.1)
        except Exception as e:
            print(f"⚠️ {raw_ticker} 건너뜀: {e}")
            continue

    return pd.DataFrame(results)

if __name__ == "__main__":
    report = get_quant_analysis()
    if not report.empty:
        # 종합점수 높은 순으로 정렬해서 저장
        report = report.sort_values(by="종합점수", ascending=False)
        report.to_csv("daily_quant_report.csv", index=False, encoding='utf-8-sig')
        print("✅ 강화된 리포트 생성 완료")
