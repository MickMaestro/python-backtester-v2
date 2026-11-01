"""dserg-linregressionbreakout — converted from MQL5: MQL5 Indicators/Dserg - LinRegression Breakout/dserg-linregressionbreakout.mq5

http://www.mql4.com/ru/users/Dserg
Copyright: Copyright © 2010, Dserg; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Dserg', 'link': '', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [16748574], 2: [16748574], 3: [16748574], 4: [16748574], 5: [2237106], 6: [65280], 7: [255], 8: [16711680]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {1: 0, 2: 0, 3: 2, 4: 2}, 'labels': {1: 'Channel Low', 2: 'Channel High', 3: 'Channel Low Extended', 4: 'Channel High Extended', 5: 'Stop_Buffer/Reverse', 6: 'BUY Signal', 7: 'SELL Signal', 8: 'Target_Buffer Signal'}, 'levels': [], 'description': ['http://www.mql4.com/ru/users/Dserg'], 'name': 'dserg-linregressionbreakout', 'source': 'MQL5 Indicators/Dserg - LinRegression Breakout/dserg-linregressionbreakout.mq5', 'folder': 'Dserg - LinRegression Breakout', 'inputs': [{'mql': 'Nlin', 'py': 'Nlin', 'param': 'Nlin', 'type': 'uint', 'default': 25, 'label': 'Minimum length of the linear regression channel', 'sinput': False}, {'mql': 'r0', 'py': 'r0', 'param': 'r0', 'type': 'uint', 'default': 150, 'label': 'Maximum height of the channel in points', 'sinput': False}, {'mql': 't0', 'py': 't0', 'param': 't0', 'type': 'double', 'default': 2.618, 'label': 'The purpose at breakdown relatively the channel width', 'sinput': False}, {'mql': 'useClose', 'py': 'useClose', 'param': 'useClose', 'type': 'bool', 'default': True, 'label': 'Use to calculate Close,\\n if false - High/Low', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Nlin = _input('Nlin', 25)  # Minimum length of the linear regression channel
r0 = _input('r0', 150)  # Maximum height of the channel in points
t0 = _input('t0', 2.618)  # The purpose at breakdown relatively the channel width
useClose = _input('useClose', True)  # Use to calculate Close,\n if false - High/Low
B1_Buffer = Arr(0, 0.0)
B0_Buffer = Arr(0, 0.0)
B3_Buffer = Arr(0, 0.0)
B4_Buffer = Arr(0, 0.0)
Stop_Buffer = Arr(0, 0.0)
Up_Buffer = Arr(0, 0.0)
Dn_Buffer = Arr(0, 0.0)
Target_Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Nlin)
    SetIndexBuffer(0, B0_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(B0_Buffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, B1_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(B1_Buffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, B3_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(B3_Buffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, B4_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(B4_Buffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, Stop_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Stop_Buffer, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(4, PLOT_ARROW, 251)
    SetIndexBuffer(5, Up_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Up_Buffer, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(5, PLOT_ARROW, 233)
    SetIndexBuffer(6, Dn_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Dn_Buffer, True)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(6, PLOT_ARROW, 234)
    SetIndexBuffer(7, Target_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Target_Buffer, True)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(7, PLOT_ARROW, 231)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Dserg-LinRegressionBreakout'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_recount
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    barj = 0
    j = 0
    isChannel = False
    a0 = 0.0
    b0 = 0.0
    a = 0.0
    b = 0.0
    c = 0.0
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    h = 0.0
    l = 0.0
    range_ = 0.0
    range0 = 0.0
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    range_ = 0.0
    range0 = 0.0
    isChannel = False
    a0 = 0.0
    b0 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_recount = limit
    else:
        limit = rates_total - prev_calculated + _s_OnCalculate_recount
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        B0_Buffer[bar] = 0.0
        B1_Buffer[bar] = 0.0
        B3_Buffer[bar] = 0.0
        B4_Buffer[bar] = 0.0
        Up_Buffer[bar] = 0.0
        Dn_Buffer[bar] = 0.0
        Stop_Buffer[bar] = 0.0
        Target_Buffer[bar] = 0.0
        if isChannel:
            up0 = (a0 * bar) + b0 + range0
            dn0 = (a0 * bar) + b0 - range0
            B3_Buffer[bar] = up0
            B4_Buffer[bar] = dn0
            if Open[bar] > up0:
                Up_Buffer[bar] = up0
                Stop_Buffer[bar] = dn0
                Target_Buffer[bar] = up0 + ((up0 - dn0) * (t0 - 1))
                isChannel = False
                if bar:
                    _s_OnCalculate_recount = bar - 1
            if Open[bar] < dn0:
                Dn_Buffer[bar] = dn0
                Stop_Buffer[bar] = up0
                Target_Buffer[bar] = dn0 - ((up0 - dn0) * (t0 - 1))
                isChannel = False
                if bar:
                    _s_OnCalculate_recount = bar - 1
            continue
        flag = False
        j = 0
        for j in range(j, _int(Nlin)):
            if B3_Buffer[bar + j] > 0.0 and (not isChannel):
                flag = True
                break
        else:
            j = _range_end(j, _int(Nlin), 1)
        if flag:
            continue
        sumx = 0.0
        sumy = 0.0
        sumxy = 0.0
        sumx2 = 0.0
        j = 0
        for j in range(j, _int(Nlin)):
            barj = bar + j
            sumy += Close[barj]
            sumxy += Close[barj] * barj
            sumx += barj
            sumx2 += barj * barj
        else:
            j = _range_end(j, _int(Nlin), 1)
        c = (sumx2 * Nlin) - (sumx * sumx)
        if not c:
            Alert('Error in linear regression!')
            return 0
        h = 0.0
        l = 0.0
        a = _fdiv((sumxy * Nlin) - (sumx * sumy), c)
        b = (sumy - (sumx * a)) / Nlin
        j = 0
        for j in range(j, _int(Nlin)):
            barj = bar + j
            LR = (a * barj) + b
            if useClose:
                if (Close[barj] - LR) > h:
                    h = Close[barj] - LR
                if (LR - Close[barj]) > l:
                    l = LR - Close[barj]
            else:
                if (High[barj] - LR) > h:
                    h = High[barj] - LR
                if (LR - Low[barj]) > l:
                    l = LR - Low[barj]
        else:
            j = _range_end(j, _int(Nlin), 1)
        range_ = MathMax(l, h)
        if range_ < (r0 * Point()):
            isChannel = True
            a0 = a
            b0 = b
            range0 = range_
            j = 0
            for j in range(j, _int(Nlin)):
                barj = bar + j
                res1 = (a * barj) + b
                res2 = res1 + range_
                res3 = res1 - range_
                if not j:
                    B3_Buffer[barj] = res2
                    B4_Buffer[barj] = res3
                B0_Buffer[barj] = res2
                B1_Buffer[barj] = res3
            else:
                j = _range_end(j, _int(Nlin), 1)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_recount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DsergLinregressionbreakout(_MQL5Indicator):
    name = 'dserg-linregressionbreakout'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Nlin': 25,  # Minimum length of the linear regression channel
        'r0': 150,  # Maximum height of the channel in points
        't0': 2.618,  # The purpose at breakdown relatively the channel width
        'useClose': True,  # Use to calculate Close,\n if false - High/Low
    }

