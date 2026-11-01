"""Laguerre_ADXSign — converted from MQL5: MQL5 Indicators/Laguerre_ADXSign/Laguerre_ADXSign.mq5

Copyright: Copyright © 2007, Emerald King / transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Emerald King / transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Laguerre_ADX Sell', 2: 'Laguerre_ADX Buy'}, 'levels': [], 'description': [], 'name': 'Laguerre_ADXSign', 'source': 'MQL5 Indicators/Laguerre_ADXSign/Laguerre_ADXSign.mq5', 'folder': 'Laguerre_ADXSign', 'inputs': [{'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.764, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXPeriod = _input('ADXPeriod', 14)
gamma = _input('gamma', 0.764)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ADX_Handle = 0
ATR_Handle = 0

def OnInit():
    global ADX_Handle, ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, ADXPeriod))
    ADX_Handle = iADX(None, 0, ADXPeriod)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iADX')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(BuyBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LDMIM_, _s_OnCalculate_LDMIP_, _s_OnCalculate_mL0A_, _s_OnCalculate_mL0_, _s_OnCalculate_mL1A_, _s_OnCalculate_mL1_, _s_OnCalculate_mL2A_, _s_OnCalculate_mL2_, _s_OnCalculate_mL3A_, _s_OnCalculate_mL3_, _s_OnCalculate_pL0A_, _s_OnCalculate_pL0_, _s_OnCalculate_pL1A_, _s_OnCalculate_pL1_, _s_OnCalculate_pL2A_, _s_OnCalculate_pL2_, _s_OnCalculate_pL3A_, _s_OnCalculate_pL3_
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(ADX_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    pL0 = 0.0
    pL1 = 0.0
    pL2 = 0.0
    pL3 = 0.0
    pL0A = 0.0
    pL1A = 0.0
    pL2A = 0.0
    pL3A = 0.0
    mL0 = 0.0
    mL1 = 0.0
    mL2 = 0.0
    mL3 = 0.0
    mL0A = 0.0
    mL1A = 0.0
    mL2A = 0.0
    mL3A = 0.0
    LDMIP = 0.0
    LDMIM = 0.0
    CU = 0.0
    CD = 0.0
    DMIP = Arr(0, 0.0)
    DMIM = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_pL0_ = 0.0
        _s_OnCalculate_pL1_ = 0.0
        _s_OnCalculate_pL2_ = 0.0
        _s_OnCalculate_pL3_ = 0.0
        _s_OnCalculate_pL0A_ = 0.0
        _s_OnCalculate_pL1A_ = 0.0
        _s_OnCalculate_pL2A_ = 0.0
        _s_OnCalculate_pL3A_ = 0.0
        _s_OnCalculate_mL0_ = 0.0
        _s_OnCalculate_mL1_ = 0.0
        _s_OnCalculate_mL2_ = 0.0
        _s_OnCalculate_mL3_ = 0.0
        _s_OnCalculate_mL0A_ = 0.0
        _s_OnCalculate_mL1A_ = 0.0
        _s_OnCalculate_mL2A_ = 0.0
        _s_OnCalculate_mL3A_ = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ADX_Handle, PLUSDI_LINE, 0, to_copy, DMIP) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, MINUSDI_LINE, 0, to_copy, DMIM) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(DMIP, True)
    ArraySetAsSeries(DMIM, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    pL0 = _s_OnCalculate_pL0_
    pL1 = _s_OnCalculate_pL1_
    pL2 = _s_OnCalculate_pL2_
    pL3 = _s_OnCalculate_pL3_
    pL0A = _s_OnCalculate_pL0A_
    pL1A = _s_OnCalculate_pL1A_
    pL2A = _s_OnCalculate_pL2A_
    pL3A = _s_OnCalculate_pL3A_
    mL0 = _s_OnCalculate_mL0_
    mL1 = _s_OnCalculate_mL1_
    mL2 = _s_OnCalculate_mL2_
    mL3 = _s_OnCalculate_mL3_
    mL0A = _s_OnCalculate_mL0A_
    mL1A = _s_OnCalculate_mL1A_
    mL2A = _s_OnCalculate_mL2A_
    mL3A = _s_OnCalculate_mL3A_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        pL0A = pL0
        pL1A = pL1
        pL2A = pL2
        pL3A = pL3
        pL0 = ((1 - gamma) * DMIP[bar]) + (gamma * pL0A)
        pL1 = ((-gamma) * pL0) + pL0A + (gamma * pL1A)
        pL2 = ((-gamma) * pL1) + pL1A + (gamma * pL2A)
        pL3 = ((-gamma) * pL2) + pL2A + (gamma * pL3A)
        CU = 0.0
        CD = 0.0
        if pL0 >= pL1:
            CU = pL0 - pL1
        else:
            CD = pL1 - pL0
        if pL1 >= pL2:
            CU += pL1 - pL2
        else:
            CD += pL2 - pL1
        if pL2 >= pL3:
            CU += pL2 - pL3
        else:
            CD += pL3 - pL2
        if (CU + CD) != 0:
            LDMIP = _fdiv(CU, CU + CD)
        mL0A = mL0
        mL1A = mL1
        mL2A = mL2
        mL3A = mL3
        mL0 = ((1 - gamma) * DMIM[bar]) + (gamma * mL0A)
        mL1 = ((-gamma) * mL0) + mL0A + (gamma * mL1A)
        mL2 = ((-gamma) * mL1) + mL1A + (gamma * mL2A)
        mL3 = ((-gamma) * mL2) + mL2A + (gamma * mL3A)
        CU = 0.0
        CD = 0.0
        if mL0 >= mL1:
            CU = mL0 - mL1
        else:
            CD = mL1 - mL0
        if mL1 >= mL2:
            CU += mL1 - mL2
        else:
            CD += mL2 - mL1
        if mL2 >= mL3:
            CU += mL2 - mL3
        else:
            CD += mL3 - mL2
        if (CU + CD) != 0:
            LDMIM = _fdiv(CU, CU + CD)
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if _s_OnCalculate_LDMIP_ <= _s_OnCalculate_LDMIM_ and LDMIP > LDMIM:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_LDMIP_ >= _s_OnCalculate_LDMIM_ and LDMIP < LDMIM:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar == 1:
            _s_OnCalculate_pL0_ = pL0
            _s_OnCalculate_pL1_ = pL1
            _s_OnCalculate_pL2_ = pL2
            _s_OnCalculate_pL3_ = pL3
            _s_OnCalculate_pL0A_ = pL0A
            _s_OnCalculate_pL1A_ = pL1A
            _s_OnCalculate_pL2A_ = pL2A
            _s_OnCalculate_pL3A_ = pL3A
            _s_OnCalculate_mL0_ = mL0
            _s_OnCalculate_mL1_ = mL1
            _s_OnCalculate_mL2_ = mL2
            _s_OnCalculate_mL3_ = mL3
            _s_OnCalculate_mL0A_ = mL0A
            _s_OnCalculate_mL1A_ = mL1A
            _s_OnCalculate_mL2A_ = mL2A
            _s_OnCalculate_mL3A_ = mL3A
        if bar:
            _s_OnCalculate_LDMIP_ = LDMIP
            _s_OnCalculate_LDMIM_ = LDMIM
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_pL0_ = 0.0
_s_OnCalculate_pL1_ = 0.0
_s_OnCalculate_pL2_ = 0.0
_s_OnCalculate_pL3_ = 0.0
_s_OnCalculate_pL0A_ = 0.0
_s_OnCalculate_pL1A_ = 0.0
_s_OnCalculate_pL2A_ = 0.0
_s_OnCalculate_pL3A_ = 0.0
_s_OnCalculate_LDMIP_ = 0.0
_s_OnCalculate_mL0_ = 0.0
_s_OnCalculate_mL1_ = 0.0
_s_OnCalculate_mL2_ = 0.0
_s_OnCalculate_mL3_ = 0.0
_s_OnCalculate_mL0A_ = 0.0
_s_OnCalculate_mL1A_ = 0.0
_s_OnCalculate_mL2A_ = 0.0
_s_OnCalculate_mL3A_ = 0.0
_s_OnCalculate_LDMIM_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreADXSign(_MQL5Indicator):
    name = 'Laguerre_ADXSign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXPeriod': 14,
        'gamma': 0.764,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

