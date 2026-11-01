"""pos_size — converted from MQL5: MQL5 Indicators/MQL5 Version of Position Size Calculator - Based on VP Money Management rules/pos_size.mq5

Copyright: Copyright 2018, Silverapex; Link: https://silverapex.co.uk; Version: 2.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Silverapex', 'link': 'https://silverapex.co.uk', 'version': '2.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'pos_size', 'source': 'MQL5 Indicators/MQL5 Version of Position Size Calculator - Based on VP Money Management rules/pos_size.mq5', 'folder': 'MQL5 Version of Position Size Calculator - Based on VP Money Management rules', 'inputs': [{'mql': 'InpATRperiod', 'py': 'InpATRperiod', 'param': 'InpATRperiod', 'type': 'int', 'default': 14, 'label': 'ATR Periods', 'sinput': False}, {'mql': 'InpRiskPC', 'py': 'InpRiskPC', 'param': 'InpRiskPC', 'type': 'double', 'default': 2.0, 'label': 'Risk Size %', 'sinput': False}, {'mql': 'InpSLfactor', 'py': 'InpSLfactor', 'param': 'InpSLfactor', 'type': 'double', 'default': 1.5, 'label': 'Stop Loss as a factor of ATR', 'sinput': False}, {'mql': 'InpTPfactor', 'py': 'InpTPfactor', 'param': 'InpTPfactor', 'type': 'double', 'default': 1.0, 'label': 'Take Profit as a factor of ATR', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 9, 'label': 'Font size', 'sinput': False}, {'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Color', 'sinput': False}, {'mql': 'InpBaseCorner', 'py': 'InpBaseCorner', 'param': 'InpBaseCorner', 'type': 'int', 'default': 3, 'label': 'Corner', 'sinput': False}, {'mql': 'InpFixedATR', 'py': 'InpFixedATR', 'param': 'InpFixedATR', 'type': 'double', 'default': 0.0, 'label': 'Fixed ATR points', 'sinput': False}, {'mql': 'InpBack', 'py': 'InpBack', 'param': 'InpBack', 'type': 'bool', 'default': False, 'label': 'Background object', 'sinput': False}, {'mql': 'InpSelection', 'py': 'InpSelection', 'param': 'InpSelection', 'type': 'bool', 'default': False, 'label': 'Highlight to move', 'sinput': False}, {'mql': 'InpHidden', 'py': 'InpHidden', 'param': 'InpHidden', 'type': 'bool', 'default': True, 'label': 'Hidden in the object list', 'sinput': False}, {'mql': 'InpZOrder', 'py': 'InpZOrder', 'param': 'InpZOrder', 'type': 'long', 'default': 0, 'label': 'Priority for mouse click', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpATRperiod = _input('InpATRperiod', 14)  # ATR Periods
InpRiskPC = _input('InpRiskPC', 2.0)  # Risk Size %
InpSLfactor = _input('InpSLfactor', 1.5)  # Stop Loss as a factor of ATR
InpTPfactor = _input('InpTPfactor', 1.0)  # Take Profit as a factor of ATR
InpFontSize = _input('InpFontSize', 9)  # Font size
InpColor = _input('InpColor', clrMagenta)  # Color
InpBaseCorner = _input('InpBaseCorner', CORNER_RIGHT_UPPER)  # Corner
InpFixedATR = _input('InpFixedATR', 0.0)  # Fixed ATR points
InpBack = _input('InpBack', False)  # Background object
InpSelection = _input('InpSelection', False)  # Highlight to move
InpHidden = _input('InpHidden', True)  # Hidden in the object list
InpZOrder = _input('InpZOrder', 0)  # Priority for mouse click
ExtATRBuffer = Arr(0, 0.0)
ExtTRBuffer = Arr(0, 0.0)

def OnInit():
    l = 0
    text_init(ChartID(), 'textATR', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'textBAL', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'textRISK', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'texttimeleft', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'textBuySL', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'textBuyTP', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'textSellSL', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'textSellTP', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    text_init(ChartID(), 'textlotsize', InpFontSize, InpFontSize * 3 * ((l := l + 1) - 1), InpColor, InpFontSize)
    SetIndexBuffer(0, ExtATRBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTRBuffer, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global AccntC, CounterC, ExC
    ExCRate = 1.0
    AccntC = AccountInfoString(ACCOUNT_CURRENCY)
    CounterC = StringSubstr(Symbol(), 3, 3)
    ExC = AccntC + CounterC
    if AccntC != CounterC:
        ExCRate = SymbolInfoDouble(ExC, SYMBOL_ASK)
    if ExCRate == 0:
        ExCRate = 1.0
    ATRPrice = AverageTrueRange(rates_total, prev_calculated, high, low, close)
    ATRPoints = _fdiv(ATRPrice, Point())
    if InpFixedATR != 0:
        ATRPoints = InpFixedATR
    riskVAccntC = AccountInfoDouble(ACCOUNT_EQUITY) * (InpRiskPC / 100)
    riskvalue = (ExCRate / 1) * riskVAccntC
    slpoints = ATRPoints * InpSLfactor
    riskperpoint = _fdiv(riskvalue, slpoints)
    lotSize = riskperpoint
    MTPointsPerPip = (10 if (Digits() == 3 or Digits() == 5) else 1)
    if CounterC == 'JPY':
        lotSize = riskperpoint / 100
    ATRpips = MathCeil(_fdiv(ATRPoints, MTPointsPerPip))
    bar_times = Arr(0, 0)
    ArraySetAsSeries(bar_times, True)
    CopyTime(Symbol(), Period(), 0, 2, bar_times)
    bar_span_seconds = PeriodSeconds(Period())
    last_bar_close_time = bar_times[0]
    this_bar_close_time = last_bar_close_time + bar_span_seconds
    now_mdt = MqlDateTime()
    now = TimeGMT(now_mdt)
    if Period() > PERIOD_D1:
        this_bar_close_time -= 60 * 60 * 24
    seconds_remaining = this_bar_close_time - now
    days_remaining = _idiv(seconds_remaining, 60 * 60 * 24)
    seconds_remaining = _imod(seconds_remaining, 60 * 60 * 24)
    hours_remaining = _idiv(seconds_remaining, 60 * 60)
    seconds_remaining = _imod(seconds_remaining, 60 * 60)
    minutes_remaining = _idiv(seconds_remaining, 60)
    seconds_remaining = _imod(seconds_remaining, 60)
    lstrTimeLeft = ""
    if Period() > PERIOD_D1:
        lstrTimeLeft = StringFormat('Time Left: %2.1d days, %2.2d:%2.2d:%2.2d', days_remaining, hours_remaining, minutes_remaining, seconds_remaining)
    elif Period() <= PERIOD_H1:
        lstrTimeLeft = StringFormat('Time Left: %2.2d:%2.2d', minutes_remaining, seconds_remaining)
    else:
        lstrTimeLeft = StringFormat('Time Left: %2.2d:%2.2d:%2.2d', hours_remaining, minutes_remaining, seconds_remaining)
    ask = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_ASK), Point())
    bid = _fdiv(SymbolInfoDouble(Symbol(), SYMBOL_BID), Point())
    buySLPoints = -1 * ATRPoints * InpSLfactor
    buySLPrice = (ask + buySLPoints) * Point()
    buyTPPoints = ATRPoints * InpTPfactor
    buyTPPrice = (ask + buyTPPoints) * Point()
    sellSLPoints = ATRPoints * InpSLfactor
    sellSLPrice = (ask + sellSLPoints) * Point()
    sellTPPoints = -1 * ATRPoints * InpTPfactor
    sellTPPrice = (ask + sellTPPoints) * Point()
    lstrATR = ('*FIXED*' if (InpFixedATR != 0) else '') + StringFormat('ATR(%.0f): %.0f pips', InpATRperiod, ATRpips)
    lstrBAL = StringFormat('Equity: %.2f %s', AccountInfoDouble(ACCOUNT_EQUITY), AccntC)
    lstrRISK = StringFormat('Risk %.1f%%: %.2f %s', InpRiskPC, riskVAccntC, AccntC)
    lstrBuySL = StringFormat('Buy SL: %s', DoubleToString(buySLPrice, Digits()))
    lstrBuyTP = StringFormat('Buy TP: %s', DoubleToString(buyTPPrice, Digits()))
    lstrSellSL = StringFormat('Sell SL: %s', DoubleToString(sellSLPrice, Digits()))
    lstrSellTP = StringFormat('Sell TP: %s', DoubleToString(sellTPPrice, Digits()))
    lstrVolume = StringFormat('Volume: %.2f', lotSize)
    ObjectSetString(ChartID(), 'texttimeleft', OBJPROP_TEXT, lstrTimeLeft)
    ObjectSetString(ChartID(), 'textATR', OBJPROP_TEXT, lstrATR)
    ObjectSetString(ChartID(), 'textBAL', OBJPROP_TEXT, lstrBAL)
    ObjectSetString(ChartID(), 'textRISK', OBJPROP_TEXT, lstrRISK)
    ObjectSetString(ChartID(), 'textBuySL', OBJPROP_TEXT, lstrBuySL)
    ObjectSetString(ChartID(), 'textBuyTP', OBJPROP_TEXT, lstrBuyTP)
    ObjectSetString(ChartID(), 'textSellSL', OBJPROP_TEXT, lstrSellSL)
    ObjectSetString(ChartID(), 'textSellTP', OBJPROP_TEXT, lstrSellTP)
    ObjectSetString(ChartID(), 'textlotsize', OBJPROP_TEXT, lstrVolume)
    ChartRedraw(ChartID())
    return rates_total

def AverageTrueRange(rates_total, prev_calculated, high, low, close):
    i = 0
    limit = 0
    if rates_total <= InpATRperiod:
        return 0.0
    ArraySetAsSeries(ExtATRBuffer, False)
    ArraySetAsSeries(ExtTRBuffer, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(close, False)
    if prev_calculated == 0:
        ExtTRBuffer[0] = 0.0
        ExtATRBuffer[0] = 0.0
        i = 1
        for i in range(i, rates_total):
            ExtTRBuffer[i] = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        else:
            i = _range_end(i, rates_total, 1)
        firstValue = 0.0
        i = 1
        for i in range(i, InpATRperiod + 1):
            ExtATRBuffer[i] = 0.0
            firstValue += ExtTRBuffer[i]
        else:
            i = _range_end(i, InpATRperiod + 1, 1)
        firstValue = firstValue / InpATRperiod
        ExtATRBuffer[InpATRperiod] = firstValue
        limit = InpATRperiod + 1
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtTRBuffer[i] = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        ExtATRBuffer[i] = ExtATRBuffer[i - 1] + ((ExtTRBuffer[i] - ExtTRBuffer[i - InpATRperiod]) / InpATRperiod)
    else:
        i = _range_end(i, rates_total, 1)
    return ExtATRBuffer[ArraySize(ExtATRBuffer) - 1]

def OnDeinit(reason):
    ObjectDelete(ChartID(), 'textATR')
    ObjectDelete(ChartID(), 'textBAL')
    ObjectDelete(ChartID(), 'textRISK')
    ObjectDelete(ChartID(), 'texttimeleft')
    ObjectDelete(ChartID(), 'textBuySL')
    ObjectDelete(ChartID(), 'textBuyTP')
    ObjectDelete(ChartID(), 'textSellSL')
    ObjectDelete(ChartID(), 'textSellTP')
    ObjectDelete(ChartID(), 'textlotsize')

def text_init(current_chart_id, obj_label, x_dist, y_dist, text_color, font_size):
    if not ObjectCreate(current_chart_id, obj_label, OBJ_LABEL, 0, 0, 0):
        Print("Error: can't create label! code #", GetLastError())
        return 0
    ObjectSetInteger(current_chart_id, obj_label, OBJPROP_CORNER, InpBaseCorner)
    chart_height = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, 0))
    chart_width = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0))
    y_pos = y_dist
    x_pos = x_dist
    _sw1 = InpBaseCorner
    if _sw1 == CORNER_LEFT_UPPER:
        y_pos += 50
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ALIGN, ALIGN_LEFT)
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ANCHOR, ANCHOR_LEFT_UPPER)
    elif _sw1 == CORNER_RIGHT_UPPER:
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ALIGN, ALIGN_RIGHT)
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    elif _sw1 == CORNER_LEFT_LOWER:
        y_pos = (27 * font_size) - y_pos
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ALIGN, ALIGN_LEFT)
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    elif _sw1 == CORNER_RIGHT_LOWER:
        y_pos = (27 * font_size) - y_pos
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ALIGN, ALIGN_RIGHT)
        ObjectSetInteger(current_chart_id, obj_label, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(current_chart_id, obj_label, OBJPROP_XDISTANCE, x_pos)
    ObjectSetInteger(current_chart_id, obj_label, OBJPROP_YDISTANCE, y_pos)
    ObjectSetInteger(current_chart_id, obj_label, OBJPROP_COLOR, text_color)
    ObjectSetInteger(current_chart_id, obj_label, OBJPROP_FONTSIZE, font_size)
    return 0

# ---- global variables initialised from expressions
AccntC = AccountInfoString(ACCOUNT_CURRENCY)  # Currency of Acount eg USD,GBP,EUR
CounterC = StringSubstr(Symbol(), 3, 3)  # The Count Currency eg GBPUSD is USD
ExC = AccntC + CounterC  # Create the Pair for account eg USDGBP


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PosSize(_MQL5Indicator):
    name = 'pos_size'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpATRperiod': 14,  # ATR Periods
        'InpRiskPC': 2.0,  # Risk Size %
        'InpSLfactor': 1.5,  # Stop Loss as a factor of ATR
        'InpTPfactor': 1.0,  # Take Profit as a factor of ATR
        'InpFontSize': 9,  # Font size
        'InpBaseCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=3),  # Corner
        'InpFixedATR': 0.0,  # Fixed ATR points
        'InpBack': False,  # Background object
        'InpSelection': False,  # Highlight to move
        'InpHidden': True,  # Hidden in the object list
        'InpZOrder': 0,  # Priority for mouse click
    }

