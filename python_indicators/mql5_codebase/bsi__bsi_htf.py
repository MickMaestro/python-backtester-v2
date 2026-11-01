"""bsi — converted from MQL5: MQL5 Indicators/BSI_HTF/bsi.mq5

Bounce Strength Indicator
Copyright: Copyright 2015, fxborg; Link: http://blog.livedoor.jp/fxborg/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, fxborg', 'link': 'http://blog.livedoor.jp/fxborg/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 3, 2: 3, 3: 8}, 'colors': {1: [8421376], 2: [255], 3: [16711935, 8421504, 16748574]}, 'widths': {1: 2, 2: 2, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Floor Bounce Strength', 2: 'Ceiling Bounce Strength', 3: 'Bounce Strength Index'}, 'levels': [10.0, 0.0, -10.0], 'description': ['Bounce Strength Indicator'], 'name': 'bsi', 'source': 'MQL5 Indicators/BSI_HTF/bsi.mq5', 'folder': 'BSI_HTF', 'inputs': [{'mql': 'InpRangePeriod', 'py': 'InpRangePeriod', 'param': 'InpRangePeriod', 'type': 'uint', 'default': 20, 'label': 'Range Period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpAvgPeriod', 'py': 'InpAvgPeriod', 'param': 'InpAvgPeriod', 'type': 'uint', 'default': 3, 'label': 'Avg Period', 'sinput': False}, {'mql': 'InpUsingVolumeWeight', 'py': 'InpUsingVolumeWeight', 'param': 'InpUsingVolumeWeight', 'type': 'int', 'default': 3, 'label': 'Using Volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Volume_Mode
ENUM_WITHOUT_VOLUME = 1
ENUM_VOLUME = 2
ENUM_TICKVOLUME = 3
_enum('Volume_Mode', {1: 'ENUM_WITHOUT_VOLUME', 2: 'ENUM_VOLUME', 3: 'ENUM_TICKVOLUME'})

# ---- inputs and global variables
InpRangePeriod = _input('InpRangePeriod', 20)  # Range Period
InpSlowing = _input('InpSlowing', 3)  # Slowing
InpAvgPeriod = _input('InpAvgPeriod', 3)  # Avg Period
InpUsingVolumeWeight = _input('InpUsingVolumeWeight', ENUM_TICKVOLUME)  # Using Volume
Count = Arr(0, 0)
ExtHighest = Arr(0, 0.0)
ExtLowest = Arr(0, 0.0)
ExtVolume = Arr(0, 0.0)
min_rates_total = 0
size = 0
min_rates_1 = 0
ExtPosBuffer = Arr(0, 0.0)
ExtNegBuffer = Arr(0, 0.0)
BSIBuffer = Arr(0, 0.0)
ColorBSIBuffer = Arr(0, 0.0)

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
    global min_rates_1, min_rates_total, size
    min_rates_total = _int(InpRangePeriod + InpSlowing + InpAvgPeriod)
    size = _int(MathMax(InpRangePeriod, InpSlowing))
    min_rates_1 = size
    ArrayResize(Count, size)
    ArrayResize(ExtHighest, size)
    ArrayResize(ExtLowest, size)
    ArrayResize(ExtVolume, size)
    SetIndexBuffer(0, ExtPosBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtNegBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, BSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorBSIBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    StringConcatenate(shortname, 'BSI( ', InpRangePeriod, ', ', InpSlowing, ', ', InpAvgPeriod, ', ', EnumToString(InpUsingVolumeWeight, 'Volume_Mode'), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first1 = 0
    first2 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = min_rates_1
        first2 = min_rates_total
        ArrayInitialize(Count, None)
        ArrayInitialize(ExtHighest, None)
        ArrayInitialize(ExtLowest, None)
        ArrayInitialize(ExtVolume, None)
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        dmin = 1000000.0
        dmax = -1000000.0
        volmax = 0.0
        for kkk in range(0, _int(InpRangePeriod)):
            dmin = MathMin(dmin, low[bar - kkk])
            dmax = MathMax(dmax, high[bar - kkk])
        ExtLowest[Count[0]] = dmin
        ExtHighest[Count[0]] = dmax
        _sw1 = InpUsingVolumeWeight
        if _sw1 == ENUM_WITHOUT_VOLUME:
            ExtVolume[Count[0]] = 1.0
        elif _sw1 == ENUM_VOLUME:
            for kkk in range(0, _int(InpRangePeriod)):
                volmax = MathMax(volmax, volume[bar - kkk])
            ExtVolume[Count[0]] = volmax
        elif _sw1 == ENUM_TICKVOLUME:
            for kkk in range(0, _int(InpRangePeriod)):
                volmax = MathMax(volmax, tick_volume[bar - kkk])
            ExtVolume[Count[0]] = volmax
        sumpos = 0.0
        sumneg = 0.0
        sumhigh = 0.0
        sumpvol = 0.0
        sumnvol = 0.0
        for kkk in range(0, _int(InpSlowing)):
            barkkk = bar - kkk
            vol = 1.0
            _sw2 = InpUsingVolumeWeight
            if _sw2 == ENUM_WITHOUT_VOLUME:
                pass
            elif _sw2 == ENUM_VOLUME:
                if ExtVolume[Count[kkk]]:
                    vol = _fdiv(volume[barkkk], ExtVolume[Count[kkk]])
            elif _sw2 == ENUM_TICKVOLUME:
                if ExtVolume[Count[kkk]]:
                    vol = _fdiv(tick_volume[barkkk], ExtVolume[Count[kkk]])
            ratio = 0.0
            range_ = ExtHighest[Count[kkk]] - ExtLowest[Count[kkk]]
            range_ = MathMax(range_, Point())
            sp = high[barkkk] - low[barkkk]
            if not ((close[barkkk - 1] - (sp * 0.2)) > close[barkkk]):
                if low[barkkk] == ExtLowest[Count[kkk]]:
                    ratio = 1.0
                else:
                    ratio = _fdiv(ExtHighest[Count[kkk]] - low[barkkk], range_)
                sumpos += (close[barkkk] - low[barkkk]) * ratio * vol
            if not ((close[barkkk - 1] + (sp * 0.2)) < close[barkkk]):
                if high[barkkk] == ExtHighest[Count[kkk]]:
                    ratio = 1.0
                else:
                    ratio = _fdiv(high[barkkk] - ExtLowest[Count[kkk]], range_)
                sumneg += (high[barkkk] - close[barkkk]) * ratio * vol * -1
            sumhigh += range_
        if not sumhigh:
            ExtPosBuffer[bar] = 0.0
            ExtNegBuffer[bar] = 0.0
        else:
            ExtPosBuffer[bar] = _fdiv(sumpos, sumhigh) * 100
            ExtNegBuffer[bar] = _fdiv(sumneg, sumhigh) * 100
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, size)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        sumPos = 0.0
        sumNeg = 0.0
        sum_ = 0.0
        for kkk in range(0, _int(InpAvgPeriod)):
            sum_ += ExtPosBuffer[bar - kkk] + ExtNegBuffer[bar - kkk]
        BSIBuffer[bar] = sum_ / InpAvgPeriod
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        clr = 1
        if BSIBuffer[bar - 1] > BSIBuffer[bar]:
            clr = 0
        if BSIBuffer[bar - 1] < BSIBuffer[bar]:
            clr = 2
        ColorBSIBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bsi(_MQL5Indicator):
    name = 'bsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRangePeriod': 20,  # Range Period
        'InpSlowing': 3,  # Slowing
        'InpAvgPeriod': 3,  # Avg Period
        'InpUsingVolumeWeight': _Choice({1: 'Using without Volume', 2: 'Using Volume', 3: 'Using TickVolume'}, default=3),  # Using Volume
    }

