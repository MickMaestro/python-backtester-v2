"""volatility_fba_nr — converted from MQL5: MQL5 Indicators/Volatility_FBA_NR/volatility_fba_nr.mq5

Copyright: Copyright © 2010, Svinozavr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Svinozavr', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'volatility_fba_nr', 'source': 'MQL5 Indicators/Volatility_FBA_NR/volatility_fba_nr.mq5', 'folder': 'Volatility_FBA_NR', 'inputs': [{'mql': 'Source', 'py': 'Source', 'param': 'Source', 'type': 'int', 'default': 1, 'label': 'source', 'sinput': False}, {'mql': 'SourcePeriod', 'py': 'SourcePeriod', 'param': 'SourcePeriod', 'type': 'uint', 'default': 22, 'label': 'source period', 'sinput': False}, {'mql': 'FrontPeriod', 'py': 'FrontPeriod', 'param': 'FrontPeriod', 'type': 'uint', 'default': 1, 'label': 'front smoothing period; <1', 'sinput': False}, {'mql': 'BackPeriod', 'py': 'BackPeriod', 'param': 'BackPeriod', 'type': 'uint', 'default': 444, 'label': 'damping smoothing period; <1', 'sinput': False}, {'mql': 'Sens', 'py': 'Sens', 'param': 'Sens', 'type': 'uint', 'default': 0, 'label': 'sensitivity threshold in points or in ticks (for volume)', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum AlgMode
VOLUME = 0
ATR = 1
STDEV = 2
_enum('AlgMode', {0: 'VOLUME', 1: 'ATR', 2: 'STDEV'})

# ---- inputs and global variables
Source = _input('Source', ATR)  # source
SourcePeriod = _input('SourcePeriod', 22)  # source period
FrontPeriod = _input('FrontPeriod', 1)  # front smoothing period; <1
BackPeriod = _input('BackPeriod', 444)  # damping smoothing period; <1
Sens = _input('Sens', 0)  # sensitivity threshold in points or in ticks (for volume)
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
VltBuffer = Arr(0, 0.0)
SigBuffer = Arr(0, 0.0)
per0 = 0.0
per1 = 0.0
per3 = 0.0
sens = 0.0  # sensitivity threshold in prices
FBA = 0  # 1 - front smoothing, -1 - damping smoothing, 0 - normal MA - smooth all!
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global FBA, Ind_Handle, min_rates_total, per0, per1, per3, sens
    ShortName = ""
    if Sens > 0:
        ShortName = _str(Sens) + ' '
    FBA = 0
    _fr = _str(FrontPeriod)
    _bk = _str(BackPeriod)
    _src = ""
    _sw1 = Source
    if _sw1 == VOLUME:
        _src = 'Volume'
    elif _sw1 == ATR:
        _src = 'ATR'
        Ind_Handle = iATR(None, 0, SourcePeriod)
        if Ind_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of iATR indicator')
    elif _sw1 == STDEV:
        _src = 'StDev'
        Ind_Handle = iStdDev(None, 0, SourcePeriod, 0, MODE_SMA, PRICE_CLOSE)
        if Ind_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of iStdDev indicator')
    ShortName = ShortName + '(' + _src + _str(SourcePeriod) + ')'
    if FrontPeriod != 1 or BackPeriod != 1:
        if FrontPeriod == BackPeriod:
            ShortName = ShortName + ' (' + _fr + ')'
        else:
            if FrontPeriod != 1:
                ShortName = ShortName + ' Front(' + _fr + ')'
            if BackPeriod != 1:
                ShortName = ShortName + ' Back(' + _bk + ')'
    if Source > 0:
        sens = Sens * Point()
    else:
        sens = Sens
    if FrontPeriod == BackPeriod:
        FBA = 0
        per0 = 2.0 / (1 + FrontPeriod)
        per1 = 1.0
    if FrontPeriod < BackPeriod:
        FBA = -1
        per0 = 2.0 / (1 + FrontPeriod)
        per1 = 2.0 / (1 + BackPeriod)
    else:
        FBA = 1
        per0 = 2.0 / (1 + BackPeriod)
        per1 = 2.0 / (1 + FrontPeriod)
    per3 = 2.0 / (1 + SourcePeriod)
    min_rates_total = _int(SourcePeriod + 1 + 1)
    SetIndexBuffer(0, VltBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(VltBuffer, True)
    SetIndexBuffer(1, SigBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SigBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_ema0, _s_OnCalculate_prev_ema1
    if (Source > VOLUME and BarsCalculated(Ind_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ema0 = 0.0
    ema1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        if Source == VOLUME:
            if VolumeType == VOLUME_TICK:
                _s_OnCalculate_prev_ema1 = float(tick_volume[min_rates_total])
            else:
                _s_OnCalculate_prev_ema1 = float(volume[min_rates_total])
        else:
            _s_OnCalculate_prev_ema1 = 0.0
        _s_OnCalculate_prev_ema0 = _s_OnCalculate_prev_ema1
    else:
        limit = rates_total - prev_calculated
    if Source > VOLUME:
        to_copy = limit + 1
        if CopyBuffer(Ind_Handle, 0, 0, to_copy, VltBuffer) <= 0:
            return 0
    else:
        if VolumeType == VOLUME_TICK:
            ArraySetAsSeries(tick_volume, True)
            bar = limit
            for bar in range(bar, 0 - 1, -1):
                VltBuffer[bar] = EMA_FBA(tick_volume[bar], VltBuffer[bar + 1], per3, 0)
            else:
                bar = _range_end(bar, 0 - 1, -1)
        else:
            ArraySetAsSeries(volume, True)
            bar = limit
            for bar in range(bar, 0 - 1, -1):
                VltBuffer[bar] = EMA_FBA(volume[bar], VltBuffer[bar + 1], per3, 0)
            else:
                bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ema0 = EMA_FBA(VltBuffer[bar], _s_OnCalculate_prev_ema0, per0, 0)
        ema1 = EMA_FBA(ema0, _s_OnCalculate_prev_ema1, per1, FBA)
        SigBuffer[bar] = MathMax(ema1, sens)
        if bar:
            _s_OnCalculate_prev_ema0 = ema0
            _s_OnCalculate_prev_ema1 = ema1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def EMA_FBA(Series_, EMA1, period, fba):
    if period == 1:
        return Series_
    if period > 1:
        period = _fdiv(2.0, 1 + period)
    EMA = (period * Series_) + ((1 - period) * EMA1)
    _sw2 = fba
    if _sw2 == 0:
        return EMA
    elif _sw2 == 1:
        if Series_ > EMA1:
            return EMA
        else:
            return Series_
    elif _sw2 == -1:
        if Series_ < EMA1:
            return EMA
        else:
            return Series_
    return EMA

# ---- static local variables
_s_OnCalculate_prev_ema0 = 0.0
_s_OnCalculate_prev_ema1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityFbaNr(_MQL5Indicator):
    name = 'volatility_fba_nr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Source': _Choice({0: 'volume', 1: 'ATR', 2: 'StDev'}, default=1),  # source
        'SourcePeriod': 22,  # source period
        'FrontPeriod': 1,  # front smoothing period; <1
        'BackPeriod': 444,  # damping smoothing period; <1
        'Sens': 0,  # sensitivity threshold in points or in ticks (for volume)
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

