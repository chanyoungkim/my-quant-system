import datetime
import os
from datetime import timedelta
import numpy as np
import pandas as pd
import yfinance as yf


def get_ticker_list():
    """야후 파이낸스 안정성이 검증된 KOSPI 200, KOSDAQ 150 전종목 및 거래대금 우량주 총 500여 개 마스터 리스트"""
    print("📡 📡 퀀트 분석 대상 대형주/우량주 500개 확충 리스트 로드 중...")
    backup_tickers = [
        # === [코스피 대형주 및 주요 우량 기업] ===
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
        "161890.KS", "175330.KS", "185750.KS", "192080.KS", "214320.KS", "271560.KS", "272210.KS", "282330.KS",
        "294630.KS", "298000.KS", "298020.KS", "298040.KS", "298050.KS", "302440.KS", "316140.KS", "326030.KS",
        "329180.KS", "336260.KS", "352820.KS", "361610.KS", "373220.KS", "375500.KS", "377300.KS", "381970.KS",
        "383220.KS", "450080.KS", "005385.KS", "000080.KS", "007070.KS", "014680.KS", "035250.KS", "001230.KS",
        "011790.KS", "004800.KS", "000120.KS", "011210.KS", "000880.KS", "001800.KS", "005440.KS", "004370.KS",
        "005850.KS", "005935.KS", "003230.KS", "000210.KS", "010120.KS", "001040.KS", "004000.KS", "006360.KS",
        "000725.KS", "001450.KS", "000815.KS", "007310.KS", "002380.KS", "003480.KS", "009240.KS", "014820.KS",
        "000240.KS", "017800.KS", "023590.KS", "036530.KS", "051900.KS", "064350.KS", "069730.KS", "071970.KS",
        "084670.KS", "086280.KS", "001120.KS", "001210.KS", "004990.KS", "005800.KS", "006800.KS", "007570.KS",
        "009450.KS", "010780.KS", "011200.KS", "011750.KS", "012630.KS", "014830.KS", "019170.KS", "028070.KS",
        "033240.KQ", "060980.KS", "069260.KS", "071320.KS", "073240.KS", "079550.KS", "084010.KS", "090430.KS",
        "093370.KS", "096770.KS", "103140.KS", "114070.KS", "115390.KS", "134380.KS", "145990.KS", "181710.KS",
        "204320.KS", "241560.KS", "265520.KS", "285130.KS", "307950.KS", "339770.KS", "378850.KS", "403340.KS",
        "000070.KS", "000150.KS", "000220.KS", "000300.KS", "000320.KS", "000640.KS", "000990.KS", "001060.KS",
        "001390.KS", "001430.KS", "001680.KS", "001720.KS", "001770.KS", "001820.KS", "001940.KS", "002020.KS",
        "002240.KS", "002350.KS", "002390.KS", "002410.KS", "002960.KS", "003000.KS", "003030.KS", "003240.KS",
        "003300.KS", "003470.KS", "003520.KS", "003540.KS", "003620.KS", "003850.KS", "003920.KS", "004360.KS",

        # === [코스닥 주요 우량주 및 기술 성장주] ===
        "458870.KQ", "086520.KQ", "247540.KQ", "091990.KQ", "066970.KQ", "293490.KQ", "058470.KQ", "278280.KQ",
        "035900.KQ", "067310.KQ", "112040.KQ", "034230.KQ", "041510.KQ", "028300.KQ", "036930.KQ", "064550.KQ",
        "214150.KQ", "039030.KQ", "078600.KQ", "042700.KQ", "145020.KQ", "086280.KQ", "036830.KQ", "178920.KQ",
        "060250.KQ", "048410.KQ", "054090.KQ", "036490.KQ", "025900.KQ", "000250.KQ", "084370.KQ", "036200.KQ",
        "051900.KQ", "095700.KQ", "063170.KQ", "035600.KQ", "046890.KQ", "053030.KQ", "086900.KQ", "121600.KQ",
        "253450.KQ", "065680.KQ", "032190.KQ", "098460.KQ", "051370.KQ", "033640.KQ", "089030.KQ", "038500.KQ",
        "043060.KQ", "033530.KQ", "214450.KQ", "290670.KQ", "042000.KQ", "005290.KQ", "131970.KQ", "065350.KQ",
        "192820.KQ", "207940.KQ", "402340.KQ", "448300.KQ", "294630.KQ", "141080.KQ", "196170.KQ", "022100.KQ",
        "068760.KQ", "031390.KQ", "108320.KQ", "131290.KQ", "036810.KQ", "213420.KQ", "039200.KQ", "215600.KQ",
        "069080.KQ", "041960.KQ", "054630.KQ", "036540.KQ", "096530.KQ", "060720.KQ", "088800.KQ", "058820.KQ",
        "036120.KQ", "091700.KQ", "290110.KQ", "178320.KQ", "035760.KQ", "048530.KQ", "230360.KQ", "036670.KQ",
        "053800.KQ", "065150.KQ", "083790.KQ", "092040.KQ", "102940.KQ", "122450.KQ", "122870.KQ", "134580.KQ",
        "160550.KQ", "187420.KQ", "200130.KQ", "222080.KQ", "235980.KQ", "256150.KQ", "263750.KQ", "270870.KQ",
        "287410.KQ", "290510.KQ", "319660.KQ", "357780.KQ", "365550.KQ", "368200.KQ", "388720.KQ", "393890.KQ",
        "417970.KQ", "434100.KQ", "452150.KQ", "465650.KQ", "007390.KQ", "012600.KQ", "013120.KQ", "014570.KQ",
        "016100.KQ", "017390.KQ", "018700.KQ", "023160.KQ", "024840.KQ", "024880.KQ", "024900.KQ", "025880.KQ",
        "027710.KQ", "030520.KQ", "030530.KQ", "032500.KQ", "032580.KQ", "032860.KQ", "033250.KQ", "033270.KQ",
        "033320.KQ", "034040.KQ", "034120.KQ", "034810.KQ", "035080.KQ", "035150.KQ", "035460.KQ", "035810.KQ",
        "036080.KQ", "036260.KQ", "036560.KQ", "036710.KQ", "037350.KQ", "037460.KQ", "037760.KQ", "038060.KQ",
        "038110.KQ", "038340.KQ", "038950.KQ", "039240.KQ", "039340.KQ", "039440.KQ", "039560.KQ", "039740.KQ",
        "039840.KQ", "039860.KQ", "040130.KQ", "040160.KQ", "040300.KQ", "040420.KQ", "040610.KQ", "040880.KQ",
        "040910.KQ", "041020.KQ", "041190.KQ", "041440.KQ", "041850.KQ", "042120.KQ", "042520.KQ", "043100.KQ",
        "043200.KQ", "043260.KQ", "043510.KQ", "043590.KQ", "044060.KQ", "044380.KQ", "044480.KQ", "044780.KQ",
        "044990.KQ", "045100.KQ", "045390.KQ", "045510.KQ", "045520.KQ", "046070.KQ", "046120.KQ", "046140.KQ",
        "046250.KQ", "046310.KQ", "046390.KQ", "046440.KQ", "046940.KQ", "047310.KQ", "047560.KQ", "048260.KQ",
        "048550.KQ", "048750.KQ", "049080.KQ", "049120.KQ", "049430.KQ", "049470.KQ", "049480.KQ", "049520.KQ",
        "049720.KQ", "049830.KQ", "049950.KQ", "050110.KQ", "050120.KQ", "050540.KQ", "050760.KQ", "050960.KQ",
        "051160.KQ", "051490.KQ", "051500.KQ", "051780.KQ", "052020.KQ", "052190.KQ", "052220.KQ", "052260.KQ",
        "052300.KQ", "052400.KQ", "052420.KQ", "052460.KQ", "052600.KQ", "052860.KQ", "053050.KQ", "053060.KQ",
        "053210.KQ", "053260.KQ", "053290.KQ", "053300.KQ", "053350.KQ", "053450.KQ", "053580.KQ", "053610.KQ"
    ]
    return list(set(backup_tickers))


