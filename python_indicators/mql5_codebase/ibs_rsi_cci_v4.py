"""IBS_RSI_CCI_v4 — converted from MQL5: MQL5 Indicators/IBS_RSI_CCI_v4/IBS_RSI_CCI_v4.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 14381203]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'IBS_RSI_CCI_v4'}, 'levels': [], 'description': [], 'name': 'IBS_RSI_CCI_v4', 'source': 'MQL5 Indicators/IBS_RSI_CCI_v4/IBS_RSI_CCI_v4.mq5', 'folder': 'IBS_RSI_CCI_v4', 'inputs': [{'mql': 'IBSPeriod', 'py': 'IBSPeriod', 'param': 'IBSPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'porog', 'py': 'porog', 'param': 'porog', 'type': 'int', 'default': 50, 'label': 'порог', 'sinput': False}, {'mql': 'MAType_VKWB', 'py': 'MAType_VKWB', 'param': 'MAType_VKWB', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'RangePeriod_VKWB', 'py': 'RangePeriod_VKWB', 'param': 'RangePeriod_VKWB', 'type': 'int', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'SmoothPeriod_VKWB', 'py': 'SmoothPeriod_VKWB', 'param': 'SmoothPeriod_VKWB', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
IBSPeriod = _input('IBSPeriod', 5)
MAType = _input('MAType', MODE_SMA)
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
CCIPeriod = _input('CCIPeriod', 14)
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)
porog = _input('porog', 50)  # порог
MAType_VKWB = _input('MAType_VKWB', MODE_SMA)
RangePeriod_VKWB = _input('RangePeriod_VKWB', 25)
SmoothPeriod_VKWB = _input('SmoothPeriod_VKWB', 3)
koef_ibs = 7.0
koef_rsi = 9.0
koef_cci = 1.0
ibs = True  # применять ibs для расчета средней линии
rsi = True  # применять rsi для расчета средней линии
cci = True  # применять cci для расчета средней линии
kibs = -1
kcci = -1
krsi = -1
posit = -1
xma1 = 1
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
CCI_Handle = 0
RSI_Handle = 0
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global CCI_Handle, RSI_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(MathMax(CCIPeriod, RSIPeriod) + IBSPeriod + RangePeriod_VKWB)
    min_rates_total = min_rates_1 + (SmoothPeriod_VKWB + RangePeriod_VKWB)
    CCI_Handle = iCCI(None, 0, CCIPeriod, CCIPrice)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI')
        return INIT_FAILED
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'IBS_RSI_CCI_v4')
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(CCI_Handle) < rates_total or BarsCalculated(RSI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    CCI = Arr(0, 0.0)
    RSI = Arr(0, 0.0)
    series = 0.0
    xseries = 0.0
    sum_ = 0.0
    divisor = 0.0
    raz10 = 0.0
    E0 = 0.0
    E1 = 0.0
    E3 = 0.0
    E4 = 0.0
    E5 = 0.0
    E6 = 0.0
    E7 = 0.0
    maxbar1 = rates_total - 2
    maxbar2 = rates_total - 2 - min_rates_1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        UpBuffer[limit + 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        divisor = MathMax(high[bar] - low[bar], Point())
        series = _fdiv(close[bar] - low[bar], divisor)
        xseries = XMA1.XMASeries(maxbar1, prev_calculated, rates_total, MAType, 0, IBSPeriod, series, bar, True)
        sum_ = 0.0
        sum_ += kibs * (xseries - 0.5) * 100.0 * koef_ibs
        sum_ += kcci * CCI[bar] * koef_cci
        sum_ += krsi * (RSI[bar] - 50.0) * koef_rsi
        sum_ *= 1.0 / 3.0
        E1 = posit * sum_
        E0 = UpBuffer[bar + 1]
        raz10 = E1 - E0
        if MathAbs(raz10) > porog:
            if raz10 > 0:
                E0 = E1 - (porog * xma1)
            if raz10 < 0:
                E0 = E1 + (porog * xma1)
        UpBuffer[bar] = E0
        E3 = UpBuffer[ArrayMaximum(UpBuffer, bar, RangePeriod_VKWB)]
        E4 = UpBuffer[ArrayMinimum(UpBuffer, bar, RangePeriod_VKWB)]
        E5 = XMA2.XMASeries(maxbar2, prev_calculated, rates_total, MAType_VKWB, 0, SmoothPeriod_VKWB, E3, bar, True)
        E6 = XMA3.XMASeries(maxbar2, prev_calculated, rates_total, MAType_VKWB, 0, SmoothPeriod_VKWB, E4, bar, True)
        E7 = (E5 + E6) / 2
        DnBuffer[bar] = E7
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IBSRSICCIV4(_MQL5Indicator):
    name = 'IBS_RSI_CCI_v4'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IBSPeriod': 5,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'CCIPeriod': 14,
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),
        'porog': 50,  # порог
        'MAType_VKWB': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'RangePeriod_VKWB': 25,
        'SmoothPeriod_VKWB': 3,
    }

