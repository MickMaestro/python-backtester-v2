"""RSI_OnChart — converted from MQL5: MQL5 Indicators/RSI on the Price Chart/RSI_OnChart.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {3: 1, 1: 1, 2: 1, 4: 1}, 'colors': {3: [32768], 1: [255], 2: [255], 4: [16748574]}, 'widths': {3: 1, 1: 1, 2: 1, 4: 1}, 'styles': {3: 0, 1: 0, 2: 0, 4: 0}, 'labels': {3: 'Middle', 1: 'Upper', 2: 'Lower', 4: 'RSI'}, 'levels': [], 'description': [], 'name': 'RSI_OnChart', 'source': 'MQL5 Indicators/RSI on the Price Chart/RSI_OnChart.mq5', 'folder': 'RSI on the Price Chart', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'Period RSI', 'sinput': False}, {'mql': 'InpAppliedPriceRSI', 'py': 'InpAppliedPriceRSI', 'param': 'InpAppliedPriceRSI', 'type': 'int', 'default': 1, 'label': 'Applied price RSI', 'sinput': False}, {'mql': 'InpOverBought', 'py': 'InpOverBought', 'param': 'InpOverBought', 'type': 'uint', 'default': 70, 'label': 'Level of overbought', 'sinput': False}, {'mql': 'InpOverSold', 'py': 'InpOverSold', 'param': 'InpOverSold', 'type': 'uint', 'default': 30, 'label': 'Level of oversold', 'sinput': False}, {'mql': 'InpCoeffATR', 'py': 'InpCoeffATR', 'param': 'InpCoeffATR', 'type': 'double', 'default': 5.0, 'label': 'Coefficient of ATR', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 20, 'label': 'Period MA', 'sinput': False}, {'mql': 'InpMethodMA', 'py': 'InpMethodMA', 'param': 'InpMethodMA', 'type': 'int', 'default': 0, 'label': 'Calculation method MA', 'sinput': False}, {'mql': 'InpAppliedPriceMA', 'py': 'InpAppliedPriceMA', 'param': 'InpAppliedPriceMA', 'type': 'int', 'default': 1, 'label': 'Applied price MA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # Period RSI
InpAppliedPriceRSI = _input('InpAppliedPriceRSI', PRICE_CLOSE)  # Applied price RSI
InpOverBought = _input('InpOverBought', 70)  # Level of overbought
InpOverSold = _input('InpOverSold', 30)  # Level of oversold
InpCoeffATR = _input('InpCoeffATR', 5.0)  # Coefficient of ATR
InpPeriodMA = _input('InpPeriodMA', 20)  # Period MA
InpMethodMA = _input('InpMethodMA', MODE_SMA)  # Calculation method MA
InpAppliedPriceMA = _input('InpAppliedPriceMA', PRICE_CLOSE)  # Applied price MA
BufferMiddle = Arr(0, 0.0)
BufferUpper = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferTempRSI = Arr(0, 0.0)
coeff = 0.0
period_rsi = 0
period_ma = 0
handle_ma = 0
handle_rsi = 0
handle_atr = 0

def OnInit():
    global coeff, handle_atr, handle_ma, handle_rsi, period_ma, period_rsi
    SetIndexBuffer(0, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(3, BufferRSI, INDICATOR_DATA)
    SetIndexBuffer(4, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferTempRSI, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI on chart')
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferTempRSI, True)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    coeff = (0.1 if (InpCoeffATR < 0.1) else InpCoeffATR)
    ResetLastError()
    handle_atr = iATR(Symbol(), PERIOD_CURRENT, period_ma)
    if handle_atr == INVALID_HANDLE:
        Print("Error creating ATR's handle: ", GetLastError())
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, period_ma, 0, InpMethodMA, InpAppliedPriceMA)
    if handle_ma == INVALID_HANDLE:
        Print("Error creating MA's handle: ", GetLastError())
    ResetLastError()
    handle_rsi = iRSI(Symbol(), PERIOD_CURRENT, period_rsi, InpAppliedPriceRSI)
    if handle_rsi == INVALID_HANDLE:
        Print("Error creating RSI's handle: ", GetLastError())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
        ArrayInitialize(BufferTempRSI, EMPTY_VALUE)
    copied = (rates_total if (limit > 1) else 1)
    copied_ma = CopyBuffer(handle_ma, 0, 0, copied, BufferMiddle)
    if copied_ma != copied:
        return 0
    copied_atr = CopyBuffer(handle_atr, 0, 0, copied, BufferATR)
    if copied_atr != copied:
        return 0
    copied_rsi = CopyBuffer(handle_rsi, 0, 0, copied, BufferTempRSI)
    if copied_rsi != copied:
        return 0
    for i in range(limit, 0 - 1, -1):
        atr = BufferATR[i] * coeff
        BufferUpper[i] = BufferMiddle[i] + ((atr * (InpOverBought - 50)) / 100.0)
        BufferLower[i] = BufferMiddle[i] - ((atr * (50 - InpOverSold)) / 100.0)
        BufferRSI[i] = BufferMiddle[i] + ((atr * (BufferTempRSI[i] - 50)) / 100.0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOnChart(_MQL5Indicator):
    name = 'RSI_OnChart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # Period RSI
        'InpAppliedPriceRSI': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price RSI
        'InpOverBought': 70,  # Level of overbought
        'InpOverSold': 30,  # Level of oversold
        'InpCoeffATR': 5.0,  # Coefficient of ATR
        'InpPeriodMA': 20,  # Period MA
        'InpMethodMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Calculation method MA
        'InpAppliedPriceMA': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price MA
    }

