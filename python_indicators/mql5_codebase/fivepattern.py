"""fivepattern — converted from MQL5: MQL5 Indicators/FivePattern/fivepattern.mq5

М and W Wave Patterns by A. Merrill.\\n
№  Name Indicator buffers:
0  ExtPointE[]    - Point E;
1  ExtDeltaDE[]   - Delta DE;
2  ExtEvolution[] - Point Evolution;
3  ExtMutation[]  - Point Mutation;
4  ExtSumModel[]  = Count_Evolution/(Count_Evolution + Count_Mutation).
Copyright: Copyright 2014, A. Emelyanov; Link: A.Emelyanov2010@yandex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: FileReadLong, FileWriteLong
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.mymath_pattern_mycpattern import *  # #include MyCPattern.mqh
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.mymath_extremum_mycextremum import *  # #include mycextremum.mqh
from backtester.mql5.lib.myobjects_myccomment import *  # #include myccomment.mqh
from backtester.mql5.lib.myobjects_mycarrow import *  # #include mycarrow.mqh
from backtester.mql5.lib.myobjects_myctrendline import *  # #include myctrendline.mqh
from backtester.mql5.lib.myobjects_mychline import *  # #include mychline.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2014, A. Emelyanov', 'link': 'A.Emelyanov2010@yandex.ru', 'version': '1.00', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'Point E', 2: 'Delta DE', 3: 'Evolution', 4: 'Mutation', 5: 'Sum Model'}, 'levels': [], 'description': ['М and W Wave Patterns by A. Merrill.\\n', '№  Name Indicator buffers:', '0  ExtPointE[]    - Point E;', '1  ExtDeltaDE[]   - Delta DE;', '2  ExtEvolution[] - Point Evolution;', '3  ExtMutation[]  - Point Mutation;', '4  ExtSumModel[]  = Count_Evolution/(Count_Evolution + Count_Mutation).'], 'name': 'fivepattern', 'source': 'MQL5 Indicators/FivePattern/fivepattern.mq5', 'folder': 'FivePattern', 'inputs': [{'mql': 'Depth', 'py': 'Depth', 'param': 'Depth', 'type': 'int', 'default': 24, 'label': 'Zigzag: Ширина окна поиска(Depth)', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'int', 'default': 12, 'label': 'Zigzag: Изменение цены в пуктах(Deviation)', 'sinput': False}, {'mql': 'Backstep', 'py': 'Backstep', 'param': 'Backstep', 'type': 'int', 'default': 9, 'label': 'Zigzag: Отсутп от начала данных(Backstep)', 'sinput': False}, {'mql': 'HistSize', 'py': 'HistSize', 'param': 'HistSize', 'type': 'int', 'default': 500, 'label': 'Zigzag: Размер истории для расчетов', 'sinput': True}, {'mql': 'ColorArrow', 'py': 'ColorArrow', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет паттерных точек', 'sinput': True}, {'mql': 'ColorTrend', 'py': 'ColorTrend', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Цвет паттерной линии', 'sinput': True}, {'mql': 'WidthTrend', 'py': 'WidthTrend', 'param': 'WidthTrend', 'type': 'int', 'default': 2, 'label': 'Толщина паттерной линии', 'sinput': True}, {'mql': 'BackTrend', 'py': 'BackTrend', 'param': 'BackTrend', 'type': 'bool', 'default': True, 'label': 'Задний план для паттерной линии', 'sinput': True}, {'mql': 'StyleTrend', 'py': 'StyleTrend', 'param': 'StyleTrend', 'type': 'int', 'default': 0, 'label': 'Стиль паттерной линии', 'sinput': True}, {'mql': 'ColorUpHLine', 'py': 'ColorUpHLine', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет линии сопротивления', 'sinput': True}, {'mql': 'ColorDownHLine', 'py': 'ColorDownHLine', 'param': None, 'type': 'color', 'default': 255, 'label': 'Цвет линии поддержки', 'sinput': True}, {'mql': 'WidthHLine', 'py': 'WidthHLine', 'param': 'WidthHLine', 'type': 'int', 'default': 2, 'label': 'Толщина линий уровня', 'sinput': True}, {'mql': 'BackHLine', 'py': 'BackHLine', 'param': 'BackHLine', 'type': 'bool', 'default': True, 'label': 'Задний план для линий уровня', 'sinput': True}, {'mql': 'StyleHLine', 'py': 'StyleHLine', 'param': 'StyleHLine', 'type': 'int', 'default': 0, 'label': 'Стиль линий уровня', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MyCPattern.mqh', 'Object.mqh', 'StdLibErr.mqh', 'mycextremum.mqh', 'myccomment.mqh', 'mycarrow.mqh', 'myctrendline.mqh', 'mychline.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter
MQL5_TESTER = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
Depth = _input('Depth', 24)  # Zigzag: Ширина окна поиска(Depth)
Deviation = _input('Deviation', 12)  # Zigzag: Изменение цены в пуктах(Deviation)
Backstep = _input('Backstep', 9)  # Zigzag: Отсутп от начала данных(Backstep)
HistSize = _input('HistSize', 500)  # Zigzag: Размер истории для расчетов
ColorArrow = _input('ColorArrow', clrBlue)  # Цвет паттерных точек
ColorTrend = _input('ColorTrend', clrGold)  # Цвет паттерной линии
WidthTrend = _input('WidthTrend', 2)  # Толщина паттерной линии
BackTrend = _input('BackTrend', True)  # Задний план для паттерной линии
StyleTrend = _input('StyleTrend', STYLE_SOLID)  # Стиль паттерной линии
ColorUpHLine = _input('ColorUpHLine', clrBlue)  # Цвет линии сопротивления
ColorDownHLine = _input('ColorDownHLine', clrRed)  # Цвет линии поддержки
WidthHLine = _input('WidthHLine', 2)  # Толщина линий уровня
BackHLine = _input('BackHLine', True)  # Задний план для линий уровня
StyleHLine = _input('StyleHLine', STYLE_SOLID)  # Стиль линий уровня
Line = 1  # Номер первой строки комментария
MyPatternZigzag = None  # Класс: модели паттерной системы
MyListPattern = None  # Класс: хранилище графических объектов
MyComment = None  # Класс: комментария
ExtPointE = Arr(0, 0.0)  # Буфер: для хранения точки E
ExtDeltaDE = Arr(0, 0.0)  # Буфер: для хранения длины волны D-E(в пунктах!)
ExtEvolution = Arr(0, 0.0)  # Буфер: для хранения эволюций
ExtMutation = Arr(0, 0.0)  # Буфер: для хранения мутаций
ExtSumModel = Arr(0, 0.0)  # Буфер: для хранения счетчика-модели

class MyCPatternZigzag(MyCPattern):
    _q_fields = ('Depth', 'Deviation', 'Backstep', 'SizeBuffers', 'NumberLineComment', 'pE', 'pM', 'pEv1', 'pM1', 'tA', 'tB', 'tC', 'tD', 'tE', 'tEv', 'tM', 'iA', 'iB', 'iC', 'iD', 'iE', 'iEv', 'iM', 'countEvolution', 'countMutation', 'countError', 'Extremum', 'MyComment')
    _q_ptrs = ('Extremum', 'MyComment',)
    def __init__(self):
        MyCPattern.__init__(self)
        self.Depth = 0
        self.Deviation = 0
        self.Backstep = 0
        self.SizeBuffers = 0
        self.NumberLineComment = 0
        self.pE = 0.0
        self.pM = 0.0
        self.pEv1 = 0.0
        self.pM1 = 0.0
        self.tA = 0
        self.tB = 0
        self.tC = 0
        self.tD = 0
        self.tE = 0
        self.tEv = 0
        self.tM = 0
        self.iA = 0
        self.iB = 0
        self.iC = 0
        self.iD = 0
        self.iE = 0
        self.iEv = 0
        self.iM = 0
        self.countEvolution = 0
        self.countMutation = 0
        self.countError = 0
        self.Extremum = None
        self.MyComment = None
        self.Depth = 24
        self.Deviation = 12
        self.Backstep = 9
        self.SizeBuffers = 500
        self.Extremum = MyCExtremum()
        self.tA = 0
        self.tB = 0
        self.tC = 0
        self.tD = 0
        self.tE = 0
        self.iA = 0
        self.iB = 0
        self.iC = 0
        self.iD = 0
        self.iE = 0
        self.MyComment = None
        self.NumberLineComment = 2
        self.countEvolution = 0
        self.countMutation = 0
        self.countError = 0
        self.pE = 0.0
        self.pM = 0.0
        self.pEv1 = 0.0
        self.pM1 = 0.0
        self.iEv = 0
        self.iM = 0
    def _q_dtor(self):
        _delete(self.Extremum)
    def SetDepth(self, depth):
        self.Depth = depth
    def SetDeviation(self, dev):
        self.Deviation = dev
    def SetBackstep(self, back):
        self.Backstep = back
    def SetSizeBuffers(self, size):
        self.SizeBuffers = size
    def SetNumberLineComment(self, NL):
        if NL > 0 and NL < 31:
            self.NumberLineComment = NL
        else:
            self.NumberLineComment = 1
    def GetDepth(self):
        return self.Depth
    def GetDeviation(self):
        return self.Deviation
    def GetBackstep(self):
        return self.Backstep
    def GetSizeBuffers(self):
        return self.SizeBuffers
    def GetNumberLineComment(self):
        return self.NumberLineComment
    def GetCountLineComment(self):
        if MQL5InfoInteger(MQL5_TESTER):
            return 5
        return 4
    def GetNamePattern(self, high, low, time):
        if self.SeachParams(high, low, time):
            self.Get_0()
            if self.IsPointENotReal():
                self.iE = self.SizeBuffers - 1
                self.tE = time[self.SizeBuffers - 1]
            self.CalcModelCount()
            self.CalcPrognozPoint()
            return EnumToString(self.GetLastPattern(), 'NamePattern')
        return 'ERROR'
    def GetNameLastPattern(self):
        return EnumToString(self.GetLastPattern(), 'NamePattern')
    def GetNamePrevPattern(self):
        return EnumToString(self.GetPrevPattern(), 'NamePattern')
    def GetNameEvolution(self):
        return EnumToString(self.GetNextEvolution(), 'NamePattern')
    def GetNameMutation(self):
        return EnumToString(self.GetNextMutation(), 'NamePattern')
    def GetSumModel(self):
        ret = float(self.countEvolution + self.countMutation)
        if ret != 0:
            ret = _fdiv(self.countEvolution, ret)
            return ret
        return 0.0
    def PrintComment(self):
        if self.MyComment is not None:
            self.MyComment.AddLineOfIndex(self.NumberLineComment, 'Now is pattern: ' + EnumToString(self.GetLastPattern(), 'NamePattern'))
            self.MyComment.AddLineOfIndex(self.NumberLineComment + 1, 'Next pattern(Evolution): ' + self.GetNameEvolution() + ', price = ' + DoubleToString(self.GetPointEvolution(), Digits()))
            self.MyComment.AddLineOfIndex(self.NumberLineComment + 2, 'Next pattern(Mutation ): ' + self.GetNameMutation() + ', price = ' + DoubleToString(self.GetPointMutation(), Digits()))
            if (self.countEvolution + self.countMutation + self.countError) < 10:
                self.MyComment.AddLineOfIndex(self.NumberLineComment + 3, 'No counter calculation.')
            else:
                nSumModel = self.countEvolution + self.countMutation + self.countError
                sout = 'Evolution: ' + DoubleToString(_idiv(100 * self.countEvolution, nSumModel), 2) + '% Mutation: ' + DoubleToString(_idiv(100 * self.countMutation, nSumModel), 2) + '% Error: ' + DoubleToString(_idiv(100 * self.countError, nSumModel), 2) + '%'
                self.MyComment.AddLineOfIndex(self.NumberLineComment + 3, sout)
            if MQL5InfoInteger(MQL5_TESTER):
                sout = 'DEBUG_MODE: countEvolution= ' + IntegerToString(self.countEvolution) + '; countMutation= ' + IntegerToString(self.countMutation) + '; countError= ' + IntegerToString(self.countError) + '; oldPattern= ' + EnumToString(self.oldPattern, 'NamePattern')
                self.MyComment.AddLineOfIndex(self.NumberLineComment + 4, sout)
    def GetPointEvolution(self):
        return self.pE
    def GetPointMutation(self):
        return self.pM
    def GetPointEvolutionLevel1(self):
        return self.pEv1
    def GetPointMutationLevel1(self):
        return self.pM1
    def GetTimeA(self):
        return self.tA
    def GetTimeB(self):
        return self.tB
    def GetTimeC(self):
        return self.tC
    def GetTimeD(self):
        return self.tD
    def GetTimeE(self):
        return self.tE
    def GetTimeEvolution(self):
        return self.tEv
    def GetTimeMutation(self):
        return self.tM
    def GetIndexA(self):
        return self.iA
    def GetIndexB(self):
        return self.iB
    def GetIndexC(self):
        return self.iC
    def GetIndexD(self):
        return self.iD
    def GetIndexE(self):
        return self.iE
    def GetIndexEvolution(self):
        return self.iEv
    def GetIndexMutation(self):
        return self.iM
    def AddPointerCommet(self, pComment):
        if pComment is not None:
            self.MyComment = pComment
    def SeachParams(self, high, low, time):
        ret = -1
        ind = 0
        indD = 0
        if ArrayRange(high, 0) < self.SizeBuffers:
            return False
        if ArrayRange(low, 0) < self.SizeBuffers:
            return False
        if ArrayRange(time, 0) < self.SizeBuffers:
            return False
        ret = self.Extremum.GetClassicZigzag(high, low, self.Depth, self.Deviation, self.Backstep)
        if ret > 0:
            ind = ret - 1
            for ind in range(ind, 0, -1):
                mD = self.Extremum.ZigzagBuffer[ind]
                if mD != 0:
                    self.tD = time[ind]
                    self.SetD(mD)
                    indD = ind
                    self.iD = ind
                    break
            else:
                ind = _range_end(ind, 0, -1)
            if ind > (ret - self.Backstep):
                self.tE = self.tD
                self.iE = self.iD
                self.SetE(self.GetD())
                indD = -1
                ind = ind - 1
                for ind in range(ind, 0, -1):
                    mD = self.Extremum.ZigzagBuffer[ind]
                    if mD != 0:
                        self.tD = time[ind]
                        self.SetD(mD)
                        self.iD = ind
                        break
                else:
                    ind = _range_end(ind, 0, -1)
            ind = ind - 1
            for ind in range(ind, 0, -1):
                mC = self.Extremum.ZigzagBuffer[ind]
                if mC != 0:
                    self.SetC(mC)
                    self.tC = time[ind]
                    self.iC = ind
                    break
            else:
                ind = _range_end(ind, 0, -1)
            ind = ind - 1
            for ind in range(ind, 0, -1):
                mB = self.Extremum.ZigzagBuffer[ind]
                if mB != 0:
                    self.SetB(mB)
                    self.tB = time[ind]
                    self.iB = ind
                    break
            else:
                ind = _range_end(ind, 0, -1)
            ind = ind - 1
            for ind in range(ind, 0, -1):
                mA = self.Extremum.ZigzagBuffer[ind]
                if mA != 0:
                    self.SetA(mA)
                    self.tA = time[ind]
                    self.iA = ind
                    break
            else:
                ind = _range_end(ind, 0, -1)
        else:
            return False
        if indD < 0:
            return True
        if self.GetC() > self.GetD():
            ind = ArrayMaximum(high, indD + 1, self.SizeBuffers - indD - 1)
            if ind > 0:
                self.SetE(high[ind])
                self.tE = time[ind]
                self.iE = ind
            else:
                self.SetE(high[self.SizeBuffers - 2])
                self.tE = time[self.SizeBuffers - 2]
                self.iE = self.SizeBuffers - 2
        else:
            ind = ArrayMinimum(low, indD + 1, self.SizeBuffers - indD - 1)
            if ind > 0:
                self.SetE(low[ind])
                self.tE = time[ind]
                self.iE = ind
            else:
                self.SetE(low[self.SizeBuffers - 2])
                self.tE = time[self.SizeBuffers - 2]
                self.iE = self.SizeBuffers - 2
        deltaED = MathAbs(self.GetE() - self.GetD())
        dnED = _int(_fdiv(deltaED, Point()))
        if dnED < self.Deviation:
            self.SetE(self.GetD())
            self.tE = self.tD
            self.iE = self.iD
            self.SetD(self.GetC())
            self.tD = self.tC
            self.iD = self.iC
            self.SetC(self.GetB())
            self.tC = self.tB
            self.iC = self.iB
            self.SetB(self.GetA())
            self.tB = self.tA
            self.iB = self.iA
            ind = self.iB
            ind = ind - 1
            for ind in range(ind, 0, -1):
                mA = self.Extremum.ZigzagBuffer[ind]
                if mA != 0:
                    self.SetA(mA)
                    self.tA = time[ind]
                    self.iA = ind
                    break
            else:
                ind = _range_end(ind, 0, -1)
        return True
    def CalcModelCount(self):
        if ((self.countEvolution == 0 and self.countMutation == 0) and self.countError == 0) and self.oldPattern == NOPATTERN:
            return
        if self.oldPattern == self.pattern:
            return
        if self.pattern == NOPATTERN:
            self.countError += 1
            return
        if self.oldPattern == NOPATTERN:
            return
        if self.IsRightEvolution() == 1:
            self.countEvolution += 1
            return
        if self.IsRightMutation() == 1:
            self.countMutation += 1
            return
        self.countError += 1
        return
    def CalcPrognozPoint(self):
        if self.pattern == NOPATTERN:
            self.pE = 0.0
            self.pM = 0.0
            self.iEv = 0
            self.iM = 0
            self.CalcPrognozLevel1()
            return
        iTemp = 0
        if _idiv(self.iE - self.iA, 5) < 3 and _idiv(self.iE - self.iA, 5) > (self.Backstep * 2):
            iTemp = self.iE + _idiv(self.iE - self.iA, 5)
        else:
            iTemp = self.iE + (self.Backstep * 2)
        self.tEv = ((iTemp - self.iE) * PeriodSeconds()) + self.GetTimeE()
        self.tM = ((iTemp - self.iE) * PeriodSeconds()) + self.GetTimeE()
        rA = 0.0
        rB = 0.0
        _sw1 = self.pattern
        if _sw1 == M1:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble((0.3819 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M2:
            self.pE = NormalizeDouble(self.D - (1.618 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.5 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M3:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble((0.3819 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M4:
            self.pE = NormalizeDouble(self.D - (1.272 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.5 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M5:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble((0.25 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M6:
            self.pE = NormalizeDouble(self.D - (1.272 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.3819 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M7:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble((0.3819 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M8:
            self.pE = NormalizeDouble(self.D - (0.618 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.5 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M9:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble((0.25 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M10:
            self.pE = NormalizeDouble(self.D - (0.618 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.3819 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M11:
            self.pE = NormalizeDouble(self.D - (0.5 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.5 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M12:
            self.pE = NormalizeDouble(self.D - (3.0 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.3819 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M13:
            self.pE = NormalizeDouble(self.D - (1.618 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.5 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M14:
            self.pE = NormalizeDouble(self.D - (1.618 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.25 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M15:
            self.pE = NormalizeDouble(self.C - ((self.C - self.A) / 1.618), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E + ((self.B - self.E) / 1.618), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == M16:
            self.pE = NormalizeDouble(self.D - (0.618 * (self.D - self.C)), Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble((0.5 * (self.D - self.E)) + self.E, Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W1:
            self.pE = NormalizeDouble((0.618 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.5 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W2:
            self.pE = NormalizeDouble((1.272 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.3819 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W3:
            self.pE = NormalizeDouble((1.618 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.25 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W4:
            self.pE = NormalizeDouble((1.618 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.5 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W5:
            self.pE = NormalizeDouble((3.0 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.3819 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W6:
            self.pE = NormalizeDouble((0.5 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.5 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W7:
            self.pE = NormalizeDouble((0.618 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.3819 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W8:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble(self.E - (0.25 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W9:
            self.pE = NormalizeDouble((0.618 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.5 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W10:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble(self.E - (0.3819 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W11:
            self.pE = NormalizeDouble((1.272 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.3819 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W12:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble(self.E - (0.25 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W13:
            self.pE = NormalizeDouble((1.272 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.5 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W14:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble(self.E - (0.3819 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W15:
            self.pE = NormalizeDouble((1.618 * (self.C - self.D)) + self.D, Digits())
            self.iEv = iTemp
            self.pM = NormalizeDouble(self.E - (0.5 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        elif _sw1 == W16:
            self.pE = 0.0
            self.iEv = 0
            self.pM = NormalizeDouble(self.E - (0.3819 * (self.E - self.D)), Digits())
            self.iM = iTemp
            self.CalcPrognozLevel1()
        else:
            self.pE = 0.0
            self.pM = 0.0
            self.iEv = 0
            self.iM = 0
            self.CalcPrognozLevel1()
    def CalcPrognozLevel1(self):
        rA = Box(0.0)
        rB = Box(0.0)
        _sw2 = self.pattern
        if _sw2 == M1:
            self.pEv1 = 0.0
            self.pM1 = NormalizeDouble(self.E + ((self.B - self.D) * 1.618), Digits())
        elif _sw2 == M3:
            self.pEv1 = 0.0
            self.pM1 = NormalizeDouble(self.E + ((self.B - self.D) * 1.618), Digits())
        elif _sw2 == M5:
            self.pEv1 = 0.0
            rA.v = self.B
            rB.v = self.D
            self.pM1 = NormalizeDouble(self.CalcRegress(self.iM, rA, self.iB, rB, self.iD), Digits())
        elif _sw2 == M13:
            self.pEv1 = NormalizeDouble(self.E - ((self.B - self.A) * 0.618), Digits())
            self.pM1 = NormalizeDouble(self.E + ((self.B - self.A) * 0.618), Digits())
        elif _sw2 == M15:
            self.pEv1 = NormalizeDouble(self.E - ((self.D - self.E) * 1.618), Digits())
            self.pM1 = NormalizeDouble(self.E + ((self.D - self.E) * 1.618), Digits())
        elif _sw2 == M16:
            self.pEv1 = NormalizeDouble(self.A - ((self.B - self.A) * 0.618), Digits())
            self.pM1 = NormalizeDouble(self.E + ((self.D - self.E) * 1.618), Digits())
        elif _sw2 == W1:
            self.pEv1 = NormalizeDouble(self.E + ((self.A - self.B) * 1.618), Digits())
            self.pM1 = NormalizeDouble(self.E - ((self.C - self.D) * 0.618), Digits())
        elif _sw2 == W2:
            self.pEv1 = NormalizeDouble(self.E + ((self.E - self.D) * 1.618), Digits())
            self.pM1 = NormalizeDouble(self.E - ((self.E - self.D) * 1.618), Digits())
        elif _sw2 == W4:
            self.pEv1 = NormalizeDouble(self.E + ((self.B - self.A) * 0.618), Digits())
            self.pM1 = NormalizeDouble(self.E - ((self.B - self.A) * 0.618), Digits())
        elif _sw2 == W12:
            self.pEv1 = 0.0
            rA.v = self.B
            rB.v = self.D
            self.pM1 = NormalizeDouble(self.CalcRegress(self.iM, rA, self.iB, rB, self.iD), Digits())
        elif _sw2 == W14:
            self.pEv1 = 0.0
            self.pM1 = NormalizeDouble(self.E - ((self.C - self.B) * 1.618), Digits())
        elif _sw2 == W16:
            self.pEv1 = 0.0
            self.pM1 = NormalizeDouble(self.E - ((self.C - self.B) * 1.618), Digits())
        else:
            self.pEv1 = 0.0
            self.pM1 = 0.0
    def CalcRegress(self, nLast, a, nA, b, nB, c=0.0, nC=0):
        dA = Box(0.0)
        dB = Box(0.0)
        ret = -1.0
        ArDataX = Arr(0, 0.0)
        ArDataY = Arr(0, 0.0)
        if nC > 0:
            ArrayResize(ArDataX, 3)
            ArrayResize(ArDataY, 3)
        else:
            ArrayResize(ArDataX, 2)
            ArrayResize(ArDataY, 2)
        ArDataX[0] = nA
        ArDataY[0] = a.v
        ArDataX[1] = nB
        ArDataY[1] = b.v
        if nC > 0:
            ArDataX[2] = nC
            ArDataY[2] = c
        self.MyCRegressia(ArDataX, ArDataY, dA, dB)
        ret = (dB.v * nLast) + dA.v
        a.v = dA.v
        b.v = dB.v
        return ret
    def MyCRegressia(self, fMassX, fMassY, fB0, fB1):
        i = 0
        a = 0.0
        b = 0.0
        c = 0.0
        d = 0.0
        i = 0
        for i in range(i, ArrayRange(fMassX, 0)):
            a += fMassX[i]
            b += fMassY[i]
            c += MathPow(fMassX[i], 2)
            d += fMassX[i] * fMassY[i]
        else:
            i = _range_end(i, ArrayRange(fMassX, 0), 1)
        fB1.v = _fdiv((a * b) - (i * d), MathPow(a, 2) - (i * c))
        fB0.v = _fdiv(b - (fB1.v * a), i)

class CList(CObject):
    _q_fields = ('m_first_node', 'm_last_node', 'm_curr_node', 'm_curr_idx', 'm_data_total', 'm_free_mode', 'm_data_sort', 'm_sort_mode')
    _q_ptrs = ('m_first_node', 'm_last_node', 'm_curr_node',)
    def __init__(self):
        CObject.__init__(self)
        self.m_first_node = None
        self.m_last_node = None
        self.m_curr_node = None
        self.m_curr_idx = 0
        self.m_data_total = 0
        self.m_free_mode = False
        self.m_data_sort = False
        self.m_sort_mode = 0
        self.m_first_node = None
        self.m_last_node = None
        self.m_curr_node = None
        self.m_curr_idx = -1
        self.m_data_total = 0
        self.m_free_mode = True
        self.m_data_sort = False
        self.m_sort_mode = 0
    def _q_dtor(self):
        self.Clear()
    def FreeMode_0(self):
        return self.m_free_mode
    def FreeMode_1(self, mode):
        self.m_free_mode = mode
    def Total(self):
        return self.m_data_total
    def IsSorted(self):
        return self.m_data_sort
    def SortMode(self):
        return self.m_sort_mode
    def Type(self):
        return 0x7779
    def Save(self, file_handle):
        node = None
        result = True
        if (not CheckPointer(self.m_curr_node)) or file_handle == INVALID_HANDLE:
            return False
        if _missing('FileWriteLong')(file_handle, -1) != 8:
            return False
        if FileWriteInteger(file_handle, self.Type(), INT_VALUE) != INT_VALUE:
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        node = self.m_first_node
        while node is not None:
            result &= node.Save(file_handle)
            node = node.Next_0()
        return result
    def Load(self, file_handle):
        i = 0
        num = 0
        node = None
        result = True
        if file_handle == INVALID_HANDLE:
            return False
        if _missing('FileReadLong')(file_handle) != -1:
            return False
        if FileReadInteger(file_handle, INT_VALUE) != self.Type():
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        self.Clear()
        i = 0
        for i in range(i, num):
            node = self.CreateElement()
            if node is None:
                return False
            self.Add(node)
            result &= node.Load(file_handle)
        else:
            i = _range_end(i, num, 1)
        return result
    def CreateElement(self):
        return None
    def Add(self, new_node):
        if not CheckPointer(new_node):
            return -1
        if self.m_first_node is None:
            self.m_first_node = new_node
        else:
            self.m_last_node.Next_1(new_node)
            new_node.Prev_1(self.m_last_node)
        self.m_curr_node = new_node
        self.m_curr_idx = self.m_data_total
        self.m_last_node = new_node
        self.m_data_sort = False
        return _incattr(self, 'm_data_total', 1, True)
    def Insert(self, new_node, index):
        tmp_node = None
        if not CheckPointer(new_node):
            return -1
        if index > self.m_data_total or index < 0:
            return -1
        if index == -1:
            if self.m_curr_node is None:
                return self.Add(new_node)
        else:
            if self.GetNodeAtIndex(index) is None:
                return self.Add(new_node)
        tmp_node = self.m_curr_node.Prev_0()
        new_node.Prev_1(tmp_node)
        if tmp_node is not None:
            tmp_node.Next_1(new_node)
        else:
            self.m_first_node = new_node
        new_node.Next_1(self.m_curr_node)
        self.m_curr_node.Prev_1(new_node)
        self.m_data_total += 1
        self.m_data_sort = False
        self.m_curr_node = new_node
        return index
    def IndexOf(self, node):
        if (not CheckPointer(node)) or (not CheckPointer(self.m_curr_node)):
            return -1
        if node == self.m_curr_node:
            return self.m_curr_idx
        if self.GetFirstNode() == node:
            return 0
        i = 1
        while i < self.m_data_total:
            if self.GetNextNode() == node:
                return i
            i += 1
        return -1
    def GetNodeAtIndex(self, index):
        i = 0
        revers = False
        result = None
        if index >= self.m_data_total:
            return None
        if index == self.m_curr_idx:
            return self.m_curr_node
        if index < self.m_curr_idx:
            if (self.m_curr_idx - index) < index:
                i = self.m_curr_idx
                revers = True
                result = self.m_curr_node
            else:
                i = 0
                revers = False
                result = self.m_first_node
        else:
            if (index - self.m_curr_idx) < (self.m_data_total - index - 1):
                i = self.m_curr_idx
                revers = False
                result = self.m_curr_node
            else:
                i = self.m_data_total - 1
                revers = True
                result = self.m_last_node
        if not CheckPointer(result):
            return None
        if revers:
            while i > index:
                result = result.Prev_0()
                if result is None:
                    return None
                i -= 1
        else:
            while i < index:
                result = result.Next_0()
                if result is None:
                    return None
                i += 1
        self.m_curr_idx = index
        return _setattr(self, 'm_curr_node', result)
    def GetFirstNode(self):
        if not CheckPointer(self.m_first_node):
            return None
        self.m_curr_idx = 0
        return _setattr(self, 'm_curr_node', self.m_first_node)
    def GetPrevNode(self):
        if (not CheckPointer(self.m_curr_node)) or self.m_curr_node.Prev_0() is None:
            return None
        self.m_curr_idx -= 1
        return _setattr(self, 'm_curr_node', self.m_curr_node.Prev_0())
    def GetCurrentNode(self):
        return self.m_curr_node
    def GetNextNode(self):
        if (not CheckPointer(self.m_curr_node)) or self.m_curr_node.Next_0() is None:
            return None
        self.m_curr_idx += 1
        return _setattr(self, 'm_curr_node', self.m_curr_node.Next_0())
    def GetLastNode(self):
        if not CheckPointer(self.m_last_node):
            return None
        self.m_curr_idx = self.m_data_total - 1
        return _setattr(self, 'm_curr_node', self.m_last_node)
    def DetachCurrent(self):
        tmp_node = None
        result = None
        if not CheckPointer(self.m_curr_node):
            return result
        result = self.m_curr_node
        self.m_curr_node = None
        if (tmp_node := result.Next_0()) is not None:
            tmp_node.Prev_1(result.Prev_0())
            self.m_curr_node = tmp_node
        if (tmp_node := result.Prev_0()) is not None:
            tmp_node.Next_1(result.Next_0())
            if self.m_curr_node is None:
                self.m_curr_node = tmp_node
                self.m_curr_idx = self.m_data_total - 2
        self.m_data_total -= 1
        if self.m_first_node == result:
            self.m_first_node = result.Next_0()
        if self.m_last_node == result:
            self.m_last_node = result.Prev_0()
        result.Prev_1(None)
        result.Next_1(None)
        return result
    def DeleteCurrent(self):
        result = self.DetachCurrent()
        if result is None:
            return False
        if self.m_free_mode:
            if CheckPointer(result) == POINTER_DYNAMIC:
                _delete(result)
        return True
    def Delete(self, index):
        if self.GetNodeAtIndex(index) is None:
            return False
        return self.DeleteCurrent()
    def Clear(self):
        self.GetFirstNode()
        while self.m_data_total != 0:
            if not self.DeleteCurrent():
                break
    def CompareList(self, List):
        node = None
        lnode = None
        if not CheckPointer(List):
            return False
        if (node := self.GetFirstNode()) is None:
            return False
        if (lnode := List.GetFirstNode()) is None:
            return False
        if node.Compare(lnode) != 0:
            return False
        while (node := self.GetNextNode()) is not None:
            if (lnode := List.GetNextNode()) is None:
                return False
            if node.Compare(lnode) != 0:
                return False
        return True
    def Sort(self, mode):
        if self.m_data_total == 0:
            return
        if self.m_data_sort and self.m_sort_mode == mode:
            return
        self.QuickSort(0, self.m_data_total - 1, mode)
        self.m_sort_mode = mode
        self.m_data_sort = True
    def MoveToIndex(self, index):
        if index >= self.m_data_total or (not CheckPointer(self.m_curr_node)):
            return False
        if self.m_curr_idx == index:
            return True
        if self.m_curr_idx < index:
            index -= 1
        self.Insert(self.DetachCurrent(), index)
        return True
    def Exchange(self, node1, node2):
        tmp_node = None
        node = None
        if (not CheckPointer(node1)) or (not CheckPointer(node2)):
            return False
        tmp_node = node1.Prev_0()
        node1.Prev_1(node2.Prev_0())
        if node1.Prev_0() is not None:
            node = node1.Prev_0()
            node.Next_1(node1)
        else:
            self.m_first_node = node1
        node2.Prev_1(tmp_node)
        if node2.Prev_0() is not None:
            node = node2.Prev_0()
            node.Next_1(node2)
        else:
            self.m_first_node = node2
        tmp_node = node1.Next_0()
        node1.Next_1(node2.Next_0())
        if node1.Next_0() is not None:
            node = node1.Next_0()
            node.Prev_1(node1)
        else:
            self.m_last_node = node1
        node2.Next_1(tmp_node)
        if node2.Next_0() is not None:
            node = node2.Next_0()
            node.Prev_1(node2)
        else:
            self.m_last_node = node2
        self.m_curr_idx = 0
        self.m_curr_node = self.m_first_node
        self.m_data_sort = False
        return True
    def Search(self, element):
        result = None
        if (not CheckPointer(element)) or (not self.m_data_sort):
            return None
        result = self.QuickSearch(element)
        return result
    def QuickSort(self, beg, end, mode):
        i = 0
        j = 0
        k = 0
        i_ptr = None
        j_ptr = None
        k_ptr = None
        i_ptr = self.GetNodeAtIndex((i := beg))
        j_ptr = self.GetNodeAtIndex((j := end))
        while i < end:
            k_ptr = self.GetNodeAtIndex((k := (beg + end) >> 1))
            while i < j:
                while i_ptr.Compare(k_ptr, mode) < 0:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                    i_ptr = i_ptr.Next_0()
                while j_ptr.Compare(k_ptr, mode) > 0:
                    if j == 0:
                        break
                    j -= 1
                    j_ptr = j_ptr.Prev_0()
                if i <= j:
                    self.Exchange(i_ptr, j_ptr)
                    i += 1
                    i_ptr = self.GetNodeAtIndex(i)
                    if j == 0:
                        break
                    else:
                        j -= 1
                        j_ptr = self.GetNodeAtIndex(j)
            if beg < j:
                self.QuickSort(beg, j, mode)
            beg = i
            i_ptr = self.GetNodeAtIndex((i := beg))
            j_ptr = self.GetNodeAtIndex((j := end))
    def QuickSearch(self, element):
        i = 0
        j = 0
        m = 0
        t_node = None
        if self.m_data_total == 0:
            return None
        i = 0
        j = self.m_data_total
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_node = self.GetNodeAtIndex(m)
            if t_node.Compare(element, self.m_sort_mode) == 0:
                break
            if t_node.Compare(element, self.m_sort_mode) > 0:
                j = m - 1
            else:
                i = m + 1
            t_node = None
        return t_node

class MyCListArrow(MqlObject):
    _q_fields = ('ListArrow',)
    _q_ptrs = ('ListArrow',)
    def __init__(self):
        self.ListArrow = None
        self.ListArrow = CList()
        self.ListArrow.FreeMode_1(True)
    def _q_dtor(self):
        if self.ListArrow.Total() > 0:
            self.ListArrow.Clear()
        _delete(self.ListArrow)
    def Insert_0(self):
        NewArrow = None
        NewArrow = MyCArrow()
        self.ListArrow.Add(NewArrow)
    def Insert_2(self, Price, Times):
        NewArrow = None
        NewArrow = MyCArrow(Price, Times)
        self.ListArrow.Add(NewArrow)
    def Insert_3(self, Price, Times, Type):
        NewArrow = None
        NewArrow = MyCArrow(Price, Times, Type)
        self.ListArrow.Add(NewArrow)
    def Insert_5(self, Name, Tip, Price, Times, Type):
        NewArrow = None
        if self.ListArrow.Total() > 0:
            if self.FindName(Name):
                return False
        NewArrow = MyCArrow(Name, Tip, Price, Times, Type)
        self.ListArrow.Add(NewArrow)
        return True
    def SetAtIndexName(self, ind, NewName):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetName(NewName)
        return False
    def SetAtNameOfName(self, Name, NewName):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexName(ind, NewName)
        return False
    def SetAtIndexTip(self, ind, NewTip):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetTip(NewTip)
        return False
    def SetAtNameOfTip(self, Name, NewTip):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexTip(ind, NewTip)
        return False
    def SetAtIndexPrice(self, ind, NewPrice):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetPrice(NewPrice)
        return False
    def SetAtNameOfPrice(self, Name, NewPrice):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexPrice(ind, NewPrice)
        return False
    def SetAtIndexTime(self, ind, NewTime):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetTime(NewTime)
        return False
    def SetAtNameOfTime(self, Name, NewTime):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexTime(ind, NewTime)
        return False
    def SetAtIndexType(self, ind, NewType):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetType(NewType)
        return False
    def SetAtNameOfType(self, Name, NewType):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexType(ind, NewType)
        return False
    def SetAtIndexCode(self, ind, NewCode):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetCode(NewCode)
        return False
    def SetAtNameOfCode(self, Name, NewCode):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexCode(ind, NewCode)
        return False
    def SetAtIndexColor(self, ind, NewColor):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetColor(NewColor)
        return False
    def SetAtNameOfColor(self, Name, NewColor):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexColor(ind, NewColor)
        return False
    def SetAtIndexAnchor(self, ind, ArrowAnchor):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.SetAnchor(ArrowAnchor)
        return False
    def SetAtNameOfAnchor(self, Name, ArrowAnchor):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexAnchor(ind, ArrowAnchor)
        return False
    def GetSize(self):
        return self.ListArrow.Total()
    def GetLastArrowName(self):
        NewArrow = None
        if self.ListArrow.Total() > 0:
            NewArrow = self.ListArrow.GetLastNode()
            return NewArrow.GetName()
        return ""
    def GetAtIndexName(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetName()
        return ""
    def GetAtNameOfIndex(self, Name):
        return self.iFindName(Name)
    def GetAtIndexTip(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetTip()
        return ""
    def GetAtNameOfTip(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexTip(ind)
        return ""
    def GetAtIndexPrice(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetPrice()
        return -1.0
    def GetAtNameOfPrice(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexPrice(ind)
        return -1.0
    def GetAtIndexTime(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetTime()
        return 0
    def GetAtNameOfTime(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexTime(ind)
        return 0
    def GetAtIndexType(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetType()
        return 0
    def GetAtNameOfType(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexType(ind)
        return 0
    def GetAtIndexCode(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetCode()
        return -1
    def GetAtNameOfCode(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexCode(ind)
        return -1
    def GetAtIndexColor(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetColor()
        return 0
    def GetAtNameOfColor(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexColor(ind)
        return 0
    def GetAtIndexAnchor(self, ind):
        NewArrow = None
        if self.ListArrow.Total() > ind:
            NewArrow = self.ListArrow.GetNodeAtIndex(ind)
            return NewArrow.GetAnchor()
        return 0
    def GetAtNameOfAnchor(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexAnchor(ind)
        return 0
    def ClearAll(self):
        if self.ListArrow.Total() > 0:
            self.ListArrow.Clear()
    def DeletAtIndex(self, ind):
        if self.ListArrow.Total() > ind:
            return self.ListArrow.Delete(ind)
        return False
    def DeletAtName(self, Name):
        if self.ListArrow.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.DeletAtIndex(ind)
        return False
    def FindName(self, Name):
        ind = 0
        NewArrow = None
        if self.ListArrow.Total() > 0:
            while ind < self.ListArrow.Total():
                NewArrow = self.ListArrow.GetNodeAtIndex(ind)
                if Name == NewArrow.GetName():
                    return True
                ind += 1
        return False
    def iFindName(self, Name):
        ind = 0
        ret = -1
        NewArrow = None
        if self.ListArrow.Total() > 0:
            while ind < self.ListArrow.Total():
                NewArrow = self.ListArrow.GetNodeAtIndex(ind)
                if Name == NewArrow.GetName():
                    ret = ind
                    break
                ind += 1
        return ret

class MyCListTrendLine(MqlObject):
    _q_fields = ('ListTrendLine',)
    _q_ptrs = ('ListTrendLine',)
    def __init__(self):
        self.ListTrendLine = None
        self.ListTrendLine = CList()
        self.ListTrendLine.FreeMode_1(True)
    def _q_dtor(self):
        if self.ListTrendLine.Total() > 0:
            self.ListTrendLine.Clear()
        _delete(self.ListTrendLine)
    def Insert_0(self):
        NewTrend = None
        NewTrend = MyCTrendLine()
        self.ListTrendLine.Add(NewTrend)
    def Insert_4(self, Price1, Time1, Price2, Time2):
        NewTrend = None
        NewTrend = MyCTrendLine(Price1, Time1, Price2, Time2)
        self.ListTrendLine.Add(NewTrend)
    def Insert_5(self, Price1, Time1, Price2, Time2, Style):
        NewTrend = None
        NewTrend = MyCTrendLine(Price1, Time1, Price2, Time2, Style)
        self.ListTrendLine.Add(NewTrend)
    def Insert_6(self, Name, Price1, Time1, Price2, Time2, Style):
        NewTrend = None
        if self.ListTrendLine.Total() > 0:
            if self.FindName(Name):
                return False
        NewTrend = MyCTrendLine(Name, Price1, Time1, Price2, Time2, Style)
        self.ListTrendLine.Add(NewTrend)
        return True
    def SetAtIndexName(self, ind, NewName):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetName(NewName)
        return False
    def SetAtNameOfName(self, Name, NewName):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexName(ind, NewName)
        return False
    def SetAtIndexPrice1(self, ind, NewPrice):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetPrice1(NewPrice)
        return False
    def SetAtIndexPrice2(self, ind, NewPrice):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetPrice2(NewPrice)
        return False
    def SetAtNameOfPrice1(self, Name, NewPrice):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexPrice1(ind, NewPrice)
        return False
    def SetAtNameOfPrice2(self, Name, NewPrice):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexPrice2(ind, NewPrice)
        return False
    def SetAtIndexTime1(self, ind, NewTime):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetTime1(NewTime)
        return False
    def SetAtIndexTime2(self, ind, NewTime):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetTime2(NewTime)
        return False
    def SetAtNameOfTime1(self, Name, NewTime):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexTime1(ind, NewTime)
        return False
    def SetAtNameOfTime2(self, Name, NewTime):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexTime2(ind, NewTime)
        return False
    def SetAtIndexColor(self, ind, NewColor):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetColor(NewColor)
        return False
    def SetAtNameOfColor(self, Name, NewColor):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexColor(ind, NewColor)
        return False
    def SetAtIndexStyle(self, ind, style):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetStyle(style)
        return False
    def SetAtNameOfStyle(self, Name, style):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexStyle(ind, style)
        return False
    def SetAtIndexWidth(self, ind, width):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetWidth(width)
        return False
    def SetAtNameOfWidth(self, Name, width):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexWidth(ind, width)
        return False
    def SetAtIndexBack(self, ind, back):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetBack(back)
        return False
    def SetAtNameOfBack(self, Name, back):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexBack(ind, back)
        return False
    def SetAtIndexRayLeft(self, ind, left):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetRayLeft(left)
        return False
    def SetAtNameOfRayLeft(self, Name, left):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexRayLeft(ind, left)
        return False
    def SetAtIndexRayRight(self, ind, right):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetRayRight(right)
        return False
    def SetAtNameOfRayRight(self, Name, rigth):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexRayRight(ind, rigth)
        return False
    def SetAtIndexHidden(self, ind, hidden):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.SetHidden(hidden)
        return False
    def SetAtNameOfHidden(self, Name, hidden):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexHidden(ind, hidden)
        return False
    def GetSize(self):
        return self.ListTrendLine.Total()
    def GetAtIndexName(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetName()
        return ""
    def GetLastTrendName(self):
        NewTrend = None
        if self.ListTrendLine.Total() > 0:
            NewTrend = self.ListTrendLine.GetLastNode()
            return NewTrend.GetName()
        return ""
    def GetLastName(self):
        return self.GetLastTrendName()
    def GetAtNameOfIndex(self, Name):
        return self.iFindName(Name)
    def GetAtIndexPrice1(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetPrice1()
        return -1.0
    def GetAtIndexPrice2(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetPrice2()
        return -1.0
    def GetAtNameOfPrice1(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexPrice1(ind)
        return -1.0
    def GetAtNameOfPrice2(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexPrice2(ind)
        return -1.0
    def GetAtIndexTime1(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetTime1()
        return 0
    def GetAtIndexTime2(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetTime2()
        return 0
    def GetAtNameOfTime1(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexTime1(ind)
        return 0
    def GetAtNameOfTime2(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexTime2(ind)
        return 0
    def GetAtIndexColor(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetColor()
        return 0
    def GetAtNameOfColor(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexColor(ind)
        return 0
    def GetAtIndexStyle(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetStyle()
        return 0
    def GetAtNameOfStyle(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexStyle(ind)
        return 0
    def GetAtIndexWidth(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetWidth()
        return -1
    def GetAtNameOfWidth(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexWidth(ind)
        return -1
    def GetAtIndexBack(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetBack()
        return False
    def GetAtNameOfBack(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexBack(ind)
        return False
    def GetAtIndexRayLeft(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetRayLeft()
        return False
    def GetAtNameOfRayLeft(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexRayLeft(ind)
        return False
    def GetAtIndexRayRight(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetRayRight()
        return False
    def GetAtNameOfRayRight(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexRayRight(ind)
        return False
    def GetAtIndexHidden(self, ind):
        NewTrend = None
        if self.ListTrendLine.Total() > ind:
            NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
            return NewTrend.GetHidden()
        return False
    def GetAtNameOfHidden(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexHidden(ind)
        return False
    def ClearAll(self):
        if self.ListTrendLine.Total() > 0:
            self.ListTrendLine.Clear()
    def DeletAtIndex(self, ind):
        if self.ListTrendLine.Total() > ind:
            return self.ListTrendLine.Delete(ind)
        return False
    def DeletAtName(self, Name):
        if self.ListTrendLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.DeletAtIndex(ind)
        return False
    def FindName(self, Name):
        ind = 0
        NewTrend = None
        if self.ListTrendLine.Total() > 0:
            while ind < self.ListTrendLine.Total():
                NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
                if Name == NewTrend.GetName():
                    return True
                ind += 1
        return False
    def iFindName(self, Name):
        ind = 0
        ret = -1
        NewTrend = None
        if self.ListTrendLine.Total() > 0:
            while ind < self.ListTrendLine.Total():
                NewTrend = self.ListTrendLine.GetNodeAtIndex(ind)
                if Name == NewTrend.GetName():
                    ret = ind
                    break
                ind += 1
        return ret

class MyCListHLine(MqlObject):
    _q_fields = ('ListHLine',)
    _q_ptrs = ('ListHLine',)
    def __init__(self):
        self.ListHLine = None
        self.ListHLine = CList()
        self.ListHLine.FreeMode_1(True)
    def _q_dtor(self):
        if self.ListHLine.Total() > 0:
            self.ListHLine.Clear()
        _delete(self.ListHLine)
    def Insert_0(self):
        NewHLine = None
        NewHLine = MyCHLine()
        self.ListHLine.Add(NewHLine)
    def Insert_1(self, Price):
        NewHLine = None
        NewHLine = MyCHLine(Price)
        self.ListHLine.Add(NewHLine)
    def Insert_2(self, Price, Style):
        NewHLine = None
        NewHLine = MyCHLine(Price, Style)
        self.ListHLine.Add(NewHLine)
    def Insert_3(self, Name, Price, Style):
        NewHLine = None
        if self.ListHLine.Total() > 0:
            if self.FindName(Name):
                return False
        NewHLine = MyCHLine(Name, Price, Style)
        self.ListHLine.Add(NewHLine)
        return True
    def SetAtIndexName(self, ind, NewName):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.SetName(NewName)
        return False
    def SetAtNameOfName(self, Name, NewName):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexName(ind, NewName)
        return False
    def SetAtIndexPrice(self, ind, NewPrice):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.SetPrice(NewPrice)
        return False
    def SetAtNameOfPrice(self, Name, NewPrice):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexPrice(ind, NewPrice)
        return False
    def SetAtIndexColor(self, ind, NewColor):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.SetColor(NewColor)
        return False
    def SetAtNameOfColor(self, Name, NewColor):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexColor(ind, NewColor)
        return False
    def SetAtIndexStyle(self, ind, style):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.SetStyle(style)
        return False
    def SetAtNameOfStyle(self, Name, style):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexStyle(ind, style)
        return False
    def SetAtIndexWidth(self, ind, width):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.SetWidth(width)
        return False
    def SetAtNameOfWidth(self, Name, width):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexWidth(ind, width)
        return False
    def SetAtIndexBack(self, ind, back):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.SetBack(back)
        return False
    def SetAtNameOfBack(self, Name, back):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexBack(ind, back)
        return False
    def SetAtIndexHidden(self, ind, hidden):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.SetHidden(hidden)
        return False
    def SetAtNameOfHidden(self, Name, hidden):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.SetAtIndexHidden(ind, hidden)
        return False
    def GetSize(self):
        return self.ListHLine.Total()
    def GetAtIndexName(self, ind):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.GetName()
        return ""
    def GetLastHLineName(self):
        NewHLine = None
        if self.ListHLine.Total() > 0:
            NewHLine = self.ListHLine.GetLastNode()
            return NewHLine.GetName()
        return ""
    def GetLastName(self):
        return self.GetLastHLineName()
    def GetAtNameOfIndex(self, Name):
        return self.iFindName(Name)
    def GetAtIndexPrice(self, ind):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.GetPrice()
        return -1.0
    def GetAtNameOfPrice(self, Name):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexPrice(ind)
        return -1.0
    def GetAtIndexColor(self, ind):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.GetColor()
        return 0
    def GetAtNameOfColor(self, Name):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexColor(ind)
        return 0
    def GetAtIndexStyle(self, ind):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.GetStyle()
        return 0
    def GetAtNameOfStyle(self, Name):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexStyle(ind)
        return 0
    def GetAtIndexWidth(self, ind):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.GetWidth()
        return -1
    def GetAtNameOfWidth(self, Name):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexWidth(ind)
        return -1
    def GetAtIndexBack(self, ind):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.GetBack()
        return False
    def GetAtNameOfBack(self, Name):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexBack(ind)
        return False
    def GetAtIndexHidden(self, ind):
        NewHLine = None
        if self.ListHLine.Total() > ind:
            NewHLine = self.ListHLine.GetNodeAtIndex(ind)
            return NewHLine.GetHidden()
        return False
    def GetAtNameOfHidden(self, Name):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.GetAtIndexHidden(ind)
        return False
    def ClearAll(self):
        if self.ListHLine.Total() > 0:
            self.ListHLine.Clear()
    def DeletAtIndex(self, ind):
        if self.ListHLine.Total() > ind:
            return self.ListHLine.Delete(ind)
        return False
    def DeletAtName(self, Name):
        if self.ListHLine.Total() > 0:
            ind = self.iFindName(Name)
            if ind > -1:
                return self.DeletAtIndex(ind)
        return False
    def FindName(self, Name):
        ind = 0
        NewHLine = None
        if self.ListHLine.Total() > 0:
            while ind < self.ListHLine.Total():
                NewHLine = self.ListHLine.GetNodeAtIndex(ind)
                if Name == NewHLine.GetName():
                    return True
                ind += 1
        return False
    def iFindName(self, Name):
        ind = 0
        ret = -1
        NewHLine = None
        if self.ListHLine.Total() > 0:
            while ind < self.ListHLine.Total():
                NewHLine = self.ListHLine.GetNodeAtIndex(ind)
                if Name == NewHLine.GetName():
                    ret = ind
                    break
                ind += 1
        return ret

class MyCListPattern(MqlObject):
    _q_fields = ('ColorArrow', 'ColorTrend', 'StyleTrend', 'WidthTrend', 'BackTrend', 'StyleHLine', 'ColorUpHLine', 'ColorDownHLine', 'WidthHLine', 'BackHLine', 'ListArrow', 'ListTrend', 'ListHLine')
    _q_ptrs = ('ListArrow', 'ListTrend', 'ListHLine',)
    def __init__(self):
        self.ColorArrow = 0
        self.ColorTrend = 0
        self.StyleTrend = 0
        self.WidthTrend = 0
        self.BackTrend = False
        self.StyleHLine = 0
        self.ColorUpHLine = 0
        self.ColorDownHLine = 0
        self.WidthHLine = 0
        self.BackHLine = False
        self.ListArrow = None
        self.ListTrend = None
        self.ListHLine = None
        self.ListArrow = MyCListArrow()
        self.ListTrend = MyCListTrendLine()
        self.ListHLine = MyCListHLine()
        self.ColorArrow = clrBlue
        self.ColorTrend = clrGold
        self.StyleTrend = STYLE_SOLID
        self.WidthTrend = 1
        self.BackTrend = True
        self.StyleHLine = STYLE_SOLID
        self.ColorUpHLine = clrBlue
        self.ColorDownHLine = clrRed
        self.WidthHLine = 1
        self.BackHLine = True
    def _q_dtor(self):
        _delete(self.ListArrow)
        _delete(self.ListTrend)
        _delete(self.ListHLine)
    def Insert(self, A, tA, B, tB, C, tC, D, tD, E, tE, Ev, tEv, M, tM):
        if (((A < 0 or B < 0) or C < 0) or D < 0) or E < 0:
            return
        if self.ListArrow.GetSize() > 0:
            self.ListArrow.ClearAll()
        if self.ListTrend.GetSize() > 0:
            self.ListTrend.ClearAll()
        if self.ListHLine.GetSize() > 0:
            self.ListHLine.ClearAll()
        self.ListArrow.Insert_2(self.CorrectArrowChart(-6, tA, A), tA)
        self.ListArrow.SetAtNameOfCode(self.ListArrow.GetLastArrowName(), 140)
        self.ListArrow.SetAtNameOfColor(self.ListArrow.GetLastArrowName(), self.ColorArrow)
        self.ListArrow.SetAtNameOfTip(self.ListArrow.GetLastArrowName(), 'point A')
        self.ListArrow.Insert_2(self.CorrectArrowChart(-6, tB, B), tB)
        self.ListArrow.SetAtNameOfCode(self.ListArrow.GetLastArrowName(), 141)
        self.ListArrow.SetAtNameOfColor(self.ListArrow.GetLastArrowName(), self.ColorArrow)
        self.ListArrow.SetAtNameOfTip(self.ListArrow.GetLastArrowName(), 'point B')
        self.ListArrow.Insert_2(self.CorrectArrowChart(-6, tC, C), tC)
        self.ListArrow.SetAtNameOfCode(self.ListArrow.GetLastArrowName(), 142)
        self.ListArrow.SetAtNameOfColor(self.ListArrow.GetLastArrowName(), self.ColorArrow)
        self.ListArrow.SetAtNameOfTip(self.ListArrow.GetLastArrowName(), 'point C')
        self.ListArrow.Insert_2(self.CorrectArrowChart(-6, tD, D), tD)
        self.ListArrow.SetAtNameOfCode(self.ListArrow.GetLastArrowName(), 143)
        self.ListArrow.SetAtNameOfColor(self.ListArrow.GetLastArrowName(), self.ColorArrow)
        self.ListArrow.SetAtNameOfTip(self.ListArrow.GetLastArrowName(), 'point D')
        self.ListArrow.Insert_2(self.CorrectArrowChart(-6, tE, E), tE)
        self.ListArrow.SetAtNameOfCode(self.ListArrow.GetLastArrowName(), 144)
        self.ListArrow.SetAtNameOfColor(self.ListArrow.GetLastArrowName(), self.ColorArrow)
        self.ListArrow.SetAtNameOfTip(self.ListArrow.GetLastArrowName(), 'point E')
        if Ev > 0:
            self.ListArrow.Insert_2(self.CorrectArrowChart(-6, tEv, Ev), tEv)
            self.ListArrow.SetAtNameOfCode(self.ListArrow.GetLastArrowName(), 108)
            self.ListArrow.SetAtNameOfColor(self.ListArrow.GetLastArrowName(), self.ColorArrow)
            self.ListArrow.SetAtNameOfTip(self.ListArrow.GetLastArrowName(), 'Evolution')
        if M > 0:
            self.ListArrow.Insert_2(self.CorrectArrowChart(-6, tM, M), tM)
            self.ListArrow.SetAtNameOfCode(self.ListArrow.GetLastArrowName(), 109)
            self.ListArrow.SetAtNameOfColor(self.ListArrow.GetLastArrowName(), self.ColorArrow)
            self.ListArrow.SetAtNameOfTip(self.ListArrow.GetLastArrowName(), 'Mutation')
        self.ListTrend.Insert_6('Line_A-B', A, tA, B, tB, self.StyleTrend)
        self.ListTrend.SetAtNameOfColor(self.ListTrend.GetLastTrendName(), self.ColorTrend)
        self.ListTrend.SetAtNameOfWidth(self.ListTrend.GetLastTrendName(), self.WidthTrend)
        self.ListTrend.SetAtNameOfBack(self.ListTrend.GetLastTrendName(), self.BackTrend)
        self.ListTrend.Insert_6('Line_B-C', B, tB, C, tC, self.StyleTrend)
        self.ListTrend.SetAtNameOfColor(self.ListTrend.GetLastTrendName(), self.ColorTrend)
        self.ListTrend.SetAtNameOfWidth(self.ListTrend.GetLastTrendName(), self.WidthTrend)
        self.ListTrend.SetAtNameOfBack(self.ListTrend.GetLastTrendName(), self.BackTrend)
        self.ListTrend.Insert_6('Line_C-D', C, tC, D, tD, self.StyleTrend)
        self.ListTrend.SetAtNameOfColor(self.ListTrend.GetLastTrendName(), self.ColorTrend)
        self.ListTrend.SetAtNameOfWidth(self.ListTrend.GetLastTrendName(), self.WidthTrend)
        self.ListTrend.SetAtNameOfBack(self.ListTrend.GetLastTrendName(), self.BackTrend)
        self.ListTrend.Insert_6('Line_D-E', D, tD, E, tE, self.StyleTrend)
        self.ListTrend.SetAtNameOfColor(self.ListTrend.GetLastTrendName(), self.ColorTrend)
        self.ListTrend.SetAtNameOfWidth(self.ListTrend.GetLastTrendName(), self.WidthTrend)
        self.ListTrend.SetAtNameOfBack(self.ListTrend.GetLastTrendName(), self.BackTrend)
        if Ev > 0:
            self.ListTrend.Insert_6('Line_Evolution', E, tE, Ev, tEv, STYLE_DOT)
            self.ListTrend.SetAtNameOfColor(self.ListTrend.GetLastTrendName(), self.ColorTrend)
            self.ListTrend.SetAtNameOfWidth(self.ListTrend.GetLastTrendName(), 1)
            self.ListTrend.SetAtNameOfBack(self.ListTrend.GetLastTrendName(), self.BackTrend)
        if M > 0:
            self.ListTrend.Insert_6('Line_Mutation', E, tE, M, tM, STYLE_DOT)
            self.ListTrend.SetAtNameOfColor(self.ListTrend.GetLastTrendName(), self.ColorTrend)
            self.ListTrend.SetAtNameOfWidth(self.ListTrend.GetLastTrendName(), 1)
            self.ListTrend.SetAtNameOfBack(self.ListTrend.GetLastTrendName(), self.BackTrend)
        if A > B:
            self.ListHLine.Insert_2(A, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorUpHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
        else:
            self.ListHLine.Insert_2(A, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorDownHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
        if B > C:
            self.ListHLine.Insert_2(B, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorUpHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
        else:
            self.ListHLine.Insert_2(B, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorDownHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
        if C > D:
            self.ListHLine.Insert_2(C, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorUpHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
        else:
            self.ListHLine.Insert_2(C, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorDownHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
        if D > E:
            self.ListHLine.Insert_2(D, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorUpHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
        else:
            self.ListHLine.Insert_2(D, self.StyleHLine)
            self.ListHLine.SetAtNameOfColor(self.ListHLine.GetLastHLineName(), self.ColorDownHLine)
            self.ListHLine.SetAtNameOfWidth(self.ListHLine.GetLastHLineName(), self.WidthHLine)
            self.ListHLine.SetAtNameOfBack(self.ListHLine.GetLastHLineName(), self.BackHLine)
    def GetColorArrow(self):
        return self.ColorArrow
    def GetColorTrend(self):
        return self.ColorTrend
    def GetStyleTrend(self):
        return self.StyleTrend
    def GetWidthTrend(self):
        return self.WidthTrend
    def GetBackTrend(self):
        return self.BackTrend
    def GetStyleHLine(self):
        return self.StyleHLine
    def GetColorUpHLine(self):
        return self.ColorUpHLine
    def GetColorDownHLine(self):
        return self.ColorDownHLine
    def GetWidthHLine(self):
        return self.WidthHLine
    def GetBackHLine(self):
        return self.BackHLine
    def SetColorArrow(self, New):
        self.ColorArrow = New
    def SetColorTrend(self, New):
        self.ColorTrend = New
    def SetStyleTrend(self, New):
        self.StyleTrend = New
    def SetWidthTrend(self, New):
        self.WidthTrend = New
    def SetBackTrend(self, New):
        self.BackTrend = New
    def SetStyleHLine(self, New):
        self.StyleHLine = New
    def SetColorUpHLine(self, New):
        self.ColorUpHLine = New
    def SetColorDownHLine(self, New):
        self.ColorDownHLine = New
    def SetWidthHLine(self, New):
        self.WidthHLine = New
    def SetBackHLine(self, New):
        self.BackHLine = New
    def CorrectArrowChart(self, nCorrectY, time, price):
        x = Box(0)
        y = Box(0)
        sub_window = Box(0)
        m_price = Box(price)
        m_time = Box(time)
        if ChartTimePriceToXY(0, sub_window.v, m_time.v, m_price.v, x, y):
            if ChartXYToTimePrice(0, x.v, y.v + nCorrectY, sub_window, m_time, m_price):
                return m_price.v
        return price

def OnInit():
    global MyComment, MyListPattern, MyPatternZigzag
    if not ChartShiftGet(0):
        ChartShiftSet(True, 0)
    SetIndexBuffer(0, ExtPointE, INDICATOR_DATA)
    SetIndexBuffer(1, ExtDeltaDE, INDICATOR_DATA)
    SetIndexBuffer(2, ExtEvolution, INDICATOR_DATA)
    SetIndexBuffer(3, ExtMutation, INDICATOR_DATA)
    SetIndexBuffer(4, ExtSumModel, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    MyPatternZigzag = MyCPatternZigzag()
    MyComment = MyCComment()
    MyListPattern = MyCListPattern()
    MyPatternZigzag.SetDepth(Depth)
    MyPatternZigzag.SetDeviation(Deviation)
    MyPatternZigzag.SetBackstep(Backstep)
    MyPatternZigzag.AddPointerCommet(MyComment)
    MyPatternZigzag.SetNumberLineComment(Line)
    MyPatternZigzag.SetSizeBuffers(HistSize)
    MyListPattern.SetColorArrow(ColorArrow)
    MyListPattern.SetColorTrend(ColorTrend)
    MyListPattern.SetStyleTrend(StyleTrend)
    MyListPattern.SetWidthTrend(WidthTrend)
    MyListPattern.SetBackTrend(BackTrend)
    MyListPattern.SetStyleHLine(StyleHLine)
    MyListPattern.SetColorUpHLine(ColorUpHLine)
    MyListPattern.SetColorDownHLine(ColorDownHLine)
    MyListPattern.SetWidthHLine(WidthHLine)
    MyListPattern.SetBackHLine(BackHLine)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    _delete(MyPatternZigzag)
    _delete(MyListPattern)
    _delete(MyComment)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total > HistSize:
        nHowMush = rates_total - prev_calculated
        if nHowMush > 0:
            new_high = Arr(0, 0.0)
            new_low = Arr(0, 0.0)
            new_time = Arr(0, 0)
            ArrayResize(new_high, HistSize, 0)
            ArrayResize(new_low, HistSize, 0)
            ArrayResize(new_time, HistSize, 0)
            nStart = 0
            nCopy = 0
            if prev_calculated == 0:
                nStart = HistSize - 1
            else:
                nStart = prev_calculated - 1
            while nStart < rates_total:
                nCopy = 1 + nStart - HistSize
                ArrayCopy(new_low, low, 0, nCopy, HistSize)
                ArrayCopy(new_high, high, 0, nCopy, HistSize)
                ArrayCopy(new_time, time, 0, nCopy, HistSize)
                MyPatternZigzag.GetNamePattern(new_high, new_low, new_time)
                dwDE = MathAbs(MyPatternZigzag.GetE() - MyPatternZigzag.GetD())
                dwDE = _fdiv(dwDE, Point())
                ExtDeltaDE[nStart] = dwDE
                ExtPointE[nStart] = MyPatternZigzag.GetE()
                ExtEvolution[nStart] = MyPatternZigzag.GetPointEvolution()
                ExtMutation[nStart] = MyPatternZigzag.GetPointMutation()
                ExtSumModel[nStart] = MyPatternZigzag.GetSumModel()
                nStart += 1
            DrawPattern()
    else:
        return 0
    return rates_total

def DrawPattern():
    MyPatternZigzag.PrintComment()
    MyListPattern.Insert(MyPatternZigzag.GetA(), MyPatternZigzag.GetTimeA(), MyPatternZigzag.GetB(), MyPatternZigzag.GetTimeB(), MyPatternZigzag.GetC(), MyPatternZigzag.GetTimeC(), MyPatternZigzag.GetD(), MyPatternZigzag.GetTimeD(), MyPatternZigzag.GetE(), MyPatternZigzag.GetTimeE(), MyPatternZigzag.GetPointEvolution(), MyPatternZigzag.GetTimeEvolution(), MyPatternZigzag.GetPointMutation(), MyPatternZigzag.GetTimeMutation())

def ChartShiftGet(chart_ID=0):
    value = Box(0)
    ResetLastError()
    if not ChartGetInteger(chart_ID, CHART_SHIFT, 0, value):
        Print('ChartShiftGet' + ', Error Code = ', GetLastError())
        return False
    if value.v <= 0:
        return False
    return True

def ChartShiftSet(value, chart_ID=0):
    ResetLastError()
    if not ChartSetInteger(chart_ID, CHART_SHIFT, 0, value):
        Print('ChartShiftSet' + ', Error Code = ', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fivepattern(_MQL5Indicator):
    name = 'fivepattern'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Depth': 24,  # Zigzag: Ширина окна поиска(Depth)
        'Deviation': 12,  # Zigzag: Изменение цены в пуктах(Deviation)
        'Backstep': 9,  # Zigzag: Отсутп от начала данных(Backstep)
        'HistSize': 500,  # Zigzag: Размер истории для расчетов
        'WidthTrend': 2,  # Толщина паттерной линии
        'BackTrend': True,  # Задний план для паттерной линии
        'StyleTrend': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Стиль паттерной линии
        'WidthHLine': 2,  # Толщина линий уровня
        'BackHLine': True,  # Задний план для линий уровня
        'StyleHLine': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Стиль линий уровня
    }

