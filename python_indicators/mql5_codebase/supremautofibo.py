"""SupremAutoFibo — converted from MQL5: MQL5 Indicators/SupremAutoFibo/SupremAutoFibo.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'SupremAutoFibo', 'source': 'MQL5 Indicators/SupremAutoFibo/SupremAutoFibo.mq5', 'folder': 'SupremAutoFibo', 'inputs': [{'mql': 'FiboName', 'py': 'FiboName', 'param': None, 'type': 'string', 'default': 'SupremAutoFibo', 'label': 'Имя объекта', 'sinput': False}, {'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм индикатора для расчета уровней Фибоначи', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер стартового бара для поиска экстремумов', 'sinput': False}, {'mql': 'nPeriod', 'py': 'nPeriod', 'param': 'nPeriod', 'type': 'uint', 'default': 30, 'label': 'Количество баров для поиска экстремумов', 'sinput': False}, {'mql': 'FiboColor', 'py': 'FiboColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Цвет Фибо', 'sinput': False}, {'mql': 'FiboLevel1', 'py': 'FiboLevel1', 'param': 'FiboLevel1', 'type': 'double', 'default': -1.0, 'label': 'значение фибоуровня 1', 'sinput': False}, {'mql': 'StyleLevel1', 'py': 'StyleLevel1', 'param': 'StyleLevel1', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 1', 'sinput': False}, {'mql': 'WidthLevel1', 'py': 'WidthLevel1', 'param': 'WidthLevel1', 'type': 'uint', 'default': 4, 'label': 'толщина линии фибоуровня 1', 'sinput': False}, {'mql': 'Color_Level1', 'py': 'Color_Level1', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 1', 'sinput': False}, {'mql': 'FiboLevel2', 'py': 'FiboLevel2', 'param': 'FiboLevel2', 'type': 'double', 'default': -0.764, 'label': 'значение фибоуровня 2', 'sinput': False}, {'mql': 'StyleLevel2', 'py': 'StyleLevel2', 'param': 'StyleLevel2', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 2', 'sinput': False}, {'mql': 'WidthLevel2', 'py': 'WidthLevel2', 'param': 'WidthLevel2', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 2', 'sinput': False}, {'mql': 'Color_Level2', 'py': 'Color_Level2', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 2', 'sinput': False}, {'mql': 'FiboLevel3', 'py': 'FiboLevel3', 'param': 'FiboLevel3', 'type': 'double', 'default': -0.618, 'label': 'значение фибоуровня 3', 'sinput': False}, {'mql': 'StyleLevel3', 'py': 'StyleLevel3', 'param': 'StyleLevel3', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 3', 'sinput': False}, {'mql': 'WidthLevel3', 'py': 'WidthLevel3', 'param': 'WidthLevel3', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 3', 'sinput': False}, {'mql': 'Color_Level3', 'py': 'Color_Level3', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 3', 'sinput': False}, {'mql': 'FiboLevel4', 'py': 'FiboLevel4', 'param': 'FiboLevel4', 'type': 'double', 'default': -0.5, 'label': 'значение фибоуровня 4', 'sinput': False}, {'mql': 'StyleLevel4', 'py': 'StyleLevel4', 'param': 'StyleLevel4', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 4', 'sinput': False}, {'mql': 'WidthLevel4', 'py': 'WidthLevel4', 'param': 'WidthLevel4', 'type': 'uint', 'default': 2, 'label': 'толщина линии фибоуровня 4', 'sinput': False}, {'mql': 'Color_Level4', 'py': 'Color_Level4', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 4', 'sinput': False}, {'mql': 'FiboLevel5', 'py': 'FiboLevel5', 'param': 'FiboLevel5', 'type': 'double', 'default': -0.382, 'label': 'значение фибоуровня 5', 'sinput': False}, {'mql': 'StyleLevel5', 'py': 'StyleLevel5', 'param': 'StyleLevel5', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 5', 'sinput': False}, {'mql': 'WidthLevel5', 'py': 'WidthLevel5', 'param': 'WidthLevel5', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 5', 'sinput': False}, {'mql': 'Color_Level5', 'py': 'Color_Level5', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 5', 'sinput': False}, {'mql': 'FiboLevel6', 'py': 'FiboLevel6', 'param': 'FiboLevel6', 'type': 'double', 'default': -0.236, 'label': 'значение фибоуровня 6', 'sinput': False}, {'mql': 'StyleLevel6', 'py': 'StyleLevel6', 'param': 'StyleLevel6', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 6', 'sinput': False}, {'mql': 'WidthLevel6', 'py': 'WidthLevel6', 'param': 'WidthLevel6', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 6', 'sinput': False}, {'mql': 'Color_Level6', 'py': 'Color_Level6', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет фибоуровня 6', 'sinput': False}, {'mql': 'FiboLevel7', 'py': 'FiboLevel7', 'param': 'FiboLevel7', 'type': 'double', 'default': 0.0, 'label': 'значение фибоуровня 7', 'sinput': False}, {'mql': 'StyleLevel7', 'py': 'StyleLevel7', 'param': 'StyleLevel7', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 7', 'sinput': False}, {'mql': 'WidthLevel7', 'py': 'WidthLevel7', 'param': 'WidthLevel7', 'type': 'uint', 'default': 4, 'label': 'толщина линии фибоуровня 7', 'sinput': False}, {'mql': 'Color_Level7', 'py': 'Color_Level7', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 7', 'sinput': False}, {'mql': 'FiboLevel8', 'py': 'FiboLevel8', 'param': 'FiboLevel8', 'type': 'double', 'default': 0.236, 'label': 'значение фибоуровня 8', 'sinput': False}, {'mql': 'StyleLevel8', 'py': 'StyleLevel8', 'param': 'StyleLevel8', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 8', 'sinput': False}, {'mql': 'WidthLevel8', 'py': 'WidthLevel8', 'param': 'WidthLevel8', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 8', 'sinput': False}, {'mql': 'Color_Level8', 'py': 'Color_Level8', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 8', 'sinput': False}, {'mql': 'FiboLevel9', 'py': 'FiboLevel9', 'param': 'FiboLevel9', 'type': 'double', 'default': 0.382, 'label': 'значение фибоуровня 9', 'sinput': False}, {'mql': 'StyleLevel9', 'py': 'StyleLevel9', 'param': 'StyleLevel9', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 9', 'sinput': False}, {'mql': 'WidthLevel9', 'py': 'WidthLevel9', 'param': 'WidthLevel9', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 9', 'sinput': False}, {'mql': 'Color_Level9', 'py': 'Color_Level9', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 9', 'sinput': False}, {'mql': 'FiboLevel10', 'py': 'FiboLevel10', 'param': 'FiboLevel10', 'type': 'double', 'default': 0.5, 'label': 'значение фибоуровня 10', 'sinput': False}, {'mql': 'StyleLevel10', 'py': 'StyleLevel10', 'param': 'StyleLevel10', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 10', 'sinput': False}, {'mql': 'WidthLevel10', 'py': 'WidthLevel10', 'param': 'WidthLevel10', 'type': 'uint', 'default': 2, 'label': 'толщина линии фибоуровня 10', 'sinput': False}, {'mql': 'Color_Level10', 'py': 'Color_Level10', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 10', 'sinput': False}, {'mql': 'FiboLevel11', 'py': 'FiboLevel11', 'param': 'FiboLevel11', 'type': 'double', 'default': 0.618, 'label': 'значение фибоуровня 11', 'sinput': False}, {'mql': 'StyleLevel11', 'py': 'StyleLevel11', 'param': 'StyleLevel11', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 11', 'sinput': False}, {'mql': 'WidthLevel11', 'py': 'WidthLevel11', 'param': 'WidthLevel11', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 11', 'sinput': False}, {'mql': 'Color_Level11', 'py': 'Color_Level11', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 11', 'sinput': False}, {'mql': 'FiboLevel12', 'py': 'FiboLevel12', 'param': 'FiboLevel12', 'type': 'double', 'default': 0.764, 'label': 'значение фибоуровня 12', 'sinput': False}, {'mql': 'StyleLevel12', 'py': 'StyleLevel12', 'param': 'StyleLevel12', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 12', 'sinput': False}, {'mql': 'WidthLevel12', 'py': 'WidthLevel12', 'param': 'WidthLevel12', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 12', 'sinput': False}, {'mql': 'Color_Level12', 'py': 'Color_Level12', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет фибоуровня 12', 'sinput': False}, {'mql': 'FiboLevel13', 'py': 'FiboLevel13', 'param': 'FiboLevel13', 'type': 'double', 'default': 1.0, 'label': 'значение фибоуровня 13', 'sinput': False}, {'mql': 'StyleLevel13', 'py': 'StyleLevel13', 'param': 'StyleLevel13', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 13', 'sinput': False}, {'mql': 'WidthLevel13', 'py': 'WidthLevel13', 'param': 'WidthLevel13', 'type': 'uint', 'default': 4, 'label': 'толщина линии фибоуровня 13', 'sinput': False}, {'mql': 'Color_Level13', 'py': 'Color_Level13', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 13', 'sinput': False}, {'mql': 'FiboLevel14', 'py': 'FiboLevel14', 'param': 'FiboLevel14', 'type': 'double', 'default': 1.236, 'label': 'значение фибоуровня 14', 'sinput': False}, {'mql': 'StyleLevel14', 'py': 'StyleLevel14', 'param': 'StyleLevel14', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 14', 'sinput': False}, {'mql': 'WidthLevel14', 'py': 'WidthLevel14', 'param': 'WidthLevel14', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 14', 'sinput': False}, {'mql': 'Color_Level14', 'py': 'Color_Level14', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвет фибоуровня 14', 'sinput': False}, {'mql': 'FiboLevel15', 'py': 'FiboLevel15', 'param': 'FiboLevel15', 'type': 'double', 'default': 1.382, 'label': 'значение фибоуровня 15', 'sinput': False}, {'mql': 'StyleLevel15', 'py': 'StyleLevel15', 'param': 'StyleLevel15', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 15', 'sinput': False}, {'mql': 'WidthLevel15', 'py': 'WidthLevel15', 'param': 'WidthLevel15', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 15', 'sinput': False}, {'mql': 'Color_Level15', 'py': 'Color_Level15', 'param': None, 'type': 'color', 'default': 42495, 'label': 'цвет фибоуровня 15', 'sinput': False}, {'mql': 'FiboLevel16', 'py': 'FiboLevel16', 'param': 'FiboLevel16', 'type': 'double', 'default': 1.5, 'label': 'значение фибоуровня 16', 'sinput': False}, {'mql': 'StyleLevel16', 'py': 'StyleLevel16', 'param': 'StyleLevel16', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 16', 'sinput': False}, {'mql': 'WidthLevel16', 'py': 'WidthLevel16', 'param': 'WidthLevel16', 'type': 'uint', 'default': 2, 'label': 'толщина линии фибоуровня 16', 'sinput': False}, {'mql': 'Color_Level16', 'py': 'Color_Level16', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет фибоуровня 16', 'sinput': False}, {'mql': 'FiboLevel17', 'py': 'FiboLevel17', 'param': 'FiboLevel17', 'type': 'double', 'default': 1.618, 'label': 'значение фибоуровня 17', 'sinput': False}, {'mql': 'StyleLevel17', 'py': 'StyleLevel17', 'param': 'StyleLevel17', 'type': 'int', 'default': 1, 'label': 'стиль линии фибоуровня 17', 'sinput': False}, {'mql': 'WidthLevel17', 'py': 'WidthLevel17', 'param': 'WidthLevel17', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 17', 'sinput': False}, {'mql': 'Color_Level17', 'py': 'Color_Level17', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет фибоуровня 17', 'sinput': False}, {'mql': 'FiboLevel18', 'py': 'FiboLevel18', 'param': 'FiboLevel18', 'type': 'double', 'default': 1.764, 'label': 'значение фибоуровня 18', 'sinput': False}, {'mql': 'StyleLevel18', 'py': 'StyleLevel18', 'param': 'StyleLevel18', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 18', 'sinput': False}, {'mql': 'WidthLevel18', 'py': 'WidthLevel18', 'param': 'WidthLevel18', 'type': 'uint', 'default': 1, 'label': 'толщина линии фибоуровня 18', 'sinput': False}, {'mql': 'Color_Level18', 'py': 'Color_Level18', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет фибоуровня 18', 'sinput': False}, {'mql': 'FiboLevel19', 'py': 'FiboLevel19', 'param': 'FiboLevel19', 'type': 'double', 'default': 2.0, 'label': 'значение фибоуровня 19', 'sinput': False}, {'mql': 'StyleLevel19', 'py': 'StyleLevel19', 'param': 'StyleLevel19', 'type': 'int', 'default': 0, 'label': 'стиль линии фибоуровня 19', 'sinput': False}, {'mql': 'WidthLevel19', 'py': 'WidthLevel19', 'param': 'WidthLevel19', 'type': 'uint', 'default': 4, 'label': 'толщина линии фибоуровня 19', 'sinput': False}, {'mql': 'Color_Level19', 'py': 'Color_Level19', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет фибоуровня 19', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FiboName = _input('FiboName', 'SupremAutoFibo')  # Имя объекта
Timeframe = _input('Timeframe', PERIOD_D1)  # Таймфрейм индикатора для расчета уровней Фибоначи
NumberofBar = _input('NumberofBar', 1)  # Номер стартового бара для поиска экстремумов
nPeriod = _input('nPeriod', 30)  # Количество баров для поиска экстремумов
FiboColor = _input('FiboColor', clrGray)  # Цвет Фибо
FiboLevel1 = _input('FiboLevel1', -1.0)  # значение фибоуровня 1
StyleLevel1 = _input('StyleLevel1', STYLE_SOLID)  # стиль линии фибоуровня 1
WidthLevel1 = _input('WidthLevel1', 4)  # толщина линии фибоуровня 1
Color_Level1 = _input('Color_Level1', clrRed)  # цвет фибоуровня 1
FiboLevel2 = _input('FiboLevel2', -0.764)  # значение фибоуровня 2
StyleLevel2 = _input('StyleLevel2', STYLE_SOLID)  # стиль линии фибоуровня 2
WidthLevel2 = _input('WidthLevel2', 1)  # толщина линии фибоуровня 2
Color_Level2 = _input('Color_Level2', clrDarkViolet)  # цвет фибоуровня 2
FiboLevel3 = _input('FiboLevel3', -0.618)  # значение фибоуровня 3
StyleLevel3 = _input('StyleLevel3', STYLE_DASH)  # стиль линии фибоуровня 3
WidthLevel3 = _input('WidthLevel3', 1)  # толщина линии фибоуровня 3
Color_Level3 = _input('Color_Level3', clrOrange)  # цвет фибоуровня 3
FiboLevel4 = _input('FiboLevel4', -0.5)  # значение фибоуровня 4
StyleLevel4 = _input('StyleLevel4', STYLE_SOLID)  # стиль линии фибоуровня 4
WidthLevel4 = _input('WidthLevel4', 2)  # толщина линии фибоуровня 4
Color_Level4 = _input('Color_Level4', clrMagenta)  # цвет фибоуровня 4
FiboLevel5 = _input('FiboLevel5', -0.382)  # значение фибоуровня 5
StyleLevel5 = _input('StyleLevel5', STYLE_DASH)  # стиль линии фибоуровня 5
WidthLevel5 = _input('WidthLevel5', 1)  # толщина линии фибоуровня 5
Color_Level5 = _input('Color_Level5', clrBlue)  # цвет фибоуровня 5
FiboLevel6 = _input('FiboLevel6', -0.236)  # значение фибоуровня 6
StyleLevel6 = _input('StyleLevel6', STYLE_SOLID)  # стиль линии фибоуровня 6
WidthLevel6 = _input('WidthLevel6', 1)  # толщина линии фибоуровня 6
Color_Level6 = _input('Color_Level6', clrGray)  # цвет фибоуровня 6
FiboLevel7 = _input('FiboLevel7', 0.0)  # значение фибоуровня 7
StyleLevel7 = _input('StyleLevel7', STYLE_SOLID)  # стиль линии фибоуровня 7
WidthLevel7 = _input('WidthLevel7', 4)  # толщина линии фибоуровня 7
Color_Level7 = _input('Color_Level7', clrRed)  # цвет фибоуровня 7
FiboLevel8 = _input('FiboLevel8', 0.236)  # значение фибоуровня 8
StyleLevel8 = _input('StyleLevel8', STYLE_SOLID)  # стиль линии фибоуровня 8
WidthLevel8 = _input('WidthLevel8', 1)  # толщина линии фибоуровня 8
Color_Level8 = _input('Color_Level8', clrDarkViolet)  # цвет фибоуровня 8
FiboLevel9 = _input('FiboLevel9', 0.382)  # значение фибоуровня 9
StyleLevel9 = _input('StyleLevel9', STYLE_DASH)  # стиль линии фибоуровня 9
WidthLevel9 = _input('WidthLevel9', 1)  # толщина линии фибоуровня 9
Color_Level9 = _input('Color_Level9', clrOrange)  # цвет фибоуровня 9
FiboLevel10 = _input('FiboLevel10', 0.5)  # значение фибоуровня 10
StyleLevel10 = _input('StyleLevel10', STYLE_SOLID)  # стиль линии фибоуровня 10
WidthLevel10 = _input('WidthLevel10', 2)  # толщина линии фибоуровня 10
Color_Level10 = _input('Color_Level10', clrMagenta)  # цвет фибоуровня 10
FiboLevel11 = _input('FiboLevel11', 0.618)  # значение фибоуровня 11
StyleLevel11 = _input('StyleLevel11', STYLE_DASH)  # стиль линии фибоуровня 11
WidthLevel11 = _input('WidthLevel11', 1)  # толщина линии фибоуровня 11
Color_Level11 = _input('Color_Level11', clrBlue)  # цвет фибоуровня 11
FiboLevel12 = _input('FiboLevel12', 0.764)  # значение фибоуровня 12
StyleLevel12 = _input('StyleLevel12', STYLE_SOLID)  # стиль линии фибоуровня 12
WidthLevel12 = _input('WidthLevel12', 1)  # толщина линии фибоуровня 12
Color_Level12 = _input('Color_Level12', clrGray)  # цвет фибоуровня 12
FiboLevel13 = _input('FiboLevel13', 1.0)  # значение фибоуровня 13
StyleLevel13 = _input('StyleLevel13', STYLE_SOLID)  # стиль линии фибоуровня 13
WidthLevel13 = _input('WidthLevel13', 4)  # толщина линии фибоуровня 13
Color_Level13 = _input('Color_Level13', clrRed)  # цвет фибоуровня 13
FiboLevel14 = _input('FiboLevel14', 1.236)  # значение фибоуровня 14
StyleLevel14 = _input('StyleLevel14', STYLE_SOLID)  # стиль линии фибоуровня 14
WidthLevel14 = _input('WidthLevel14', 1)  # толщина линии фибоуровня 14
Color_Level14 = _input('Color_Level14', clrDarkViolet)  # цвет фибоуровня 14
FiboLevel15 = _input('FiboLevel15', 1.382)  # значение фибоуровня 15
StyleLevel15 = _input('StyleLevel15', STYLE_DASH)  # стиль линии фибоуровня 15
WidthLevel15 = _input('WidthLevel15', 1)  # толщина линии фибоуровня 15
Color_Level15 = _input('Color_Level15', clrOrange)  # цвет фибоуровня 15
FiboLevel16 = _input('FiboLevel16', 1.5)  # значение фибоуровня 16
StyleLevel16 = _input('StyleLevel16', STYLE_SOLID)  # стиль линии фибоуровня 16
WidthLevel16 = _input('WidthLevel16', 2)  # толщина линии фибоуровня 16
Color_Level16 = _input('Color_Level16', clrMagenta)  # цвет фибоуровня 16
FiboLevel17 = _input('FiboLevel17', 1.618)  # значение фибоуровня 17
StyleLevel17 = _input('StyleLevel17', STYLE_DASH)  # стиль линии фибоуровня 17
WidthLevel17 = _input('WidthLevel17', 1)  # толщина линии фибоуровня 17
Color_Level17 = _input('Color_Level17', clrBlue)  # цвет фибоуровня 17
FiboLevel18 = _input('FiboLevel18', 1.764)  # значение фибоуровня 18
StyleLevel18 = _input('StyleLevel18', STYLE_SOLID)  # стиль линии фибоуровня 18
WidthLevel18 = _input('WidthLevel18', 1)  # толщина линии фибоуровня 18
Color_Level18 = _input('Color_Level18', clrGray)  # цвет фибоуровня 18
FiboLevel19 = _input('FiboLevel19', 2.0)  # значение фибоуровня 19
StyleLevel19 = _input('StyleLevel19', STYLE_SOLID)  # стиль линии фибоуровня 19
WidthLevel19 = _input('WidthLevel19', 4)  # толщина линии фибоуровня 19
Color_Level19 = _input('Color_Level19', clrRed)  # цвет фибоуровня 19
Values = Arr(19, 0.0, dyn=False)
Colors = Arr(19, 0, dyn=False)
Styles = Arr(19, 0, dyn=False)
Widths = Arr(19, 0, dyn=False)
nOpen = Arr(0, 0.0)
nClose = Arr(0, 0.0)
nHigh = Arr(0, 0.0)
nLow = Arr(0, 0.0)
nTime = Arr(0, 0)

def FiboLevelsCreate(chart_ID=0, name='FiboLevels', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, ray_left=False, ray_right=False, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    ChangeFiboLevelsEmptyPoints(time1, price1, time2, price2)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_FIBO, sub_window, time1.v, price1.v, time2.v, price2.v):
        Print('FiboLevelsCreate', ': не удалось создать "Уровни Фибоначчи"! Код ошибки = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def FiboLevelsSet(levels, values, colors, styles, widths, chart_ID=0, name='FiboLevels'):
    if ((levels != ArraySize(colors) or levels != ArraySize(styles)) or levels != ArraySize(widths)) or levels != ArraySize(widths):
        Print('FiboLevelsSet', ': длина массива не соответствует количеству уровней, ошибка!')
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_LEVELS, levels)
    for i in range(0, levels):
        ObjectSetDouble(chart_ID, name, OBJPROP_LEVELVALUE, i, values[i])
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELCOLOR, i, colors[i])
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELSTYLE, i, styles[i])
        ObjectSetInteger(chart_ID, name, OBJPROP_LEVELWIDTH, i, _int(widths[i]))
        ObjectSetString(chart_ID, name, OBJPROP_LEVELTEXT, i, DoubleToString(100 * values[i], 1))
    return True

def FiboLevelsPointChange(chart_ID=0, name='FiboLevels', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('FiboLevelsPointChange', ': не удалось переместить точку привязки! Код ошибки = ', GetLastError())
        return False
    return True

def FiboLevelsDelete(chart_ID=0, name='FiboLevels'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('FiboLevelsDelete', ': не удалось удалить "Уровни Фибоначчи"! Код ошибки = ', GetLastError())
        return False
    return True

def ChangeFiboLevelsEmptyPoints(time1, price1, time2, price2):
    if not time2.v:
        time2.v = TimeCurrent()
    if not price2.v:
        price2.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if not time1.v:
        temp = Arr(10, 0, dyn=False)
        CopyTime(Symbol(), Period(), _DT(time2.v), 10, temp)
        time1.v = temp[0]
    if not price1.v:
        price1.v = price2.v - (200 * SymbolInfoDouble(Symbol(), SYMBOL_POINT))

def OnInit():
    Values[0] = FiboLevel1
    Values[1] = FiboLevel2
    Values[2] = FiboLevel3
    Values[3] = FiboLevel4
    Values[4] = FiboLevel5
    Values[5] = FiboLevel6
    Values[6] = FiboLevel7
    Values[7] = FiboLevel8
    Values[8] = FiboLevel9
    Values[9] = FiboLevel10
    Values[10] = FiboLevel11
    Values[11] = FiboLevel12
    Values[12] = FiboLevel13
    Values[13] = FiboLevel14
    Values[14] = FiboLevel15
    Values[15] = FiboLevel16
    Values[16] = FiboLevel17
    Values[17] = FiboLevel18
    Values[18] = FiboLevel19
    Colors[0] = Color_Level1
    Colors[1] = Color_Level2
    Colors[2] = Color_Level3
    Colors[3] = Color_Level4
    Colors[4] = Color_Level5
    Colors[5] = Color_Level6
    Colors[6] = Color_Level7
    Colors[7] = Color_Level8
    Colors[8] = Color_Level9
    Colors[9] = Color_Level10
    Colors[10] = Color_Level11
    Colors[11] = Color_Level12
    Colors[12] = Color_Level13
    Colors[13] = Color_Level14
    Colors[14] = Color_Level15
    Colors[15] = Color_Level16
    Colors[16] = Color_Level17
    Colors[17] = Color_Level18
    Colors[18] = Color_Level19
    Styles[0] = StyleLevel1
    Styles[1] = StyleLevel2
    Styles[2] = StyleLevel3
    Styles[3] = StyleLevel4
    Styles[4] = StyleLevel5
    Styles[5] = StyleLevel6
    Styles[6] = StyleLevel7
    Styles[7] = StyleLevel8
    Styles[8] = StyleLevel9
    Styles[9] = StyleLevel10
    Styles[10] = StyleLevel11
    Styles[11] = StyleLevel12
    Styles[12] = StyleLevel13
    Styles[13] = StyleLevel14
    Styles[14] = StyleLevel15
    Styles[15] = StyleLevel16
    Styles[16] = StyleLevel17
    Styles[17] = StyleLevel18
    Styles[18] = StyleLevel19
    Widths[0] = WidthLevel1
    Widths[1] = WidthLevel2
    Widths[2] = WidthLevel3
    Widths[3] = WidthLevel4
    Widths[4] = WidthLevel5
    Widths[5] = WidthLevel6
    Widths[6] = WidthLevel7
    Widths[7] = WidthLevel8
    Widths[8] = WidthLevel9
    Widths[9] = WidthLevel10
    Widths[10] = WidthLevel11
    Widths[11] = WidthLevel12
    Widths[12] = WidthLevel13
    Widths[13] = WidthLevel14
    Widths[14] = WidthLevel15
    Widths[15] = WidthLevel16
    Widths[16] = WidthLevel17
    Widths[17] = WidthLevel18
    Widths[18] = WidthLevel19
    ArrayResize(nTime, nPeriod)
    ArrayResize(nHigh, nPeriod)
    ArrayResize(nLow, nPeriod)
    ArraySetAsSeries(nTime, True)
    ArraySetAsSeries(nHigh, True)
    ArraySetAsSeries(nLow, True)
    if not FiboLevelsCreate(0, FiboName, 0, 0, 0.0, 0, 0.0, FiboColor, STYLE_SOLID, 0, True, False, False, True, False, 0):
        Print('Не удалось создать Фибо!')
        return INIT_FAILED
    if not FiboLevelsSet(19, Values, Colors, Styles, Widths, 0, FiboName):
        Print('Не удалось настроить Фибо!')
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'SupremAutoFibo')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    FiboLevelsDelete(0, FiboName)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not ObjectFind(0, FiboName):
        if not FiboLevelsCreate(0, FiboName, 0, 0, 0.0, 0, 0.0, FiboColor, STYLE_SOLID, 0, True, False, False, True, False, 0):
            Print('Не удалось создать Фибо!')
            return 0
        if not FiboLevelsSet(19, Values, Colors, Styles, Widths, 0, FiboName):
            Print('Не удалось настроить Фибо!')
            return 0
    P1 = 0.0
    P2 = 0.0
    to_copy = 0
    D1 = 0
    D2 = 0
    ArraySetAsSeries(time, True)
    to_copy = _int(nPeriod)
    if CopyTime(None, Timeframe, NumberofBar, to_copy, nTime) < to_copy:
        return 0
    if CopyHigh(None, Timeframe, NumberofBar, to_copy, nHigh) < to_copy:
        return 0
    if CopyLow(None, Timeframe, NumberofBar, to_copy, nLow) < to_copy:
        return 0
    hbar = ArrayMaximum(nHigh, 0, nPeriod)
    lbar = ArrayMinimum(nLow, 0, nPeriod)
    if lbar <= hbar:
        P1 = nHigh[hbar]
        P2 = nLow[lbar]
    else:
        P1 = nLow[lbar]
        P2 = nHigh[hbar]
    D1 = nTime[nPeriod - 1]
    D2 = TimeCurrent()
    if not FiboLevelsPointChange(0, FiboName, 0, D1, P1):
        return rates_total
    if not FiboLevelsPointChange(0, FiboName, 1, D2, P2):
        return rates_total
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SupremAutoFibo(_MQL5Indicator):
    name = 'SupremAutoFibo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм индикатора для расчета уровней Фибоначи
        'NumberofBar': 1,  # Номер стартового бара для поиска экстремумов
        'nPeriod': 30,  # Количество баров для поиска экстремумов
        'FiboLevel1': -1.0,  # значение фибоуровня 1
        'StyleLevel1': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 1
        'WidthLevel1': 4,  # толщина линии фибоуровня 1
        'FiboLevel2': -0.764,  # значение фибоуровня 2
        'StyleLevel2': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 2
        'WidthLevel2': 1,  # толщина линии фибоуровня 2
        'FiboLevel3': -0.618,  # значение фибоуровня 3
        'StyleLevel3': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 3
        'WidthLevel3': 1,  # толщина линии фибоуровня 3
        'FiboLevel4': -0.5,  # значение фибоуровня 4
        'StyleLevel4': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 4
        'WidthLevel4': 2,  # толщина линии фибоуровня 4
        'FiboLevel5': -0.382,  # значение фибоуровня 5
        'StyleLevel5': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 5
        'WidthLevel5': 1,  # толщина линии фибоуровня 5
        'FiboLevel6': -0.236,  # значение фибоуровня 6
        'StyleLevel6': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 6
        'WidthLevel6': 1,  # толщина линии фибоуровня 6
        'FiboLevel7': 0.0,  # значение фибоуровня 7
        'StyleLevel7': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 7
        'WidthLevel7': 4,  # толщина линии фибоуровня 7
        'FiboLevel8': 0.236,  # значение фибоуровня 8
        'StyleLevel8': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 8
        'WidthLevel8': 1,  # толщина линии фибоуровня 8
        'FiboLevel9': 0.382,  # значение фибоуровня 9
        'StyleLevel9': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 9
        'WidthLevel9': 1,  # толщина линии фибоуровня 9
        'FiboLevel10': 0.5,  # значение фибоуровня 10
        'StyleLevel10': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 10
        'WidthLevel10': 2,  # толщина линии фибоуровня 10
        'FiboLevel11': 0.618,  # значение фибоуровня 11
        'StyleLevel11': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 11
        'WidthLevel11': 1,  # толщина линии фибоуровня 11
        'FiboLevel12': 0.764,  # значение фибоуровня 12
        'StyleLevel12': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 12
        'WidthLevel12': 1,  # толщина линии фибоуровня 12
        'FiboLevel13': 1.0,  # значение фибоуровня 13
        'StyleLevel13': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 13
        'WidthLevel13': 4,  # толщина линии фибоуровня 13
        'FiboLevel14': 1.236,  # значение фибоуровня 14
        'StyleLevel14': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 14
        'WidthLevel14': 1,  # толщина линии фибоуровня 14
        'FiboLevel15': 1.382,  # значение фибоуровня 15
        'StyleLevel15': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 15
        'WidthLevel15': 1,  # толщина линии фибоуровня 15
        'FiboLevel16': 1.5,  # значение фибоуровня 16
        'StyleLevel16': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 16
        'WidthLevel16': 2,  # толщина линии фибоуровня 16
        'FiboLevel17': 1.618,  # значение фибоуровня 17
        'StyleLevel17': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # стиль линии фибоуровня 17
        'WidthLevel17': 1,  # толщина линии фибоуровня 17
        'FiboLevel18': 1.764,  # значение фибоуровня 18
        'StyleLevel18': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 18
        'WidthLevel18': 1,  # толщина линии фибоуровня 18
        'FiboLevel19': 2.0,  # значение фибоуровня 19
        'StyleLevel19': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии фибоуровня 19
        'WidthLevel19': 4,  # толщина линии фибоуровня 19
    }