def get_quant_analysis():
    print("🔍 500대 종목 대상 기술 지표 및 거래량/수급 턴어라운드 정밀 스캔 가동...")
    tickers = get_ticker_list()
    results = []

    for symbol in tickers:
        try:
            clean_ticker = symbol.split(".")[0]

            # 주가 및 거래량 데이터 다운로드 (최근 3개월)
            df = yf.download(symbol, period="3mo", progress=False)

            if df.empty or len(df) < 20:
                continue

            # MultiIndex 혹은 단일 인덱스 상관없이 강제 Squeeze 처리
            close = df["Close"].squeeze()
            high = df["High"].squeeze()
            low = df["Low"].squeeze()
            volume = df["Volume"].squeeze()

            if close.isnull().all() or high.isnull().all() or low.isnull().all():
                continue

            # === 거래량 관련 지표 계산 ===
            current_close = float(close.iloc[-1])
            current_volume = float(volume.iloc[-1])

            # 최근 5일 평균 거래량 계산
            avg_volume_5d = float(volume.iloc[-5:].mean())

            # 지표 1: 5일 평균 대비 거래량 비율 (%)
            volume_ratio_5d = (current_volume / avg_volume_5d) * 100 if avg_volume_5d > 0 else 0

            # 지표 2: 당일 거래대금 (단위: 억 원)
            trading_value_krw = (current_close * current_volume) / 100_000_000

            # 1. RSI 계산
            delta = close.diff()
            up = delta.clip(lower=0).rolling(window=14).mean()
            down = -delta.clip(upper=0).rolling(window=14).mean()

            roll_up = up.iloc[-1]
            roll_down = down.iloc[-1]
            if roll_down == 0:
                rsi = 100 if roll_up > 0 else 50
            else:
                rsi = 100 - (100 / (1 + (roll_up / roll_down)))

            # 2. CCI 계산
            tp = (high + low + close) / 3
            ma = tp.rolling(window=20).mean()
            mad = tp.rolling(window=20).apply(lambda x: np.abs(x - x.mean()).mean())

            if mad.iloc[-1] == 0:
                cci = 0
            else:
                cci = ((tp - ma) / (0.015 * mad)).iloc[-1]

            # 3. MFI 계산
            typical_price = (high + low + close) / 3
            money_flow = typical_price * volume
            positive_flow = (money_flow.where(typical_price > typical_price.shift(1), 0)).rolling(window=14).sum()
            negative_flow = (money_flow.where(typical_price < typical_price.shift(1), 0)).rolling(window=14).sum()

            pos_f = positive_flow.iloc[-1]
            neg_f = negative_flow.iloc[-1]
            if neg_f == 0:
                mfi = 100 if pos_f > 0 else 50
            else:
                mfr = pos_f / neg_f
                mfi = 100 - (100 / (1 + mfr))

            # 4. 최근 5거래일 추정 자금 순유입량 계산
            price_direction = np.sign(close.diff())
            volume_flow = price_direction * volume
            recent_5d_flow = volume_flow.tail(5).sum()
            est_net_purchase = round(float(recent_5d_flow) / 10000, 1)

            # 역발상 종합 점수 계산 (지표가 극단 바닥일수록 높은 점수)
            rsi_score = 100 - rsi
            mfi_score = 100 - mfi
            cci_score = (-cci + 200) / 4
            total_score = (rsi_score + mfi_score + cci_score) / 3

            if np.isnan(rsi) or np.isnan(mfi) or np.isnan(cci) or np.isnan(total_score):
                continue

            results.append({
                "티커": clean_ticker,
                "현재가": int(current_close),
                "RSI": round(float(rsi), 2),
                "MFI": round(float(mfi), 2),
                "CCI": round(float(cci), 2),
                "추정수급(5일,만주)": est_net_purchase,
                "거래량비율(5일평균대비)": round(volume_ratio_5d, 2),
                "당일거래대금(억)": round(trading_value_krw, 2),
                "종합점수": round(float(total_score), 2)
            })

        except Exception as e:
            continue

    if not results:
        return pd.DataFrame()

    final_df = pd.DataFrame(results)
    final_df = final_df.dropna(subset=["RSI", "MFI", "CCI", "거래량비율(5일평균대비)", "종합점수"])
    return final_df


if __name__ == "__main__":
    report = get_quant_analysis()
    if not report.empty:
        report = report.sort_values(by="종합점수", ascending=False)
        report.to_csv("daily_quant_report.csv", index=False, encoding="utf-8-sig")
        print(f"📊 [성공] 총 {len(report)}개 종목 분석 완료! 500선 수급 리포트가 정상 생성되었습니다.")