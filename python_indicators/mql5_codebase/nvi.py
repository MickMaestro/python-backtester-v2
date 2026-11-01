"""NVI — converted from MQL5: MQL5 Indicators/Negative Volume Index indicator/NVI.mq5

Negative Volume Index calculates only price changes accompanied by negative change in volume.
This implementation includes the following features:
 * Multi-timeframe (MTF) option
 * Positive Volume Index switch
Copyright: www.Wolfforex.com, 2025; Version: 2.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '2.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'NVI'}, 'levels': [], 'description': ['Negative Volume Index calculates only price changes accompanied by negative change in volume.', 'This implementation includes the following features:', ' * Multi-timeframe (MTF) option', ' * Positive Volume Index switch'], 'name': 'NVI', 'source': 'MQL5 Indicators/Negative Volume Index indicator/NVI.mq5', 'folder': 'Negative Volume Index indicator', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Indicator shift', 'sinput': False}, {'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 0, 'label': 'Timeframe', 'sinput': False}, {'mql': 'Positive', 'py': 'Positive', 'param': 'Positive', 'type': 'bool', 'default': False, 'label': 'Positive Volume Index?', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # Indicator shift
InpTimeframe = _input('InpTimeframe', PERIOD_CURRENT)  # Timeframe
Positive = _input('Positive', False)  # Positive Volume Index?
VolumeType = _input('VolumeType', VOLUME_TICK)
NVI = Arr(0, 0.0)
UpperTFShift = Arr(0, 0.0)
Timeframe = 0  # Timeframe of operation.
deltaHighTF = 0  # Difference in candles count from the higher timeframe.

def OnInit():
    global Timeframe, deltaHighTF
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    name = Box('NVI')
    SetIndexBuffer(0, NVI, INDICATOR_DATA)
    SetIndexBuffer(1, UpperTFShift, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    Timeframe = InpTimeframe
    if InpTimeframe < Period():
        Timeframe = Period()
    elif InpTimeframe > Period():
        name.v += ' @ ' + EnumToString(Timeframe, 'ENUM_TIMEFRAMES')
        StringReplace(name, 'PERIOD_', '')
    IndicatorSetString(INDICATOR_SHORTNAME, name.v)
    deltaHighTF = 0
    if Timeframe > Period():
        deltaHighTF = _idiv(Timeframe, Period())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if iBars(Symbol(), Timeframe) < 2 or rates_total < 2:
        return 0
    Upper_RT = iBars(Symbol(), Timeframe)
    pos = 0
    pos = prev_calculated - 1 - deltaHighTF
    if pos < 0:
        pos = 0
        if Timeframe != Period():
            for i in range(pos, rates_total):
                index = rates_total - 1 - i
                shift = index
                if Timeframe != Period():
                    shift = iBarShift(Symbol(), Timeframe, iTime(Symbol(), PERIOD_CURRENT, index))
                UpperTFShift[i] = Upper_RT - 1 - shift
        pos = 1
        NVI[0] = 1.0
    for i in range(pos, rates_total):
        index = rates_total - 1 - i
        shift = index
        if Timeframe != Period():
            shift = iBarShift(Symbol(), Timeframe, iTime(Symbol(), PERIOD_CURRENT, index))
            if (Upper_RT - 1 - shift) == UpperTFShift[i - 1]:
                NVI[i] = NVI[i - 1]
                UpperTFShift[i] = Upper_RT - 1 - shift
                continue
        vol_cur = 0
        vol_prev = 0
        if VolumeType == VOLUME_REAL:
            vol_cur = volume[i]
            vol_prev = volume[i - 1]
        else:
            vol_cur = tick_volume[i]
            vol_prev = tick_volume[i - 1]
        if ((not Positive) and vol_cur < vol_prev) or (Positive and vol_cur > vol_prev):
            NVI[i] = _fdiv(NVI[i - 1] * close[i], close[i - 1])
        else:
            NVI[i] = NVI[i - 1]
        UpperTFShift[i] = Upper_RT - 1 - shift
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NVIIndicator(_MQL5Indicator):
    name = 'NVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Indicator shift
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe
        'Positive': False,  # Positive Volume Index?
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),
    }

