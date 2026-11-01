"""ibbands_htf — converted from MQL5: MQL5 Indicators/iBBands_HTF/ibbands_htf.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 2, 2: 2, 3: 2}, 'colors': {1: [11186720], 2: [16711680], 3: [16711935]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ibbands_htf', 'source': 'MQL5 Indicators/iBBands_HTF/ibbands_htf.mq5', 'folder': 'iBBands_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'uint', 'default': 15, 'label': 'Period of averaging', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
MA_Period = _input('MA_Period', 15)  # Period of averaging
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Price constant
Deviation = _input('Deviation', 2.0)  # Deviation
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
MdIndBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
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
        Print('iBBands indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    Ind_Handle = iBands(None, TimeFrame, MA_Period, 0, Deviation, Applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return INIT_FAILED
    min_rates_total = _int(_idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT)) * MA_Period)
    Symbol_ = Symbol()
    Word = 'iBBands' + ' indicator: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper ' + 'iBBands')
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(1, MdIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(1, PLOT_LABEL, 'Middle ' + 'iBBands')
    ArraySetAsSeries(MdIndBuffer, True)
    SetIndexBuffer(2, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(2, PLOT_LABEL, 'Lower ' + 'iBBands')
    ArraySetAsSeries(DnIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'iBBands')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_FAILED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if (BarsCalculated(Ind_Handle) < 2 or rates_total < min_rates_total) or (not Init):
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    UpBB = Arr(1, 0.0, dyn=False)
    MdBB = Arr(1, 0.0, dyn=False)
    DnBB = Arr(1, 0.0, dyn=False)
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
        UpIndBuffer[bar + 1] = 0.0
        MdIndBuffer[bar + 1] = 0.0
        DnIndBuffer[bar + 1] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            if CopyBuffer(Ind_Handle, UPPER_BAND, _DT(time[bar + 1]), 1, UpBB) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, BASE_LINE, _DT(time[bar + 1]), 1, MdBB) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, LOWER_BAND, _DT(time[bar + 1]), 1, DnBB) <= 0:
                return 0
            _s_OnCalculate_LastCountBar = bar
            UpIndBuffer[bar + 1] = UpBB[0] + dPriceShift
            MdIndBuffer[bar + 1] = MdBB[0] + dPriceShift
            DnIndBuffer[bar + 1] = DnBB[0] + dPriceShift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if CopyBuffer(Ind_Handle, UPPER_BAND, _DT(time[0]), 1, UpBB) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, BASE_LINE, _DT(time[0]), 1, MdBB) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, LOWER_BAND, _DT(time[0]), 1, DnBB) <= 0:
        return 0
    UpIndBuffer[0] = UpBB[0] + dPriceShift
    MdIndBuffer[0] = MdBB[0] + dPriceShift
    DnIndBuffer[0] = DnBB[0] + dPriceShift
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IbbandsHtf(_MQL5Indicator):
    name = 'ibbands_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'MA_Period': 15,  # Period of averaging
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price constant
        'Deviation': 2.0,  # Deviation
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

