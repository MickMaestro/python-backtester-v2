"""gannzigzag — converted from MQL5: MQL5 Indicators/GannZIGZAG_Levels/gannzigzag.mq5

Copyright: Copyright © 2005, Profi_R; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Profi_R', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [15624315]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'GannZIGZAG'}, 'levels': [], 'description': [''], 'name': 'gannzigzag', 'source': 'MQL5 Indicators/GannZIGZAG_Levels/gannzigzag.mq5', 'folder': 'GannZIGZAG_Levels', 'inputs': [{'mql': 'GSv_range', 'py': 'GSv_range', 'param': 'GSv_range', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
GSv_range = _input('GSv_range', 2)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
h = 0.0
l = 0.0
cur_h = False
cur_l = False
draw_up = False
draw_dn = False
initfl = False
fPoint_i = 0
sPoint_i = 0
s_up = 0
s_dn = 0
drawf = 0
lb = 0
idFile = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'GannZIGZAG')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global cur_h, cur_l, draw_dn, draw_up, fPoint_i, h, initfl, l, lb, sPoint_i, s_dn, s_up
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    i = 0
    bar = 0
    bar1 = 0
    limit = 0
    count = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        initfl = (0 != 0)
        draw_up = (0 != 0)
        draw_dn = (0 != 0)
        initfl = (0 != 0)
        cur_h = (0 != 0)
        cur_l = (0 != 0)
    else:
        limit = rates_total - prev_calculated
    if initfl != 1:
        myInit(rates_total, open, high, low, close)
    bars2 = rates_total - 2
    bars1 = rates_total - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bar1 = bar + 1
        count = bars1 - bar
        IndBuffer[bar] = 0.0
        if IndBuffer[bar1] > 0 and lb != count:
            if draw_up:
                s_dn = 0
            elif draw_dn:
                s_up = 0
        if lb != count:
            cur_h = (0 != 0)
            cur_l = (0 != 0)
        if bar > (bars2 - drawf) or (high[bar] <= high[bar1] and low[bar] >= low[bar1]):
            continue
        if draw_up:
            if high[bar] > h:
                h = high[bar]
                cur_h = (1 != 0)
            if low[bar] < l:
                l = low[bar]
                if lb != count or cur_l != 1:
                    s_dn += 1
                cur_l = (1 != 0)
            if s_up == s_dn:
                if cur_h == cur_l and cur_l == 1:
                    if close[bar] <= open[bar]:
                        draw_up = (0 != 0)
                        draw_dn = (1 != 0)
                        fPoint_i = sPoint_i
                        sPoint_i = count
                        IndBuffer[bar] = l
                        i = bars2 - fPoint_i
                        for i in range(i, bar, -1):
                            IndBuffer[i] = 0.0
                        else:
                            i = _range_end(i, bar, -1)
                    else:
                        sPoint_i = count
                        IndBuffer[bar] = h
                        i = bars2 - fPoint_i
                        for i in range(i, bar, -1):
                            IndBuffer[i] = 0.0
                        else:
                            i = _range_end(i, bar, -1)
                else:
                    if cur_h == 1:
                        sPoint_i = count
                        IndBuffer[bar] = h
                        l = low[bar]
                        i = bars2 - fPoint_i
                        for i in range(i, bar, -1):
                            IndBuffer[i] = 0.0
                        else:
                            i = _range_end(i, bar, -1)
                    else:
                        if cur_l == 1:
                            draw_up = (0 != 0)
                            draw_dn = (1 != 0)
                            fPoint_i = sPoint_i
                            sPoint_i = count
                            IndBuffer[bar] = l
                            h = high[bar]
                            i = bars2 - fPoint_i
                            for i in range(i, bar, -1):
                                IndBuffer[i] = 0.0
                            else:
                                i = _range_end(i, bar, -1)
            else:
                if cur_h == 1:
                    sPoint_i = count
                    IndBuffer[bar] = h
                    i = bars2 - fPoint_i
                    for i in range(i, bar, -1):
                        IndBuffer[i] = 0.0
                    else:
                        i = _range_end(i, bar, -1)
                    l = low[bar]
        else:
            if high[bar] > h:
                h = high[bar]
                if lb != count or cur_h != 1:
                    s_up += 1
                cur_h = (1 != 0)
            if low[bar] < l:
                l = low[bar]
                cur_l = (1 != 0)
            if s_up == s_dn:
                if cur_h == cur_l and cur_l == 1:
                    if close[bar] <= open[bar]:
                        sPoint_i = count
                        IndBuffer[bar] = l
                        i = bars2 - fPoint_i
                        for i in range(i, bar, -1):
                            IndBuffer[i] = 0.0
                        else:
                            i = _range_end(i, bar, -1)
                    else:
                        draw_up = (1 != 0)
                        draw_dn = (0 != 0)
                        fPoint_i = sPoint_i
                        sPoint_i = count
                        IndBuffer[bar] = h
                        i = bars2 - fPoint_i
                        for i in range(i, bar, -1):
                            IndBuffer[i] = 0.0
                        else:
                            i = _range_end(i, bar, -1)
                else:
                    if cur_h == 1:
                        draw_up = (1 != 0)
                        draw_dn = (0 != 0)
                        fPoint_i = sPoint_i
                        sPoint_i = count
                        IndBuffer[bar] = h
                        l = low[bar]
                        i = bars2 - fPoint_i
                        for i in range(i, bar, -1):
                            IndBuffer[i] = 0.0
                        else:
                            i = _range_end(i, bar, -1)
                    else:
                        if cur_l == 1:
                            sPoint_i = count
                            IndBuffer[bar] = l
                            h = high[bar]
                            i = bars2 - fPoint_i
                            for i in range(i, bar, -1):
                                IndBuffer[i] = 0.0
                            else:
                                i = _range_end(i, bar, -1)
            else:
                if cur_l == 1:
                    sPoint_i = count
                    IndBuffer[bar] = l
                    i = bars2 - fPoint_i
                    for i in range(i, bar, -1):
                        IndBuffer[i] = 0.0
                    else:
                        i = _range_end(i, bar, -1)
                    h = high[bar]
        if lb != count:
            lb = count
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def myInit(bars, Open, High, Low, Close):
    global draw_dn, draw_up, drawf, fPoint_i, h, initfl, l, sPoint_i, s_dn, s_up
    index = 0
    index1 = 0
    bars1 = bars - 1
    fPoint_i = 0
    h = High[bars1]
    l = Low[bars1]
    index = bars - 2
    for index in range(index, 0 - 1, -1):
        index1 = index + 1
        if High[index] > High[index1] or Low[index] < Low[index1]:
            if High[index] > h and High[index] > High[index1]:
                s_up += 1
            if Low[index] < l and Low[index] < Low[index1]:
                s_dn += 1
        else:
            continue
        if s_up == s_dn and s_up == GSv_range:
            h = High[index]
            l = Low[index]
            sPoint_i = bars1 - index
            if Close[index] >= Open[index]:
                s_dn = 0
                IndBuffer[bars1] = Low[bars1]
                IndBuffer[index] = High[index]
                draw_up = (1 != 0)
                break
            else:
                s_up = 0
                IndBuffer[bars1] = High[bars1]
                IndBuffer[index] = Low[index]
                draw_dn = (1 != 0)
                break
        else:
            h = High[index]
            l = Low[index]
            sPoint_i = bars1 - index
            if s_up == GSv_range:
                s_dn = 0
                IndBuffer[bars1] = Low[bars1]
                IndBuffer[index] = High[index]
                draw_up = (1 != 0)
                break
            else:
                if s_dn == GSv_range:
                    s_up = 0
                    IndBuffer[bars1] = High[bars1]
                    IndBuffer[index] = Low[index]
                    draw_dn = (1 != 0)
                    break
    else:
        index = _range_end(index, 0 - 1, -1)
    initfl = (1 != 0)
    drawf = sPoint_i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Gannzigzag(_MQL5Indicator):
    name = 'gannzigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'GSv_range': 2,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

