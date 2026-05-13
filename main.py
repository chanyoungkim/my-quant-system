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
        # 테스트용 기본 리스트 (축약)
        tickers = ["005930.KS", "000660.KS", "000100.KS", "012750.KS"]
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
