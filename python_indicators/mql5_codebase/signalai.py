"""SignalAI — converted from MQL5: MQL5 Indicators/SignalAI - Indicator/SignalAI.mq5

Copyright: Copyright 2025, Signal AI; Link: https://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Signal AI', 'link': 'https://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'SignalAI', 'source': 'MQL5 Indicators/SignalAI - Indicator/SignalAI.mq5', 'folder': 'SignalAI - Indicator', 'inputs': [{'mql': 'FastLength', 'py': 'FastLength', 'param': 'FastLength', 'type': 'int', 'default': 9, 'label': 'Fast MA Length', 'sinput': False}, {'mql': 'SlowLength', 'py': 'SlowLength', 'param': 'SlowLength', 'type': 'int', 'default': 21, 'label': 'Slow MA Length', 'sinput': False}, {'mql': 'RsiLength', 'py': 'RsiLength', 'param': 'RsiLength', 'type': 'int', 'default': 14, 'label': 'RSI Length', 'sinput': False}, {'mql': 'ConfidenceThreshold', 'py': 'ConfidenceThreshold', 'param': 'ConfidenceThreshold', 'type': 'int', 'default': 75, 'label': 'Min Confidence % (0-100)', 'sinput': False}, {'mql': 'RangeFilterEnabled', 'py': 'RangeFilterEnabled', 'param': 'RangeFilterEnabled', 'type': 'bool', 'default': True, 'label': 'Enable Range Filter?', 'sinput': False}, {'mql': 'AtrLength', 'py': 'AtrLength', 'param': 'AtrLength', 'type': 'int', 'default': 14, 'label': 'ATR Length', 'sinput': False}, {'mql': 'MinATR', 'py': 'MinATR', 'param': 'MinATR', 'type': 'double', 'default': 1.5, 'label': 'Min ATR (Volatility Threshold)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastLength = _input('FastLength', 9)  # Fast MA Length
SlowLength = _input('SlowLength', 21)  # Slow MA Length
RsiLength = _input('RsiLength', 14)  # RSI Length
ConfidenceThreshold = _input('ConfidenceThreshold', 75)  # Min Confidence % (0-100)
RangeFilterEnabled = _input('RangeFilterEnabled', True)  # Enable Range Filter?
AtrLength = _input('AtrLength', 14)  # ATR Length
MinATR = _input('MinATR', 1.5)  # Min ATR (Volatility Threshold)
FastMABuffer = Arr(0, 0.0)
SlowMABuffer = Arr(0, 0.0)
BuySignalBuffer = Arr(0, 0.0)
SellSignalBuffer = Arr(0, 0.0)
ConfidenceBuffer = Arr(0, 0.0)
AtrBuffer = Arr(0, 0.0)
rsiHandle = 0
atrHandle = 0
stochHandle = 0
fastMaHandle = 0
slowMaHandle = 0

def OnInit():
    global atrHandle, fastMaHandle, rsiHandle, slowMaHandle, stochHandle
    SetIndexBuffer(0, FastMABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SlowMABuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BuySignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, SellSignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ConfidenceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, AtrBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(FastMABuffer, True)
    ArraySetAsSeries(SlowMABuffer, True)
    ArraySetAsSeries(BuySignalBuffer, True)
    ArraySetAsSeries(SellSignalBuffer, True)
    ArraySetAsSeries(ConfidenceBuffer, True)
    ArraySetAsSeries(AtrBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, clrRoyalBlue)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, clrDarkOrange)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(2, PLOT_ARROW, 233)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, clrLime)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(3, PLOT_ARROW, 234)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, clrRed)
    rsiHandle = iRSI(None, 0, RsiLength, PRICE_CLOSE)
    atrHandle = iATR(None, 0, AtrLength)
    stochHandle = iStochastic(None, 0, 14, 3, 3, MODE_SMA, STO_LOWHIGH)
    fastMaHandle = iMA(None, 0, FastLength, 0, MODE_EMA, PRICE_CLOSE)
    slowMaHandle = iMA(None, 0, SlowLength, 0, MODE_EMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < MathMax(FastLength, MathMax(SlowLength, MathMax(RsiLength, AtrLength))):
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    CopyBuffer(fastMaHandle, 0, 0, limit, FastMABuffer)
    CopyBuffer(slowMaHandle, 0, 0, limit, SlowMABuffer)
    for i in range(limit - 1, 0 - 1, -1):
        rsi = Arr(1, 0.0, dyn=False)
        stochK = Arr(1, 0.0, dyn=False)
        stochD = Arr(1, 0.0, dyn=False)
        atr = Arr(1, 0.0, dyn=False)
        CopyBuffer(rsiHandle, 0, i, 1, rsi)
        CopyBuffer(stochHandle, 0, i, 1, stochK)
        CopyBuffer(atrHandle, 0, i, 1, atr)
        ConfidenceBuffer[i] = (rsi[0] + stochK[0]) / 2.0
        AtrBuffer[i] = atr[0]
        isVolatileEnough = AtrBuffer[i] >= MinATR or (not RangeFilterEnabled)
        trendUp = FastMABuffer[i] > SlowMABuffer[i]
        trendDown = FastMABuffer[i] < SlowMABuffer[i]
        BuySignalBuffer[i] = EMPTY_VALUE
        SellSignalBuffer[i] = EMPTY_VALUE
        if (ConfidenceBuffer[i] >= ConfidenceThreshold and trendUp) and isVolatileEnough:
            BuySignalBuffer[i] = low[i] - (10 * Point())
        if (ConfidenceBuffer[i] <= (100 - ConfidenceThreshold) and trendDown) and isVolatileEnough:
            SellSignalBuffer[i] = high[i] + (10 * Point())
    if prev_calculated == 0:
        text = 'Confidence: ' + DoubleToString(ConfidenceBuffer[0], 1) + '%'
        ObjectCreate(0, 'ConfidenceLabel', OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, 'ConfidenceLabel', OBJPROP_CORNER, CORNER_RIGHT_UPPER)
        ObjectSetInteger(0, 'ConfidenceLabel', OBJPROP_XDISTANCE, 10)
        ObjectSetInteger(0, 'ConfidenceLabel', OBJPROP_YDISTANCE, 20)
        ObjectSetInteger(0, 'ConfidenceLabel', OBJPROP_COLOR, clrWhite)
        ObjectSetInteger(0, 'ConfidenceLabel', OBJPROP_BGCOLOR, clrRoyalBlue)
        ObjectSetInteger(0, 'ConfidenceLabel', OBJPROP_BACK, False)
        ObjectSetString(0, 'ConfidenceLabel', OBJPROP_TEXT, text)
        ObjectSetString(0, 'ConfidenceLabel', OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, 'ConfidenceLabel', OBJPROP_FONTSIZE, 10)
    return rates_total

def OnDeinit(reason):
    ObjectsDeleteAll(0, -1, OBJ_LABEL)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SignalAI(_MQL5Indicator):
    name = 'SignalAI'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastLength': 9,  # Fast MA Length
        'SlowLength': 21,  # Slow MA Length
        'RsiLength': 14,  # RSI Length
        'ConfidenceThreshold': 75,  # Min Confidence % (0-100)
        'RangeFilterEnabled': True,  # Enable Range Filter?
        'AtrLength': 14,  # ATR Length
        'MinATR': 1.5,  # Min ATR (Volatility Threshold)
    }

