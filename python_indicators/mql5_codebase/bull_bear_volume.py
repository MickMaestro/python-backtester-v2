"""Bull Bear Volume — converted from MQL5: MQL5 Indicators/Bull Bear Volume/Bull Bear Volume.mq5

Copyright: Nick Molchanoff; Link: https://www.WiseStockTrader.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Nick Molchanoff', 'link': 'https://www.WiseStockTrader.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 17, 'indicator_plots': 8}, 'types': {1: 3, 2: 3, 3: 3, 4: 1, 5: 8, 6: 8, 7: 1, 8: 10}, 'colors': {1: [16777215], 2: [32768], 3: [255], 4: [16777215], 5: [32768, 4294967295], 6: [255, 4294967295], 7: [16711935], 8: [10025880, 13353215]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, 'labels': {1: 'Total Volume MA', 2: 'Bull Volume MA', 3: 'Bear Volume MA', 4: 'Total Volume MA Line', 5: 'Bull Volume MA Line', 6: 'Bear Volume MA Line', 7: 'Convergence Oscillator', 8: 'Rise/Fall Shadows'}, 'levels': [], 'description': [], 'name': 'Bull Bear Volume', 'source': 'MQL5 Indicators/Bull Bear Volume/Bull Bear Volume.mq5', 'folder': 'Bull Bear Volume', 'inputs': [{'mql': 'VolPer', 'py': 'VolPer', 'param': 'VolPer', 'type': 'int', 'default': 34, 'label': 'TEMA period for volume (bull, bear, total)', 'sinput': False}, {'mql': 'ConvPer', 'py': 'ConvPer', 'param': 'ConvPer', 'type': 'int', 'default': 9, 'label': 'TEMA period for convergence oscillator', 'sinput': False}, {'mql': 'ShowOscillatorOnly', 'py': 'ShowOscillatorOnly', 'param': 'ShowOscillatorOnly', 'type': 'bool', 'default': False, 'label': 'Show only convergence oscillator', 'sinput': False}, {'mql': 'ShowBullLevel', 'py': 'ShowBullLevel', 'param': 'ShowBullLevel', 'type': 'bool', 'default': True, 'label': 'Show horizontal line at current bull volume MA', 'sinput': False}, {'mql': 'ShowBearLevel', 'py': 'ShowBearLevel', 'param': 'ShowBearLevel', 'type': 'bool', 'default': True, 'label': 'Show horizontal line at current bull volume MA', 'sinput': False}, {'mql': 'ShowBullVolume', 'py': 'ShowBullVolume', 'param': 'ShowBullVolume', 'type': 'bool', 'default': True, 'label': 'Show bull volume histogram and line', 'sinput': False}, {'mql': 'ShowBearVolume', 'py': 'ShowBearVolume', 'param': 'ShowBearVolume', 'type': 'bool', 'default': True, 'label': 'Show bear volume histogram and line', 'sinput': False}, {'mql': 'ShowTotalVolume', 'py': 'ShowTotalVolume', 'param': 'ShowTotalVolume', 'type': 'bool', 'default': True, 'label': 'Show total volume histogram and line', 'sinput': False}, {'mql': 'ShowConvergenceOscillator', 'py': 'ShowConvergenceOscillator', 'param': 'ShowConvergenceOscillator', 'type': 'bool', 'default': False, 'label': 'Show convergence oscillator', 'sinput': False}, {'mql': 'ShowRiseFallShadows', 'py': 'ShowRiseFallShadows', 'param': 'ShowRiseFallShadows', 'type': 'bool', 'default': False, 'label': 'Show rise/fall shadows', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
use_multi_timeframe = False  # Enable multitimeframe mode
timeframe = PERIOD_D1  # Timeframe to examine
VolPer = _input('VolPer', 34)  # TEMA period for volume (bull, bear, total)
ConvPer = _input('ConvPer', 9)  # TEMA period for convergence oscillator
ShowOscillatorOnly = _input('ShowOscillatorOnly', False)  # Show only convergence oscillator
ShowBullLevel = _input('ShowBullLevel', True)  # Show horizontal line at current bull volume MA
ShowBearLevel = _input('ShowBearLevel', True)  # Show horizontal line at current bull volume MA
ShowBullVolume = _input('ShowBullVolume', True)  # Show bull volume histogram and line
ShowBearVolume = _input('ShowBearVolume', True)  # Show bear volume histogram and line
ShowTotalVolume = _input('ShowTotalVolume', True)  # Show total volume histogram and line
ShowConvergenceOscillator = _input('ShowConvergenceOscillator', False)  # Show convergence oscillator
ShowRiseFallShadows = _input('ShowRiseFallShadows', False)  # Show rise/fall shadows
TotalVolMABuffer = Arr(0, 0.0)  # Total volume TEMA (white histogram)
BullVolMABuffer = Arr(0, 0.0)  # Bull volume TEMA (green histogram)
BearVolMABuffer = Arr(0, 0.0)  # Bear volume TEMA (red histogram)
TotalVolMALineBuffer = Arr(0, 0.0)  # Total volume TEMA line (white line)
BullVolMALineBuffer = Arr(0, 0.0)  # Bull volume TEMA or level (green line)
BearVolMALineBuffer = Arr(0, 0.0)  # Bear volume TEMA or level (red line)
BullVolMAColBuffer = Arr(0, 0.0)  # Bull volume TEMA or level (green line)
BearVolMAColBuffer = Arr(0, 0.0)  # Bear volume TEMA or level (red line)
ConvergenceBuffer = Arr(0, 0.0)  # Convergence oscillator (magenta line)
UpVolBuffer = Arr(0, 0.0)  # D1 bullish volume
DownVolBuffer = Arr(0, 0.0)  # D1 bearish volume
ShadowBuffer = Arr(0, 0.0)  # Rise/fall shadows histogram
ShadowColorBuffer = Arr(0, 0.0)  # Shadow colors (0: pale green, 1: pink)
temp_buffer = Arr(0, 0.0)
ema1 = Arr(0, 0.0)
ema2 = Arr(0, 0.0)
ema3 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, TotalVolMABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BullVolMABuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BearVolMABuffer, INDICATOR_DATA)
    SetIndexBuffer(3, TotalVolMALineBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, BullVolMALineBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, BullVolMAColBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, BearVolMALineBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, BearVolMAColBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, ConvergenceBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, ShadowBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, ShadowColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(11, UpVolBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, DownVolBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, temp_buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, ema1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, ema2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, ema3, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TotalVolMABuffer, True)
    ArraySetAsSeries(BullVolMABuffer, True)
    ArraySetAsSeries(BearVolMABuffer, True)
    ArraySetAsSeries(TotalVolMALineBuffer, True)
    ArraySetAsSeries(BullVolMALineBuffer, True)
    ArraySetAsSeries(BearVolMALineBuffer, True)
    ArraySetAsSeries(ConvergenceBuffer, True)
    ArraySetAsSeries(UpVolBuffer, True)
    ArraySetAsSeries(DownVolBuffer, True)
    ArraySetAsSeries(ShadowBuffer, True)
    ArraySetAsSeries(ShadowColorBuffer, True)
    ArraySetAsSeries(BearVolMAColBuffer, True)
    ArraySetAsSeries(BullVolMAColBuffer, True)
    ArraySetAsSeries(temp_buffer, True)
    ArraySetAsSeries(ema1, True)
    ArraySetAsSeries(ema2, True)
    ArraySetAsSeries(ema3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, (('BullBearVolume' + '(' + timeframeToString(timeframe) + ')') if use_multi_timeframe else 'BullBearVolume(Current)'))
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, ConvPer)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, ConvPer)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGreen)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_SOLID)
    return INIT_SUCCEEDED

def CalculateTEMA(inp, period, output, prev_calculated):
    alpha = _fdiv(2.0, period + 1)
    limit = ((period * 3) if (prev_calculated < (period * 3)) else (prev_calculated - 1))
    for i in range(limit - 1, 0 - 1, -1):
        if i == (limit - 1):
            ema1[i] = inp[i]
            ema2[i] = inp[i]
            ema3[i] = inp[i]
        else:
            ema1[i] = (inp[i] * alpha) + (ema1[i + 1] * (1 - alpha))
            ema2[i] = (ema1[i] * alpha) + (ema2[i + 1] * (1 - alpha))
            ema3[i] = (ema2[i] * alpha) + (ema3[i + 1] * (1 - alpha))
        output[i] = (3 * ema1[i]) - (3 * ema2[i]) + ema3[i]

def timeframeToString(TF):
    _sw1 = TF
    if _sw1 == PERIOD_CURRENT:
        return 'Current'
    elif _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M2:
        return 'M2'
    elif _sw1 == PERIOD_M3:
        return 'M3'
    elif _sw1 == PERIOD_M4:
        return 'M4'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M6:
        return 'M6'
    elif _sw1 == PERIOD_M10:
        return 'M10'
    elif _sw1 == PERIOD_M12:
        return 'M12'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M20:
        return 'M20'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H2:
        return 'H2'
    elif _sw1 == PERIOD_H3:
        return 'H3'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_H6:
        return 'H6'
    elif _sw1 == PERIOD_H8:
        return 'H8'
    elif _sw1 == PERIOD_H12:
        return 'H12'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Current'

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < ((VolPer * 3) + (ConvPer * 3) + 1):
        return prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(tick_volume, True)
    barsToUse = (rates_total if (prev_calculated < 0 or prev_calculated > rates_total) else (rates_total - prev_calculated + 1))
    if prev_calculated == 0:
        ArrayInitialize(UpVolBuffer, 0.0)
        ArrayInitialize(DownVolBuffer, 0.0)
        ArrayInitialize(temp_buffer, 0.0)
        ArrayInitialize(ema1, 0.0)
        ArrayInitialize(ema2, 0.0)
        ArrayInitialize(ema3, 0.0)
        ArrayInitialize(TotalVolMABuffer, EMPTY_VALUE)
        ArrayInitialize(BullVolMABuffer, EMPTY_VALUE)
        ArrayInitialize(BearVolMABuffer, EMPTY_VALUE)
        ArrayInitialize(TotalVolMALineBuffer, EMPTY_VALUE)
        ArrayInitialize(BullVolMALineBuffer, EMPTY_VALUE)
        ArrayInitialize(BearVolMALineBuffer, EMPTY_VALUE)
        ArrayInitialize(ConvergenceBuffer, EMPTY_VALUE)
        ArrayInitialize(ShadowBuffer, EMPTY_VALUE)
    dailyOpen = Arr(0, 0.0)
    dailyClose = Arr(0, 0.0)
    dailyVolume = Arr(0, 0)
    if use_multi_timeframe:
        ArraySetAsSeries(dailyOpen, True)
        ArraySetAsSeries(dailyClose, True)
        ArraySetAsSeries(dailyVolume, True)
        if (CopyOpen(Symbol(), timeframe, 0, barsToUse, dailyOpen) <= 0 or CopyClose(Symbol(), timeframe, 0, barsToUse, dailyClose) <= 0) or CopyTickVolume(Symbol(), timeframe, 0, barsToUse, dailyVolume) <= 0:
            Print('Failed to fetch data')
            return prev_calculated
    else:
        ArraySetAsSeries(dailyOpen, True)
        ArraySetAsSeries(dailyClose, True)
        ArraySetAsSeries(dailyVolume, True)
        ArrayCopy(dailyOpen, open)
        ArrayCopy(dailyClose, close)
        ArrayCopy(dailyVolume, tick_volume)
    limit = ((VolPer * 3) if (prev_calculated < (VolPer * 3)) else (prev_calculated - 1))
    shadowLimit = ((ConvPer * 3) if (prev_calculated < (ConvPer * 3)) else (prev_calculated - 1))
    for i in range(limit - 1, 0 - 1, -1):
        d1Index = -1
        if use_multi_timeframe:
            d1Index = iBarShift(Symbol(), timeframe, time[i], False)
            if d1Index < 0 or d1Index >= barsToUse:
                UpVolBuffer[i] = 0.0
                DownVolBuffer[i] = 0.0
                continue
        else:
            d1Index = i
        uc = False
        dc = False
        ud = False
        dd = False
        uc = close[i] > close[i + 1]
        dc = close[i] <= close[i + 1]
        ud = dailyClose[d1Index] > dailyOpen[d1Index]
        dd = dailyClose[d1Index] <= dailyOpen[d1Index]
        vType = 0
        if ud and uc:
            vType = 1
        elif ud and dc:
            vType = 3
        elif dd and dc:
            vType = 4
        elif dd and uc:
            vType = 2
        else:
            vType = 5
        UpVolBuffer[i] = 0.0
        DownVolBuffer[i] = 0.0
        if vType == 1 or vType == 2:
            UpVolBuffer[i] = float(dailyVolume[d1Index])
        if vType == 3 or vType == 4:
            DownVolBuffer[i] = float(dailyVolume[d1Index])
        BearVolMAColBuffer[i] = (1 if (BullVolMABuffer[i] > BearVolMABuffer[i]) else 0)
        BullVolMAColBuffer[i] = (1 if (BearVolMABuffer[i] > BullVolMABuffer[i]) else 0)
    if ShowTotalVolume and (not ShowOscillatorOnly):
        for i in range(limit - 1, 0 - 1, -1):
            d1Index = (iBarShift(Symbol(), timeframe, time[i], False) if use_multi_timeframe else i)
            if use_multi_timeframe:
                temp_buffer[i] = (float(dailyVolume[d1Index]) if (d1Index >= 0 and d1Index < barsToUse) else 0.0)
            else:
                temp_buffer[i] = float(tick_volume[i])
        CalculateTEMA(temp_buffer, VolPer, TotalVolMABuffer, prev_calculated)
        ArrayCopy(TotalVolMALineBuffer, TotalVolMABuffer, 0, 0, limit + 1)
    if ShowBullVolume and (not ShowOscillatorOnly):
        CalculateTEMA(UpVolBuffer, VolPer, BullVolMABuffer, prev_calculated)
        ArrayCopy(BullVolMALineBuffer, BullVolMABuffer, 0, 0, limit + 1)
    if ShowBearVolume and (not ShowOscillatorOnly):
        CalculateTEMA(DownVolBuffer, VolPer, BearVolMABuffer, prev_calculated)
        ArrayCopy(BearVolMALineBuffer, BearVolMABuffer, 0, 0, limit + 1)
    if (ShowConvergenceOscillator or ShowOscillatorOnly) or ShowRiseFallShadows:
        for i in range(limit - 1, 0 - 1, -1):
            temp_buffer[i] = BullVolMABuffer[i] - BearVolMABuffer[i]
        CalculateTEMA(temp_buffer, ConvPer, ConvergenceBuffer, prev_calculated)
    if ShowRiseFallShadows:
        for i in range(shadowLimit - 1, 0 - 1, -1):
            convergeUp = ConvergenceBuffer[i] > (ConvergenceBuffer[i + 1] if ((i + 1) < rates_total) else ConvergenceBuffer[i])
            convergeOver = ConvergenceBuffer[i] > 0
            rising = convergeUp and convergeOver
            falling = (not convergeUp) and convergeOver
            ShadowBuffer[i] = (ConvergenceBuffer[i] if (rising or falling) else 0.0)
            ShadowColorBuffer[i] = (0 if rising else 1)
    if ShowBearLevel and (not ShowOscillatorOnly):
        selectedBear = BearVolMABuffer[0]
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, selectedBear)
    if ShowBullLevel and (not ShowOscillatorOnly):
        selectedBull = BullVolMABuffer[0]
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, selectedBull)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BullBearVolume(_MQL5Indicator):
    name = 'Bull Bear Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'VolPer': 34,  # TEMA period for volume (bull, bear, total)
        'ConvPer': 9,  # TEMA period for convergence oscillator
        'ShowOscillatorOnly': False,  # Show only convergence oscillator
        'ShowBullLevel': True,  # Show horizontal line at current bull volume MA
        'ShowBearLevel': True,  # Show horizontal line at current bull volume MA
        'ShowBullVolume': True,  # Show bull volume histogram and line
        'ShowBearVolume': True,  # Show bear volume histogram and line
        'ShowTotalVolume': True,  # Show total volume histogram and line
        'ShowConvergenceOscillator': False,  # Show convergence oscillator
        'ShowRiseFallShadows': False,  # Show rise/fall shadows
    }

