"""ravi_fx_fisher — converted from MQL5: MQL5 Indicators/RAVI_FX_Fisher/ravi_fx_fisher.mq5

Copyright: Copyright © 2005, Luis Guilherme Damiani; Link: http://www.damianifx.com.br; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Luis Guilherme Damiani', 'link': 'http://www.damianifx.com.br', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 9639167, 8421504, 16711680, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RAVI FX Fisher'}, 'levels': [], 'description': [], 'name': 'ravi_fx_fisher', 'source': 'MQL5 Indicators/RAVI_FX_Fisher/ravi_fx_fisher.mq5', 'folder': 'RAVI_FX_Fisher', 'inputs': [{'mql': 'MAfast', 'py': 'MAfast', 'param': 'MAfast', 'type': 'int', 'default': 4, 'label': 'fast moving average period', 'sinput': False}, {'mql': 'MAslow', 'py': 'MAslow', 'param': 'MAslow', 'type': 'int', 'default': 49, 'label': 'slow moving average period', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': 'smoothing method', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'price', 'sinput': False}, {'mql': 'UpTrigger', 'py': 'UpTrigger', 'param': 'UpTrigger', 'type': 'double', 'default': 0.07, 'label': 'breakthrough levelь', 'sinput': False}, {'mql': 'DnTrigger', 'py': 'DnTrigger', 'param': 'DnTrigger', 'type': 'double', 'default': -0.07, 'label': 'breakthrough level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAfast = _input('MAfast', 4)  # fast moving average period
MAslow = _input('MAslow', 49)  # slow moving average period
MAType = _input('MAType', MODE_EMA)  # smoothing method
MAPrice = _input('MAPrice', PRICE_CLOSE)  # price
UpTrigger = _input('UpTrigger', 0.07)  # breakthrough levelь
DnTrigger = _input('DnTrigger', -0.07)  # breakthrough level
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
FsATR_Handle = 0
SlATR_Handle = 0
FsMA_Handle = 0
SlMA_Handle = 0

def OnInit():
    global FsATR_Handle, FsMA_Handle, SlATR_Handle, SlMA_Handle, min_rates_total
    min_rates_total = MathMax(MAfast, MAslow)
    FsATR_Handle = iATR(None, PERIOD_CURRENT, MAslow)
    if FsATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SlATR_Handle = iATR(None, PERIOD_CURRENT, MAslow)
    if SlATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    FsMA_Handle = iMA(None, 0, MAfast, 0, MAType, MAPrice)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SlMA_Handle = iMA(None, 0, MAslow, 0, MAType, MAPrice)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RAVI FX Fisher')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpTrigger)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, DnTrigger)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(FsMA_Handle) < rates_total or BarsCalculated(SlMA_Handle) < rates_total) or BarsCalculated(FsATR_Handle) < rates_total) or BarsCalculated(SlATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    MAValue = 0.0
    IFish0 = 0.0
    IFish1 = 0.0
    FsMA = Arr(0, 0.0)
    SlMA = Arr(0, 0.0)
    FsATR = Arr(0, 0.0)
    SlATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FsMA) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlMA) <= 0:
        return 0
    if CopyBuffer(FsATR_Handle, 0, 0, to_copy, FsATR) <= 0:
        return 0
    if CopyBuffer(SlATR_Handle, 0, 0, to_copy, SlATR) <= 0:
        return 0
    ArraySetAsSeries(FsMA, True)
    ArraySetAsSeries(SlMA, True)
    ArraySetAsSeries(SlATR, True)
    ArraySetAsSeries(FsATR, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        MAValue = _fdiv(_fdiv(100 * (FsMA[bar] - SlMA[bar]) * FsATR[bar], SlMA[bar]), SlATR[bar])
        IFish0 = _fdiv(MathExp(2 * MAValue) - 1.0, MathExp(2 * MAValue) + 1.0)
        IndBuffer[bar] = IFish0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        IFish0 = IndBuffer[bar]
        IFish1 = IndBuffer[bar + 1]
        if IFish0 > UpTrigger:
            if IFish0 > IFish1:
                clr = 4
            if IFish0 < IFish1:
                clr = 3
        if IFish0 < DnTrigger:
            if IFish0 < IFish1:
                clr = 0
            if IFish0 > IFish1:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RaviFxFisher(_MQL5Indicator):
    name = 'ravi_fx_fisher'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAfast': 4,  # fast moving average period
        'MAslow': 49,  # slow moving average period
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # smoothing method
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # price
        'UpTrigger': 0.07,  # breakthrough levelь
        'DnTrigger': -0.07,  # breakthrough level
    }

