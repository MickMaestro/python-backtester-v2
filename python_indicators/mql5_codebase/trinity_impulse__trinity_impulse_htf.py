"""trinity-impulse — converted from MQL5: MQL5 Indicators/Trinity-Impulse_HTF/trinity-impulse.mq5

Copyright: Copyright © 2010, basisforex@gmail.com; Link: basisforex@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, basisforex@gmail.com', 'link': 'basisforex@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14053594]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Trinity-Impulse'}, 'levels': [], 'description': [], 'name': 'trinity-impulse', 'source': 'MQL5 Indicators/Trinity-Impulse_HTF/trinity-impulse.mq5', 'folder': 'Trinity-Impulse_HTF', 'inputs': [{'mql': 'nPeriod', 'py': 'nPeriod', 'param': 'nPeriod', 'type': 'int', 'default': 5, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'nLevel', 'py': 'nLevel', 'param': 'nLevel', 'type': 'int', 'default': 34, 'label': 'Уровень срабатывания', 'sinput': False}, {'mql': 'nType', 'py': 'nType', 'param': 'nType', 'type': 'int', 'default': 3, 'label': 'Тип усреднения', 'sinput': False}, {'mql': 'nPrice', 'py': 'nPrice', 'param': 'nPrice', 'type': 'int', 'default': 7, 'label': 'Цена', 'sinput': False}, {'mql': 'nVolume', 'py': 'nVolume', 'param': 'nVolume', 'type': 'int', 'default': 0, 'label': 'Тип объема', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
nPeriod = _input('nPeriod', 5)  # Период индикатора
nLevel = _input('nLevel', 34)  # Уровень срабатывания
nType = _input('nType', MODE_LWMA)  # Тип усреднения
nPrice = _input('nPrice', PRICE_WEIGHTED)  # Цена
nVolume = _input('nVolume', VOLUME_TICK)  # Тип объема
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
CCI_Handle = 0
Force_Handle = 0

def OnInit():
    global CCI_Handle, Force_Handle, min_rates_total
    min_rates_total = nPeriod
    CCI_Handle = iCCI(None, 0, nPeriod, nPrice)
    if CCI_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора iCCI')
        return INIT_FAILED
    Force_Handle = iForce(None, 0, nPeriod, nType, nVolume)
    if Force_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора iForce')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Trinity-Impulse(', nPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(CCI_Handle) < rates_total or BarsCalculated(Force_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    CCI = Arr(0, 0.0)
    FORCE = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(FORCE, True)
    to_copy = limit + 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    if CopyBuffer(Force_Handle, 0, 0, to_copy, FORCE) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if (CCI[bar] * FORCE[bar]) >= nLevel:
            if CCI[bar] > 0 and FORCE[bar] > 0:
                ExtLineBuffer[bar] = 1.0
            if CCI[bar] < 0 and FORCE[bar] < 0:
                ExtLineBuffer[bar] = -1.0
        else:
            ExtLineBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrinityImpulse(_MQL5Indicator):
    name = 'trinity-impulse'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'nPeriod': 5,  # Период индикатора
        'nLevel': 34,  # Уровень срабатывания
        'nType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Тип усреднения
        'nPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Цена
        'nVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Тип объема
    }

