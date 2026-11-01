"""usdx — converted from MQL5: MQL5 Indicators/USDx dollar index/usdx.mq5

Copyright: Copyright 2010, Bekmetov Denis; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, Bekmetov Denis', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'USDx'}, 'levels': [], 'description': [], 'name': 'usdx', 'source': 'MQL5 Indicators/USDx dollar index/usdx.mq5', 'folder': 'USDx dollar index', 'inputs': [{'mql': 'MaxBar', 'py': 'MaxBar', 'param': 'MaxBar', 'type': 'int', 'default': 1000, 'label': 'Number of bars for calculation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MaxBar = _input('MaxBar', 1000)  # Number of bars for calculation
USDx = Arr(0, 0.0)
mEURUSD = Arr(0, 0.0)
mUSDJPY = Arr(0, 0.0)
mGBPUSD = Arr(0, 0.0)
mUSDCAD = Arr(0, 0.0)
mUSDSEK = Arr(0, 0.0)
mUSDCHF = Arr(0, 0.0)
F = Arr(0, 0.0)
handle1 = 0
handle2 = 0
handle3 = 0
handle4 = 0
handle5 = 0
handle6 = 0
sEURUSD = 0.0
sUSDJPY = 0.0
sGBPUSD = 0.0
sUSDCAD = 0.0
sUSDSEK = 0.0
sUSDCHF = 0.0

def OnInit():
    SetIndexBuffer(0, USDx, INDICATOR_DATA)
    SetIndexBuffer(1, mEURUSD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, mUSDJPY, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, mGBPUSD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, mUSDCAD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, mUSDSEK, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, mUSDCHF, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(mEURUSD, True)
    ArraySetAsSeries(mUSDJPY, True)
    ArraySetAsSeries(mGBPUSD, True)
    ArraySetAsSeries(mUSDCAD, True)
    ArraySetAsSeries(mUSDSEK, True)
    ArraySetAsSeries(mUSDCHF, True)
    ArraySetAsSeries(USDx, True)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global sEURUSD, sGBPUSD, sUSDCAD, sUSDCHF, sUSDJPY, sUSDSEK
    if rates_total != prev_calculated:
        if ((((CopyClose('EURUSD', PERIOD_CURRENT, 0, MaxBar, mEURUSD) <= 0 or CopyClose('USDJPY', PERIOD_CURRENT, 0, MaxBar, mUSDJPY) <= 0) or CopyClose('GBPUSD', PERIOD_CURRENT, 0, MaxBar, mGBPUSD) <= 0) or CopyClose('USDCAD', PERIOD_CURRENT, 0, MaxBar, mUSDCAD) <= 0) or CopyClose('USDSEK', PERIOD_CURRENT, 0, MaxBar, mUSDSEK) <= 0) or CopyClose('USDCHF', PERIOD_CURRENT, 0, MaxBar, mUSDCHF) <= 0:
            return 0
    i = 0
    i = prev_calculated
    for i in range(i, rates_total):
        sEURUSD = MathPow(mEURUSD[i], -0.576)
        sUSDJPY = MathPow(mUSDJPY[i], 0.136)
        sGBPUSD = MathPow(mGBPUSD[i], -0.119)
        sUSDCAD = MathPow(mUSDCAD[i], 0.091)
        sUSDSEK = MathPow(mUSDSEK[i], 0.042)
        sUSDCHF = MathPow(mUSDCHF[i], 0.036)
        USDx[i] = 50.14348112 * sEURUSD * sUSDJPY * sGBPUSD * sUSDCAD * sUSDSEK * sUSDCHF
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def OnTradeTransaction(trans, request, result):
    pass


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Usdx(_MQL5Indicator):
    name = 'usdx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MaxBar': 1000,  # Number of bars for calculation
    }

