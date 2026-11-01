"""volatilitypivot_htf — converted from MQL5: MQL5 Indicators/VolatilityPivot_HTF/volatilitypivot_htf.mq5

The VolatilityPivot indicator with timeframe selection option available in input parameters
Copyright: Copyright © 2013, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.61

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.61', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [11823615], 3: [16760576], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 4, 2: 4}, 'labels': {1: 'Upper VolatilityPivot', 2: 'Lower VolatilityPivot', 3: 'Buy VolatilityPivot', 4: 'Sell VolatilityPivot'}, 'levels': [], 'description': ['The VolatilityPivot indicator with timeframe selection option available in input parameters'], 'name': 'volatilitypivot_htf', 'source': 'MQL5 Indicators/VolatilityPivot_HTF/volatilitypivot_htf.mq5', 'folder': 'VolatilityPivot_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period', 'sinput': False}, {'mql': 'atr_range', 'py': 'atr_range', 'param': 'atr_range', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'ima_range', 'py': 'ima_range', 'param': 'ima_range', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'atr_factor', 'py': 'atr_factor', 'param': 'atr_factor', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DeltaPrice', 'py': 'DeltaPrice', 'param': 'DeltaPrice', 'type': 'uint', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode_
Mode_ATR = 0
Mode_Price = 1
_enum('Mode_', {0: 'Mode_ATR', 1: 'Mode_Price'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period
atr_range = _input('atr_range', 100)
ima_range = _input('ima_range', 10)
atr_factor = _input('atr_factor', 3.0)
Mode = _input('Mode', Mode_ATR)
DeltaPrice = _input('DeltaPrice', 200)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
Ind4Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck(' VolatilityPivot', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'VolatilityPivot', atr_range, ima_range, atr_factor, Mode, DeltaPrice, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of VolatilityPivot')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(2, Ind3Buffer, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(3, Ind4Buffer, EMPTY_VALUE, min_rates_total, Shift)
    PlotIndexSetInteger(2, PLOT_ARROW, 118)
    PlotIndexSetInteger(3, PLOT_ARROW, 118)
    shortname = Box("")
    StringConcatenate(shortname, ' VolatilityPivot', '(', EnumToString(TimeFrame, 'ENUM_TIMEFRAMES'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, Symbol(), TimeFrame, Ind_Handle, 0, Ind1Buffer, 1, Ind2Buffer, 2, Ind3Buffer, 3, Ind4Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, BuyBuffNumb, BuyIndBuf, SellBuffNumb, SellIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        UpIndBuf[bar] = EMPTY_VALUE
        DnIndBuf[bar] = EMPTY_VALUE
        BuyIndBuf[bar] = EMPTY_VALUE
        SellIndBuf[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = Arr_[0]
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            DnIndBuf[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuyBuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            BuyIndBuf[bar] = Arr_[0]
            if CopyBuffer(IndHandle, SellBuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            SellIndBuf[bar] = Arr_[0]
        else:
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            DnIndBuf[bar] = DnIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Chart period for the ' + IndName + ' indicator cannot be less than the period of the current chart!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilitypivotHtf(_MQL5Indicator):
    name = 'volatilitypivot_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period
        'atr_range': 100,
        'ima_range': 10,
        'atr_factor': 3.0,
        'Mode': _Choice({0: 'ATR', 1: 'price deviation'}, default=0),
        'DeltaPrice': 200,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

