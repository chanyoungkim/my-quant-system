import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def get_ticker_list():
    """야후 파이낸스 안정성이 검증된 KOSPI 200 및 KOSDAQ 우량주 총 300여 개 마스터 리스트"""
    print("📡 퀀트 분석 대상 대형주 300개 리스트 로드 중...")
    backup_tickers = [
        # === 코스피 대형주 및 주요 기업 (KOSPI 200 중심) ===
        "005930.KS", "000660.KS", "005380.KS", "000270.KS", "035420.KS", "005490.KS", "051910.KS", "006400.KS", 
        "105560.KS", "068270.KS", "035720.KS", "012330.KS", "028260.KS", "000810.KS", "055550.KS", "011780.KS", 
        "032830.KS", "003550.KS", "033780.KS", "000100.KS", "009150.KS", "010130.KS", "018260.KS", "010140.KS", 
        "086790.KS", "003670.KS", "017670.KS", "011070.KS", "010950.KS", "009540.KS", "030200.KS", "034220.KS",
        "011170.KS", "005830.KS", "004020.KS", "036570.KS", "000720.KS", "009830.KS", "024110.KS", "034020.KS",
        "029780.KS", "008770.KS", "002790.KS", "012450.KS", "005940.KS", "071050.KS", "267250.KS", "016360.KS",
        "001440.KS", "003090.KS", "011000.KS", "006260.KS", "000670.KS", "001740.KS", "001500.KS", "004170.KS",
        "005180.KS", "000990.KS", "003410.KS", "003490.KS", "005250.KS", "009420.KS", "010060.KS", "010620.KS",
        "011760.KS", "012750.KS", "015760.KS", "020150.KS", "021240.KS", "023530.KS", "028050.KS", "028670.KS",
        "032640.KS", "034730.KS", "036460.KS", "042660.KS", "047040.KS", "047810.KS", "051600.KS", "052690.KS",
        "069500.KS", "069620.KS", "071090.KS", "071840.KS", "078350.KS", "079160.KS", "081660.KS", "088350.KS",
        "120110.KS", "128940.KS", "137310.KS", "138040.KS", "138930.KS", "139130.KS", "139480.KS", "161390.KS",
        "161890.KS", "175330.KS", "180640.KS", "185750.KS", "192080.KS", "214320.KS", "271560.KS", "272210.KS",
        "282330.KS", "294630.KS", "298000.KS", "298020.KS", "298040.KS", "298050.KS", "302440.KS", "316140.KS",
        "326030.KS", "329180.KS", "336260.KS", "336330.KS", "352820.KS", "361610.KS", "373220.KS", "375500.KS",
        "377300.KS", "381970.KS", "383220.KS", "450080.KS", "005385.KS", "000080.KS", "007070.KS", "014680.KS",
        "035250.KS", "001230.KS", "011790.KS", "004800.KS", "000120.KS", "011210.KS", "000880.KS", "001800.KS",
        "005440.KS", "004370.KS", "005850.KS", "005935.KS", "003230.KS", "000210.KS", "010120.KS", "001040.KS",
        "004000.KS", "006360.KS", "000995.KS", "000725.KS", "001450.KS", "000060.KS", "000815.KS", "011075.KS",
        "007310.KS", "002380.KS", "003480.KS", "009240.KS", "014820.KS", "001240.KS", "000240.KS", "017800.KS",
        "023590.KS", "036530.KS", "051900.KS", "064350.KS", "069730.KS", "071970.KS", "084670.KS", "086280.KS",

        # === 코스닥 주요 우량주 및 기술주 (KOSDAQ 150 중심) ===
        "458870.KQ", "086520.KQ", "247540.KQ", "091990.KQ", "066970.KQ", "293490.KQ", "058470.KQ", "278280.KQ", 
        "035900.KQ", "067310.KQ", "112040.KQ", "034230.KQ", "041510.KQ", "028300.KQ", "036930.KQ", "064550.KQ", 
        "214150.KQ", "039030.KQ", "078600.KQ", "042700.KQ", "145020.KQ", "086280.KQ", "036830.KQ", "178920.KQ",
        "060250.KQ", "048410.KQ", "054090.KQ", "036490.KQ", "025900.KQ", "000250.KQ", "084370.KQ", "036200.KQ",
        "051900.KQ", "095700.KQ", "063170.KQ", "035600.KQ", "046890.KQ", "053030.KQ", "086900.KQ", "121600.KQ",
        "253450.KQ", "065680.KQ", "032190.KQ", "098460.KQ", "051370.KQ", "033640.KQ", "089030.KQ", "038500.KQ",
        "043060.KQ", "033530.KQ", "214450.KQ", "290670.KQ", "042000.KQ", "005290.KQ", "131970.KQ", "065350.KQ",
        "192820.KQ", "207940.KQ", "402340.KQ", "448300.KQ", "294630.KQ", "036490.KQ", "141080.KQ", "196170.KQ",
        "022100.KQ", "068760.KQ", "031390.KQ", "108320.KQ", "131290.KQ", "036810.KQ", "213420.KQ", "039200.KQ",
        "215600.KQ", "069080.KQ", "041960.KQ", "054630.KQ", "036540.KQ", "096530.KQ", "060720.KQ", "088800.KQ",
        "058820.KQ", "036120.KQ", "091700.KQ", "290110.KQ", "178320.KQ", "035760.KQ", "048530.KQ", "230360.KQ",
        "036670.KQ", "053800.KQ", "065150.KQ", "083790.KQ", "092040.KQ", "102940.KQ", "122450.KQ", "122870.KQ",
        "134580.KQ", "160550.KQ", "187420.KQ", "200130.KQ", "222080.KQ", "235980.KQ", "256150.KQ", "263750.KQ",
        "270870.KQ", "287410.KQ", "290510.KQ", "319660.KQ", "357780.KQ", "365550.KQ", "368200.KQ", "388720.KQ",
        "393890.KQ", "417970.KQ", "434100.KQ", "452150.KQ", "465650.KQ"
    ]
    # 중복 티커 거부 후 안전 반환
    return list(set(backup_tickers))

