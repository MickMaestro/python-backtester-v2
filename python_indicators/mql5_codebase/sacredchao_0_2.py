"""sacredchao-0_2 — converted from MQL5: MQL5 Indicators/Sacred Chao - Signals from Trading Chaos, 2nd Edition/sacredchao-0_2.mq5

Copyright: Copyleft 2014, Eristocrat; Link: http://eristocrat.has-no-homepage.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyleft 2014, Eristocrat', 'link': 'http://eristocrat.has-no-homepage.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 16, 'indicator_plots': 12}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 1, 11: 1, 12: 0}, 'colors': {1: [16711680], 2: [255], 3: [65280], 4: [32768], 5: [255], 6: [32768], 7: [255], 8: [32768], 9: [255], 10: [15631086], 11: [15631086]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 1, 11: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 2, 11: 2}, 'labels': {1: 'Jaws', 2: 'Teeth', 3: 'Lips', 4: 'BullishDivergentBar', 5: 'BearishDivergentBar', 6: 'BullishSuperAO', 7: 'BearishSuperAO', 8: 'BullishFractal', 9: 'BearishFractal', 10: 'TrailingMaxHigh', 11: 'TrailingMinLow', 12: 'Angulation Deviation'}, 'levels': [], 'description': [], 'name': 'sacredchao-0_2', 'source': 'MQL5 Indicators/Sacred Chao - Signals from Trading Chaos, 2nd Edition/sacredchao-0_2.mq5', 'folder': 'Sacred Chao - Signals from Trading Chaos, 2nd Edition', 'inputs': [{'mql': 'InpJawsPeriod', 'py': 'InpJawsPeriod', 'param': 'InpJawsPeriod', 'type': 'int', 'default': 13, 'label': 'Jaws period', 'sinput': False}, {'mql': 'InpJawsShift', 'py': 'InpJawsShift', 'param': 'InpJawsShift', 'type': 'int', 'default': 8, 'label': 'Jaws shift', 'sinput': False}, {'mql': 'InpTeethPeriod', 'py': 'InpTeethPeriod', 'param': 'InpTeethPeriod', 'type': 'int', 'default': 8, 'label': 'Teeth period', 'sinput': False}, {'mql': 'InpTeethShift', 'py': 'InpTeethShift', 'param': 'InpTeethShift', 'type': 'int', 'default': 5, 'label': 'Teeth shift', 'sinput': False}, {'mql': 'InpLipsPeriod', 'py': 'InpLipsPeriod', 'param': 'InpLipsPeriod', 'type': 'int', 'default': 5, 'label': 'Lips period', 'sinput': False}, {'mql': 'InpLipsShift', 'py': 'InpLipsShift', 'param': 'InpLipsShift', 'type': 'int', 'default': 3, 'label': 'Lips shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'Moving average method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 5, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpATRPeriod', 'py': 'InpATRPeriod', 'param': 'InpATRPeriod', 'type': 'int', 'default': 14, 'label': 'ATR Period', 'sinput': False}, {'mql': 'InpPendingAddATRFactor', 'py': 'InpPendingAddATRFactor', 'param': 'InpPendingAddATRFactor', 'type': 'double', 'default': 0.2, 'label': 'ATR*Factor added to pending orders', 'sinput': False}, {'mql': 'InpStopAddATRFactor', 'py': 'InpStopAddATRFactor', 'param': 'InpStopAddATRFactor', 'type': 'double', 'default': 0.5, 'label': 'ATR*Factor added to trailing stop', 'sinput': False}, {'mql': 'InpHLBars', 'py': 'InpHLBars', 'param': 'InpHLBars', 'type': 'int', 'default': 3, 'label': 'Trailing Highest High/Lowest Low of x bars', 'sinput': False}, {'mql': 'InpAngulationColor', 'py': 'InpAngulationColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Angulation color', 'sinput': False}, {'mql': 'InpAngulationStyle', 'py': 'InpAngulationStyle', 'param': 'InpAngulationStyle', 'type': 'int', 'default': 3, 'label': 'Angulation style', 'sinput': False}, {'mql': 'InpAngulationWidth', 'py': 'InpAngulationWidth', 'param': 'InpAngulationWidth', 'type': 'int', 'default': 1, 'label': 'Angulation width', 'sinput': False}, {'mql': 'InpURLArrowCode', 'py': 'InpURLArrowCode', 'param': None, 'type': 'string', 'default': 'http://www.mql5.com/en/docs/constants/objectconstants/wingdings', 'label': 'Find Arrowcodes here:', 'sinput': False}, {'mql': 'InpBuDBArrowCode', 'py': 'InpBuDBArrowCode', 'param': 'InpBuDBArrowCode', 'type': 'int', 'default': 236, 'label': 'Bullish Divergent Arrowcode', 'sinput': False}, {'mql': 'InpBeDBArrowCode', 'py': 'InpBeDBArrowCode', 'param': 'InpBeDBArrowCode', 'type': 'int', 'default': 238, 'label': 'Bearish Divergent Arrowcode', 'sinput': False}, {'mql': 'InpBuSAOArrowCode', 'py': 'InpBuSAOArrowCode', 'param': 'InpBuSAOArrowCode', 'type': 'int', 'default': 142, 'label': 'Bullish Super AO Arrowcode', 'sinput': False}, {'mql': 'InpBeSAOArrowCode', 'py': 'InpBeSAOArrowCode', 'param': 'InpBeSAOArrowCode', 'type': 'int', 'default': 142, 'label': 'Bearish Super AO Arrowcode', 'sinput': False}, {'mql': 'InpBuFrcArrowCode', 'py': 'InpBuFrcArrowCode', 'param': 'InpBuFrcArrowCode', 'type': 'int', 'default': 217, 'label': 'Bullish Fractal Arrowcode', 'sinput': False}, {'mql': 'InpBeFrcArrowCode', 'py': 'InpBeFrcArrowCode', 'param': 'InpBeFrcArrowCode', 'type': 'int', 'default': 218, 'label': 'Bearish Fractal Arrowcode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpJawsPeriod = _input('InpJawsPeriod', 13)  # Jaws period
InpJawsShift = _input('InpJawsShift', 8)  # Jaws shift
InpTeethPeriod = _input('InpTeethPeriod', 8)  # Teeth period
InpTeethShift = _input('InpTeethShift', 5)  # Teeth shift
InpLipsPeriod = _input('InpLipsPeriod', 5)  # Lips period
InpLipsShift = _input('InpLipsShift', 3)  # Lips shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # Moving average method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_MEDIAN)  # Applied price
InpATRPeriod = _input('InpATRPeriod', 14)  # ATR Period
InpPendingAddATRFactor = _input('InpPendingAddATRFactor', 0.2)  # ATR*Factor added to pending orders
InpStopAddATRFactor = _input('InpStopAddATRFactor', 0.5)  # ATR*Factor added to trailing stop
InpHLBars = _input('InpHLBars', 3)  # Trailing Highest High/Lowest Low of x bars
InpAngulationColor = _input('InpAngulationColor', clrMagenta)  # Angulation color
InpAngulationStyle = _input('InpAngulationStyle', STYLE_DASHDOT)  # Angulation style
InpAngulationWidth = _input('InpAngulationWidth', 1)  # Angulation width
InpURLArrowCode = _input('InpURLArrowCode', 'http://www.mql5.com/en/docs/constants/objectconstants/wingdings')  # Find Arrowcodes here:
InpBuDBArrowCode = _input('InpBuDBArrowCode', 236)  # Bullish Divergent Arrowcode
InpBeDBArrowCode = _input('InpBeDBArrowCode', 238)  # Bearish Divergent Arrowcode
InpBuSAOArrowCode = _input('InpBuSAOArrowCode', 142)  # Bullish Super AO Arrowcode
InpBeSAOArrowCode = _input('InpBeSAOArrowCode', 142)  # Bearish Super AO Arrowcode
InpBuFrcArrowCode = _input('InpBuFrcArrowCode', 217)  # Bullish Fractal Arrowcode
InpBeFrcArrowCode = _input('InpBeFrcArrowCode', 218)  # Bearish Fractal Arrowcode
JawsBuffer = Arr(0, 0.0)
TeethBuffer = Arr(0, 0.0)
LipsBuffer = Arr(0, 0.0)
BullishDivergentBarBuffer = Arr(0, 0.0)
BearishDivergentBarBuffer = Arr(0, 0.0)
BullishSuperAOBuffer = Arr(0, 0.0)
BearishSuperAOBuffer = Arr(0, 0.0)
BullishFractalBuffer = Arr(0, 0.0)
BearishFractalBuffer = Arr(0, 0.0)
TrailingMaxHighBuffer = Arr(0, 0.0)
TrailingMinLowBuffer = Arr(0, 0.0)
AOBuffer = Arr(0, 0.0)
ATRBuffer = Arr(0, 0.0)
AngulationBuffer = Arr(0, 0.0)
UpFractalsBuffer = Arr(0, 0.0)
DownFractalsBuffer = Arr(0, 0.0)
gJawsHandle = 0
gTeethHandle = 0
gLipsHandle = 0
gAOHandle = 0
gATRHandle = 0
gFractalsHandle = 0
gBarsMin = 0

def OnInit():
    global gAOHandle, gATRHandle, gBarsMin, gFractalsHandle, gJawsHandle, gLipsHandle, gTeethHandle
    SetIndexBuffer(0, JawsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, TeethBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LipsBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, BullishDivergentBarBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, BearishDivergentBarBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, BullishSuperAOBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, BearishSuperAOBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, BullishFractalBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, BearishFractalBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, TrailingMaxHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, TrailingMinLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(11, AOBuffer, INDICATOR_DATA)
    SetIndexBuffer(12, ATRBuffer, INDICATOR_DATA)
    SetIndexBuffer(13, AngulationBuffer, INDICATOR_DATA)
    SetIndexBuffer(14, UpFractalsBuffer, INDICATOR_DATA)
    SetIndexBuffer(15, DownFractalsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(JawsBuffer, True)
    ArraySetAsSeries(TeethBuffer, True)
    ArraySetAsSeries(LipsBuffer, True)
    ArraySetAsSeries(BullishDivergentBarBuffer, True)
    ArraySetAsSeries(BearishDivergentBarBuffer, True)
    ArraySetAsSeries(BullishSuperAOBuffer, True)
    ArraySetAsSeries(BearishSuperAOBuffer, True)
    ArraySetAsSeries(BullishFractalBuffer, True)
    ArraySetAsSeries(BearishFractalBuffer, True)
    ArraySetAsSeries(TrailingMaxHighBuffer, True)
    ArraySetAsSeries(TrailingMinLowBuffer, True)
    ArraySetAsSeries(AOBuffer, True)
    ArraySetAsSeries(ATRBuffer, True)
    ArraySetAsSeries(AngulationBuffer, True)
    ArraySetAsSeries(UpFractalsBuffer, True)
    ArraySetAsSeries(DownFractalsBuffer, True)
    PlotIndexSetInteger(3, PLOT_ARROW, InpBuDBArrowCode)
    PlotIndexSetInteger(4, PLOT_ARROW, InpBeDBArrowCode)
    PlotIndexSetInteger(5, PLOT_ARROW, InpBuSAOArrowCode)
    PlotIndexSetInteger(6, PLOT_ARROW, InpBeSAOArrowCode)
    PlotIndexSetInteger(7, PLOT_ARROW, InpBuFrcArrowCode)
    PlotIndexSetInteger(8, PLOT_ARROW, InpBeFrcArrowCode)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpJawsPeriod - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpTeethPeriod - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpLipsPeriod - 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpJawsShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, InpTeethShift)
    PlotIndexSetInteger(2, PLOT_SHIFT, InpLipsShift)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(10, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'Jaws(' + _str(InpJawsPeriod) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Teeth(' + _str(InpTeethPeriod) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Lips(' + _str(InpLipsPeriod) + ')')
    gJawsHandle = iMA(None, 0, InpJawsPeriod, 0, InpMAMethod, InpAppliedPrice)
    gTeethHandle = iMA(None, 0, InpTeethPeriod, 0, InpMAMethod, InpAppliedPrice)
    gLipsHandle = iMA(None, 0, InpLipsPeriod, 0, InpMAMethod, InpAppliedPrice)
    gAOHandle = iAO(None, 0)
    gATRHandle = iATR(None, 0, InpATRPeriod)
    gFractalsHandle = iFractals(None, 0)
    gBarsMin = MathMax(MathMax(InpJawsPeriod + InpJawsShift, InpTeethPeriod + InpTeethShift), InpLipsPeriod + InpLipsPeriod)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < gBarsMin:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - gBarsMin
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(gJawsHandle, 0, 0, to_copy, JawsBuffer) <= 0:
        return 0
    if CopyBuffer(gTeethHandle, 0, 0, to_copy, TeethBuffer) <= 0:
        return 0
    if CopyBuffer(gLipsHandle, 0, 0, to_copy, LipsBuffer) <= 0:
        return 0
    if CopyBuffer(gAOHandle, 0, 0, to_copy, AOBuffer) <= 0:
        return 0
    if CopyBuffer(gATRHandle, 0, 0, to_copy, ATRBuffer) <= 0:
        return 0
    if CopyBuffer(gFractalsHandle, UPPER_LINE, 1, to_copy, UpFractalsBuffer) <= 0:
        return 0
    if CopyBuffer(gFractalsHandle, LOWER_LINE, 1, to_copy, DownFractalsBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BullishDivergentBarBuffer[bar] = 0.0
        BearishDivergentBarBuffer[bar] = 0.0
        BullishSuperAOBuffer[bar] = 0.0
        BearishSuperAOBuffer[bar] = 0.0
        BullishFractalBuffer[bar] = 0.0
        BearishFractalBuffer[bar] = 0.0
        AngulationBuffer[bar] = 0.0
        angbars = 0
        angpnow = 0.0
        angppast = 0.0
        anganow = 0.0
        angapast = 0.0
        if ((low[bar] < low[bar + 1] and close[bar] > ((high[bar] + low[bar]) / 2)) and AOBuffer[bar] < AOBuffer[bar + 1]) and high[bar] < MathMin(JawsBuffer[bar + InpJawsShift], MathMin(LipsBuffer[bar + InpLipsShift], TeethBuffer[bar + InpTeethShift])):
            while high[bar + angbars] < MathMax(JawsBuffer[bar + angbars + InpJawsShift], MathMax(LipsBuffer[bar + angbars + InpLipsShift], TeethBuffer[bar + angbars + InpTeethShift])):
                angbars += 1
            angppast = low[bar + angbars]
            angpnow = low[bar]
            angapast = NormalizeDouble((JawsBuffer[bar + angbars + InpJawsShift] + TeethBuffer[bar + angbars + InpTeethShift]) / 2, Digits())
            anganow = NormalizeDouble((JawsBuffer[bar + InpJawsShift] + TeethBuffer[bar + InpTeethShift]) / 2, Digits())
            patmp = 'PriceAngle' + _str(bar)
            aatmp = 'AlligatorAngle' + _str(bar)
            drawAngulationLine(patmp, time[bar + angbars], angppast, time[bar], angpnow)
            drawAngulationLine(aatmp, time[bar + angbars], angapast, time[bar], anganow)
            if angbars != 0:
                AngulationBuffer[bar] = _fdiv(_fdiv(anganow - angpnow - (angapast - angppast), angbars), Point())
            BullishDivergentBarBuffer[bar] = NormalizeDouble(high[bar] + (ATRBuffer[bar] * InpPendingAddATRFactor), Digits())
        if ((high[bar] > high[bar + 1] and close[bar] < ((high[bar] + low[bar]) / 2)) and AOBuffer[bar] > AOBuffer[bar + 1]) and low[bar] > MathMax(JawsBuffer[bar + InpJawsShift], MathMax(LipsBuffer[bar + InpLipsShift], TeethBuffer[bar + InpTeethShift])):
            while low[bar + angbars] > MathMin(JawsBuffer[bar + angbars + InpJawsShift], MathMin(LipsBuffer[bar + angbars + InpLipsShift], TeethBuffer[bar + angbars + InpTeethShift])):
                angbars += 1
            angppast = high[bar + angbars]
            angpnow = high[bar]
            angapast = NormalizeDouble((JawsBuffer[bar + angbars + InpJawsShift] + TeethBuffer[bar + angbars + InpTeethShift]) / 2, Digits())
            anganow = NormalizeDouble((JawsBuffer[bar + InpJawsShift] + TeethBuffer[bar + InpTeethShift]) / 2, Digits())
            patmp = 'PriceAngle' + _str(bar)
            aatmp = 'AlligatorAngle' + _str(bar)
            drawAngulationLine(patmp, time[bar + angbars], angppast, time[bar], angpnow)
            drawAngulationLine(aatmp, time[bar + angbars], angapast, time[bar], anganow)
            if angbars != 0:
                AngulationBuffer[bar] = _fdiv(_fdiv(anganow - angpnow - (angapast - angppast), angbars), Point())
            BearishDivergentBarBuffer[bar] = NormalizeDouble(low[bar] - (ATRBuffer[bar] * InpPendingAddATRFactor), Digits())
        if ((AOBuffer[bar] > AOBuffer[bar + 1] and AOBuffer[bar + 1] > AOBuffer[bar + 2]) and AOBuffer[bar + 2] > AOBuffer[bar + 3]) and AOBuffer[bar + 3] < AOBuffer[bar + 4]:
            BullishSuperAOBuffer[bar] = NormalizeDouble(high[bar] + (ATRBuffer[bar] * InpPendingAddATRFactor), Digits())
        if ((AOBuffer[bar] < AOBuffer[bar + 1] and AOBuffer[bar + 1] < AOBuffer[bar + 2]) and AOBuffer[bar + 2] < AOBuffer[bar + 3]) and AOBuffer[bar + 3] > AOBuffer[bar + 4]:
            BearishSuperAOBuffer[bar] = NormalizeDouble(low[bar] - (ATRBuffer[bar] * InpPendingAddATRFactor), Digits())
        if UpFractalsBuffer[bar + 3] != EMPTY_VALUE and low[bar + 3] > TeethBuffer[bar]:
            BullishFractalBuffer[bar + 3] = NormalizeDouble(high[bar + 3] + (ATRBuffer[bar] * InpPendingAddATRFactor), Digits())
        if DownFractalsBuffer[bar + 3] != EMPTY_VALUE and high[bar + 3] < TeethBuffer[bar]:
            BearishFractalBuffer[bar + 3] = NormalizeDouble(low[bar + 3] - (ATRBuffer[bar] * InpPendingAddATRFactor), Digits())
        highsbuf = Arr(0, 0.0)
        lowsbuf = Arr(0, 0.0)
        if CopyHigh(None, 0, bar, InpHLBars, highsbuf) <= 0:
            return 0
        TrailingMaxHighBuffer[bar] = NormalizeDouble(highsbuf[ArrayMaximum(highsbuf)] + (ATRBuffer[bar] * InpStopAddATRFactor), Digits())
        if CopyLow(None, 0, bar, InpHLBars, lowsbuf) <= 0:
            return 0
        TrailingMinLowBuffer[bar] = NormalizeDouble(lowsbuf[ArrayMinimum(lowsbuf)] - (ATRBuffer[bar] * InpStopAddATRFactor), Digits())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def drawAngulationLine(name, starttime, startval, stoptime, stopval):
    ObjectCreate(0, name, OBJ_TREND, 0, starttime, startval, stoptime, stopval)
    ObjectSetInteger(0, name, OBJPROP_COLOR, InpAngulationColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, InpAngulationStyle)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, InpAngulationWidth)
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sacredchao02(_MQL5Indicator):
    name = 'sacredchao-0_2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpJawsPeriod': 13,  # Jaws period
        'InpJawsShift': 8,  # Jaws shift
        'InpTeethPeriod': 8,  # Teeth period
        'InpTeethShift': 5,  # Teeth shift
        'InpLipsPeriod': 5,  # Lips period
        'InpLipsShift': 3,  # Lips shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Moving average method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Applied price
        'InpATRPeriod': 14,  # ATR Period
        'InpPendingAddATRFactor': 0.2,  # ATR*Factor added to pending orders
        'InpStopAddATRFactor': 0.5,  # ATR*Factor added to trailing stop
        'InpHLBars': 3,  # Trailing Highest High/Lowest Low of x bars
        'InpAngulationStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=3),  # Angulation style
        'InpAngulationWidth': 1,  # Angulation width
        'InpBuDBArrowCode': 236,  # Bullish Divergent Arrowcode
        'InpBeDBArrowCode': 238,  # Bearish Divergent Arrowcode
        'InpBuSAOArrowCode': 142,  # Bullish Super AO Arrowcode
        'InpBeSAOArrowCode': 142,  # Bearish Super AO Arrowcode
        'InpBuFrcArrowCode': 217,  # Bullish Fractal Arrowcode
        'InpBeFrcArrowCode': 218,  # Bearish Fractal Arrowcode
    }

