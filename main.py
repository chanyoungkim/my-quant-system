import yfinance as yf
import pandas as pd
import numpy as np  # 추가
from datetime import datetime, timedelta
import os

def get_quant_analysis():
    print("🔍 CCI, MFI 포함 정밀 분석 시작...")
    
    # tickers.txt 경로 및 로드 (기존 로직 유지)
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "tickers.txt")
    
    if not os.path.exists(file_path):
             tickers = [
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
    else:
        with open(file_path, "r") as f:
            tickers = [line.strip() for line in f.readlines() if line.strip()]

    results = []
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

            results.append({
                "티커": clean_ticker,
                "현재가": int(close.iloc[-1]),
                "RSI": round(float(rsi), 2),
                "MFI": round(float(mfi), 2),
                "CCI": round(float(cci), 2),
                "종합점수": round(float(total_score), 2)
            })
            print(f"✅ {symbol} 분석 완료")
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