def get_quant_analysis():
    print("🔍 대형주 300선 대상 기술 지표 및 야후 거래량 추정 수급 정밀 스캔 가동...")
    
    tickers = get_ticker_list()    
    results = []

    for symbol in tickers:
        try:
            clean_ticker = symbol.split('.')[0]
            
            # 주가 및 거래량 데이터 다운로드 (최근 3개월)
            df = yf.download(symbol, period="3mo", progress=False)
            
            if df.empty or len(df) < 20:
                continue

            # MultiIndex 혹은 단일 인덱스 상관없이 강제 Squeeze 처리
            close = df['Close'].squeeze()
            high = df['High'].squeeze()
            low = df['Low'].squeeze()
            volume = df['Volume'].squeeze()

            # 1. RSI 계산
            delta = close.diff()
            up = delta.clip(lower=0).rolling(window=14).mean()
            down = -delta.clip(upper=0).rolling(window=14).mean()
            rsi = (100 - (100 / (1 + (up / down)))).iloc[-1]

            # 2. CCI 계산
            tp = (high + low + close) / 3
            ma = tp.rolling(window=20).mean()
            mad = tp.rolling(window=20).apply(lambda x: np.abs(x - x.mean()).mean())
            cci = ((tp - ma) / (0.015 * mad)).iloc[-1]

            # 3. MFI 계산
            typical_price = (high + low + close) / 3
            money_flow = typical_price * volume
            positive_flow = (money_flow.where(typical_price > typical_price.shift(1), 0)).rolling(window=14).sum()
            negative_flow = (money_flow.where(typical_price < typical_price.shift(1), 0)).rolling(window=14).sum()
            mfr = positive_flow / negative_flow
            mfi = (100 - (100 / (1 + mfr))).iloc[-1]

            # 4. [대안 A] 야후 거래량 기반 최근 5거래일 추정 자금 순유입량 계산
            price_direction = np.sign(close.diff())
            volume_flow = price_direction * volume
            recent_5d_flow = volume_flow.tail(5).sum()
            est_net_purchase = round(float(recent_5d_flow) / 10000, 1)

            # 역발상 종합 점수 계산 (지표가 극단 바닥일수록 높은 점수)
            rsi_score = 100 - rsi
            mfi_score = 100 - mfi
            cci_score = ((-cci + 200) / 4)
            total_score = (rsi_score + mfi_score + cci_score) / 3

            results.append({
                "티커": clean_ticker,
                "현재가": int(close.iloc[-1]),
                "RSI": round(float(rsi), 2),
                "MFI": round(float(mfi), 2),
                "CCI": round(float(cci), 2),
                "추정수급(5일,만주)": est_net_purchase,
                "종합점수": round(float(total_score), 2)
            })
            
        except Exception as e:
            # 수집 중 에러가 나는 개별 종목은 스킵하고 안정적으로 전진
            continue

    return pd.DataFrame(results)

if __name__ == "__main__":
    report = get_quant_analysis()
    if not report.empty:
        # 역발상 기회가 높은(종합점수가 높은) 순서대로 배치
        report = report.sort_values(by="종합점수", ascending=False)
        report.to_csv("daily_quant_report.csv", index=False, encoding='utf-8-sig')
        print(f"📊 [성공] 총 {len(report)}개 종목 분석 완료! 거래량 추정 수급 리포트가 정상 생성되었습니다.")
