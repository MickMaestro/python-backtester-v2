"""MA_Filter — converted from MQL5: MQL5 Indicators/MA_Filter/MA_Filter.mq5

MA with filter
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 8, 2: 12, 3: 5, 4: 5, 5: 5}, 'colors': {1: [32768, 255, 11119017], 2: [32768, 255, 11119017], 3: [3329434], 4: [55295], 5: [13882323]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'MA', 2: 'Substrate', 3: 'Swing to Up', 4: 'Swing to Down', 5: 'Swing to Neutral'}, 'levels': [], 'description': ['MA with filter'], 'name': 'MA_Filter', 'source': 'MQL5 Indicators/MA_Filter/MA_Filter.mq5', 'folder': 'MA_Filter', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 20, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpShiftMA', 'py': 'InpShiftMA', 'param': 'InpShiftMA', 'type': 'uint', 'default': 1, 'label': 'MA anchor shift', 'sinput': False}, {'mql': 'InpMinDiffMA', 'py': 'InpMinDiffMA', 'param': 'InpMinDiffMA', 'type': 'uint', 'default': 10, 'label': 'MA anchor difference', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_width1 = 2  # #property indicator_width1

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 20)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpShiftMA = _input('InpShiftMA', 1)  # MA anchor shift
InpMinDiffMA = _input('InpMinDiffMA', 10)  # MA anchor difference
BufferMA = Arr(0, 0.0)
BufferColorsMA = Arr(0, 0.0)
BufferArrSub = Arr(0, 0.0)
BufferColorsArrSub = Arr(0, 0.0)
BufferArrUP = Arr(0, 0.0)
BufferArrDN = Arr(0, 0.0)
BufferArrNL = Arr(0, 0.0)
diff_pt = 0.0
period = 0
shift = 0
handle_ma = 0

def OnInit():
    global diff_pt, handle_ma, period, shift
    period = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    shift = (1 if (InpShiftMA < 1) else InpShiftMA)
    diff = (1 if (InpMinDiffMA < 1) else InpMinDiffMA)
    diff_pt = diff * Point()
    width_sub = _int(indicator_width1 + 1)
    width_arr = (1 if ((width_sub - 2) < 1) else (width_sub - 2))
    SetIndexBuffer(0, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColorsMA, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferArrSub, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColorsArrSub, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferArrUP, INDICATOR_DATA)
    SetIndexBuffer(5, BufferArrDN, INDICATOR_DATA)
    SetIndexBuffer(6, BufferArrNL, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    method = StringSubstr(EnumToString(InpMethod, 'ENUM_MA_METHOD'), 5)
    IndicatorSetString(INDICATOR_SHORTNAME, method + ' with filter (' + _str(period) + ',' + _str(shift) + ',' + _str(diff) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, width_sub)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, width_arr)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, width_arr)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, width_arr)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferColorsMA, True)
    ArraySetAsSeries(BufferArrSub, True)
    ArraySetAsSeries(BufferColorsArrSub, True)
    ArraySetAsSeries(BufferArrUP, True)
    ArraySetAsSeries(BufferArrDN, True)
    ArraySetAsSeries(BufferArrNL, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - shift - 3
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferColorsMA, 2)
        ArrayInitialize(BufferArrSub, EMPTY_VALUE)
        ArrayInitialize(BufferArrUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrDN, EMPTY_VALUE)
        ArrayInitialize(BufferArrNL, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if BufferMA[i] > BufferMA[i + shift] and fabs(BufferMA[i] - BufferMA[i + shift]) > diff_pt:
            BufferColorsMA[i] = 0.0
            if BufferColorsMA[i + 1] != 0:
                BufferArrSub[i + 1] = BufferMA[i + 1]
                BufferArrUP[i + 1] = BufferArrSub[i + 1]
                BufferColorsArrSub[i + 1] = 0.0
        else:
            if BufferMA[i] < BufferMA[i + shift] and fabs(BufferMA[i] - BufferMA[i + shift]) > diff_pt:
                BufferColorsMA[i] = 1.0
                if BufferColorsMA[i + 1] != 1:
                    BufferArrSub[i + 1] = BufferMA[i + 1]
                    BufferArrDN[i + 1] = BufferArrSub[i + 1]
                    BufferColorsArrSub[i + 1] = 1.0
            else:
                BufferColorsMA[i] = 2.0
                if BufferColorsMA[i + 1] != 2:
                    BufferArrSub[i + 1] = BufferMA[i + 1]
                    BufferArrNL[i + 1] = BufferArrSub[i + 1]
                    BufferColorsArrSub[i + 1] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAFilter(_MQL5Indicator):
    name = 'MA_Filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodMA': 20,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpShiftMA': 1,  # MA anchor shift
        'InpMinDiffMA': 10,  # MA anchor difference
    }

