"""zigzag_int — converted from MQL5: MQL5 Indicators/ZigZag_INT/zigzag_int.mq5

ZigZag
Copyright: Copyright © 2005, Integer; Link: http://dmffx.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Integer', 'link': 'http://dmffx.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [16711935]}, 'widths': {1: 1}, 'styles': {1: 1}, 'labels': {1: 'ZigZag_INT'}, 'levels': [], 'description': ['ZigZag'], 'name': 'zigzag_int', 'source': 'MQL5 Indicators/ZigZag_INT/zigzag_int.mq5', 'folder': 'ZigZag_INT', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HLPeriod = 12  # Indicator period (equivalent to ExtDepth of ZigZag indicator)
MinHight = 1  # Minimum vertical knee height (in points)
ZZBuffer = Arr(0, 0.0)
dMinHight = 0.0
min_rates_total = 0

def OnInit():
    global dMinHight, min_rates_total
    min_rates_total = HLPeriod
    dMinHight = MinHight * Point()
    SetIndexBuffer(0, ZZBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ZZBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag(', HLPeriod, ', ', MinHight, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_cDir, _s_OnCalculate_lht1, _s_OnCalculate_llt1, _s_OnCalculate_pDir
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    lht0 = 0
    llt0 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_cDir = 0
        _s_OnCalculate_pDir = 0
        _s_OnCalculate_lht1 = 1
        _s_OnCalculate_llt1 = 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if prev_calculated != rates_total:
            _s_OnCalculate_pDir = _s_OnCalculate_cDir
        else:
            _s_OnCalculate_cDir = _s_OnCalculate_pDir
        hb = ArrayMaximum(High, bar, HLPeriod)
        lb = ArrayMinimum(Low, bar, HLPeriod)
        lhb = rates_total - _s_OnCalculate_lht1
        llb = rates_total - _s_OnCalculate_llt1
        lht0 = _s_OnCalculate_lht1
        llt0 = _s_OnCalculate_llt1
        ZZBuffer[bar] = 0.0
        if llb > lhb:
            ZZBuffer[lhb] = High[lhb]
        else:
            ZZBuffer[llb] = Low[llb]
        if hb == lb:
            if hb == bar:
                _sw1 = _s_OnCalculate_cDir
                if _sw1 == 1:
                    if High[bar] > ZZBuffer[lhb]:
                        ZZBuffer[lhb] = 0.0
                        ZZBuffer[bar] = High[bar]
                        lht0 = rates_total - bar
                    elif Low[bar] <= (ZZBuffer[lhb] - dMinHight):
                        ZZBuffer[bar] = Low[bar]
                        llt0 = rates_total - bar
                        _s_OnCalculate_cDir = -1
                elif _sw1 == -1:
                    if Low[bar] < ZZBuffer[llb]:
                        ZZBuffer[llb] = 0.0
                        ZZBuffer[bar] = Low[bar]
                        llt0 = rates_total - bar
                    elif High[bar] >= (ZZBuffer[llb] + dMinHight):
                        ZZBuffer[bar] = High[bar]
                        lht0 = rates_total - bar
                        _s_OnCalculate_cDir = 1
        elif lb > hb:
            if hb == bar:
                if _s_OnCalculate_cDir == 1:
                    if High[bar] > ZZBuffer[lhb]:
                        ZZBuffer[lhb] = 0.0
                        ZZBuffer[bar] = High[bar]
                        lht0 = rates_total - bar
                elif High[bar] >= (ZZBuffer[llb] + dMinHight):
                    ZZBuffer[bar] = High[bar]
                    lht0 = rates_total - bar
                    _s_OnCalculate_cDir = 1
        elif hb > lb:
            if lb == bar:
                if _s_OnCalculate_cDir == -1:
                    if Low[bar] < ZZBuffer[llb]:
                        ZZBuffer[llb] = 0.0
                        ZZBuffer[bar] = Low[bar]
                        llt0 = rates_total - bar
                elif Low[bar] <= (ZZBuffer[lhb] - dMinHight):
                    ZZBuffer[bar] = Low[bar]
                    llt0 = rates_total - bar
                    _s_OnCalculate_cDir = -1
        if bar > 0:
            _s_OnCalculate_llt1 = llt0
            _s_OnCalculate_lht1 = lht0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_cDir = 0
_s_OnCalculate_pDir = 0
_s_OnCalculate_lht1 = 0
_s_OnCalculate_llt1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigzagInt(_MQL5Indicator):
    name = 'zigzag_int'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

