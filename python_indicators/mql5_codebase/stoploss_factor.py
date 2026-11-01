"""stoploss_factor — converted from MQL5: MQL5 Indicators/ATR Stop Loss bands/stoploss_factor.mq5

Copyright: Copyright 2022, mr_schmidt.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, mr_schmidt.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Stop Loss Upper', 2: 'Stop Loss Lower'}, 'levels': [], 'description': [], 'name': 'stoploss_factor', 'source': 'MQL5 Indicators/ATR Stop Loss bands/stoploss_factor.mq5', 'folder': 'ATR Stop Loss bands', 'inputs': [{'mql': 'InpATRPeriod', 'py': 'InpATRPeriod', 'param': 'InpATRPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpATRPercent', 'py': 'InpATRPercent', 'param': 'InpATRPercent', 'type': 'double', 'default': 1.5, 'label': 'ATR factor', 'sinput': False}, {'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 1, 'label': 'MA period (keep at 1 for standard price action)', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 0, 'label': 'MA method (keep at SMA for standard price action)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpATRPeriod = _input('InpATRPeriod', 14)  # ATR period
InpATRPercent = _input('InpATRPercent', 1.5)  # ATR factor
InpMAPeriod = _input('InpMAPeriod', 1)  # MA period (keep at 1 for standard price action)
InpMAMethod = _input('InpMAMethod', MODE_SMA)  # MA method (keep at SMA for standard price action)
BufferMA = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferMAUpper = Arr(0, 0.0)
BufferMALower = Arr(0, 0.0)
MaxPeriod = 0
HandleMA = 0
HandleATR = 0

def OnInit():
    global HandleATR, HandleMA, MaxPeriod
    SetIndexBuffer(0, BufferMAUpper, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, BufferMALower, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(3, BufferATR, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    MaxPeriod = _int(MathMax(MathMax(InpATRPeriod, InpATRPercent), InpMAPeriod))
    HandleATR = iATR(Symbol(), PERIOD_CURRENT, InpATRPeriod)
    HandleMA = iMA(Symbol(), PERIOD_CURRENT, InpMAPeriod, 0, InpMAMethod, PRICE_OPEN)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MaxPeriod)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if False:
        return 0
    if rates_total < MaxPeriod:
        return 0
    if BarsCalculated(HandleATR) < rates_total:
        return 0
    if BarsCalculated(HandleMA) < rates_total:
        return 0
    copyBars = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        copyBars = rates_total
    else:
        copyBars = rates_total - prev_calculated
        if prev_calculated > 0:
            copyBars += 1
    for i in range(1, rates_total):
        BufferMAUpper[i] = NormalizeDouble(BufferMA[i] + (BufferATR[i] * InpATRPercent), Digits())
        BufferMALower[i] = NormalizeDouble(BufferMA[i] - (BufferATR[i] * InpATRPercent), Digits())
    if False:
        return 0
    if CopyBuffer(HandleMA, 0, 0, copyBars, BufferMA) <= 0:
        return 0
    if CopyBuffer(HandleATR, 0, 0, copyBars, BufferATR) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StoplossFactor(_MQL5Indicator):
    name = 'stoploss_factor'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpATRPeriod': 14,  # ATR period
        'InpATRPercent': 1.5,  # ATR factor
        'InpMAPeriod': 1,  # MA period (keep at 1 for standard price action)
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method (keep at SMA for standard price action)
    }

