"""forexofftrendsign — converted from MQL5: MQL5 Indicators/ForexOFFTrend_HTF_Signal/forexofftrendsign.mq5

Copyright: Copyright © 2006, rewritten by CrazyChart; Link: http://viac.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, rewritten by CrazyChart', 'link': 'http://viac.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [14053594], 2: [3329330]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'ForexOFFTrendSign Sell', 2: 'ForexOFFTrendSign Buy'}, 'levels': [], 'description': [], 'name': 'forexofftrendsign', 'source': 'MQL5 Indicators/ForexOFFTrend_HTF_Signal/forexofftrendsign.mq5', 'folder': 'ForexOFFTrend_HTF_Signal', 'inputs': [{'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'uint', 'default': 7, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'KPer', 'py': 'KPer', 'param': 'KPer', 'type': 'uint', 'default': 7, 'label': 'Период сдвига сигнальной огибающей', 'sinput': False}, {'mql': 'Kmax', 'py': 'Kmax', 'param': 'Kmax', 'type': 'double', 'default': 50.6, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SSP = _input('SSP', 7)  # Период поиска экстремумов
KPer = _input('KPer', 7)  # Период сдвига сигнальной огибающей
Kmax = _input('Kmax', 50.6)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
KPer3 = 0
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
Count = Arr(0, 0)
Value = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global ATR_Handle, KPer3, min_rates_total
    min_rates_total = _int(MathMax(SSP, KPer) + KPer)
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, min_rates_total) + 3
    KPer3 = _int(KPer + 3)
    ArrayResize(Count, KPer3)
    ArrayResize(Value, KPer3)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value, 0.0)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 93)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 93)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ForexOFFTrendSign(' + _str(SSP) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - _int(MathMax(SSP, KPer)) - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    for bar in range(limit, 0 - 1, -1):
        HH = High[ArrayMaximum(High, bar, SSP)]
        LL = Low[ArrayMinimum(Low, bar, SSP)]
        Value[Count[0]] = HH - (((HH - LL) * Kmax) / 100)
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if Value[Count[1]] <= Value[Count[KPer + 1]] and Value[Count[0]] > Value[Count[KPer]]:
            if CopyBuffer(ATR_Handle, 0, _DT(Time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = Low[bar] - ((ATR[0] * 3) / 8)
        if Value[Count[1]] >= Value[Count[KPer + 1]] and Value[Count[0]] < Value[Count[KPer]]:
            if CopyBuffer(ATR_Handle, 0, _DT(Time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = High[bar] + ((ATR[0] * 3) / 8)
        if bar:
            Recount_ArrayZeroPos(Count, KPer3)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Forexofftrendsign(_MQL5Indicator):
    name = 'forexofftrendsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SSP': 7,  # Период поиска экстремумов
        'KPer': 7,  # Период сдвига сигнальной огибающей
        'Kmax': 50.6,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

