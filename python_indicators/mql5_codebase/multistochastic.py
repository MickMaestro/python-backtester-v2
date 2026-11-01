"""multistochastic — converted from MQL5: MQL5 Indicators/Multistochastic/multistochastic.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 15, 'indicator_plots': 15}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 3, 12: 3, 13: 3, 14: 5, 15: 5}, 'colors': {1: [65280], 2: [255], 3: [65280], 4: [255], 5: [65280], 6: [255], 7: [14822282], 8: [14822282], 9: [14822282], 10: [14822282], 11: [8421504], 12: [255], 13: [65280], 14: [16776960], 15: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 5, 15: 5}, 'styles': {1: 0, 2: 4, 3: 0, 4: 4, 5: 0, 6: 4, 7: 0, 8: 0, 9: 0, 10: 0}, 'labels': {1: 'MultiStochastic', 2: 'MultiStochastic', 3: 'MultiStochastic', 4: 'MultiStochastic', 5: 'MultiStochastic', 6: 'MultiStochastic', 7: 'Level', 8: 'Level', 9: 'Level', 10: 'Level'}, 'levels': [280.0, 250.0, 220.0, 180.0, 150.0, 120.0, 80.0, 50.0, 20.0], 'description': [], 'name': 'multistochastic', 'source': 'MQL5 Indicators/Multistochastic/multistochastic.mq5', 'folder': 'Multistochastic', 'inputs': [{'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'int', 'default': 5, 'label': 'K-period (number of bars for calculations)', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'int', 'default': 3, 'label': 'D-period (primary smoothing period)', 'sinput': False}, {'mql': 'slowing', 'py': 'slowing', 'param': 'slowing', 'type': 'int', 'default': 3, 'label': 'Slowing period', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'Stochastic calculation method', 'sinput': False}, {'mql': 'SymbolA', 'py': 'SymbolA', 'param': None, 'type': 'string', 'default': 'EURJPY', 'label': '', 'sinput': False}, {'mql': 'SymbolB', 'py': 'SymbolB', 'param': None, 'type': 'string', 'default': 'EURJPY', 'label': '', 'sinput': False}, {'mql': 'SymbolC', 'py': 'SymbolC', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Kperiod = _input('Kperiod', 5)  # K-period (number of bars for calculations)
Dperiod = _input('Dperiod', 3)  # D-period (primary smoothing period)
slowing = _input('slowing', 3)  # Slowing period
ma_method = _input('ma_method', MODE_SMA)  # Smoothing type
price_field = _input('price_field', STO_LOWHIGH)  # Stochastic calculation method
SymbolA = _input('SymbolA', 'EURJPY')
SymbolB = _input('SymbolB', 'EURJPY')
SymbolC = _input('SymbolC', 'USDJPY')
Sto0_Buffer = Arr(0, 0.0)
Sto1_Buffer = Arr(0, 0.0)
Sto2_Buffer = Arr(0, 0.0)
Sig0_Buffer = Arr(0, 0.0)
Sig1_Buffer = Arr(0, 0.0)
Sig2_Buffer = Arr(0, 0.0)
Lev1_Buffer = Arr(0, 0.0)
Lev2_Buffer = Arr(0, 0.0)
Lev3_Buffer = Arr(0, 0.0)
Lev4_Buffer = Arr(0, 0.0)
Fl_Buffer = Arr(0, 0.0)
Dn_Buffer = Arr(0, 0.0)
Up_Buffer = Arr(0, 0.0)
UpEnd_Buffer = Arr(0, 0.0)
DnEnd_Buffer = Arr(0, 0.0)
MinBars = 0
CrossA = 0
CrossB = 0
CrossC = 0

def OnInit():
    global CrossA, CrossB, CrossC, MinBars
    CrossA = iStochastic(SymbolA, 0, Kperiod, Dperiod, slowing, ma_method, price_field)
    CrossB = iStochastic(SymbolB, 0, Kperiod, Dperiod, slowing, ma_method, price_field)
    CrossC = iStochastic(SymbolC, 0, Kperiod, Dperiod, slowing, ma_method, price_field)
    InitIndexBuffer1(0, Sto0_Buffer, 'Stochastic ' + SymbolA)
    InitIndexBuffer1(1, Sig0_Buffer, 'Signal Stochastic ' + SymbolA)
    InitIndexBuffer1(2, Sto1_Buffer, 'Stochastic ' + SymbolB)
    InitIndexBuffer1(3, Sig1_Buffer, 'Signal Stochastic ' + SymbolB)
    InitIndexBuffer1(4, Sto2_Buffer, 'Stochastic ' + SymbolC)
    InitIndexBuffer1(5, Sig2_Buffer, 'Signal Stochastic ' + SymbolC)
    InitIndexBuffer2(6, Lev1_Buffer, 'separator 0', 100)
    InitIndexBuffer2(7, Lev2_Buffer, 'separator 100', 100)
    InitIndexBuffer2(8, Lev3_Buffer, 'separator 200', 100)
    InitIndexBuffer2(9, Lev4_Buffer, 'separator 300', 100)
    InitIndexBuffer1(10, Fl_Buffer, 'Flat')
    InitIndexBuffer1(11, Dn_Buffer, 'DownTrend')
    InitIndexBuffer1(12, Up_Buffer, 'UpTrend')
    InitIndexBuffer1(13, DnEnd_Buffer, 'StopDown')
    InitIndexBuffer1(14, UpEnd_Buffer, 'StopUp')
    PlotIndexSetInteger(13, PLOT_ARROW, 159)
    PlotIndexSetInteger(14, PLOT_ARROW, 159)
    shortname = Box("")
    StringConcatenate(shortname, 'MultiStochastic( Kperiod = ', Kperiod, ', Dperiod = ', Dperiod, ', slowing = ', slowing, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    MinBars = Kperiod + Dperiod + slowing
    ArraySetAsSeries(Sto0_Buffer, True)
    ArraySetAsSeries(Sto1_Buffer, True)
    ArraySetAsSeries(Sto2_Buffer, True)
    ArraySetAsSeries(Sig0_Buffer, True)
    ArraySetAsSeries(Sig1_Buffer, True)
    ArraySetAsSeries(Sig2_Buffer, True)
    ArraySetAsSeries(Lev1_Buffer, True)
    ArraySetAsSeries(Lev2_Buffer, True)
    ArraySetAsSeries(Lev3_Buffer, True)
    ArraySetAsSeries(Lev4_Buffer, True)
    ArraySetAsSeries(Fl_Buffer, True)
    ArraySetAsSeries(Dn_Buffer, True)
    ArraySetAsSeries(Up_Buffer, True)
    ArraySetAsSeries(DnEnd_Buffer, True)
    ArraySetAsSeries(UpEnd_Buffer, True)

def InitIndexBuffer1(Number, Array, Label):
    SetIndexBuffer(Number, Array, INDICATOR_DATA)
    PlotIndexSetString(Number, PLOT_LABEL, Label)

def InitIndexBuffer2(Number, Array, Label, shift):
    SetIndexBuffer(Number, Array, INDICATOR_DATA)
    PlotIndexSetString(Number, PLOT_LABEL, Label)
    PlotIndexSetInteger(Number, PLOT_SHIFT, shift)

def Rates_Total(SymbolA_, SymbolB_, SymbolC_, BarMinimum):
    Bars0 = Bars(SymbolA_, 0)
    Bars1 = Bars(SymbolB_, 0)
    Bars2 = Bars(SymbolC_, 0)
    error = GetLastError()
    ResetLastError()
    if error == 4401:
        return 0
    if (BarsCalculated(CrossA) <= BarMinimum or BarsCalculated(CrossB) <= BarMinimum) or BarsCalculated(CrossC) <= BarMinimum:
        return 0
    return MathMin(Bars0, MathMin(Bars1, Bars2))

def SynchroCheck(SymbolA_, SymbolB_, SymbolC_):
    Time_ = Arr(1, 0, dyn=False)
    Vel0 = 0
    Vel1 = 0
    Vel2 = 0
    CopyTime(SymbolA_, 0, 0, 1, Time_)
    Vel0 = Time_[0]
    CopyTime(SymbolB_, 0, 0, 1, Time_)
    Vel1 = Time_[0]
    CopyTime(SymbolC_, 0, 0, 1, Time_)
    Vel2 = Time_[0]
    if Vel0 != Vel1 or Vel1 != Vel2:
        return False
    return True

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Bars_ = Rates_Total(SymbolA, SymbolA, SymbolC, MinBars * 5)
    if Bars_ < MinBars:
        return 0
    if not SynchroCheck(SymbolA, SymbolA, SymbolC):
        return prev_calculated
    limit = 0
    limit_ = 0
    bar = 0
    Dif0 = 0.0
    Dif1 = 0.0
    Dif2 = 0.0
    Up0 = False
    Up1 = False
    Up2 = False
    Dn0 = False
    Dn1 = False
    Dn2 = False
    if prev_calculated == 0:
        limit = Bars_ - 1 - MinBars
        bar = 0
        for bar in range(bar, rates_total):
            Lev1_Buffer[bar] = 100.0
            Lev2_Buffer[bar] = 200.0
            Lev3_Buffer[bar] = 0.0
            Lev4_Buffer[bar] = 300.0
            Sto0_Buffer[bar] = EMPTY_VALUE
            Sto1_Buffer[bar] = EMPTY_VALUE
            Sto2_Buffer[bar] = EMPTY_VALUE
            Sig0_Buffer[bar] = EMPTY_VALUE
            Sig1_Buffer[bar] = EMPTY_VALUE
            Sig2_Buffer[bar] = EMPTY_VALUE
        else:
            bar = _range_end(bar, rates_total, 1)
    else:
        limit = rates_total - prev_calculated
    limit_ = limit + 1
    if CopyBuffer(CrossA, 0, 0, limit_, Sto0_Buffer) < 0:
        Print('CopyBuffer Sto0_Buffer error =', GetLastError())
    if CopyBuffer(CrossA, 1, 0, limit_, Sig0_Buffer) < 0:
        Print('CopyBuffer Sig0_Buffer error =', GetLastError())
    if CopyBuffer(CrossB, 0, 0, limit_, Sto1_Buffer) < 0:
        Print('CopyBuffer Sto1_Buffer error =', GetLastError())
    if CopyBuffer(CrossB, 1, 0, limit_, Sig1_Buffer) < 0:
        Print('CopyBuffer Sig1_Buffer error =', GetLastError())
    if CopyBuffer(CrossC, 0, 0, limit_, Sto2_Buffer) < 0:
        Print('CopyBuffer Sto2_Buffer error =', GetLastError())
    if CopyBuffer(CrossC, 1, 0, limit_, Sig2_Buffer) < 0:
        Print('CopyBuffer Sig2_Buffer error =', GetLastError())
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Sto0_Buffer[bar] += 200
        Sig0_Buffer[bar] += 200
        Sto1_Buffer[bar] += 100
        Sig1_Buffer[bar] += 100
        Lev1_Buffer[bar] = 0.0
        Lev2_Buffer[bar] = 100.0
        Lev3_Buffer[bar] = 200.0
        Lev4_Buffer[bar] = 300.0
        Fl_Buffer[bar] = 300.0
        Dn_Buffer[bar] = 0.0
        Up_Buffer[bar] = 0.0
        Up0 = False
        Up1 = False
        Up2 = False
        Dn0 = False
        Dn1 = False
        Dn2 = False
        Dif0 = NormalizeDouble(Sto0_Buffer[bar] - Sig0_Buffer[bar], Digits() + 2)
        Dif1 = NormalizeDouble(Sto1_Buffer[bar] - Sig1_Buffer[bar], Digits() + 2)
        Dif2 = NormalizeDouble(Sto2_Buffer[bar] - Sig2_Buffer[bar], Digits() + 2)
        if Dif0 > 0:
            Up0 = True
        if Dif1 > 0:
            Up1 = True
        if Dif2 > 0:
            Up2 = True
        if Dif0 < 0:
            Dn0 = True
        if Dif1 < 0:
            Dn1 = True
        if Dif2 < 0:
            Dn2 = True
        if ((Up0 and Up1) and Dn2) and MathAbs(Dif1) > MathAbs(Dif2):
            Up2 = True
        if ((Up0 and Up2) and Dn1) and MathAbs(Dif2) > MathAbs(Dif1):
            Up1 = True
        if ((Dn0 and Dn1) and Up2) and MathAbs(Dif1) > MathAbs(Dif2):
            Dn2 = True
        if ((Dn0 and Dn2) and Up1) and MathAbs(Dif2) > MathAbs(Dif1):
            Dn1 = True
        if (Up0 and Up1) and (not Dn2):
            Up2 = True
        if (Up0 and Up2) and (not Dn1):
            Up1 = True
        if (Dn0 and Dn1) and (not Up2):
            Dn2 = True
        if (Dn0 and Dn2) and (not Up1):
            Dn1 = True
        if (Up1 and Up2) and (not Dn0):
            Up0 = True
        if (Dn1 and Dn2) and (not Up0):
            Dn0 = True
        if (Up0 and Up1) and Up2:
            Up_Buffer[bar] = 300.0
            Fl_Buffer[bar] = EMPTY_VALUE
        if (Dn0 and Dn1) and Dn2:
            Dn_Buffer[bar] = 300.0
            Fl_Buffer[bar] = EMPTY_VALUE
        DnEnd_Buffer[bar] = EMPTY_VALUE
        UpEnd_Buffer[bar] = EMPTY_VALUE
        if Up0:
            DnEnd_Buffer[bar] = 300.0
        if Dn0:
            UpEnd_Buffer[bar] = 300.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Multistochastic(_MQL5Indicator):
    name = 'multistochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Kperiod': 5,  # K-period (number of bars for calculations)
        'Dperiod': 3,  # D-period (primary smoothing period)
        'slowing': 3,  # Slowing period
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing type
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic calculation method
    }

