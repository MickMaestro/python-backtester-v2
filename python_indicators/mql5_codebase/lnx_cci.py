"""lnx_cci — converted from MQL5: MQL5 Indicators/Lnx CCI/lnx_cci.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 15, 'indicator_plots': 5}, 'types': {1: 10, 2: 1}, 'colors': {1: [6908265, 32768, 255, 65535], 2: [6908265], 3: [55295], 4: [32768, 255], 5: [32768, 255]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 4, 5: 4}, 'styles': {}, 'labels': {1: 'CCI', 2: 'CCI', 3: 'Turbo CCI', 4: 'LSMA trend', 5: 'EMA trend'}, 'levels': [100.0, 200.0, 300.0, -100.0, -200.0, -300.0], 'description': [], 'name': 'lnx_cci', 'source': 'MQL5 Indicators/Lnx CCI/lnx_cci.mq5', 'folder': 'Lnx CCI', 'inputs': [{'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': 'CCI calculation period', 'sinput': False}, {'mql': 'TrendPeriod', 'py': 'TrendPeriod', 'param': 'TrendPeriod', 'type': 'int', 'default': 6, 'label': 'Number of bars determining trend', 'sinput': False}, {'mql': '_0', 'py': '_0', 'param': None, 'type': 'string', 'default': '', 'label': 'Turbo CCI parameters', 'sinput': False}, {'mql': 'ShowTurboCCI', 'py': 'ShowTurboCCI', 'param': 'ShowTurboCCI', 'type': 'bool', 'default': False, 'label': 'Show turbo CCI', 'sinput': False}, {'mql': 'TurboCCIPeriod', 'py': 'TurboCCIPeriod', 'param': 'TurboCCIPeriod', 'type': 'int', 'default': 5, 'label': 'Turbo CCI calculation period', 'sinput': False}, {'mql': '_1', 'py': '_1', 'param': None, 'type': 'string', 'default': '', 'label': 'LSMA parameters', 'sinput': False}, {'mql': 'ShowLSMA', 'py': 'ShowLSMA', 'param': 'ShowLSMA', 'type': 'bool', 'default': True, 'label': 'Show LSMA trend', 'sinput': False}, {'mql': 'LSMAPeriod', 'py': 'LSMAPeriod', 'param': 'LSMAPeriod', 'type': 'int', 'default': 25, 'label': 'LSMA period', 'sinput': False}, {'mql': 'LSMAPrice', 'py': 'LSMAPrice', 'param': 'LSMAPrice', 'type': 'int', 'default': 1, 'label': 'LSMA aplied price', 'sinput': False}, {'mql': 'LSMAPosition', 'py': 'LSMAPosition', 'param': 'LSMAPosition', 'type': 'int', 'default': 10, 'label': 'LSMA drawing position', 'sinput': False}, {'mql': '_2', 'py': '_2', 'param': None, 'type': 'string', 'default': '', 'label': 'EMA parameters', 'sinput': False}, {'mql': 'ShowEMA', 'py': 'ShowEMA', 'param': 'ShowEMA', 'type': 'bool', 'default': True, 'label': 'Show EMA trend', 'sinput': False}, {'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'int', 'default': 34, 'label': 'EMA period', 'sinput': False}, {'mql': 'EMAPrice', 'py': 'EMAPrice', 'param': 'EMAPrice', 'type': 'int', 'default': 1, 'label': 'EMA aplied price', 'sinput': False}, {'mql': 'EMAPosition', 'py': 'EMAPosition', 'param': 'EMAPosition', 'type': 'int', 'default': -10, 'label': 'EMA drawing position', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCIPeriod = _input('CCIPeriod', 14)  # CCI calculation period
TrendPeriod = _input('TrendPeriod', 6)  # Number of bars determining trend
_0 = _input('_0', '')  # Turbo CCI parameters
ShowTurboCCI = _input('ShowTurboCCI', False)  # Show turbo CCI
TurboCCIPeriod = _input('TurboCCIPeriod', 5)  # Turbo CCI calculation period
_1 = _input('_1', '')  # LSMA parameters
ShowLSMA = _input('ShowLSMA', True)  # Show LSMA trend
LSMAPeriod = _input('LSMAPeriod', 25)  # LSMA period
LSMAPrice = _input('LSMAPrice', PRICE_CLOSE)  # LSMA aplied price
LSMAPosition = _input('LSMAPosition', 10)  # LSMA drawing position
_2 = _input('_2', '')  # EMA parameters
ShowEMA = _input('ShowEMA', True)  # Show EMA trend
EMAPeriod = _input('EMAPeriod', 34)  # EMA period
EMAPrice = _input('EMAPrice', PRICE_CLOSE)  # EMA aplied price
EMAPosition = _input('EMAPosition', -10)  # EMA drawing position
CCIHisto = Arr(0, 0.0)
CCIColors = Arr(0, 0.0)
CCILine = Arr(0, 0.0)
TurboCCILine = Arr(0, 0.0)
LSMALine = Arr(0, 0.0)
LSMAColors = Arr(0, 0.0)
EMALine = Arr(0, 0.0)
EMAColors = Arr(0, 0.0)
TrendBufferUp = Arr(0, 0.0)
TrendBufferDn = Arr(0, 0.0)
LsmaMABuffer1 = Arr(0, 0.0)
LsmaMABuffer2 = Arr(0, 0.0)
EmaMABuffer = Arr(0, 0.0)
CCIBuffer = Arr(0, 0.0)
TurboCCIBuffer = Arr(0, 0.0)
LsmaMaHandle1 = 0
LsmaMaHandle2 = 0
EmaMaHandle = 0
CCIHandle = 0
TurboCCIHandle = 0

def OnInit():
    global CCIHandle, EmaMaHandle, LsmaMaHandle1, LsmaMaHandle2, TurboCCIHandle
    SetIndexBuffer(0, CCIHisto, INDICATOR_DATA)
    ArraySetAsSeries(CCIHisto, True)
    SetIndexBuffer(1, CCIColors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(CCIColors, True)
    SetIndexBuffer(2, CCILine, INDICATOR_DATA)
    ArraySetAsSeries(CCILine, True)
    SetIndexBuffer(3, TurboCCILine, INDICATOR_DATA)
    ArraySetAsSeries(TurboCCILine, True)
    SetIndexBuffer(4, LSMALine, INDICATOR_DATA)
    ArraySetAsSeries(LSMALine, True)
    SetIndexBuffer(5, LSMAColors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(LSMAColors, True)
    SetIndexBuffer(6, EMALine, INDICATOR_DATA)
    ArraySetAsSeries(EMALine, True)
    SetIndexBuffer(7, EMAColors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(EMAColors, True)
    SetIndexBuffer(8, LsmaMABuffer1, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(LsmaMABuffer1, True)
    SetIndexBuffer(9, LsmaMABuffer2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(LsmaMABuffer2, True)
    SetIndexBuffer(10, EmaMABuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(EmaMABuffer, True)
    SetIndexBuffer(11, CCIBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(CCIBuffer, True)
    SetIndexBuffer(12, TurboCCIBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TurboCCIBuffer, True)
    SetIndexBuffer(13, TrendBufferUp, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TrendBufferUp, True)
    SetIndexBuffer(14, TrendBufferDn, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TrendBufferDn, True)
    if ShowTurboCCI:
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
    else:
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
    if ShowLSMA:
        PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
    else:
        PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_NONE)
    if ShowEMA:
        PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
    else:
        PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_NONE)
    cLSMAPeriod = (LSMAPeriod if (LSMAPeriod > 0) else 1)
    cEMAPeriod = (EMAPeriod if (EMAPeriod > 0) else 1)
    cCCIPeriod = (CCIPeriod if (CCIPeriod > 0) else 1)
    cTurboCCIPeriod = (TurboCCIPeriod if (TurboCCIPeriod > 0) else 1)
    LsmaMaHandle1 = iMA(None, 0, cLSMAPeriod, 0, MODE_SMA, LSMAPrice)
    LsmaMaHandle2 = iMA(None, 0, cLSMAPeriod, 0, MODE_LWMA, LSMAPrice)
    EmaMaHandle = iMA(None, 0, cEMAPeriod, 0, MODE_EMA, EMAPrice)
    CCIHandle = iCCI(None, 0, cCCIPeriod, PRICE_TYPICAL)
    TurboCCIHandle = iCCI(None, 0, cTurboCCIPeriod, PRICE_TYPICAL)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Lnx CCI (' + _str(CCIPeriod) + ',' + _str(TurboCCIPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    if not checkCalculated(LsmaMaHandle1, rates_total, 'LSMA MA 1'):
        return prev_calculated
    if not checkCalculated(LsmaMaHandle2, rates_total, 'LSMA MA 2'):
        return prev_calculated
    if not checkCalculated(EmaMaHandle, rates_total, 'EMA MA'):
        return prev_calculated
    if not checkCalculated(CCIHandle, rates_total, 'CCI'):
        return prev_calculated
    if not checkCalculated(TurboCCIHandle, rates_total, 'Turbo CCI'):
        return prev_calculated
    if not doCopy(LsmaMaHandle1, LsmaMABuffer1, 0, limit, 'LSMA MA buffer 1'):
        return prev_calculated
    if not doCopy(LsmaMaHandle2, LsmaMABuffer2, 0, limit, 'LSMA MA buffer 2'):
        return prev_calculated
    if not doCopy(EmaMaHandle, EmaMABuffer, 0, limit, 'EMA buffer'):
        return prev_calculated
    if not doCopy(CCIHandle, CCILine, 0, limit, 'CCI line'):
        return prev_calculated
    if not doCopy(TurboCCIHandle, TurboCCILine, 0, limit, 'Turbo CCI line'):
        return prev_calculated
    if not ArrayGetAsSeries(close):
        ArraySetAsSeries(close, True)
    if prev_calculated == 0:
        limit -= 2
        EMAColors[rates_total - 1] = 0.0
        LSMAColors[rates_total - 1] = 0.0
        CCIColors[rates_total - 1] = 0.0
    for i in range(limit, 0 - 1, -1):
        k = 0
        s = 0
        if CCILine[i] > 0:
            if TrendBufferUp[i + 1] != EMPTY_VALUE:
                s = TrendPeriod
            else:
                k = 1
                s = 1
                while k < TrendPeriod and (i + k) < rates_total:
                    if TrendBufferDn[i + k] != EMPTY_VALUE:
                        break
                    k += 1
                    s += 1
        if CCILine[i] < 0:
            if TrendBufferDn[i + 1] != EMPTY_VALUE:
                s = -TrendPeriod
            else:
                k = 1
                s = -1
                while k < TrendPeriod and (i + k) < rates_total:
                    if TrendBufferUp[i + k] != EMPTY_VALUE:
                        break
                    k += 1
                    s -= 1
        TrendBufferUp[i] = EMPTY_VALUE
        TrendBufferDn[i] = EMPTY_VALUE
        if s == TrendPeriod:
            TrendBufferUp[i] = CCILine[i]
        if s == (-TrendPeriod):
            TrendBufferDn[i] = CCILine[i]
        CCIHisto[i] = CCILine[i]
        CCIColors[i] = 0.0
        if TrendBufferUp[i] != EMPTY_VALUE:
            CCIColors[i] = 1.0
        if TrendBufferDn[i] != EMPTY_VALUE:
            CCIColors[i] = 2.0
        if MathAbs(s) == (TrendPeriod - 1):
            CCIColors[i] = 3.0
        lsma = (3.0 * LsmaMABuffer1[i]) - (2.0 * LsmaMABuffer2[i])
        LSMALine[i] = LSMAPosition
        LSMAColors[i] = LSMAColors[i + 1]
        if close[i] > lsma:
            LSMAColors[i] = 0.0
        if close[i] < lsma:
            LSMAColors[i] = 1.0
        EMALine[i] = EMAPosition
        EMAColors[i] = EMAColors[i + 1]
        if close[i] > EmaMABuffer[i]:
            EMAColors[i] = 0.0
        if close[i] < EmaMABuffer[i]:
            EMAColors[i] = 1.0
    return rates_total

def checkCalculated(bufferHandle, total, checkDescription):
    calculated = BarsCalculated(bufferHandle)
    if calculated < total:
        Print('Not all data of ' + checkDescription + ' calculated (', _str(total - calculated), ' un-calculated bars )')
        return False
    return True

def doCopy(bufferHandle, buffer, buffNum, copyCount, copyDescription):
    if CopyBuffer(bufferHandle, buffNum, 0, copyCount, buffer) <= 0:
        Print('Getting ' + copyDescription + ' failed! Error', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LnxCci(_MQL5Indicator):
    name = 'lnx_cci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'CCIPeriod': 14,  # CCI calculation period
        'TrendPeriod': 6,  # Number of bars determining trend
        'ShowTurboCCI': False,  # Show turbo CCI
        'TurboCCIPeriod': 5,  # Turbo CCI calculation period
        'ShowLSMA': True,  # Show LSMA trend
        'LSMAPeriod': 25,  # LSMA period
        'LSMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # LSMA aplied price
        'LSMAPosition': 10,  # LSMA drawing position
        'ShowEMA': True,  # Show EMA trend
        'EMAPeriod': 34,  # EMA period
        'EMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # EMA aplied price
        'EMAPosition': -10,  # EMA drawing position
    }

