"""AlphaTrend — converted from MQL5: MQL5 Indicators/AlphaTrend/AlphaTrend.mq5

Copyright: Mahmut Deniz; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Mahmut Deniz', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [6908265, 32768, 255], 2: [32768], 3: [255]}, 'widths': {1: 3, 2: 1, 3: 1}, 'styles': {1: 0}, 'labels': {1: 'AlphaTrend', 2: 'Buy Signal', 3: 'Sell Signal'}, 'levels': [], 'description': [], 'name': 'AlphaTrend', 'source': 'MQL5 Indicators/AlphaTrend/AlphaTrend.mq5', 'folder': 'AlphaTrend', 'inputs': [{'mql': 'Multiplier', 'py': 'Multiplier', 'param': 'Multiplier', 'type': 'double', 'default': 1.0, 'label': 'Multiplier', 'sinput': False}, {'mql': 'CommonPeriod', 'py': 'CommonPeriod', 'param': 'CommonPeriod', 'type': 'int', 'default': 14, 'label': 'Common Period', 'sinput': False}, {'mql': 'ShowSignals', 'py': 'ShowSignals', 'param': 'ShowSignals', 'type': 'bool', 'default': False, 'label': 'Show Signals?', 'sinput': False}, {'mql': 'NoVolumeData', 'py': 'NoVolumeData', 'param': 'NoVolumeData', 'type': 'bool', 'default': False, 'label': 'Change calculation (no volume data)?', 'sinput': False}, {'mql': 'PriceType', 'py': 'PriceType', 'param': 'PriceType', 'type': 'int', 'default': 1, 'label': 'Applied Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Multiplier = _input('Multiplier', 1.0)  # Multiplier
CommonPeriod = _input('CommonPeriod', 14)  # Common Period
ShowSignals = _input('ShowSignals', False)  # Show Signals?
NoVolumeData = _input('NoVolumeData', False)  # Change calculation (no volume data)?
PriceType = _input('PriceType', PRICE_CLOSE)  # Applied Price
AlphaTrendBuffer = Arr(0, 0.0)  # Main AlphaTrend buffer
ColorBuffer = Arr(0, 0.0)  # Color buffer
BuyBuffer = Arr(0, 0.0)  # Buy signals buffer
SellBuffer = Arr(0, 0.0)  # Sell signals buffer
ATRBuffer = Arr(0, 0.0)  # ATR buffer
RSIBuffer = Arr(0, 0.0)  # RSI buffer
MFIBuffer = Arr(0, 0.0)  # MFI buffer
PrevAlphaTrend = Arr(0, 0.0)  # Previous AlphaTrend values
atr_handle = 0  # ATR indicator handle
rsi_handle = 0  # RSI indicator handle
mfi_handle = 0  # MFI indicator handle

def OnInit():
    global atr_handle, mfi_handle, rsi_handle
    SetIndexBuffer(0, AlphaTrendBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BuyBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, SellBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ATRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, RSIBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, MFIBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, PrevAlphaTrend, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetInteger(2, PLOT_ARROW, 234)
    atr_handle = iATR(None, 0, CommonPeriod)
    rsi_handle = iRSI(None, 0, CommonPeriod, PriceType)
    mfi_handle = iMFI(None, 0, CommonPeriod, VOLUME_TICK)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < CommonPeriod:
        return 0
    start = ((prev_calculated - 1) if (prev_calculated > 0) else CommonPeriod)
    if CopyBuffer(atr_handle, 0, 0, rates_total, ATRBuffer) <= 0:
        return 0
    if CopyBuffer(rsi_handle, 0, 0, rates_total, RSIBuffer) <= 0:
        return 0
    if CopyBuffer(mfi_handle, 0, 0, rates_total, MFIBuffer) <= 0:
        return 0
    for i in range(start, rates_total):
        upT = low[i] - (ATRBuffer[i] * Multiplier)
        downT = high[i] + (ATRBuffer[i] * Multiplier)
        trend_condition = ((RSIBuffer[i] >= 50) if NoVolumeData else (MFIBuffer[i] >= 50))
        if trend_condition:
            AlphaTrendBuffer[i] = (AlphaTrendBuffer[i - 1] if (upT < AlphaTrendBuffer[i - 1]) else upT)
        else:
            AlphaTrendBuffer[i] = (AlphaTrendBuffer[i - 1] if (downT > AlphaTrendBuffer[i - 1]) else downT)
        PrevAlphaTrend[i] = AlphaTrendBuffer[i - 2]
        ColorBuffer[i] = (1 if (AlphaTrendBuffer[i] > PrevAlphaTrend[i]) else 2 if (AlphaTrendBuffer[i] < PrevAlphaTrend[i]) else 0)
        if ShowSignals:
            if AlphaTrendBuffer[i] > PrevAlphaTrend[i] and AlphaTrendBuffer[i - 1] <= PrevAlphaTrend[i - 1]:
                BuyBuffer[i] = low[i] * 0.9999
            else:
                BuyBuffer[i] = EMPTY_VALUE
            if AlphaTrendBuffer[i] < PrevAlphaTrend[i] and AlphaTrendBuffer[i - 1] >= PrevAlphaTrend[i - 1]:
                SellBuffer[i] = high[i] * 1.0001
            else:
                SellBuffer[i] = EMPTY_VALUE
    return rates_total

def OnDeinit(reason):
    IndicatorRelease(atr_handle)
    IndicatorRelease(rsi_handle)
    IndicatorRelease(mfi_handle)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlphaTrend(_MQL5Indicator):
    name = 'AlphaTrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Multiplier': 1.0,  # Multiplier
        'CommonPeriod': 14,  # Common Period
        'ShowSignals': False,  # Show Signals?
        'NoVolumeData': False,  # Change calculation (no volume data)?
        'PriceType': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price
    }

