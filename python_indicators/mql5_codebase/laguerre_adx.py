"""Laguerre_ADX — converted from MQL5: MQL5 Indicators/Laguerre_ADX/Laguerre_ADX.mq5

Copyright: Copyright © 2007, Emerald King / transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Emerald King / transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Laguerre_ADX'}, 'levels': [0.75, 0.45, 0.15], 'description': [], 'name': 'Laguerre_ADX', 'source': 'MQL5 Indicators/Laguerre_ADX/Laguerre_ADX.mq5', 'folder': 'Laguerre_ADX', 'inputs': [{'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.764, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXPeriod = _input('ADXPeriod', 14)
gamma = _input('gamma', 0.764)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
ADX_Handle = 0

def OnInit():
    global ADX_Handle, min_rates_total
    min_rates_total = _int(ADXPeriod)
    ADX_Handle = iADX(None, 0, ADXPeriod)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iADX')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_mL0A_, _s_OnCalculate_mL0_, _s_OnCalculate_mL1A_, _s_OnCalculate_mL1_, _s_OnCalculate_mL2A_, _s_OnCalculate_mL2_, _s_OnCalculate_mL3A_, _s_OnCalculate_mL3_, _s_OnCalculate_pL0A_, _s_OnCalculate_pL0_, _s_OnCalculate_pL1A_, _s_OnCalculate_pL1_, _s_OnCalculate_pL2A_, _s_OnCalculate_pL2_, _s_OnCalculate_pL3A_, _s_OnCalculate_pL3_
    if BarsCalculated(ADX_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    LDMIP = 0.0
    LDMIM = 0.0
    CU = 0.0
    CD = 0.0
    DMIP = Arr(0, 0.0)
    DMIM = Arr(0, 0.0)
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
    ArraySetAsSeries(DMIP, True)
    L0 = _s_OnCalculate_pL0_
    L1 = _s_OnCalculate_pL1_
    L2 = _s_OnCalculate_pL2_
    L3 = _s_OnCalculate_pL3_
    L0A = _s_OnCalculate_pL0A_
    L1A = _s_OnCalculate_pL1A_
    L2A = _s_OnCalculate_pL2A_
    L3A = _s_OnCalculate_pL3A_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1 - gamma) * DMIP[bar]) + (gamma * L0A)
        L1 = ((-gamma) * L0) + L0A + (gamma * L1A)
        L2 = ((-gamma) * L1) + L1A + (gamma * L2A)
        L3 = ((-gamma) * L2) + L2A + (gamma * L3A)
        CU = 0.0
        CD = 0.0
        if L0 >= L1:
            CU = L0 - L1
        else:
            CD = L1 - L0
        if L1 >= L2:
            CU += L1 - L2
        else:
            CD += L2 - L1
        if L2 >= L3:
            CU += L2 - L3
        else:
            CD += L3 - L2
        if (CU + CD) != 0:
            LDMIP = _fdiv(CU, CU + CD)
        UpIndBuffer[bar] = LDMIP
        if bar == 1:
            _s_OnCalculate_pL0_ = L0
            _s_OnCalculate_pL1_ = L1
            _s_OnCalculate_pL2_ = L2
            _s_OnCalculate_pL3_ = L3
            _s_OnCalculate_pL0A_ = L0A
            _s_OnCalculate_pL1A_ = L1A
            _s_OnCalculate_pL2A_ = L2A
            _s_OnCalculate_pL3A_ = L3A
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if CopyBuffer(ADX_Handle, MINUSDI_LINE, 0, to_copy, DMIM) <= 0:
        return 0
    ArraySetAsSeries(DMIM, True)
    L0 = _s_OnCalculate_mL0_
    L1 = _s_OnCalculate_mL1_
    L2 = _s_OnCalculate_mL2_
    L3 = _s_OnCalculate_mL3_
    L0A = _s_OnCalculate_mL0A_
    L1A = _s_OnCalculate_mL1A_
    L2A = _s_OnCalculate_mL2A_
    L3A = _s_OnCalculate_mL3A_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1 - gamma) * DMIM[bar]) + (gamma * L0A)
        L1 = ((-gamma) * L0) + L0A + (gamma * L1A)
        L2 = ((-gamma) * L1) + L1A + (gamma * L2A)
        L3 = ((-gamma) * L2) + L2A + (gamma * L3A)
        CU = 0.0
        CD = 0.0
        if L0 >= L1:
            CU = L0 - L1
        else:
            CD = L1 - L0
        if L1 >= L2:
            CU += L1 - L2
        else:
            CD += L2 - L1
        if L2 >= L3:
            CU += L2 - L3
        else:
            CD += L3 - L2
        if (CU + CD) != 0:
            LDMIM = _fdiv(CU, CU + CD)
        DnIndBuffer[bar] = LDMIM
        if bar == 1:
            _s_OnCalculate_mL0_ = L0
            _s_OnCalculate_mL1_ = L1
            _s_OnCalculate_mL2_ = L2
            _s_OnCalculate_mL3_ = L3
            _s_OnCalculate_mL0A_ = L0A
            _s_OnCalculate_mL1A_ = L1A
            _s_OnCalculate_mL2A_ = L2A
            _s_OnCalculate_mL3A_ = L3A
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
_s_OnCalculate_mL0_ = 0.0
_s_OnCalculate_mL1_ = 0.0
_s_OnCalculate_mL2_ = 0.0
_s_OnCalculate_mL3_ = 0.0
_s_OnCalculate_mL0A_ = 0.0
_s_OnCalculate_mL1A_ = 0.0
_s_OnCalculate_mL2A_ = 0.0
_s_OnCalculate_mL3A_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreADX(_MQL5Indicator):
    name = 'Laguerre_ADX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXPeriod': 14,
        'gamma': 0.764,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

