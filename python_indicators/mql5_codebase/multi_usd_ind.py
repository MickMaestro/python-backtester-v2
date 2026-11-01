"""multi_usd_ind — converted from MQL5: MQL5 Indicators/Multi-Currency Indicator with USD reference/multi_usd_ind.mq5

Multi Currency Indicator with USD reference
Copyright: Winston; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Winston', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 2, 7: 2}, 'colors': {1: [42495], 2: [16777215], 3: [255], 4: [65535], 5: [16776960], 6: [8388352], 7: [15631086]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 2, 6: 2, 7: 2}, 'labels': {1: 'USD'}, 'levels': [], 'description': ['Multi Currency Indicator with USD reference'], 'name': 'multi_usd_ind', 'source': 'MQL5 Indicators/Multi-Currency Indicator with USD reference/multi_usd_ind.mq5', 'folder': 'Multi-Currency Indicator with USD reference', 'inputs': [{'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 1.0, 'label': 'Smoothing factor', 'sinput': False}, {'mql': 'p', 'py': 'p', 'param': 'p', 'type': 'int', 'default': 60, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
k = _input('k', 1.0)  # Smoothing factor
p = _input('p', 60)  # Period
T_v = 0
n = p
aug = Arr(0, 0.0)  # Display indicators
eug = Arr(0, 0.0)  # Display indicators
gug = Arr(0, 0.0)  # Display indicators
nug = Arr(0, 0.0)  # Display indicators
cug = Arr(0, 0.0)  # Display indicators
hug = Arr(0, 0.0)  # Display indicators
jug = Arr(0, 0.0)  # Display indicators

def OnInit():
    ArraySetAsSeries(aug, True)
    ArraySetAsSeries(eug, True)
    ArraySetAsSeries(gug, True)
    ArraySetAsSeries(nug, True)
    ArraySetAsSeries(cug, True)
    ArraySetAsSeries(hug, True)
    ArraySetAsSeries(jug, True)
    SetIndexBuffer(0, aug, INDICATOR_DATA)
    SetIndexBuffer(1, eug, INDICATOR_DATA)
    SetIndexBuffer(2, gug, INDICATOR_DATA)
    SetIndexBuffer(3, nug, INDICATOR_DATA)
    SetIndexBuffer(4, cug, INDICATOR_DATA)
    SetIndexBuffer(5, hug, INDICATOR_DATA)
    SetIndexBuffer(6, jug, INDICATOR_DATA)
    ArraySetAsSeries(AU, True)
    ArraySetAsSeries(EU, True)
    ArraySetAsSeries(GU, True)
    ArraySetAsSeries(NU, True)
    ArraySetAsSeries(UC, True)
    ArraySetAsSeries(UH, True)
    ArraySetAsSeries(UJ, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AUD-org EUR-wht GBP-red NZD-yel CAD-blu CHF-green JPY-vio')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global T_v, n
    TimeCurrent(tim)
    if T_v != tim.min:
        T_v = tim.min
        n += 1
    ArrayInitialize(aug, 0)
    ArrayInitialize(eug, 0)
    ArrayInitialize(gug, 0)
    ArrayInitialize(nug, 0)
    ArrayInitialize(cug, 0)
    ArrayInitialize(hug, 0)
    ArrayInitialize(jug, 0)
    CopyRates('AUDUSD', 0, 0, n + 1, AU)
    CopyRates('EURUSD', 0, 0, n + 1, EU)
    CopyRates('GBPUSD', 0, 0, n + 1, GU)
    CopyRates('NZDUSD', 0, 0, n + 1, NU)
    CopyRates('USDCAD', 0, 0, n + 1, UC)
    CopyRates('USDCHF', 0, 0, n + 1, UH)
    CopyRates('USDJPY', 0, 0, n + 1, UJ)
    au = 0.0
    eu = 0.0
    gu = 0.0
    nu = 0.0
    uc = 0.0
    uh = 0.0
    uj = 0.0
    for i in range(n, 0 - 1, -1):
        if (AU[i].close * AU[n].close) > 0:
            au += k * (1 - _fdiv(AU[n].close, AU[i].close) - au)
            aug[i] = au
        if (EU[i].close * EU[n].close) > 0:
            eu += k * (1 - _fdiv(EU[n].close, EU[i].close) - eu)
            eug[i] = eu
        if (GU[i].close * GU[n].close) > 0:
            gu += k * (1 - _fdiv(GU[n].close, GU[i].close) - gu)
            gug[i] = gu
        if (NU[i].close * NU[n].close) > 0:
            nu += k * (1 - _fdiv(NU[n].close, NU[i].close) - nu)
            nug[i] = nu
        if (UC[i].close * UC[n].close) > 0:
            uc += k * (1 - _fdiv(UC[i].close, UC[n].close) - uc)
            cug[i] = uc
        if (UH[i].close * UH[n].close) > 0:
            uh += k * (1 - _fdiv(UH[i].close, UH[n].close) - uh)
            hug[i] = uh
        if (UJ[i].close * UJ[n].close) > 0:
            uj += k * (1 - _fdiv(UJ[i].close, UJ[n].close) - uj)
            jug[i] = uj
    return rates_total

# ---- global variables initialised from expressions
AU = Arr(0, 0, factory=MqlRates)
EU = Arr(0, 0, factory=MqlRates)
GU = Arr(0, 0, factory=MqlRates)
NU = Arr(0, 0, factory=MqlRates)
UC = Arr(0, 0, factory=MqlRates)
UH = Arr(0, 0, factory=MqlRates)
UJ = Arr(0, 0, factory=MqlRates)
tim = MqlDateTime()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiUsdInd(_MQL5Indicator):
    name = 'multi_usd_ind'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'k': 1.0,  # Smoothing factor
        'p': 60,  # Period
    }

