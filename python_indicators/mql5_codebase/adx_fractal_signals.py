"""ADX_Fractal_Signals — converted from MQL5: MQL5 Indicators/ADX_Fractal_Signals/ADX_Fractal_Signals.mq5

ADX Fractal Signals indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Signal Buy', 2: 'Signal Sell'}, 'levels': [], 'description': ['ADX Fractal Signals indicator'], 'name': 'ADX_Fractal_Signals', 'source': 'MQL5 Indicators/ADX_Fractal_Signals/ADX_Fractal_Signals.mq5', 'folder': 'ADX_Fractal_Signals', 'inputs': [{'mql': 'InpPeriodADX', 'py': 'InpPeriodADX', 'param': 'InpPeriodADX', 'type': 'uint', 'default': 14, 'label': 'ADX period', 'sinput': False}, {'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 200, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpLevB', 'py': 'InpLevB', 'param': 'InpLevB', 'type': 'double', 'default': 0.0, 'label': 'CCI bullish signal level', 'sinput': False}, {'mql': 'InpLevS', 'py': 'InpLevS', 'param': 'InpLevS', 'type': 'double', 'default': 0.0, 'label': 'CCI bearish signal level', 'sinput': False}, {'mql': 'InpUseAlert', 'py': 'InpUseAlert', 'param': 'InpUseAlert', 'type': 'int', 'default': 1, 'label': 'Use alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodADX = _input('InpPeriodADX', 14)  # ADX period
InpPeriodCCI = _input('InpPeriodCCI', 200)  # CCI period
InpLevB = _input('InpLevB', 0.0)  # CCI bullish signal level
InpLevS = _input('InpLevS', 0.0)  # CCI bearish signal level
InpUseAlert = _input('InpUseAlert', INPUT_YES)  # Use alerts
BufferSigB = Arr(0, 0.0)
BufferSigS = Arr(0, 0.0)
BufferADX = Arr(0, 0.0)
BufferDMIP = Arr(0, 0.0)
BufferDMIM = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferFRU = Arr(0, 0.0)
BufferFRL = Arr(0, 0.0)
lev_buy_cci = 0.0
lev_sell_cci = 0.0
point = 0.0
period_adx = 0
period_cci = 0
handle_adx = 0
handle_cci = 0
handle_fr = 0

def OnInit():
    global handle_adx, handle_cci, handle_fr, lev_buy_cci, lev_sell_cci, period_adx, period_cci, point
    point = Point()
    period_adx = (1 if (InpPeriodADX < 1) else InpPeriodADX)
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    lev_buy_cci = InpLevB
    lev_sell_cci = InpLevS
    SetIndexBuffer(0, BufferSigB, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSigS, INDICATOR_DATA)
    SetIndexBuffer(2, BufferADX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDMIP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDMIM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferFRU, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferFRL, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADX Fractal Signals (' + _str(period_adx) + ',' + _str(period_cci) + ',' + DoubleToString(lev_buy_cci, 1) + ',' + DoubleToString(lev_sell_cci, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSigB, True)
    ArraySetAsSeries(BufferSigS, True)
    ArraySetAsSeries(BufferADX, True)
    ArraySetAsSeries(BufferDMIP, True)
    ArraySetAsSeries(BufferDMIM, True)
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferFRU, True)
    ArraySetAsSeries(BufferFRL, True)
    ResetLastError()
    handle_adx = iADX(None, PERIOD_CURRENT, period_adx)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX(', _str(period_adx), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_fr = iFractals(None, PERIOD_CURRENT)
    if handle_fr == INVALID_HANDLE:
        Print('The iFractals object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferSigB, EMPTY_VALUE)
        ArrayInitialize(BufferSigS, EMPTY_VALUE)
        ArrayInitialize(BufferADX, 0)
        ArrayInitialize(BufferDMIP, 0)
        ArrayInitialize(BufferDMIM, 0)
        ArrayInitialize(BufferCCI, 0)
        ArrayInitialize(BufferFRU, 0)
        ArrayInitialize(BufferFRL, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx, MAIN_LINE, 0, count, BufferADX)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, PLUSDI_LINE, 0, count, BufferDMIP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, MINUSDI_LINE, 0, count, BufferDMIM)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_fr, UPPER_LINE, 0, count, BufferFRU)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_fr, LOWER_LINE, 0, count, BufferFRL)
    if copied != count:
        return 0
    alert = ''
    for i in range(limit, 0 - 1, -1):
        BufferSigB[i] = EMPTY_VALUE
        BufferSigS[i] = BufferSigB[i]
        if ((((((BufferADX[i] > BufferADX[i + 1] and BufferADX[i + 1] > BufferADX[i + 2]) and BufferDMIP[i] > BufferDMIM[i]) and BufferCCI[i] > lev_buy_cci) and BufferCCI[i + 1] > lev_buy_cci) and BufferCCI[i + 2] > lev_buy_cci) and BufferFRL[i + 2] > 0) and BufferFRL[i + 2] < EMPTY_VALUE:
            BufferSigB[i] = low[i] - (20 * point)
            if limit > 1 and i == 0:
                alert = 'ADX Fractal Signal: BUY'
        if ((((((BufferADX[i] > BufferADX[i + 1] and BufferADX[i + 1] > BufferADX[i + 2]) and BufferDMIM[i] > BufferDMIP[i]) and BufferCCI[i] < lev_sell_cci) and BufferCCI[i + 1] < lev_sell_cci) and BufferCCI[i + 2] < lev_sell_cci) and BufferFRU[i + 2] > 0) and BufferFRU[i + 2] < EMPTY_VALUE:
            BufferSigS[i] = high[i] + (20 * point)
            if limit > 1 and i == 0:
                alert = 'ADX Fractal Signal: SELL'
    if (InpUseAlert and time[0] > _s_OnCalculate_last_time) and alert != '':
        Alert(Symbol() + ' ' + TimeframeToString(Period()) + ': ' + alert)
        _s_OnCalculate_last_time = TimeCurrent()
    return rates_total

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXFractalSignals(_MQL5Indicator):
    name = 'ADX_Fractal_Signals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodADX': 14,  # ADX period
        'InpPeriodCCI': 200,  # CCI period
        'InpLevB': 0.0,  # CCI bullish signal level
        'InpLevS': 0.0,  # CCI bearish signal level
        'InpUseAlert': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use alerts
    }

