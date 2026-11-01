"""fantailvma2 — converted from MQL5: MQL5 Indicators/FantailVMA/fantailvma2.mq5

FantailVMA
Copyright: 2007, www.forex-tsd; Link: http://www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2007, www.forex-tsd', 'link': 'http://www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['FantailVMA'], 'name': 'fantailvma2', 'source': 'MQL5 Indicators/FantailVMA/fantailvma2.mq5', 'folder': 'FantailVMA', 'inputs': [{'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'int', 'default': 1, 'label': 'Period of MA', 'sinput': False}, {'mql': 'VarMA_Length', 'py': 'VarMA_Length', 'param': 'VarMA_Length', 'type': 'int', 'default': 4, 'label': 'Period of VarMA', 'sinput': False}, {'mql': 'ADX_Length', 'py': 'ADX_Length', 'param': 'ADX_Length', 'type': 'int', 'default': 8, 'label': 'Period of ADX', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Length = _input('MA_Length', 1)  # Period of MA
VarMA_Length = _input('VarMA_Length', 4)  # Period of VarMA
ADX_Length = _input('ADX_Length', 8)  # Period of ADX
dSmoothFactor = 0.0
MA = Arr(0, 0.0)
VarMA = Arr(0, 0.0)
VMA = Arr(0, 0.0)
ADX = Arr(0, 0.0)
sPDI = Arr(0, 0.0)
sMDI = Arr(0, 0.0)
STR = Arr(0, 0.0)

def OnInit():
    global dSmoothFactor
    dSmoothFactor = _fdiv(2.0, 1.0 + MA_Length)
    SetIndexBuffer(0, MA, INDICATOR_DATA)
    SetIndexBuffer(1, VarMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, VMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ADX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, sPDI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, sMDI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, STR, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ADX_Length)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FantailVMA')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    pos = prev_calculated
    shift = 0
    counted_bars = rates_total
    alfa = 1.0 / ADX_Length
    if pos == rates_total:
        pos -= 2
    shift = pos + 1
    for shift in range(shift, rates_total):
        Hi = high[shift]
        Hi1 = high[shift - 1]
        Lo = low[shift]
        Lo1 = low[shift - 1]
        Close1 = close[shift - 1]
        Bulls = 0.5 * (MathAbs(Hi - Hi1) + (Hi - Hi1))
        Bears = 0.5 * (MathAbs(Lo1 - Lo) + (Lo1 - Lo))
        if Bulls > Bears:
            Bears = 0.0
        elif Bulls < Bears:
            Bulls = 0.0
        elif Bulls == Bears:
            Bulls = 0.0
            Bears = 0.0
        sPDI[shift] = sPDI[shift - 1] + (alfa * (Bulls - sPDI[shift - 1]))
        sMDI[shift] = sMDI[shift - 1] + (alfa * (Bears - sMDI[shift - 1]))
        TR = MathMax(Hi - Lo, Hi - Close1)
        STR[shift] = STR[shift - 1] + (alfa * (TR - STR[shift - 1]))
        PDI = 0.0
        MDI = 0.0
        DX = 0.0
        MaInd = 0.0
        Const = 0.0
        if STR[shift] > 0:
            PDI = _fdiv(100 * sPDI[shift], STR[shift])
            MDI = _fdiv(100 * sMDI[shift], STR[shift])
        if (PDI + MDI) > 0:
            DX = _fdiv(100 * MathAbs(PDI - MDI), PDI + MDI)
        else:
            DX = 0.0
        ADX[shift] = ADX[shift - 1] + (alfa * (DX - ADX[shift - 1]))
        vADX = ADX[shift]
        if VarMA_Length > 0:
            MaInd = _fdiv(2.0, 1.0 + VarMA_Length)
        else:
            MaInd = 0.2
        ADXmin = ADX[shift]
        ADXmax = ADX[shift]
        i = 0
        for i in range(i, ADX_Length - 1 + 1):
            if (shift - i) < 0:
                break
            if ADXmin > ADX[shift - i]:
                ADXmin = ADX[shift - i]
            if ADXmax < ADX[shift - i]:
                ADXmax = ADX[shift - i]
        else:
            i = _range_end(i, ADX_Length - 1 + 1, 1)
        Diff = ADXmax - ADXmin
        if Diff > 0:
            Const = _fdiv(vADX - ADXmin, Diff)
        else:
            Const = MaInd
        if Const > MaInd:
            Const = MaInd
        else:
            Const = Const
        VarMA[shift] = (((2 - Const) * VarMA[shift - 1]) + (Const * close[shift])) / 2
    else:
        shift = _range_end(shift, rates_total, 1)
    i = pos + 1
    for i in range(i, rates_total):
        MA[i] = (VarMA[i] * dSmoothFactor) + (MA[i - 1] * (1.0 - dSmoothFactor))
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fantailvma2(_MQL5Indicator):
    name = 'fantailvma2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Length': 1,  # Period of MA
        'VarMA_Length': 4,  # Period of VarMA
        'ADX_Length': 8,  # Period of ADX
    }

