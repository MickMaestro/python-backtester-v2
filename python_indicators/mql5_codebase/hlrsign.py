"""hlrsign — converted from MQL5: MQL5 Indicators/HLRSign/hlrsign.mq5

Copyright: Copyright © 2006, Alexandre; Link: http://www.kroufr.ru/content/view/1184/124/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alexandre', 'link': 'http://www.kroufr.ru/content/view/1184/124/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [7504122], 2: [7451452]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'HLRSign Sell', 2: 'HLRSign Buy'}, 'levels': [], 'description': [], 'name': 'hlrsign', 'source': 'MQL5 Indicators/HLRSign/hlrsign.mq5', 'folder': 'HLRSign', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': 'Пробойный алгоритм', 'sinput': False}, {'mql': 'HLR_Range', 'py': 'HLR_Range', 'param': 'HLR_Range', 'type': 'uint', 'default': 40, 'label': 'Период усреднения индикатора', 'sinput': False}, {'mql': 'HLR_UpLevel', 'py': 'HLR_UpLevel', 'param': 'HLR_UpLevel', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'HLR_DnLevel', 'py': 'HLR_DnLevel', 'param': 'HLR_DnLevel', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Alg_Method
MODE_IN = 0
MODE_OUT = 1
_enum('Alg_Method', {0: 'MODE_IN', 1: 'MODE_OUT'})

# ---- inputs and global variables
Mode = _input('Mode', MODE_IN)  # Пробойный алгоритм
HLR_Range = _input('HLR_Range', 40)  # Период усреднения индикатора
HLR_UpLevel = _input('HLR_UpLevel', 80)  # Уровень перекупленности
HLR_DnLevel = _input('HLR_DnLevel', 20)  # Уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 100
    min_rates_total = _int(MathMax(HLR_Range + 1, ATR_Period))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    if HLR_UpLevel <= HLR_DnLevel:
        Print('Уровень перекупленности всегда должен быть больше уровня перепроданности!!!')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 171)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 171)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'HLRSign(', HLR_Range, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_HLR1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    m_pr = 0.0
    HH = 0.0
    LL = 0.0
    HL = 0.0
    HLR0 = 0.0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_HLR1 = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    HLR0 = _s_OnCalculate_HLR1
    for bar in range(limit, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        HH = high[ArrayMaximum(high, bar, HLR_Range)]
        LL = low[ArrayMinimum(low, bar, HLR_Range)]
        m_pr = (high[bar] + low[bar]) / 2.0
        HL = HH - LL
        if HL:
            HLR0 = _fdiv(100.0 * (m_pr - LL), HL)
        else:
            HLR0 = 0.0
        if Mode == MODE_IN:
            if HLR0 > HLR_UpLevel and _s_OnCalculate_HLR1 <= HLR_UpLevel:
                BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
            if HLR0 < HLR_DnLevel and _s_OnCalculate_HLR1 >= HLR_DnLevel:
                SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        else:
            if HLR0 < HLR_UpLevel and _s_OnCalculate_HLR1 >= HLR_UpLevel:
                SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
            if HLR0 > HLR_DnLevel and _s_OnCalculate_HLR1 <= HLR_DnLevel:
                BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if bar:
            _s_OnCalculate_HLR1 = HLR0
    return rates_total

# ---- static local variables
_s_OnCalculate_HLR1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hlrsign(_MQL5Indicator):
    name = 'hlrsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Mode': _Choice({0: 'Алгоритм на входе в зоны ПЗ и ПП', 1: 'Алгоритм на выходе в зоны ПЗ и ПП'}, default=0),  # Пробойный алгоритм
        'HLR_Range': 40,  # Период усреднения индикатора
        'HLR_UpLevel': 80,  # Уровень перекупленности
        'HLR_DnLevel': 20,  # Уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

