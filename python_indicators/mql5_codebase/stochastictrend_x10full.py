"""StochasticTrend_x10Full — converted from MQL5: MQL5 Indicators/StochasticTrend_x10Full/StochasticTrend_x10Full.mq5

Индикатор отображает положение осциллятора Stochastic с разных таймфреймов
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор отображает положение осциллятора Stochastic с разных таймфреймов'], 'name': 'StochasticTrend_x10Full', 'source': 'MQL5 Indicators/StochasticTrend_x10Full/StochasticTrend_x10Full.mq5', 'folder': 'StochasticTrend_x10Full', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16385, 'label': 'период графика 1', 'sinput': False}, {'mql': 'KPeriod1', 'py': 'KPeriod1', 'param': 'KPeriod1', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod1', 'py': 'DPeriod1', 'param': 'DPeriod1', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing1', 'py': 'Slowing1', 'param': 'Slowing1', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field1', 'py': 'Price_field1', 'param': 'Price_field1', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel1', 'py': 'UpLevel1', 'param': 'UpLevel1', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 1', 'sinput': False}, {'mql': 'DnLevel1', 'py': 'DnLevel1', 'param': 'DnLevel1', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'период графика 2', 'sinput': False}, {'mql': 'KPeriod2', 'py': 'KPeriod2', 'param': 'KPeriod2', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'DPeriod2', 'py': 'DPeriod2', 'param': 'DPeriod2', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing2', 'py': 'Slowing2', 'param': 'Slowing2', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field2', 'py': 'Price_field2', 'param': 'Price_field2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel2', 'py': 'UpLevel2', 'param': 'UpLevel2', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 2', 'sinput': False}, {'mql': 'DnLevel2', 'py': 'DnLevel2', 'param': 'DnLevel2', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 2', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16385, 'label': 'период графика 3', 'sinput': False}, {'mql': 'KPeriod3', 'py': 'KPeriod3', 'param': 'KPeriod3', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'DPeriod3', 'py': 'DPeriod3', 'param': 'DPeriod3', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing3', 'py': 'Slowing3', 'param': 'Slowing3', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method3', 'py': 'MA_Method3', 'param': 'MA_Method3', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field3', 'py': 'Price_field3', 'param': 'Price_field3', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel3', 'py': 'UpLevel3', 'param': 'UpLevel3', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 3', 'sinput': False}, {'mql': 'DnLevel3', 'py': 'DnLevel3', 'param': 'DnLevel3', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 3', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16385, 'label': 'период графика 4', 'sinput': False}, {'mql': 'KPeriod4', 'py': 'KPeriod4', 'param': 'KPeriod4', 'type': 'uint', 'default': 17, 'label': '', 'sinput': False}, {'mql': 'DPeriod4', 'py': 'DPeriod4', 'param': 'DPeriod4', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing4', 'py': 'Slowing4', 'param': 'Slowing4', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method4', 'py': 'MA_Method4', 'param': 'MA_Method4', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field4', 'py': 'Price_field4', 'param': 'Price_field4', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel4', 'py': 'UpLevel4', 'param': 'UpLevel4', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 4', 'sinput': False}, {'mql': 'DnLevel4', 'py': 'DnLevel4', 'param': 'DnLevel4', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 4', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16385, 'label': 'период графика 5', 'sinput': False}, {'mql': 'KPeriod5', 'py': 'KPeriod5', 'param': 'KPeriod5', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'DPeriod5', 'py': 'DPeriod5', 'param': 'DPeriod5', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing5', 'py': 'Slowing5', 'param': 'Slowing5', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method5', 'py': 'MA_Method5', 'param': 'MA_Method5', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field5', 'py': 'Price_field5', 'param': 'Price_field5', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel5', 'py': 'UpLevel5', 'param': 'UpLevel5', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 5', 'sinput': False}, {'mql': 'DnLevel5', 'py': 'DnLevel5', 'param': 'DnLevel5', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 5', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16385, 'label': 'период графика 6', 'sinput': False}, {'mql': 'KPeriod6', 'py': 'KPeriod6', 'param': 'KPeriod6', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'DPeriod6', 'py': 'DPeriod6', 'param': 'DPeriod6', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing6', 'py': 'Slowing6', 'param': 'Slowing6', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method6', 'py': 'MA_Method6', 'param': 'MA_Method6', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field6', 'py': 'Price_field6', 'param': 'Price_field6', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel6', 'py': 'UpLevel6', 'param': 'UpLevel6', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 6', 'sinput': False}, {'mql': 'DnLevel6', 'py': 'DnLevel6', 'param': 'DnLevel6', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 6', 'sinput': False}, {'mql': 'TimeFrame7', 'py': 'TimeFrame7', 'param': 'TimeFrame7', 'type': 'int', 'default': 16385, 'label': 'период графика 7', 'sinput': False}, {'mql': 'KPeriod7', 'py': 'KPeriod7', 'param': 'KPeriod7', 'type': 'uint', 'default': 29, 'label': '', 'sinput': False}, {'mql': 'DPeriod7', 'py': 'DPeriod7', 'param': 'DPeriod7', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing7', 'py': 'Slowing7', 'param': 'Slowing7', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method7', 'py': 'MA_Method7', 'param': 'MA_Method7', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field7', 'py': 'Price_field7', 'param': 'Price_field7', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel7', 'py': 'UpLevel7', 'param': 'UpLevel7', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 7', 'sinput': False}, {'mql': 'DnLevel7', 'py': 'DnLevel7', 'param': 'DnLevel7', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 7', 'sinput': False}, {'mql': 'TimeFrame8', 'py': 'TimeFrame8', 'param': 'TimeFrame8', 'type': 'int', 'default': 16385, 'label': 'период графика 8', 'sinput': False}, {'mql': 'KPeriod8', 'py': 'KPeriod8', 'param': 'KPeriod8', 'type': 'uint', 'default': 33, 'label': '', 'sinput': False}, {'mql': 'DPeriod8', 'py': 'DPeriod8', 'param': 'DPeriod8', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing8', 'py': 'Slowing8', 'param': 'Slowing8', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method8', 'py': 'MA_Method8', 'param': 'MA_Method8', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field8', 'py': 'Price_field8', 'param': 'Price_field8', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel8', 'py': 'UpLevel8', 'param': 'UpLevel8', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 8', 'sinput': False}, {'mql': 'DnLevel8', 'py': 'DnLevel8', 'param': 'DnLevel8', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 8', 'sinput': False}, {'mql': 'TimeFrame9', 'py': 'TimeFrame9', 'param': 'TimeFrame9', 'type': 'int', 'default': 16385, 'label': 'период графика 9', 'sinput': False}, {'mql': 'KPeriod9', 'py': 'KPeriod9', 'param': 'KPeriod9', 'type': 'uint', 'default': 37, 'label': '', 'sinput': False}, {'mql': 'DPeriod9', 'py': 'DPeriod9', 'param': 'DPeriod9', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing9', 'py': 'Slowing9', 'param': 'Slowing9', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method9', 'py': 'MA_Method9', 'param': 'MA_Method9', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field9', 'py': 'Price_field9', 'param': 'Price_field9', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel9', 'py': 'UpLevel9', 'param': 'UpLevel9', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 9', 'sinput': False}, {'mql': 'DnLevel9', 'py': 'DnLevel9', 'param': 'DnLevel9', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 9', 'sinput': False}, {'mql': 'TimeFrame10', 'py': 'TimeFrame10', 'param': 'TimeFrame10', 'type': 'int', 'default': 16385, 'label': 'период графика 10', 'sinput': False}, {'mql': 'KPeriod10', 'py': 'KPeriod10', 'param': 'KPeriod10', 'type': 'uint', 'default': 41, 'label': '', 'sinput': False}, {'mql': 'DPeriod10', 'py': 'DPeriod10', 'param': 'DPeriod10', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing10', 'py': 'Slowing10', 'param': 'Slowing10', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method10', 'py': 'MA_Method10', 'param': 'MA_Method10', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field10', 'py': 'Price_field10', 'param': 'Price_field10', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpLevel10', 'py': 'UpLevel10', 'param': 'UpLevel10', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 10', 'sinput': False}, {'mql': 'DnLevel10', 'py': 'DnLevel10', 'param': 'DnLevel10', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 10', 'sinput': False}, {'mql': 'CpColor', 'py': 'CpColor', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'цвет названия индикатора', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 10156544, 'label': 'цвет перекупленности индикатора', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет перепроданности индикатора', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет без изменения', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'размер шрифта', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'тип шрифта', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'угол расположения', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'расположение по вертикали', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'расположение по горизонтали', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_H1)  # период графика 1
KPeriod1 = _input('KPeriod1', 5)
DPeriod1 = _input('DPeriod1', 3)
Slowing1 = _input('Slowing1', 3)
MA_Method1 = _input('MA_Method1', MODE_SMA)
Price_field1 = _input('Price_field1', STO_LOWHIGH)
UpLevel1 = _input('UpLevel1', 70)  # уровень перезакупа 1
DnLevel1 = _input('DnLevel1', 30)  # уровень перепроданности 1
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # период графика 2
KPeriod2 = _input('KPeriod2', 9)
DPeriod2 = _input('DPeriod2', 3)
Slowing2 = _input('Slowing2', 3)
MA_Method2 = _input('MA_Method2', MODE_SMA)
Price_field2 = _input('Price_field2', STO_LOWHIGH)
UpLevel2 = _input('UpLevel2', 70)  # уровень перезакупа 2
DnLevel2 = _input('DnLevel2', 30)  # уровень перепроданности 2
TimeFrame3 = _input('TimeFrame3', PERIOD_H1)  # период графика 3
KPeriod3 = _input('KPeriod3', 13)
DPeriod3 = _input('DPeriod3', 3)
Slowing3 = _input('Slowing3', 3)
MA_Method3 = _input('MA_Method3', MODE_SMA)
Price_field3 = _input('Price_field3', STO_LOWHIGH)
UpLevel3 = _input('UpLevel3', 70)  # уровень перезакупа 3
DnLevel3 = _input('DnLevel3', 30)  # уровень перепроданности 3
TimeFrame4 = _input('TimeFrame4', PERIOD_H1)  # период графика 4
KPeriod4 = _input('KPeriod4', 17)
DPeriod4 = _input('DPeriod4', 3)
Slowing4 = _input('Slowing4', 3)
MA_Method4 = _input('MA_Method4', MODE_SMA)
Price_field4 = _input('Price_field4', STO_LOWHIGH)
UpLevel4 = _input('UpLevel4', 70)  # уровень перезакупа 4
DnLevel4 = _input('DnLevel4', 30)  # уровень перепроданности 4
TimeFrame5 = _input('TimeFrame5', PERIOD_H1)  # период графика 5
KPeriod5 = _input('KPeriod5', 21)
DPeriod5 = _input('DPeriod5', 3)
Slowing5 = _input('Slowing5', 3)
MA_Method5 = _input('MA_Method5', MODE_SMA)
Price_field5 = _input('Price_field5', STO_LOWHIGH)
UpLevel5 = _input('UpLevel5', 70)  # уровень перезакупа 5
DnLevel5 = _input('DnLevel5', 30)  # уровень перепроданности 5
TimeFrame6 = _input('TimeFrame6', PERIOD_H1)  # период графика 6
KPeriod6 = _input('KPeriod6', 25)
DPeriod6 = _input('DPeriod6', 3)
Slowing6 = _input('Slowing6', 3)
MA_Method6 = _input('MA_Method6', MODE_SMA)
Price_field6 = _input('Price_field6', STO_LOWHIGH)
UpLevel6 = _input('UpLevel6', 70)  # уровень перезакупа 6
DnLevel6 = _input('DnLevel6', 30)  # уровень перепроданности 6
TimeFrame7 = _input('TimeFrame7', PERIOD_H1)  # период графика 7
KPeriod7 = _input('KPeriod7', 29)
DPeriod7 = _input('DPeriod7', 3)
Slowing7 = _input('Slowing7', 3)
MA_Method7 = _input('MA_Method7', MODE_SMA)
Price_field7 = _input('Price_field7', STO_LOWHIGH)
UpLevel7 = _input('UpLevel7', 70)  # уровень перезакупа 7
DnLevel7 = _input('DnLevel7', 30)  # уровень перепроданности 7
TimeFrame8 = _input('TimeFrame8', PERIOD_H1)  # период графика 8
KPeriod8 = _input('KPeriod8', 33)
DPeriod8 = _input('DPeriod8', 3)
Slowing8 = _input('Slowing8', 3)
MA_Method8 = _input('MA_Method8', MODE_SMA)
Price_field8 = _input('Price_field8', STO_LOWHIGH)
UpLevel8 = _input('UpLevel8', 70)  # уровень перезакупа 8
DnLevel8 = _input('DnLevel8', 30)  # уровень перепроданности 8
TimeFrame9 = _input('TimeFrame9', PERIOD_H1)  # период графика 9
KPeriod9 = _input('KPeriod9', 37)
DPeriod9 = _input('DPeriod9', 3)
Slowing9 = _input('Slowing9', 3)
MA_Method9 = _input('MA_Method9', MODE_SMA)
Price_field9 = _input('Price_field9', STO_LOWHIGH)
UpLevel9 = _input('UpLevel9', 70)  # уровень перезакупа 9
DnLevel9 = _input('DnLevel9', 30)  # уровень перепроданности 9
TimeFrame10 = _input('TimeFrame10', PERIOD_H1)  # период графика 10
KPeriod10 = _input('KPeriod10', 41)
DPeriod10 = _input('DPeriod10', 3)
Slowing10 = _input('Slowing10', 3)
MA_Method10 = _input('MA_Method10', MODE_SMA)
Price_field10 = _input('Price_field10', STO_LOWHIGH)
UpLevel10 = _input('UpLevel10', 70)  # уровень перезакупа 10
DnLevel10 = _input('DnLevel10', 30)  # уровень перепроданности 10
CpColor = _input('CpColor', clrDarkOrchid)  # цвет названия индикатора
UpColor = _input('UpColor', clrMediumSpringGreen)  # цвет перекупленности индикатора
DnColor = _input('DnColor', clrMagenta)  # цвет перепроданности индикатора
ZrColor = _input('ZrColor', clrGray)  # цвет без изменения
FontSize = _input('FontSize', 11)  # размер шрифта
FontType = _input('FontType', Font14)  # тип шрифта
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # угол расположения
Y_ = _input('Y_', 20)  # расположение по вертикали
X_ = _input('X_', 5)  # расположение по горизонтали
sFontType = ""
min_rates_total = 0
xshift = 0
shift = Arr(11, 0, dyn=False)
sPer = Arr(10, "", dyn=False)
sPerA = Arr(10, "", dyn=False)
sPerB = Arr(10, "", dyn=False)
Cap = ""
ePer = Arr(10, 0, dyn=False)

class CIndArrow(MqlObject):
    _q_fields = ('m_Ind', 'm_Handle', 'm_TimeFrame', 'm_KPeriod', 'm_DPeriod', 'm_Slowing', 'm_MA_Method', 'm_Price_field', 'm_UpLevel', 'm_DnLevel')
    def __init__(self, *args):
        self.m_Ind = Arr(1, 0.0, dyn=False)
        self.m_Handle = 0
        self.m_TimeFrame = 0
        self.m_KPeriod = 0
        self.m_DPeriod = 0
        self.m_Slowing = 0
        self.m_MA_Method = 0
        self.m_Price_field = 0
        self.m_UpLevel = 0.0
        self.m_DnLevel = 0.0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Cap, min_rates_total, sFontType, xshift
    ePer[0] = TimeFrame1
    ePer[1] = TimeFrame2
    ePer[2] = TimeFrame3
    ePer[3] = TimeFrame4
    ePer[4] = TimeFrame5
    ePer[5] = TimeFrame6
    ePer[6] = TimeFrame7
    ePer[7] = TimeFrame8
    ePer[8] = TimeFrame9
    ePer[9] = TimeFrame10
    for poz in range(0, 10):
        Ind[poz].m_TimeFrame = ePer[poz]
    Ind[0].m_KPeriod = KPeriod1
    Ind[1].m_KPeriod = KPeriod2
    Ind[2].m_KPeriod = KPeriod3
    Ind[3].m_KPeriod = KPeriod4
    Ind[4].m_KPeriod = KPeriod5
    Ind[5].m_KPeriod = KPeriod6
    Ind[6].m_KPeriod = KPeriod7
    Ind[7].m_KPeriod = KPeriod8
    Ind[8].m_KPeriod = KPeriod9
    Ind[9].m_KPeriod = KPeriod10
    Ind[0].m_DPeriod = DPeriod1
    Ind[1].m_DPeriod = DPeriod2
    Ind[2].m_DPeriod = DPeriod3
    Ind[3].m_DPeriod = DPeriod4
    Ind[4].m_DPeriod = DPeriod5
    Ind[5].m_DPeriod = DPeriod6
    Ind[6].m_DPeriod = DPeriod7
    Ind[7].m_DPeriod = DPeriod8
    Ind[8].m_DPeriod = DPeriod9
    Ind[9].m_DPeriod = DPeriod10
    Ind[0].m_Slowing = Slowing1
    Ind[1].m_Slowing = Slowing2
    Ind[2].m_Slowing = Slowing3
    Ind[3].m_Slowing = Slowing4
    Ind[4].m_Slowing = Slowing5
    Ind[5].m_Slowing = Slowing6
    Ind[6].m_Slowing = Slowing7
    Ind[7].m_Slowing = Slowing8
    Ind[8].m_Slowing = Slowing9
    Ind[9].m_Slowing = Slowing10
    Ind[0].m_MA_Method = MA_Method1
    Ind[1].m_MA_Method = MA_Method2
    Ind[2].m_MA_Method = MA_Method3
    Ind[3].m_MA_Method = MA_Method4
    Ind[4].m_MA_Method = MA_Method5
    Ind[5].m_MA_Method = MA_Method6
    Ind[6].m_MA_Method = MA_Method7
    Ind[7].m_MA_Method = MA_Method8
    Ind[8].m_MA_Method = MA_Method9
    Ind[9].m_MA_Method = MA_Method10
    Ind[0].m_Price_field = Price_field1
    Ind[1].m_Price_field = Price_field2
    Ind[2].m_Price_field = Price_field3
    Ind[3].m_Price_field = Price_field4
    Ind[4].m_Price_field = Price_field5
    Ind[5].m_Price_field = Price_field6
    Ind[6].m_Price_field = Price_field7
    Ind[7].m_Price_field = Price_field8
    Ind[8].m_Price_field = Price_field9
    Ind[9].m_Price_field = Price_field10
    Ind[0].m_UpLevel = UpLevel1
    Ind[1].m_UpLevel = UpLevel2
    Ind[2].m_UpLevel = UpLevel3
    Ind[3].m_UpLevel = UpLevel4
    Ind[4].m_UpLevel = UpLevel5
    Ind[5].m_UpLevel = UpLevel6
    Ind[6].m_UpLevel = UpLevel7
    Ind[7].m_UpLevel = UpLevel8
    Ind[8].m_UpLevel = UpLevel9
    Ind[9].m_UpLevel = UpLevel10
    Ind[0].m_DnLevel = DnLevel1
    Ind[1].m_DnLevel = DnLevel2
    Ind[2].m_DnLevel = DnLevel3
    Ind[3].m_DnLevel = DnLevel4
    Ind[4].m_DnLevel = DnLevel5
    Ind[5].m_DnLevel = DnLevel6
    Ind[6].m_DnLevel = DnLevel7
    Ind[7].m_DnLevel = DnLevel8
    Ind[8].m_DnLevel = DnLevel9
    Ind[9].m_DnLevel = DnLevel10
    for poz in range(0, 10):
        Ind[poz].m_Handle = iStochastic(Symbol(), Ind[poz].m_TimeFrame, Ind[poz].m_KPeriod, Ind[poz].m_DPeriod, Ind[poz].m_Slowing, Ind[poz].m_MA_Method, Ind[poz].m_Price_field)
        if Ind[poz].m_Handle == INVALID_HANDLE:
            Print('OnInit()(', poz, '): Не удалось получить хендл индикатора Stochastic', poz)
            return False
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    max_ = 0
    for poz in range(0, 10):
        res = Ind[poz].m_KPeriod + Ind[poz].m_DPeriod + Ind[poz].m_Slowing
        if res > max_:
            max_ = _int(res)
    min_rates_total = _int(max_ + 1)
    xshift = _int(X_ + (8.3 * FontSize))
    Cap = 'StochasticTrend_x10Full'
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        for poz in range(0, 10 + 1):
            shift[10 - poz] = Y_ + (22 * poz)
    elif _sw1 == CORNER_LEFT_LOWER:
        for poz in range(0, 10 + 1):
            shift[10 - poz] = Y_ + (22 * poz)
    else:
        for poz in range(0, 10 + 1):
            shift[poz] = Y_ + (22 * poz)
    for poz in range(0, 10):
        sPer[poz] = _str(poz + 1) + ' ' + GetStringTimeframe(ePer[poz])
        sPerA[poz] = sPer[poz] + 'Stat+'
        sPerB[poz] = sPer[poz] + 'Stat_'
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def Deinit():
    for poz in range(0, 10):
        ObjectDelete(0, sPerA[poz])
        ObjectDelete(0, sPerB[poz])
    ObjectDelete(0, Cap)

def CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chart_id, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)
    ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
    ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for poz in range(0, 10):
        if Bars(Symbol(), ePer[poz]) < min_rates_total:
            return 0
    for poz in range(0, 10):
        if CopyBuffer(Ind[poz].m_Handle, MAIN_LINE, 1, 1, Ind[poz].m_Ind) <= 0:
            return 0
    ColorGain = Arr(10, 0, dyn=False)
    ArrayInitialize(ColorGain, ZrColor)
    for poz in range(0, 10):
        if Ind[poz].m_Ind[0] > Ind[poz].m_UpLevel:
            ColorGain[poz] = UpColor
        if Ind[poz].m_Ind[0] < Ind[poz].m_DnLevel:
            ColorGain[poz] = DnColor
    for poz in range(0, 10):
        SetTLabel(0, sPerA[poz], 0, WhatCorner, 2 * WhatCorner, X_, shift[poz + 1], sPer[poz] + ': ', ColorGain[poz], sFontType, FontSize)
        SetTLabel(0, sPerB[poz], 0, WhatCorner, 2 * WhatCorner, xshift, shift[poz + 1], 'n', ColorGain[poz], 'Wingdings', FontSize)
    SetTLabel(0, Cap, 0, WhatCorner, 2 * WhatCorner, X_, shift[0], Cap, CpColor, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(10, 0, dyn=False, factory=CIndArrow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticTrendX10Full(_MQL5Indicator):
    name = 'StochasticTrend_x10Full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 1
        'KPeriod1': 5,
        'DPeriod1': 3,
        'Slowing1': 3,
        'MA_Method1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field1': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel1': 70,  # уровень перезакупа 1
        'DnLevel1': 30,  # уровень перепроданности 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 2
        'KPeriod2': 9,
        'DPeriod2': 3,
        'Slowing2': 3,
        'MA_Method2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field2': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel2': 70,  # уровень перезакупа 2
        'DnLevel2': 30,  # уровень перепроданности 2
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 3
        'KPeriod3': 13,
        'DPeriod3': 3,
        'Slowing3': 3,
        'MA_Method3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field3': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel3': 70,  # уровень перезакупа 3
        'DnLevel3': 30,  # уровень перепроданности 3
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 4
        'KPeriod4': 17,
        'DPeriod4': 3,
        'Slowing4': 3,
        'MA_Method4': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field4': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel4': 70,  # уровень перезакупа 4
        'DnLevel4': 30,  # уровень перепроданности 4
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 5
        'KPeriod5': 21,
        'DPeriod5': 3,
        'Slowing5': 3,
        'MA_Method5': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field5': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel5': 70,  # уровень перезакупа 5
        'DnLevel5': 30,  # уровень перепроданности 5
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 6
        'KPeriod6': 25,
        'DPeriod6': 3,
        'Slowing6': 3,
        'MA_Method6': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field6': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel6': 70,  # уровень перезакупа 6
        'DnLevel6': 30,  # уровень перепроданности 6
        'TimeFrame7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 7
        'KPeriod7': 29,
        'DPeriod7': 3,
        'Slowing7': 3,
        'MA_Method7': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field7': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel7': 70,  # уровень перезакупа 7
        'DnLevel7': 30,  # уровень перепроданности 7
        'TimeFrame8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 8
        'KPeriod8': 33,
        'DPeriod8': 3,
        'Slowing8': 3,
        'MA_Method8': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field8': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel8': 70,  # уровень перезакупа 8
        'DnLevel8': 30,  # уровень перепроданности 8
        'TimeFrame9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 9
        'KPeriod9': 37,
        'DPeriod9': 3,
        'Slowing9': 3,
        'MA_Method9': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field9': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel9': 70,  # уровень перезакупа 9
        'DnLevel9': 30,  # уровень перепроданности 9
        'TimeFrame10': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 10
        'KPeriod10': 41,
        'DPeriod10': 3,
        'Slowing10': 3,
        'MA_Method10': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field10': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'UpLevel10': 70,  # уровень перезакупа 10
        'DnLevel10': 30,  # уровень перепроданности 10
        'FontSize': 11,  # размер шрифта
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # тип шрифта
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # угол расположения
        'Y_': 20,  # расположение по вертикали
        'X_': 5,  # расположение по горизонтали
    }

