"""3d_oscilatorsign — converted from MQL5: MQL5 Indicators/3D_OscilatorSign/3d_oscilatorsign.mq5

Copyright: Copyright © 2005, Luis Damiani; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Luis Damiani', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: '3D_Oscilator Sell', 2: '3D_Oscilator Buy'}, 'levels': [], 'description': [], 'name': '3d_oscilatorsign', 'source': 'MQL5 Indicators/3D_OscilatorSign/3d_oscilatorsign.mq5', 'folder': '3D_OscilatorSign', 'inputs': [{'mql': 'D1RSIPer', 'py': 'D1RSIPer', 'param': 'D1RSIPer', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'D2StochPer', 'py': 'D2StochPer', 'param': 'D2StochPer', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'D3tunnelPer', 'py': 'D3tunnelPer', 'param': 'D3tunnelPer', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'hot', 'py': 'hot', 'param': 'hot', 'type': 'double', 'default': 0.4, 'label': '', 'sinput': False}, {'mql': 'sigsmooth', 'py': 'sigsmooth', 'param': 'sigsmooth', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
D1RSIPer = _input('D1RSIPer', 13)
D2StochPer = _input('D2StochPer', 8)
D3tunnelPer = _input('D3tunnelPer', 8)
hot = _input('hot', 0.4)
sigsmooth = _input('sigsmooth', 4)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
sk = 0.0
sk2 = 0.0
ss = 0
min_rates_total = 0
ATR_Handle = 0
RSI_Handle = 0
CCI_Handle = 0

def OnInit():
    global ATR_Handle, CCI_Handle, RSI_Handle, min_rates_total, sk, sk2, ss
    ss = sigsmooth
    if ss < 2:
        ss = 2
    sk = _fdiv(2.0, ss + 1.0)
    sk2 = _fdiv(2.0, (ss * 0.8) + 1.0)
    ATR_Period = 15
    min_rates_total = _int(D1RSIPer + D2StochPer + D2StochPer + hot + sigsmooth)
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    RSI_Handle = iRSI(None, 0, D1RSIPer, PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    CCI_Handle = iCCI(None, 0, D3tunnelPer, PRICE_TYPICAL)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = '3D OscillatorSign'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_ind, _s_OnCalculate_prev_sig
    if ((BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(CCI_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    rsi = 0.0
    maxrsi = 0.0
    minrsi = 0.0
    storsi = 0.0
    E3D = 0.0
    RSI = Arr(0, 0.0)
    CCI = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    rangrsi = 0.0
    ind = 0.0
    sig = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + D2StochPer + 3
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    to_copy = limit + 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        rsi = RSI[bar]
        maxrsi = rsi
        minrsi = rsi
        for iii in range(bar + D2StochPer, bar - 1, -1):
            rsi = RSI[iii]
            if rsi > maxrsi:
                maxrsi = rsi
            if rsi < minrsi:
                minrsi = rsi
        rangrsi = maxrsi - minrsi
        if rangrsi == 0:
            storsi = 0.0
        else:
            storsi = _fdiv(rsi - minrsi, (maxrsi - minrsi) * 200) - 100
        E3D = (hot * CCI[bar]) + ((1.0 - hot) * storsi)
        ind = (sk * E3D) + ((1.0 - sk) * _s_OnCalculate_prev_ind)
        sig = (sk2 * _s_OnCalculate_prev_ind) + ((1.0 - sk2) * _s_OnCalculate_prev_sig)
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if ind > sig and _s_OnCalculate_prev_ind < _s_OnCalculate_prev_sig:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if ind < sig and _s_OnCalculate_prev_ind > _s_OnCalculate_prev_sig:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_prev_ind = ind
            _s_OnCalculate_prev_sig = sig
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_ind = 0.0
_s_OnCalculate_prev_sig = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3dOscilatorsign(_MQL5Indicator):
    name = '3d_oscilatorsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'D1RSIPer': 13,
        'D2StochPer': 8,
        'D3tunnelPer': 8,
        'hot': 0.4,
        'sigsmooth': 4,
    }

