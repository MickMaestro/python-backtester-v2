"""volatilitypivot — converted from MQL5: MQL5 Indicators/BackgroundCandle_VolatilityPivot_HTF/volatilitypivot.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [11823615], 3: [16760576], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 4, 2: 4}, 'labels': {1: 'Upper VolatilityPivot', 2: 'Lower VolatilityPivot', 3: 'Buy VolatilityPivot', 4: 'Sell VolatilityPivot'}, 'levels': [], 'description': [], 'name': 'volatilitypivot', 'source': 'MQL5 Indicators/BackgroundCandle_VolatilityPivot_HTF/volatilitypivot.mq5', 'folder': 'BackgroundCandle_VolatilityPivot_HTF', 'inputs': [{'mql': 'atr_range', 'py': 'atr_range', 'param': 'atr_range', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'ima_range', 'py': 'ima_range', 'param': 'ima_range', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'atr_factor', 'py': 'atr_factor', 'param': 'atr_factor', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DeltaPrice', 'py': 'DeltaPrice', 'param': 'DeltaPrice', 'type': 'uint', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Mode_
Mode_ATR = 0
Mode_Price = 1
_enum('Mode_', {0: 'Mode_ATR', 1: 'Mode_Price'})

# ---- inputs and global variables
atr_range = _input('atr_range', 100)
ima_range = _input('ima_range', 10)
atr_factor = _input('atr_factor', 3.0)
Mode = _input('Mode', Mode_ATR)
DeltaPrice = _input('DeltaPrice', 200)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
dDeltaPrice = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, dDeltaPrice, min_rates_total
    if Mode == Mode_ATR:
        min_rates_total = _int(atr_range + ima_range) + 1
        ATR_Handle = iATR(None, 0, atr_range)
        if ATR_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the ATR indicator')
            return INIT_FAILED
    else:
        min_rates_total = 3
        dDeltaPrice = DeltaPrice * Point()
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 118)
    SetIndexBuffer(3, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 118)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VolatilityPivot')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_PrevStop
    if (BarsCalculated(ATR_Handle) < rates_total and Mode == Mode_ATR) or rates_total < min_rates_total:
        return 0
    DeltaStop = 0.0
    Stop = 0.0
    limit = 0
    bar = 0
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_PrevStop = close[limit + 1]
    else:
        limit = rates_total - prev_calculated
    if Mode == Mode_Price:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            ExtMapBufferUp1[bar] = EMPTY_VALUE
            ExtMapBufferDown1[bar] = EMPTY_VALUE
            DeltaStop = dDeltaPrice
            if close[bar] == _s_OnCalculate_PrevStop:
                Stop = _s_OnCalculate_PrevStop
            else:
                if close[bar + 1] < _s_OnCalculate_PrevStop and close[bar] < _s_OnCalculate_PrevStop:
                    Stop = MathMin(_s_OnCalculate_PrevStop, close[bar] + DeltaStop)
                else:
                    if close[bar + 1] > _s_OnCalculate_PrevStop and close[bar] > _s_OnCalculate_PrevStop:
                        Stop = MathMax(_s_OnCalculate_PrevStop, close[bar] - DeltaStop)
                    else:
                        if close[bar] > _s_OnCalculate_PrevStop:
                            Stop = close[bar] - DeltaStop
                        else:
                            Stop = close[bar] + DeltaStop
            if close[bar] > Stop:
                ExtMapBufferUp[bar] = Stop
            else:
                ExtMapBufferUp[bar] = EMPTY_VALUE
            if close[bar] < Stop:
                ExtMapBufferDown[bar] = Stop
            else:
                ExtMapBufferDown[bar] = EMPTY_VALUE
            if ExtMapBufferUp[bar + 1] == EMPTY_VALUE and ExtMapBufferUp[bar] != EMPTY_VALUE:
                ExtMapBufferUp1[bar] = ExtMapBufferUp[bar]
            if ExtMapBufferDown[bar + 1] == EMPTY_VALUE and ExtMapBufferDown[bar] != EMPTY_VALUE:
                ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
            if bar:
                _s_OnCalculate_PrevStop = Stop
        else:
            bar = _range_end(bar, 0 - 1, -1)
    if Mode == Mode_ATR:
        ATR = Arr(0, 0.0)
        to_copy = 0
        maxbar = 0
        ArraySetAsSeries(ATR, True)
        to_copy = limit + 1
        if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
            return 0
        maxbar = rates_total - min_rates_total - 1
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            ExtMapBufferUp1[bar] = EMPTY_VALUE
            ExtMapBufferDown1[bar] = EMPTY_VALUE
            DeltaStop = atr_factor * _s_OnCalculate_EMA.EMASeries(maxbar, prev_calculated, rates_total, ima_range, ATR[bar], bar, True)
            if close[bar] == _s_OnCalculate_PrevStop:
                Stop = _s_OnCalculate_PrevStop
            else:
                if close[bar + 1] < _s_OnCalculate_PrevStop and close[bar] < _s_OnCalculate_PrevStop:
                    Stop = MathMin(_s_OnCalculate_PrevStop, close[bar] + DeltaStop)
                else:
                    if close[bar + 1] > _s_OnCalculate_PrevStop and close[bar] > _s_OnCalculate_PrevStop:
                        Stop = MathMax(_s_OnCalculate_PrevStop, close[bar] - DeltaStop)
                    else:
                        if close[bar] > _s_OnCalculate_PrevStop:
                            Stop = close[bar] - DeltaStop
                        else:
                            Stop = close[bar] + DeltaStop
            if close[bar] > Stop:
                ExtMapBufferUp[bar] = Stop
            else:
                ExtMapBufferUp[bar] = EMPTY_VALUE
            if close[bar] < Stop:
                ExtMapBufferDown[bar] = Stop
            else:
                ExtMapBufferDown[bar] = EMPTY_VALUE
            if ExtMapBufferUp[bar + 1] == EMPTY_VALUE and ExtMapBufferUp[bar] != EMPTY_VALUE:
                ExtMapBufferUp1[bar] = ExtMapBufferUp[bar]
            if ExtMapBufferDown[bar + 1] == EMPTY_VALUE and ExtMapBufferDown[bar] != EMPTY_VALUE:
                ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
            if bar:
                _s_OnCalculate_PrevStop = Stop
        else:
            bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_PrevStop = 0.0
_s_OnCalculate_EMA = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Volatilitypivot(_MQL5Indicator):
    name = 'volatilitypivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'atr_range': 100,
        'ima_range': 10,
        'atr_factor': 3.0,
        'Mode': _Choice({0: 'ATR', 1: 'Price deviation'}, default=0),
        'DeltaPrice': 200,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

