"""MFITrend_x10Full — converted from MQL5: MQL5 Indicators/MFITrend_x10Full/MFITrend_x10Full.mq5

Индикатор отображает положение осциллятора MFI с разных таймфреймов
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор отображает положение осциллятора MFI с разных таймфреймов'], 'name': 'MFITrend_x10Full', 'source': 'MQL5 Indicators/MFITrend_x10Full/MFITrend_x10Full.mq5', 'folder': 'MFITrend_x10Full', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16385, 'label': 'период графика 1', 'sinput': False}, {'mql': 'MFIPeriod1', 'py': 'MFIPeriod1', 'param': 'MFIPeriod1', 'type': 'uint', 'default': 7, 'label': 'период MFI 1', 'sinput': False}, {'mql': 'VolumeType1', 'py': 'VolumeType1', 'param': 'VolumeType1', 'type': 'int', 'default': 0, 'label': 'объём 1', 'sinput': False}, {'mql': 'UpLevel1', 'py': 'UpLevel1', 'param': 'UpLevel1', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 1', 'sinput': False}, {'mql': 'DnLevel1', 'py': 'DnLevel1', 'param': 'DnLevel1', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'период графика 2', 'sinput': False}, {'mql': 'MFIPeriod2', 'py': 'MFIPeriod2', 'param': 'MFIPeriod2', 'type': 'uint', 'default': 11, 'label': 'период MFI 2', 'sinput': False}, {'mql': 'VolumeType2', 'py': 'VolumeType2', 'param': 'VolumeType2', 'type': 'int', 'default': 0, 'label': 'объём 2', 'sinput': False}, {'mql': 'UpLevel2', 'py': 'UpLevel2', 'param': 'UpLevel2', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 2', 'sinput': False}, {'mql': 'DnLevel2', 'py': 'DnLevel2', 'param': 'DnLevel2', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 2', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16385, 'label': 'период графика 3', 'sinput': False}, {'mql': 'MFIPeriod3', 'py': 'MFIPeriod3', 'param': 'MFIPeriod3', 'type': 'uint', 'default': 15, 'label': 'период MFI 3', 'sinput': False}, {'mql': 'VolumeType3', 'py': 'VolumeType3', 'param': 'VolumeType3', 'type': 'int', 'default': 0, 'label': 'объём 3', 'sinput': False}, {'mql': 'UpLevel3', 'py': 'UpLevel3', 'param': 'UpLevel3', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 3', 'sinput': False}, {'mql': 'DnLevel3', 'py': 'DnLevel3', 'param': 'DnLevel3', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 3', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16385, 'label': 'период графика 4', 'sinput': False}, {'mql': 'MFIPeriod4', 'py': 'MFIPeriod4', 'param': 'MFIPeriod4', 'type': 'uint', 'default': 19, 'label': 'период MFI 4', 'sinput': False}, {'mql': 'VolumeType4', 'py': 'VolumeType4', 'param': 'VolumeType4', 'type': 'int', 'default': 0, 'label': 'объём 4', 'sinput': False}, {'mql': 'UpLevel4', 'py': 'UpLevel4', 'param': 'UpLevel4', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 4', 'sinput': False}, {'mql': 'DnLevel4', 'py': 'DnLevel4', 'param': 'DnLevel4', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 4', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16385, 'label': 'период графика 5', 'sinput': False}, {'mql': 'MFIPeriod5', 'py': 'MFIPeriod5', 'param': 'MFIPeriod5', 'type': 'uint', 'default': 23, 'label': 'период MFI 5', 'sinput': False}, {'mql': 'VolumeType5', 'py': 'VolumeType5', 'param': 'VolumeType5', 'type': 'int', 'default': 0, 'label': 'объём 5', 'sinput': False}, {'mql': 'UpLevel5', 'py': 'UpLevel5', 'param': 'UpLevel5', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 5', 'sinput': False}, {'mql': 'DnLevel5', 'py': 'DnLevel5', 'param': 'DnLevel5', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 5', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16385, 'label': 'период графика 6', 'sinput': False}, {'mql': 'MFIPeriod6', 'py': 'MFIPeriod6', 'param': 'MFIPeriod6', 'type': 'uint', 'default': 27, 'label': 'период MFI 6', 'sinput': False}, {'mql': 'VolumeType6', 'py': 'VolumeType6', 'param': 'VolumeType6', 'type': 'int', 'default': 0, 'label': 'объём 6', 'sinput': False}, {'mql': 'UpLevel6', 'py': 'UpLevel6', 'param': 'UpLevel6', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 6', 'sinput': False}, {'mql': 'DnLevel6', 'py': 'DnLevel6', 'param': 'DnLevel6', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 6', 'sinput': False}, {'mql': 'TimeFrame7', 'py': 'TimeFrame7', 'param': 'TimeFrame7', 'type': 'int', 'default': 16385, 'label': 'период графика 7', 'sinput': False}, {'mql': 'MFIPeriod7', 'py': 'MFIPeriod7', 'param': 'MFIPeriod7', 'type': 'uint', 'default': 31, 'label': 'период MFI 7', 'sinput': False}, {'mql': 'VolumeType7', 'py': 'VolumeType7', 'param': 'VolumeType7', 'type': 'int', 'default': 0, 'label': 'объём 7', 'sinput': False}, {'mql': 'UpLevel7', 'py': 'UpLevel7', 'param': 'UpLevel7', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 7', 'sinput': False}, {'mql': 'DnLevel7', 'py': 'DnLevel7', 'param': 'DnLevel7', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 7', 'sinput': False}, {'mql': 'TimeFrame8', 'py': 'TimeFrame8', 'param': 'TimeFrame8', 'type': 'int', 'default': 16385, 'label': 'период графика 8', 'sinput': False}, {'mql': 'MFIPeriod8', 'py': 'MFIPeriod8', 'param': 'MFIPeriod8', 'type': 'uint', 'default': 35, 'label': 'период MFI 8', 'sinput': False}, {'mql': 'VolumeType8', 'py': 'VolumeType8', 'param': 'VolumeType8', 'type': 'int', 'default': 0, 'label': 'объём 8', 'sinput': False}, {'mql': 'UpLevel8', 'py': 'UpLevel8', 'param': 'UpLevel8', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 8', 'sinput': False}, {'mql': 'DnLevel8', 'py': 'DnLevel8', 'param': 'DnLevel8', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 8', 'sinput': False}, {'mql': 'TimeFrame9', 'py': 'TimeFrame9', 'param': 'TimeFrame9', 'type': 'int', 'default': 16385, 'label': 'период графика 9', 'sinput': False}, {'mql': 'MFIPeriod9', 'py': 'MFIPeriod9', 'param': 'MFIPeriod9', 'type': 'uint', 'default': 39, 'label': 'период MFI 9', 'sinput': False}, {'mql': 'VolumeType9', 'py': 'VolumeType9', 'param': 'VolumeType9', 'type': 'int', 'default': 0, 'label': 'объём 9', 'sinput': False}, {'mql': 'UpLevel9', 'py': 'UpLevel9', 'param': 'UpLevel9', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 9', 'sinput': False}, {'mql': 'DnLevel9', 'py': 'DnLevel9', 'param': 'DnLevel9', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 9', 'sinput': False}, {'mql': 'TimeFrame10', 'py': 'TimeFrame10', 'param': 'TimeFrame10', 'type': 'int', 'default': 16385, 'label': 'период графика 10', 'sinput': False}, {'mql': 'MFIPeriod10', 'py': 'MFIPeriod10', 'param': 'MFIPeriod10', 'type': 'uint', 'default': 43, 'label': 'период MFI 10', 'sinput': False}, {'mql': 'VolumeType10', 'py': 'VolumeType10', 'param': 'VolumeType10', 'type': 'int', 'default': 0, 'label': 'объём 10', 'sinput': False}, {'mql': 'UpLevel10', 'py': 'UpLevel10', 'param': 'UpLevel10', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа 10', 'sinput': False}, {'mql': 'DnLevel10', 'py': 'DnLevel10', 'param': 'DnLevel10', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности 10', 'sinput': False}, {'mql': 'CpColor', 'py': 'CpColor', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'цвет названия индикатора', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет перекупленности индикатора', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 55295, 'label': 'цвет перепроданности индикатора', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет без изменения', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'размер шрифта', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'тип шрифта', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'угол расположения', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'расположение по вертикали', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'расположение по горизонтали', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_H1)  # период графика 1
MFIPeriod1 = _input('MFIPeriod1', 7)  # период MFI 1
VolumeType1 = _input('VolumeType1', VOLUME_TICK)  # объём 1
UpLevel1 = _input('UpLevel1', 70)  # уровень перезакупа 1
DnLevel1 = _input('DnLevel1', 30)  # уровень перепроданности 1
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # период графика 2
MFIPeriod2 = _input('MFIPeriod2', 11)  # период MFI 2
VolumeType2 = _input('VolumeType2', VOLUME_TICK)  # объём 2
UpLevel2 = _input('UpLevel2', 70)  # уровень перезакупа 2
DnLevel2 = _input('DnLevel2', 30)  # уровень перепроданности 2
TimeFrame3 = _input('TimeFrame3', PERIOD_H1)  # период графика 3
MFIPeriod3 = _input('MFIPeriod3', 15)  # период MFI 3
VolumeType3 = _input('VolumeType3', VOLUME_TICK)  # объём 3
UpLevel3 = _input('UpLevel3', 70)  # уровень перезакупа 3
DnLevel3 = _input('DnLevel3', 30)  # уровень перепроданности 3
TimeFrame4 = _input('TimeFrame4', PERIOD_H1)  # период графика 4
MFIPeriod4 = _input('MFIPeriod4', 19)  # период MFI 4
VolumeType4 = _input('VolumeType4', VOLUME_TICK)  # объём 4
UpLevel4 = _input('UpLevel4', 70)  # уровень перезакупа 4
DnLevel4 = _input('DnLevel4', 30)  # уровень перепроданности 4
TimeFrame5 = _input('TimeFrame5', PERIOD_H1)  # период графика 5
MFIPeriod5 = _input('MFIPeriod5', 23)  # период MFI 5
VolumeType5 = _input('VolumeType5', VOLUME_TICK)  # объём 5
UpLevel5 = _input('UpLevel5', 70)  # уровень перезакупа 5
DnLevel5 = _input('DnLevel5', 30)  # уровень перепроданности 5
TimeFrame6 = _input('TimeFrame6', PERIOD_H1)  # период графика 6
MFIPeriod6 = _input('MFIPeriod6', 27)  # период MFI 6
VolumeType6 = _input('VolumeType6', VOLUME_TICK)  # объём 6
UpLevel6 = _input('UpLevel6', 70)  # уровень перезакупа 6
DnLevel6 = _input('DnLevel6', 30)  # уровень перепроданности 6
TimeFrame7 = _input('TimeFrame7', PERIOD_H1)  # период графика 7
MFIPeriod7 = _input('MFIPeriod7', 31)  # период MFI 7
VolumeType7 = _input('VolumeType7', VOLUME_TICK)  # объём 7
UpLevel7 = _input('UpLevel7', 70)  # уровень перезакупа 7
DnLevel7 = _input('DnLevel7', 30)  # уровень перепроданности 7
TimeFrame8 = _input('TimeFrame8', PERIOD_H1)  # период графика 8
MFIPeriod8 = _input('MFIPeriod8', 35)  # период MFI 8
VolumeType8 = _input('VolumeType8', VOLUME_TICK)  # объём 8
UpLevel8 = _input('UpLevel8', 70)  # уровень перезакупа 8
DnLevel8 = _input('DnLevel8', 30)  # уровень перепроданности 8
TimeFrame9 = _input('TimeFrame9', PERIOD_H1)  # период графика 9
MFIPeriod9 = _input('MFIPeriod9', 39)  # период MFI 9
VolumeType9 = _input('VolumeType9', VOLUME_TICK)  # объём 9
UpLevel9 = _input('UpLevel9', 70)  # уровень перезакупа 9
DnLevel9 = _input('DnLevel9', 30)  # уровень перепроданности 9
TimeFrame10 = _input('TimeFrame10', PERIOD_H1)  # период графика 10
MFIPeriod10 = _input('MFIPeriod10', 43)  # период MFI 10
VolumeType10 = _input('VolumeType10', VOLUME_TICK)  # объём 10
UpLevel10 = _input('UpLevel10', 70)  # уровень перезакупа 10
DnLevel10 = _input('DnLevel10', 30)  # уровень перепроданности 10
CpColor = _input('CpColor', clrDarkOrchid)  # цвет названия индикатора
UpColor = _input('UpColor', clrBlue)  # цвет перекупленности индикатора
DnColor = _input('DnColor', clrGold)  # цвет перепроданности индикатора
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
    _q_fields = ('m_Ind', 'm_Handle', 'm_TimeFrame', 'm_Period', 'm_VolumeType', 'm_UpLevel', 'm_DnLevel')
    def __init__(self, *args):
        self.m_Ind = Arr(1, 0.0, dyn=False)
        self.m_Handle = 0
        self.m_TimeFrame = 0
        self.m_Period = 0
        self.m_VolumeType = 0
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
    Ind[0].m_Period = MFIPeriod1
    Ind[1].m_Period = MFIPeriod2
    Ind[2].m_Period = MFIPeriod3
    Ind[3].m_Period = MFIPeriod4
    Ind[4].m_Period = MFIPeriod5
    Ind[5].m_Period = MFIPeriod6
    Ind[6].m_Period = MFIPeriod7
    Ind[7].m_Period = MFIPeriod8
    Ind[8].m_Period = MFIPeriod9
    Ind[9].m_Period = MFIPeriod10
    Ind[0].m_VolumeType = VolumeType1
    Ind[1].m_VolumeType = VolumeType2
    Ind[2].m_VolumeType = VolumeType3
    Ind[3].m_VolumeType = VolumeType4
    Ind[4].m_VolumeType = VolumeType5
    Ind[5].m_VolumeType = VolumeType6
    Ind[6].m_VolumeType = VolumeType7
    Ind[7].m_VolumeType = VolumeType8
    Ind[8].m_VolumeType = VolumeType9
    Ind[9].m_VolumeType = VolumeType10
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
        Ind[poz].m_Handle = iMFI(Symbol(), Ind[poz].m_TimeFrame, Ind[poz].m_Period, Ind[poz].m_VolumeType)
        if Ind[poz].m_Handle == INVALID_HANDLE:
            Print('OnInit()(', poz, '): Не удалось получить хендл индикатора MFI', poz)
            return False
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    max_ = 0
    for poz in range(0, 10):
        if Ind[poz].m_Period > max_:
            max_ = Ind[poz].m_Period
    min_rates_total = _int(max_ + 1)
    xshift = _int(X_ + (8.3 * FontSize))
    Cap = 'MFITrend_x10Full'
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


class MFITrendX10Full(_MQL5Indicator):
    name = 'MFITrend_x10Full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 1
        'MFIPeriod1': 7,  # период MFI 1
        'VolumeType1': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 1
        'UpLevel1': 70,  # уровень перезакупа 1
        'DnLevel1': 30,  # уровень перепроданности 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 2
        'MFIPeriod2': 11,  # период MFI 2
        'VolumeType2': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 2
        'UpLevel2': 70,  # уровень перезакупа 2
        'DnLevel2': 30,  # уровень перепроданности 2
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 3
        'MFIPeriod3': 15,  # период MFI 3
        'VolumeType3': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 3
        'UpLevel3': 70,  # уровень перезакупа 3
        'DnLevel3': 30,  # уровень перепроданности 3
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 4
        'MFIPeriod4': 19,  # период MFI 4
        'VolumeType4': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 4
        'UpLevel4': 70,  # уровень перезакупа 4
        'DnLevel4': 30,  # уровень перепроданности 4
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 5
        'MFIPeriod5': 23,  # период MFI 5
        'VolumeType5': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 5
        'UpLevel5': 70,  # уровень перезакупа 5
        'DnLevel5': 30,  # уровень перепроданности 5
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 6
        'MFIPeriod6': 27,  # период MFI 6
        'VolumeType6': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 6
        'UpLevel6': 70,  # уровень перезакупа 6
        'DnLevel6': 30,  # уровень перепроданности 6
        'TimeFrame7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 7
        'MFIPeriod7': 31,  # период MFI 7
        'VolumeType7': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 7
        'UpLevel7': 70,  # уровень перезакупа 7
        'DnLevel7': 30,  # уровень перепроданности 7
        'TimeFrame8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 8
        'MFIPeriod8': 35,  # период MFI 8
        'VolumeType8': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 8
        'UpLevel8': 70,  # уровень перезакупа 8
        'DnLevel8': 30,  # уровень перепроданности 8
        'TimeFrame9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 9
        'MFIPeriod9': 39,  # период MFI 9
        'VolumeType9': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 9
        'UpLevel9': 70,  # уровень перезакупа 9
        'DnLevel9': 30,  # уровень перепроданности 9
        'TimeFrame10': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 10
        'MFIPeriod10': 43,  # период MFI 10
        'VolumeType10': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём 10
        'UpLevel10': 70,  # уровень перезакупа 10
        'DnLevel10': 30,  # уровень перепроданности 10
        'FontSize': 11,  # размер шрифта
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # тип шрифта
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # угол расположения
        'Y_': 20,  # расположение по вертикали
        'X_': 5,  # расположение по горизонтали
    }

