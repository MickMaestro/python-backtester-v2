"""CCI_OBOS_With_Confirmation — converted from MQL5: MQL5 Indicators/CCI_OBOS_With_Confirmation/CCI_OBOS_With_Confirmation.mq5

CCI OBOS With Confirmation indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 15, 'indicator_plots': 3}, 'types': {1: 17, 2: 5, 3: 5}, 'colors': {1: [32768, 8388352, 255, 42495, 16748574, 11119017], 2: [32768], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Open;High;Low;Close', 2: 'Bullish signal', 3: 'Bearish signal'}, 'levels': [], 'description': ['CCI OBOS With Confirmation indicator'], 'name': 'CCI_OBOS_With_Confirmation', 'source': 'MQL5 Indicators/CCI_OBOS_With_Confirmation/CCI_OBOS_With_Confirmation.mq5', 'folder': 'CCI_OBOS_With_Confirmation', 'inputs': [{'mql': 'InpPeriodOBOS', 'py': 'InpPeriodOBOS', 'param': 'InpPeriodOBOS', 'type': 'uint', 'default': 9, 'label': 'OBOS period', 'sinput': False}, {'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpColorCandle', 'py': 'InpColorCandle', 'param': 'InpColorCandle', 'type': 'int', 'default': 0, 'label': 'Color candle', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodOBOS = _input('InpPeriodOBOS', 9)  # OBOS period
InpPeriodCCI = _input('InpPeriodCCI', 14)  # CCI period
InpColorCandle = _input('InpColorCandle', INPUT_NO)  # Color candle
BufferUp = Arr(0, 0.0)
BufferDn = Arr(0, 0.0)
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferUpOBOS = Arr(0, 0.0)
BufferDnOBOS = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferAvgRAW = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
period_obos = 0
period_cci = 0
handle_ma = 0
handle_dev = 0
handle_cci = 0

def OnInit():
    global handle_cci, handle_dev, handle_ma, period_cci, period_obos
    period_obos = (1 if (InpPeriodOBOS < 1) else InpPeriodOBOS)
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    SetIndexBuffer(0, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferUp, INDICATOR_DATA)
    SetIndexBuffer(6, BufferDn, INDICATOR_DATA)
    SetIndexBuffer(7, BufferCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferUpOBOS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferDnOBOS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferAvgRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferDev, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI OBOS With Confirmation (' + _str(period_obos) + ',' + _str(period_cci) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, InpColorCandle)
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferUp, True)
    ArraySetAsSeries(BufferDn, True)
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferUpOBOS, True)
    ArraySetAsSeries(BufferDnOBOS, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferAvgRAW, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_obos, 0, MODE_EMA, PRICE_WEIGHTED)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_obos), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_obos, 0, MODE_EMA, PRICE_WEIGHTED)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_obos), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_obos, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferUp, EMPTY_VALUE)
        ArrayInitialize(BufferDn, EMPTY_VALUE)
        ArrayInitialize(BufferCCI, 0)
        ArrayInitialize(BufferUpOBOS, 0)
        ArrayInitialize(BufferDnOBOS, 0)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferAvgRAW, 0)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDev, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferPrice[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        BufferRAW[i] = (_fdiv((BufferPrice[i] - BufferMA[i]) * 100.0, BufferDev[i]) if (BufferDev[i] != 0) else 0)
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_obos, BufferRAW, BufferAvgRAW) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_obos, BufferAvgRAW, BufferUpOBOS) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_obos, BufferUpOBOS, BufferDnOBOS) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferUp[i] = EMPTY_VALUE
        BufferDn[i] = BufferUp[i]
        OBOS_H0 = fmax(BufferUpOBOS[i], BufferDnOBOS[i])
        OBOS_H1 = fmax(BufferUpOBOS[i + 1], BufferDnOBOS[i + 1])
        OBOS_L0 = fmin(BufferUpOBOS[i], BufferDnOBOS[i])
        OBOS_L1 = fmin(BufferUpOBOS[i + 1], BufferDnOBOS[i + 1])
        if BufferCCI[i + 1] < OBOS_H1 and BufferCCI[i] > OBOS_H0:
            BufferUp[i] = open[i]
        else:
            if BufferCCI[i + 1] > OBOS_L1 and BufferCCI[i] < OBOS_L0:
                BufferDn[i] = open[i]
        if InpColorCandle:
            BufferCandleOpen[i] = open[i]
            BufferCandleHigh[i] = high[i]
            BufferCandleLow[i] = low[i]
            BufferCandleClose[i] = close[i]
            if BufferUpOBOS[i + 1] < BufferUpOBOS[i] and BufferDnOBOS[i + 1] < BufferDnOBOS[i]:
                BufferColors[i] = (0 if (open[i] < close[i]) else 1 if (open[i] > close[i]) else 5)
            elif BufferUpOBOS[i + 1] > BufferUpOBOS[i] and BufferDnOBOS[i + 1] > BufferDnOBOS[i]:
                BufferColors[i] = (2 if (open[i] > close[i]) else 3 if (open[i] < close[i]) else 5)
            else:
                BufferColors[i] = 4.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIOBOSWithConfirmation(_MQL5Indicator):
    name = 'CCI_OBOS_With_Confirmation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodOBOS': 9,  # OBOS period
        'InpPeriodCCI': 14,  # CCI period
        'InpColorCandle': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Color candle
    }

