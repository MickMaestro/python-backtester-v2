"""Differential Average by Sultonov — converted from MQL5: MQL5 Indicators/Differential indicator by Sultonov/Differential Average by Sultonov.mq5

English: Sultonovs Differential Indicator.
Russian: Дифференциальный индикатор Султонова
Copyright: Scriptong by Sultonov's idea, starring Sevan62; Link: http://advancetools.net; Version: VERSION

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': "Scriptong by Sultonov's idea, starring Sevan62", 'link': 'http://advancetools.net', 'version': 'VERSION', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Bulls Power', 2: 'Bears Power'}, 'levels': [], 'description': ['English: Sultonovs Differential Indicator.', 'Russian: Дифференциальный индикатор Султонова'], 'name': 'Differential Average by Sultonov', 'source': 'MQL5 Indicators/Differential indicator by Sultonov/Differential Average by Sultonov.mq5', 'folder': 'Differential indicator by Sultonov', 'inputs': [{'mql': 'i_nPeriod', 'py': 'i_nPeriod', 'param': 'i_nPeriod', 'type': 'int', 'default': 1000, 'label': 'Calculate period / Период расчета', 'sinput': False}, {'mql': 'i_nIndBarsCount', 'py': 'i_nIndBarsCount', 'param': 'i_nIndBarsCount', 'type': 'int', 'default': 10000, 'label': 'Number of bars to display / Количество баров отображения', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
i_nPeriod = _input('i_nPeriod', 1000)  # Calculate period / Период расчета
i_nIndBarsCount = _input('i_nIndBarsCount', 10000)  # Number of bars to display / Количество баров отображения
g_bIsActivate = False
g_fPoint = 0.0
g_farrBullsPower = Arr(0, 0.0)
g_farrBearsPower = Arr(0, 0.0)

def OnInit():
    global g_bIsActivate
    Print('Version: ', '220.917')
    g_bIsActivate = False
    if not TuningParameters():
        return INIT_FAILED
    if not BuffersBind():
        return INIT_FAILED
    g_bIsActivate = True
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, farrClose, tick_volume, volume, spread):
    global g_bIsActivate
    if not g_bIsActivate:
        return rates_total
    nTotal = Box(0)
    nLimit = GetRecalcIndex(nTotal, rates_total, prev_calculated)
    if not ShowIndicatorData(nLimit, farrClose):
        g_bIsActivate = False
    return rates_total

def TuningParameters():
    global g_fPoint
    name = MQLInfoString(MQL_PROGRAM_NAME)
    if i_nPeriod <= 0:
        Alert(name, ', ', Symbol(), (': величина периода расчета должна быть больше нуля. Индикатор отключен.' if (TerminalInfoString(TERMINAL_LANGUAGE) == 'Russian') else ': value of period must be greate than zero. Indicator has turned off.'))
        return False
    g_fPoint = Point() / 10
    if g_fPoint <= 0.0:
        Alert(name, ', ', Symbol(), (': фатальная ошибка - величина пункта равна нулю. Индикатор отключен.' if (TerminalInfoString(TERMINAL_LANGUAGE) == 'Russian') else ': fatal error - the point value equals to zero. Indicator has turned off.'))
        return False
    return True

def BuffersBind():
    if (not SetIndexBuffer(0, g_farrBullsPower, INDICATOR_DATA)) or (not SetIndexBuffer(1, g_farrBearsPower, INDICATOR_DATA)):
        Alert(MQLInfoString(MQL_PROGRAM_NAME), ', ', Symbol(), (': ошибка связывания массивов с буферами индикатора. Ошибка №' if (TerminalInfoString(TERMINAL_LANGUAGE) == 'Russian') else ': indicator buffers binding error N'), GetLastError())
        return False
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
    ArraySetAsSeries(g_farrBullsPower, True)
    ArraySetAsSeries(g_farrBearsPower, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Differential Average by Sultonov (' + IntegerToString(i_nPeriod) + ')')
    return True

def GetRecalcIndex(nTotal, nRatesTotal, nPrevCalculated):
    nTotal.v = nRatesTotal - 1 - i_nPeriod
    if i_nIndBarsCount > 0 and i_nIndBarsCount < nTotal.v:
        nTotal.v = MathMin(i_nIndBarsCount, nTotal.v)
    if nPrevCalculated < (nRatesTotal - 1):
        InitializeBuffers()
        return nTotal.v
    return MathMin(nRatesTotal - nPrevCalculated, nTotal.v)

def InitializeBuffers():
    ArrayInitialize(g_farrBullsPower, EMPTY_VALUE)
    ArrayInitialize(g_farrBearsPower, EMPTY_VALUE)

def ShowIndicatorData(nLimit, farrClose):
    ArraySetAsSeries(farrClose, True)
    for i in range(nLimit, 0 - 1, -1):
        if not ProcessBar(i, farrClose):
            return False
    return True

def ProcessBar(nBarIndex, farrClose):
    if (nBarIndex + i_nPeriod) > ArraySize(farrClose):
        return True
    fBullsSumm = 0.0
    fBearsSumm = 0.0
    nBullsCnt = 0
    nBearsCnt = 0
    for i in range(nBarIndex + i_nPeriod - 1, nBarIndex - 1, -1):
        fPower = farrClose[i] - farrClose[i + 1]
        if fPower > (2 * DBL_EPSILON):
            fBullsSumm += fPower
            nBullsCnt += 1
        if fPower < (-2 * DBL_EPSILON):
            fBearsSumm -= fPower
            nBearsCnt += 1
    g_farrBullsPower[nBarIndex] = (0.0 if (nBullsCnt == 0) else _fdiv(_fdiv(fBullsSumm, nBullsCnt), g_fPoint))
    g_farrBearsPower[nBarIndex] = (0.0 if (nBearsCnt == 0) else _fdiv(_fdiv(fBearsSumm, nBearsCnt), g_fPoint))
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DifferentialAverageBySultonov(_MQL5Indicator):
    name = 'Differential Average by Sultonov'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_nPeriod': 1000,  # Calculate period / Период расчета
        'i_nIndBarsCount': 10000,  # Number of bars to display / Количество баров отображения
    }

