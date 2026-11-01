"""cci_diversign — converted from MQL5: MQL5 Indicators/CCI_DiverSign/cci_diversign.mq5

Copyright: Copyright © 2015, olegok83; Link: https://www.mql5.com/ru/users/olegok83; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, olegok83', 'link': 'https://www.mql5.com/ru/users/olegok83', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [8721863], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'CCI_DiverSign Sell', 2: 'CCI_DiverSign Buy'}, 'levels': [], 'description': [], 'name': 'cci_diversign', 'source': 'MQL5 Indicators/CCI_DiverSign/cci_diversign.mq5', 'folder': 'CCI_DiverSign', 'inputs': [{'mql': 'iPeriod1', 'py': 'iPeriod1', 'param': 'iPeriod1', 'type': 'uint', 'default': 3, 'label': 'Период быстрого индикатора', 'sinput': False}, {'mql': 'CCIPrice1', 'py': 'CCIPrice1', 'param': 'CCIPrice1', 'type': 'int', 'default': 1, 'label': 'Цена быстрого индикатора', 'sinput': False}, {'mql': 'iPeriod2', 'py': 'iPeriod2', 'param': 'iPeriod2', 'type': 'uint', 'default': 7, 'label': 'Период медленого индикатора', 'sinput': False}, {'mql': 'CCIPrice2', 'py': 'CCIPrice2', 'param': 'CCIPrice2', 'type': 'int', 'default': 1, 'label': 'Цена медленого индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod1 = _input('iPeriod1', 3)  # Период быстрого индикатора
CCIPrice1 = _input('CCIPrice1', PRICE_CLOSE)  # Цена быстрого индикатора
iPeriod2 = _input('iPeriod2', 7)  # Период медленого индикатора
CCIPrice2 = _input('CCIPrice2', PRICE_CLOSE)  # Цена медленого индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
Ind_Handle1 = 0
Ind_Handle2 = 0
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global ATR_Handle, Ind_Handle1, Ind_Handle2, min_rates_, min_rates_total
    ATR_Period = 10
    min_rates_ = _int(MathMax(iPeriod1, iPeriod2))
    min_rates_total = min_rates_ + _int(MathMax(iPeriod1, iPeriod2)) + 5
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    Ind_Handle1 = iCCI(Symbol(), PERIOD_CURRENT, iPeriod1, CCIPrice1)
    if Ind_Handle1 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CCI1')
        return INIT_FAILED
    Ind_Handle2 = iCCI(Symbol(), PERIOD_CURRENT, iPeriod2, CCIPrice2)
    if Ind_Handle2 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CCI2')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 174)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 174)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = 'CCI_DiverSign'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(Ind_Handle1) < rates_total) or BarsCalculated(Ind_Handle2) < rates_total) or rates_total < min_rates_total:
        return 0
    Ind1 = Arr(0, 0.0)
    Ind2 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(Ind1, True)
    ArraySetAsSeries(Ind2, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 4
    if CopyBuffer(Ind_Handle1, 0, 0, to_copy, Ind1) <= 0:
        return 0
    if CopyBuffer(Ind_Handle2, 0, 0, to_copy, Ind2) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if SellCheck(open, close, bar):
            if (Ind1[bar + 4] < Ind1[bar + 3] and Ind1[bar + 3] > Ind1[bar + 2]) and Ind1[bar + 2] < Ind1[bar + 1]:
                if (Ind2[bar + 4] < Ind2[bar + 3] and Ind2[bar + 3] > Ind2[bar + 2]) and Ind2[bar + 2] < Ind2[bar + 1]:
                    if (Ind1[bar + 3] > Ind1[bar + 1] and Ind2[bar + 3] < Ind2[bar + 1]) or (Ind1[bar + 3] < Ind1[bar + 1] and Ind2[bar + 3] > Ind2[bar + 1]):
                        SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if BuyCheck(open, close, bar):
            if (Ind1[bar + 4] > Ind1[bar + 3] and Ind1[bar + 3] < Ind1[bar + 2]) and Ind1[bar + 2] > Ind1[bar + 1]:
                if (Ind2[bar + 4] > Ind2[bar + 3] and Ind2[bar + 3] < Ind2[bar + 2]) and Ind2[bar + 2] > Ind2[bar + 1]:
                    if (Ind1[bar + 3] > Ind1[bar + 1] and Ind2[bar + 3] < Ind2[bar + 1]) or (Ind1[bar + 3] < Ind1[bar + 1] and Ind2[bar + 3] > Ind2[bar + 1]):
                        BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def SellCheck(Open, Close, index):
    if (Open[index + 3] < Close[index + 3] and Open[index + 2] > Close[index + 2]) and Open[index + 1] < Close[index + 1]:
        return True
    return False

def BuyCheck(Open, Close, index):
    if (Open[index + 3] > Close[index + 3] and Open[index + 2] < Close[index + 2]) and Open[index + 1] > Close[index + 1]:
        return True
    return False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciDiversign(_MQL5Indicator):
    name = 'cci_diversign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod1': 3,  # Период быстрого индикатора
        'CCIPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена быстрого индикатора
        'iPeriod2': 7,  # Период медленого индикатора
        'CCIPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена медленого индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

