"""HLCrossSigForWPR — converted from MQL5: MQL5 Indicators/HLCrossSigForWPR_HTF/HLCrossSigForWPR.mq5

Copyright: Copyright © 2008, Bigeev Rustem; Link: http://www.parch.ru/; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Bigeev Rustem', 'link': 'http://www.parch.ru/', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [255], 2: [65280], 3: [16711935], 4: [16776960], 5: [16711935], 6: [16776960], 7: [255], 8: [65280]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2, 5: 1, 6: 1, 7: 3, 8: 3}, 'styles': {}, 'labels': {1: 'Sell Stop', 2: 'Buy Stop', 3: 'Sell TakeProfit', 4: 'Buy TakeProfit', 5: 'Sell Signal', 6: 'Buy Signal', 7: 'Sell Input', 8: 'Buy Input'}, 'levels': [], 'description': [], 'name': 'HLCrossSigForWPR', 'source': 'MQL5 Indicators/HLCrossSigForWPR_HTF/HLCrossSigForWPR.mq5', 'folder': 'HLCrossSigForWPR_HTF', 'inputs': [{'mql': 'Supr_Period', 'py': 'Supr_Period', 'param': 'Supr_Period', 'type': 'int', 'default': 6, 'label': 'Период пробиваемого диапазона, чем больше значение, тем более поздние сигналы и реже', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 21, 'label': 'Период для Heiken Ashi variable. Служит в качестве доп. фильтра', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'int', 'default': 0, 'label': 'Максимальный риск в пипсах для расчета уровня входа исходя из уровня ближайшего MAX/MIN', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 120, 'label': 'Период АТR. Служит для расчета уровня волатильности.', 'sinput': False}, {'mql': 'Q', 'py': 'Q', 'param': 'Q', 'type': 'double', 'default': 0.7, 'label': 'Параметр для постановки Тейка. - Доля от размера Стопа. если =1, Тейк = Стопу', 'sinput': False}, {'mql': 'WPR_Period', 'py': 'WPR_Period', 'param': 'WPR_Period', 'type': 'int', 'default': 12, 'label': 'Период WPR. Служит в качестве доп. фильтра', 'sinput': False}, {'mql': 'HLine', 'py': 'HLine', 'param': 'HLine', 'type': 'int', 'default': -38, 'label': 'Верхняя сигнальная линия стопов для WPR', 'sinput': False}, {'mql': 'LLine', 'py': 'LLine', 'param': 'LLine', 'type': 'int', 'default': -62, 'label': 'Нижняя сигнальная линия стопов для WPR', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Supr_Period = _input('Supr_Period', 6)  # Период пробиваемого диапазона, чем больше значение, тем более поздние сигналы и реже
MA_Period = _input('MA_Period', 21)  # Период для Heiken Ashi variable. Служит в качестве доп. фильтра
Risk = _input('Risk', 0)  # Максимальный риск в пипсах для расчета уровня входа исходя из уровня ближайшего MAX/MIN
ATR_Period = _input('ATR_Period', 120)  # Период АТR. Служит для расчета уровня волатильности.
Q = _input('Q', 0.7)  # Параметр для постановки Тейка. - Доля от размера Стопа. если =1, Тейк = Стопу
WPR_Period = _input('WPR_Period', 12)  # Период WPR. Служит в качестве доп. фильтра
HLine = _input('HLine', -38)  # Верхняя сигнальная линия стопов для WPR
LLine = _input('LLine', -62)  # Нижняя сигнальная линия стопов для WPR
Sell = Arr(0, 0.0)
Buy = Arr(0, 0.0)
SellStop = Arr(0, 0.0)
BuyStop = Arr(0, 0.0)
SellTake = Arr(0, 0.0)
BuyTake = Arr(0, 0.0)
SellInput = Arr(0, 0.0)
BuyInput = Arr(0, 0.0)
PointRisk = 0.0
PointRisk10 = 0.0
min_rates_total = 0
WPR_Handle = 0
ATR_Handle = 0
MA_Handle = 0
MA1_Handle = 0

def OnInit():
    global ATR_Handle, MA1_Handle, MA_Handle, PointRisk, PointRisk10, WPR_Handle, min_rates_total
    min_rates_total = MathMax(MA_Period, MathMax(WPR_Period, MathMax(ATR_Period, Supr_Period + 1)))
    PointRisk = Risk * Point()
    PointRisk10 = 10 * PointRisk
    MA_Handle = iMA(None, 0, MA_Period, 0, MODE_SMA, PRICE_MEDIAN)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора MA')
    MA1_Handle = iMA(None, 0, 1, 0, MODE_SMA, PRICE_MEDIAN)
    if MA1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора MA1')
    WPR_Handle = iWPR(None, 0, WPR_Period)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора WPR')
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    SetIndexBuffer(0, SellStop, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(SellStop, True)
    SetIndexBuffer(1, BuyStop, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BuyStop, True)
    SetIndexBuffer(2, SellTake, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 158)
    ArraySetAsSeries(SellTake, True)
    SetIndexBuffer(3, BuyTake, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 158)
    ArraySetAsSeries(BuyTake, True)
    SetIndexBuffer(4, Sell, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 234)
    ArraySetAsSeries(Sell, True)
    SetIndexBuffer(5, Buy, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 233)
    ArraySetAsSeries(Buy, True)
    SetIndexBuffer(6, SellInput, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_ARROW, 177)
    ArraySetAsSeries(SellInput, True)
    SetIndexBuffer(7, BuyInput, INDICATOR_DATA)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_ARROW, 177)
    ArraySetAsSeries(BuyInput, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'HL Cross Signal for WPR')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Flag_
    if (((BarsCalculated(MA_Handle) < rates_total or BarsCalculated(MA1_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or BarsCalculated(WPR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Flag = 0
    WPR = Arr(1, 0.0, dyn=False)
    ATR = Arr(1, 0.0, dyn=False)
    MA = Arr(1, 0.0, dyn=False)
    MA1 = Arr(1, 0.0, dyn=False)
    Lhigh = 0.0
    Llow = 0.0
    Spread = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(spread, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_Flag_ = 0
    else:
        limit = rates_total - prev_calculated
    Flag = _s_OnCalculate_Flag_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_Flag_ = Flag
        SellInput[bar] = 0.0
        SellStop[bar] = SellInput[bar]
        SellTake[bar] = SellStop[bar]
        Sell[bar] = SellTake[bar]
        BuyInput[bar] = 0.0
        BuyStop[bar] = BuyInput[bar]
        BuyTake[bar] = BuyStop[bar]
        Buy[bar] = BuyTake[bar]
        Spread = spread[bar] * Point()
        if CopyBuffer(MA_Handle, 0, bar, 1, MA) <= 0:
            return 0
        if CopyBuffer(MA1_Handle, 0, bar, 1, MA1) <= 0:
            return 0
        if CopyBuffer(WPR_Handle, 0, bar, 1, WPR) <= 0:
            return 0
        if CopyBuffer(ATR_Handle, 0, bar, 1, ATR) <= 0:
            return 0
        Lhigh = high[ArrayMaximum(high, bar + 1, Supr_Period)]
        Llow = low[ArrayMinimum(low, bar + 1, Supr_Period)]
        if Flag <= 0:
            if ((((high[bar] >= Lhigh and close[bar] > MA1[0]) and close[bar] > MA[0]) and high[bar] > MA[0]) and WPR[0] >= HLine) or (close[bar] >= SellStop[bar + 1] and high[bar] > Lhigh):
                Buy[bar] = MathMin(close[bar], Llow + (2 * ATR[0]))
                if Risk != 0 and (Buy[bar] - Llow) > PointRisk:
                    Buy[bar] = Llow + PointRisk10
                if close[bar] < (Llow + PointRisk10):
                    Buy[bar] = close[bar]
                Flag = 1
        if Flag >= 0:
            if ((((low[bar] <= Llow and close[bar] < MA1[0]) and close[bar] < MA[0]) and low[bar] < MA[0]) and WPR[0] <= LLine) or (close[bar] <= BuyStop[bar + 1] and low[bar] < Llow):
                Sell[bar] = MathMax(close[bar], Lhigh - (2 * ATR[0]))
                if Risk != 0 and (Lhigh - Sell[bar]) > PointRisk:
                    Sell[bar] = Lhigh - PointRisk10
                if close[bar] > (Lhigh - PointRisk10):
                    Sell[bar] = close[bar]
                Flag = -1
        if Flag > 0:
            BuyStop[bar] = Llow - (Spread * 2)
            BuyTake[bar] = Lhigh + (Spread * 3)
            if BuyStop[bar] < BuyStop[bar + 1] and (not SellStop[bar + 1]):
                BuyStop[bar] = BuyStop[bar + 1]
            if BuyTake[bar] < BuyTake[bar + 1] and (not SellTake[bar + 1]):
                BuyTake[bar] = BuyTake[bar + 1]
        if Flag < 0:
            SellStop[bar] = Lhigh + (Spread * 3)
            SellTake[bar] = Llow - (Spread * 2)
            if SellStop[bar] > SellStop[bar + 1] and (not BuyStop[bar + 1]):
                SellStop[bar] = SellStop[bar + 1]
            if SellTake[bar] > SellTake[bar + 1] and (not BuyTake[bar + 1]):
                SellTake[bar] = SellTake[bar + 1]
        if Buy[bar]:
            BuyInput[bar] = Buy[bar] + ((Buy[bar] - BuyStop[bar]) * Q)
        if Sell[bar]:
            SellInput[bar] = Sell[bar] - ((SellStop[bar] - Sell[bar]) * Q) + Spread
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Flag_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HLCrossSigForWPR(_MQL5Indicator):
    name = 'HLCrossSigForWPR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Supr_Period': 6,  # Период пробиваемого диапазона, чем больше значение, тем более поздние сигналы и реже
        'MA_Period': 21,  # Период для Heiken Ashi variable. Служит в качестве доп. фильтра
        'Risk': 0,  # Максимальный риск в пипсах для расчета уровня входа исходя из уровня ближайшего MAX/MIN
        'ATR_Period': 120,  # Период АТR. Служит для расчета уровня волатильности.
        'Q': 0.7,  # Параметр для постановки Тейка. - Доля от размера Стопа. если =1, Тейк = Стопу
        'WPR_Period': 12,  # Период WPR. Служит в качестве доп. фильтра
        'HLine': -38,  # Верхняя сигнальная линия стопов для WPR
        'LLine': -62,  # Нижняя сигнальная линия стопов для WPR
    }

