"""ima_htf — converted from MQL5: MQL5 Indicators/iMa_HTF/ima_htf.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [14822282]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': [], 'name': 'ima_htf', 'source': 'MQL5 Indicators/iMa_HTF/ima_htf.mq5', 'folder': 'iMa_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'uint', 'default': 15, 'label': 'Period of averaging', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 1, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
MA_Period = _input('MA_Period', 15)  # Period of averaging
MA_Method = _input('MA_Method', MODE_EMA)  # Method of averaging
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Init = False
dPriceShift = 0.0
Symbol_ = ""
Word = ""
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global Ind_Handle, Init, Symbol_, Word, dPriceShift, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('iMA indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    Ind_Handle = iMA(None, TimeFrame, MA_Period, 0, MA_Method, Applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return INIT_FAILED
    min_rates_total = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT)) * 3
    Symbol_ = Symbol()
    Word = 'iMA' + ' indicator: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'iMA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if (BarsCalculated(Ind_Handle) < 2 or rates_total < min_rates_total) or (not Init):
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    iMa = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 2
        _s_OnCalculate_LastCountBar = limit
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar + 1] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar + 1]), 1, iMa) <= 0:
                return 0
            _s_OnCalculate_LastCountBar = bar
            IndBuffer[bar + 1] = iMa[0] + dPriceShift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if CopyBuffer(Ind_Handle, 0, _DT(time[0]), 1, iMa) <= 0:
        return 0
    IndBuffer[0] = iMa[0] + dPriceShift
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ImaHtf(_MQL5Indicator):
    name = 'ima_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'MA_Period': 15,  # Period of averaging
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method of averaging
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

