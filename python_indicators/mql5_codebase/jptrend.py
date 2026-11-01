"""jptrend — converted from MQL5: MQL5 Indicators/JPTrend indicator/jptrend.mq5

The indicator places support and resistant lines.
JP LATHUILE  Xynium@laposte.net
Copyright: 2012, JPLathuile; Link: xynium@laposte.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2012, JPLathuile', 'link': 'xynium@laposte.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'JPTrend'}, 'levels': [], 'description': ['The indicator places support and resistant lines.', 'JP LATHUILE  Xynium@laposte.net'], 'name': 'jptrend', 'source': 'MQL5 Indicators/JPTrend indicator/jptrend.mq5', 'folder': 'JPTrend indicator', 'inputs': [{'mql': 'ipDimMaxPos', 'py': 'ipDimMaxPos', 'param': 'ipDimMaxPos', 'type': 'int', 'default': 150, 'label': 'Max bars, used in analysis', 'sinput': False}, {'mql': 'bAlertAuto', 'py': 'bAlertAuto', 'param': 'bAlertAuto', 'type': 'bool', 'default': False, 'label': 'Auto alert', 'sinput': False}, {'mql': 'dAlertSeuil', 'py': 'dAlertSeuil', 'param': 'dAlertSeuil', 'type': 'double', 'default': 0.0002, 'label': 'Trend deviation to alert', 'sinput': False}, {'mql': 'clrSup', 'py': 'clrSup', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color of support line', 'sinput': False}, {'mql': 'clrRes', 'py': 'clrRes', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color of resistance lines', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ipDimMaxPos = _input('ipDimMaxPos', 150)  # Max bars, used in analysis
bAlertAuto = _input('bAlertAuto', False)  # Auto alert
dAlertSeuil = _input('dAlertSeuil', 0.0002)  # Trend deviation to alert
clrSup = _input('clrSup', 0xFF0000)  # Color of support line
clrRes = _input('clrRes', 0x0000FF)  # Color of resistance lines
A = 0.0
B = 0.0
C = Arr(0, 0)
D = Arr(0, 0)
bb = False

def OnInit():
    ArrayResize(C, ipDimMaxPos, 1)
    ArrayResize(D, ipDimMaxPos, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'JPTrend')

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_TREND)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global A, B, bb
    icpt = 0
    limit = 0
    i = 0
    icpu = 0
    iTc = 0
    iTcc = 0
    paula = 0.0
    dy = 0.0
    fg = 0.0
    Claudia = False
    sName = ""
    iTP = 1
    if rates_total < 100:
        return 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated
    i = limit
    for i in range(i, rates_total):
        if i < 20:
            continue
        if High[i] > A:
            C[0] = i
        else:
            Lucie()
            bb = True
        A = High[i]
        if Low[i] < B:
            D[0] = i
        else:
            Jane()
            bb = True
        B = Low[i]
    else:
        i = _range_end(i, rates_total, 1)
    if bb:
        ObjectsDeleteAll(0, 0, OBJ_TREND)
        iTc = _idiv(3 * ipDimMaxPos, 4)
        icpt = iTc
        for icpt in range(icpt, iTP + 1, -1):
            icpu = icpt - 1
            for icpu in range(icpu, iTP, -1):
                fg = float(C[icpu] - C[icpt])
                if fg <= 6:
                    continue
                paula = High[C[icpu]] - High[C[icpt]]
                Claudia = True
                iTcc = _idiv(ipDimMaxPos + (2 * icpt), 3)
                i = iTcc
                for i in range(i, 1, -1):
                    dy = _fdiv(paula * (C[i] - C[icpt]), fg) + High[C[icpt]]
                    if dy < High[C[i]]:
                        Claudia = False
                        break
                else:
                    i = _range_end(i, 1, -1)
                if Claudia:
                    dy = _fdiv(paula * float(rates_total - 1 - C[icpt]), fg) + High[C[icpt]]
                    if dy > ChartGetDouble(0, CHART_PRICE_MAX, 0) or dy < ChartGetDouble(0, CHART_PRICE_MIN, 0):
                        Claudia = False
                    if fabs(dy - High[rates_total - 1]) < dAlertSeuil and bAlertAuto:
                        Alert('Resistance reached')
                if Claudia:
                    sName = 'R' + IntegerToString(icpt, 0, 32) + IntegerToString(icpu, 0, 32)
                    ObjectCreate(0, sName, OBJ_TREND, 0, Time[C[icpt]], High[C[icpt]], Time[C[icpu]], High[C[icpu]])
                    ObjectSetInteger(0, sName, OBJPROP_RAY_RIGHT, True)
                    ObjectSetInteger(0, sName, OBJPROP_COLOR, clrRes)
            else:
                icpu = _range_end(icpu, iTP, -1)
        else:
            icpt = _range_end(icpt, iTP + 1, -1)
        iTc = _idiv(3 * ipDimMaxPos, 4)
        icpt = iTc
        for icpt in range(icpt, 2, -1):
            icpu = icpt - 1
            for icpu in range(icpu, 1, -1):
                fg = float(D[icpu] - D[icpt])
                if fg < 10:
                    continue
                paula = Low[D[icpu]] - Low[D[icpt]]
                Claudia = True
                iTcc = _idiv(ipDimMaxPos + (2 * icpt), 3)
                i = iTcc
                for i in range(i, 0, -1):
                    dy = _fdiv(paula * float(D[i] - D[icpt]), fg) + Low[D[icpt]]
                    if dy > Low[D[i]]:
                        Claudia = False
                        break
                else:
                    i = _range_end(i, 0, -1)
                if Claudia:
                    dy = _fdiv(paula * float(rates_total - 1 - D[icpt]), fg) + Low[D[icpt]]
                    if dy > ChartGetDouble(0, CHART_PRICE_MAX, 0) or dy < ChartGetDouble(0, CHART_PRICE_MIN, 0):
                        Claudia = False
                    if fabs(dy - Low[rates_total - 1]) < dAlertSeuil and bAlertAuto:
                        Alert('Support reached')
                if Claudia:
                    sName = 'S' + IntegerToString(icpt, 0, 32) + IntegerToString(icpu, 0, 32)
                    ObjectCreate(0, sName, OBJ_TREND, 0, Time[D[icpt]], Low[D[icpt]], Time[D[icpu]], Low[D[icpu]])
                    ObjectSetInteger(0, sName, OBJPROP_RAY_RIGHT, True)
                    ObjectSetInteger(0, sName, OBJPROP_COLOR, clrSup)
            else:
                icpu = _range_end(icpu, 1, -1)
        else:
            icpt = _range_end(icpt, 2, -1)
        bb = False
    return rates_total

def Lucie():
    it = 0
    it = ipDimMaxPos - 1
    for it in range(it, 0, -1):
        C[it] = C[it - 1]
    else:
        it = _range_end(it, 0, -1)

def Jane():
    it = 0
    it = ipDimMaxPos - 1
    for it in range(it, 0, -1):
        D[it] = D[it - 1]
    else:
        it = _range_end(it, 0, -1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jptrend(_MQL5Indicator):
    name = 'jptrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ipDimMaxPos': 150,  # Max bars, used in analysis
        'bAlertAuto': False,  # Auto alert
        'dAlertSeuil': 0.0002,  # Trend deviation to alert
    }

