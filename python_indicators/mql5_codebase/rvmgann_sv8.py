"""rvmgann_sv8 — converted from MQL5: MQL5 Indicators/rvmGann_sv8/rvmgann_sv8.mq5

The indicator implements the Gann principle in the form of a zigzag
Copyright: Copyright © 2005, Profi_R; Link: http://www.metaquotes.net/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Profi_R', 'link': 'http://www.metaquotes.net/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'rvmGann_sv8'}, 'levels': [], 'description': ['The indicator implements the Gann principle in the form of a zigzag'], 'name': 'rvmgann_sv8', 'source': 'MQL5 Indicators/rvmGann_sv8/rvmgann_sv8.mq5', 'folder': 'rvmGann_sv8', 'inputs': [{'mql': 'GSv_tend', 'py': 'GSv_tend', 'param': 'GSv_tend', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
GSv_tend = _input('GSv_tend', 2)
Upz = Arr(0, 0.0)
Dnz = Arr(0, 0.0)
sH = Arr(0, 0.0)
sL = Arr(0, 0.0)
aH = Arr(0, 0.0)
aL = Arr(0, 0.0)
fB = Arr(0, 0.0)
lB = Arr(0, 0.0)
CurH = 0.0
CurL = 0.0
lb = 0
sp = 0
lbars = 0
draw_up = False
draw_dn = False
min_rates_total = 0

def OnInit():
    global CurH, CurL, draw_dn, draw_up, lb, lbars, min_rates_total, sp
    min_rates_total = 2
    CurH = 0.0
    CurL = 0.0
    lb = 0
    sp = 0
    lbars = 0
    draw_up = False
    draw_dn = False
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(0, Upz, INDICATOR_DATA)
    SetIndexBuffer(1, Dnz, INDICATOR_DATA)
    SetIndexBuffer(2, sH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, sL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, aH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, aL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, fB, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, lB, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Upz, True)
    ArraySetAsSeries(Dnz, True)
    ArraySetAsSeries(sH, True)
    ArraySetAsSeries(sL, True)
    ArraySetAsSeries(aH, True)
    ArraySetAsSeries(aL, True)
    ArraySetAsSeries(fB, True)
    ArraySetAsSeries(lB, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'rvmGann_sv8')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global CurH, CurL, draw_dn, draw_up, lb, lbars, sp
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ai = 0
    last = 0
    prev_calculated_ = 0
    prev_calculated_ = MathMax(0, prev_calculated)
    last = rates_total - 1
    if (last - prev_calculated_) < 2:
        limit = 0
    else:
        limit = last - prev_calculated_ - 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        sH[bar] = 0.0
        sL[bar] = 0.0
        aH[bar] = -1.0
        aL[bar] = -1.0
        fB[bar] = -1.0
        lB[bar] = -1.0
        Upz[bar] = 0.0
        Dnz[bar] = 0.0
        ai = last - bar
        if lbars != rates_total and lb == ai:
            lbars = rates_total
            continue
        if lb != ai:
            lb = ai
            if Upz[bar + 1] > 0 or Dnz[bar + 1] > 0:
                aH[bar] = high[bar + 1]
                aL[bar] = low[bar + 1]
            else:
                if high[bar + 1] <= aH[bar + 1] and low[bar + 1] >= aL[bar + 1]:
                    aH[bar] = aH[bar + 1]
                    aL[bar] = aL[bar + 1]
                    sH[bar] = sH[bar + 1]
                    sL[bar] = sL[bar + 1]
                else:
                    if high[bar + 1] > aH[bar + 1]:
                        aH[bar] = high[bar + 1]
                    else:
                        aH[bar] = aH[bar + 1]
                    if aL[bar + 1] > 0:
                        if low[bar + 1] < aL[bar + 1]:
                            aL[bar] = low[bar + 1]
                        else:
                            aL[bar] = aL[bar + 1]
                    else:
                        aL[bar] = low[bar + 1]
            if draw_up:
                if fB[bar + 1] == 1:
                    sH[bar] = sH[bar + 1] + 1
                    if lB[bar + 1] == 0:
                        sH[bar] = 0.0
                        sL[bar] = 1.0
                else:
                    if fB[bar + 1] == 0:
                        sL[bar] = sL[bar + 1] + 1
                        if lB[bar + 1] == 1:
                            sH[bar] = 1.0
                            sL[bar] = 0.0
            else:
                if draw_dn:
                    if fB[bar + 1] == 0:
                        sL[bar] = sL[bar + 1] + 1
                        if lB[bar + 1] == 1:
                            sH[bar] = 1.0
                            sL[bar] = 0.0
                    else:
                        if fB[bar + 1] == 1:
                            sH[bar] = sH[bar + 1] + 1
                            if lB[bar + 1] == 0:
                                sH[bar] = 0.0
                                sL[bar] = 1.0
                else:
                    if fB[bar + 1] == 1:
                        sH[bar] = sH[bar + 1] + 1
                        sL[bar] = sL[bar + 1]
                        if lB[bar + 1] == 0:
                            sL[bar] += 1
                    else:
                        if fB[bar + 1] == 0:
                            sH[bar] = sH[bar + 1]
                            sL[bar] = sL[bar + 1] + 1
                            if lB[bar + 1] == 1:
                                sH[bar] += 1
            if GSv_tend > 1:
                if (((sH[bar] == GSv_tend and Upz[bar + 1] > 0) and high[bar + 1] > high[bar + 2]) and low[bar + 1] < low[bar + 2]) and fB[bar + 1] == 1:
                    sL[bar] = 1.0
                else:
                    if (((sL[bar] == GSv_tend and Dnz[bar + 1] > 0) and high[bar + 1] > high[bar + 2]) and low[bar + 1] < low[bar + 2]) and fB[bar + 1] == 0:
                        sH[bar] = 1.0
            CurH = 0.0
            CurL = low[bar]
        if high[bar] <= aH[bar] and low[bar] >= aL[bar]:
            continue
        if high[bar] <= CurH and low[bar] >= CurL:
            continue
        if high[bar] > CurH:
            CurH = high[bar]
        if low[bar] < CurL:
            CurL = low[bar]
        Extr_seq(open, high, low, close, bar)
        if GSv_tend > 1:
            if (fB[bar] > 0 and sH[bar] == (GSv_tend - 1)) and sL[bar] > 0:
                sL[bar] = 0.0
            elif (fB[bar] > -1 and sL[bar] == (GSv_tend - 1)) and sH[bar] > 0:
                sH[bar] = 0.0
        if draw_up:
            if fB[bar] == 1:
                if sp != ai:
                    Upz[MathMax(0, last - sp)] = 0.0
                    sp = ai
                Upz[bar] = high[bar]
                if (lB[bar] == 0 and (sL[bar] + 1) >= GSv_tend) and GSv_tend < 2:
                    Dnz[bar] = low[bar]
                    draw_up = (0 != 0)
                    draw_dn = (1 != 0)
            else:
                if fB[bar] == 0:
                    if (sL[bar] + 1) >= GSv_tend:
                        Dnz[bar] = low[bar]
                        sp = ai
                        draw_up = (0 != 0)
                        draw_dn = (1 != 0)
                        if lB[bar] == 1 and (sH[bar] + 1) >= GSv_tend:
                            Upz[bar] = high[bar]
                            draw_up = (1 != 0)
                            draw_dn = (0 != 0)
                    else:
                        if lB[bar] == 1:
                            Upz[MathMax(0, last - sp)] = 0.0
                            sp = ai
                            Upz[bar] = high[bar]
        else:
            if draw_dn:
                if fB[bar] == 1:
                    if (sH[bar] + 1) >= GSv_tend:
                        Upz[bar] = high[bar]
                        sp = ai
                        draw_up = (1 != 0)
                        draw_dn = (0 != 0)
                        if (not lB[bar]) and (sL[bar] + 1) >= GSv_tend:
                            Dnz[bar] = low[bar]
                            draw_up = (0 != 0)
                            draw_dn = (1 != 0)
                    else:
                        if not lB[bar]:
                            Dnz[MathMax(0, last - sp)] = 0.0
                            sp = ai
                            Dnz[bar] = low[bar]
                else:
                    if not fB[bar]:
                        if sp != ai:
                            Dnz[MathMax(0, last - sp)] = 0.0
                            sp = ai
                        Dnz[bar] = low[bar]
                        if (lB[bar] == 1 and (sH[bar] + 1) >= GSv_tend) and GSv_tend < 2:
                            Upz[bar] = high[bar]
                            draw_up = (1 != 0)
                            draw_dn = (0 != 0)
            else:
                if fB[bar] == 1 and (sH[bar] + 1) >= GSv_tend:
                    Dnz[last] = low[last]
                    Upz[bar] = high[bar]
                    draw_up = (1 != 0)
                    sp = ai
                    if (not lB[bar]) and (sL[bar] + 1) >= GSv_tend:
                        Dnz[bar] = low[bar]
                        draw_up = (0 != 0)
                        draw_dn = (1 != 0)
                else:
                    if (not fB[bar]) and (sL[bar] + 1) >= GSv_tend:
                        Upz[last] = high[last]
                        Dnz[bar] = low[bar]
                        draw_dn = (1 != 0)
                        sp = ai
                        if lB[bar] == 1 and (sH[bar] + 1) >= GSv_tend:
                            Upz[bar] = high[bar]
                            draw_up = (1 != 0)
                            draw_dn = (0 != 0)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def Extr_seq(Open, High, Low, Close, index):
    if fB[index] < 0:
        if High[index] > aH[index] and Low[index] < aL[index]:
            if Open[index] > aH[index]:
                fB[index] = 1.0
                lB[index] = 0.0
            else:
                if Open[index] < aL[index]:
                    fB[index] = 0.0
                    lB[index] = 1.0
                else:
                    if Close[index] > aH[index] and Close[index] >= Open[index]:
                        fB[index] = 0.0
                        lB[index] = 1.0
                    else:
                        if Close[index] > aL[index] and Close[index] <= Open[index]:
                            fB[index] = 1.0
                            lB[index] = 0.0
                        else:
                            if Close[index] > Open[index]:
                                fB[index] = 0.0
                                lB[index] = 1.0
                            else:
                                if Close[index] < Open[index]:
                                    fB[index] = 1.0
                                    lB[index] = 0.0
                                else:
                                    if MathAbs(Open[index] - aL[index]) < MathAbs(Open[index] - aH[index]):
                                        fB[index] = 0.0
                                        lB[index] = 1.0
                                    else:
                                        if MathAbs(Open[index] - aL[index]) > MathAbs(Open[index] - aH[index]):
                                            fB[index] = 1.0
                                            lB[index] = 0.0
                                        else:
                                            if MathAbs(Open[index] - Low[index]) >= MathAbs(Open[index] - High[index]):
                                                fB[index] = 0.0
                                                lB[index] = 1.0
                                            else:
                                                fB[index] = 1.0
                                                lB[index] = 0.0
        else:
            if High[index] > aH[index]:
                fB[index] = 1.0
            else:
                fB[index] = 0.0
    else:
        if (Low[index] >= aL[index] or Close[index] == High[index]) and High[index] > aH[index]:
            lB[index] = 1.0
        else:
            if (High[index] <= aH[index] or Close[index] == Low[index]) and Low[index] < aL[index]:
                lB[index] = 0.0
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RvmgannSv8(_MQL5Indicator):
    name = 'rvmgann_sv8'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'GSv_tend': 2,
    }

