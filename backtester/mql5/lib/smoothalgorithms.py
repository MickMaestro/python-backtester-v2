"""SmoothAlgorithms.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})


class CMovSeriesTools(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def MALengthCheck_1(self, LengthName, ExternLength):
        if ExternLength < 1:
            word = Box("")
            StringConcatenate(word, 'CMovSeriesTools::MALengthCheck', ' (): Параметр ', LengthName, ' должен быть не менее 1. Вы ввели недопустимое ', ExternLength, ' будет использовано  1')
            Print(word.v)
            return
    def MALengthCheck_2(self, LengthName, ExternLength):
        if ExternLength < 1:
            word = Box("")
            StringConcatenate(word, 'CMovSeriesTools::MALengthCheck', ' (): Параметр ', LengthName, ' должен быть не менее 1. Вы ввели недопустимое ', ExternLength, ' будет использовано  1')
            Print(word.v)
            return
    def BarCheck1(self, begin, bar, Set):
        if ((not Set) and bar < begin) or (Set and bar > begin):
            return True
        return False
    def BarCheck2(self, begin, bar, Set, Length):
        if ((not Set) and bar == (begin + Length - 1)) or (Set and bar == (begin - Length + 1)):
            return True
        return False
    def BarCheck3(self, begin, bar, Set, Length):
        if ((not Set) and bar < (begin + Length - 1)) or (Set and bar > (begin - Length + 1)):
            return True
        return False
    def BarCheck4(self, rates_total, bar, Set):
        if ((not Set) and bar == (rates_total - 2)) or (Set and bar == 1):
            return True
        return False
    def BarCheck5(self, rates_total, bar, Set):
        if ((not Set) and bar == (rates_total - 1)) or (Set and bar == 0):
            return True
        return False
    def BarCheck6(self, rates_total, bar, Set):
        pass
    def LengthCheck_1(self, ExternLength):
        if ExternLength.v < 1:
            ExternLength.v = 1
    def LengthCheck_2(self, ExternLength):
        if ExternLength.v < 1:
            ExternLength.v = 1.0
    def Recount_ArrayZeroPos(self, count, Length, prev_calculated, rates_total, series, bar, Array, set_):
        if set_:
            if bar != (rates_total - prev_calculated):
                count.v -= 1
                if count.v < 0:
                    count.v = Length - 1
        else:
            if bar != (prev_calculated - 1):
                count.v -= 1
                if count.v < 0:
                    count.v = Length - 1
        Array[count.v] = series
    def Recount_ArrayNumber(self, count, Length, Number):
        ArrNumber = Number + count
        if ArrNumber > (Length - 1):
            ArrNumber -= Length
        return ArrNumber
    def SeriesArrayResize(self, FunctionsName, Length, Array, Size_):
        if Length > Size_.v:
            Size = Length + 1
            if ArrayResize(Array, Size) == -1:
                self.ArrayResizeErrorPrint(FunctionsName, Size_)
                return False
            Size_.v = Size
        return True
    def ArrayResizeErrorPrint(self, FunctionsName, Size_):
        lable = Box("")
        word = Box("")
        StringConcatenate(lable, FunctionsName, '():')
        StringConcatenate(word, lable.v, ' Ошибка!!! Не удалось изменить', ' размеры массива переменных функции ', FunctionsName, '()!')
        Print(word.v)
        error = GetLastError()
        ResetLastError()
        if error > 4000:
            StringConcatenate(word, lable.v, '(): Код ошибки ', error)
            Print(word.v)
        Size_.v = -2
        return False
        return True

class CMoving_Average(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count', 'm_weight', 'm_Moving', 'm_MOVING', 'm_Pr', 'm_sum', 'm_SUM', 'm_lsum', 'm_LSUM')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(0, 0.0)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_weight = 0
        self.m_Moving = 0.0
        self.m_MOVING = 0.0
        self.m_Pr = 0.0
        self.m_sum = 0.0
        self.m_SUM = 0.0
        self.m_lsum = 0.0
        self.m_LSUM = 0.0
    def MASeries(self, begin, prev_calculated, rates_total, Length, MA_Method, series, bar, set_):
        _sw1 = MA_Method
        if _sw1 == MODE_SMA:
            return self.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw1 == MODE_EMA:
            return self.EMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw1 == MODE_SMMA:
            return self.SMMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw1 == MODE_LWMA:
            return self.LWMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        else:
            if bar == begin:
                word = Box("")
                StringConcatenate(word, 'CMoving_Average::MASeries', '():', ' Параметр MA_Method должен быть от MODE_SMA до MODE_LWMA.', ' Вы ввели недопустимое ', MA_Method, ' будет использовано MODE_SMA!')
                Print(word.v)
            return self.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
    def SMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        iii = 0
        kkk = 0
        sma = 0.0
        self.LengthCheck_1(Length)
        if bar == begin and (not self.SeriesArrayResize('CMoving_Average::SMASeries', Length.v, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length.v, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck2(begin, bar, set_, Length.v):
            self.m_sum = 0.0
            iii = 1
            for iii in range(iii, Length.v):
                kkk = self.Recount_ArrayNumber(self.m_count, Length.v, iii)
                self.m_sum += self.m_SeriesArray[kkk]
            else:
                iii = _range_end(iii, Length.v, 1)
        elif self.BarCheck3(begin, bar, set_, Length.v):
            return EMPTY_VALUE
        self.m_sum += series
        sma = _fdiv(self.m_sum, Length.v)
        kkk = self.Recount_ArrayNumber(self.m_count, Length.v, Length.v - 1)
        self.m_sum -= self.m_SeriesArray[kkk]
        if self.BarCheck4(rates_total, bar, set_):
            self.m_SUM = self.m_sum
        if self.BarCheck5(rates_total, bar, set_):
            self.m_sum = self.m_SUM
        return sma
    def EMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        ema = 0.0
        self.LengthCheck_2(Length)
        if bar == begin:
            self.m_Pr = _fdiv(2.0, Length.v + 1.0)
            self.m_Moving = series
        self.m_Moving = (series * self.m_Pr) + (self.m_Moving * (1 - self.m_Pr))
        ema = self.m_Moving
        if self.BarCheck4(rates_total, bar, set_):
            self.m_MOVING = self.m_Moving
        if self.BarCheck5(rates_total, bar, set_):
            self.m_Moving = self.m_MOVING
        return ema
    def SMMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        iii = 0
        smma = 0.0
        self.LengthCheck_1(Length)
        if bar == begin and (not self.SeriesArrayResize('CMoving_Average::SMMASeries', Length.v, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length.v, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck2(begin, bar, set_, Length.v):
            self.m_sum = 0.0
            iii = 0
            for iii in range(iii, Length.v):
                self.m_sum += self.m_SeriesArray[iii]
            else:
                iii = _range_end(iii, Length.v, 1)
            self.m_Moving = _fdiv(self.m_sum - series, Length.v - 1)
        elif self.BarCheck3(begin, bar, set_, Length.v):
            return EMPTY_VALUE
        self.m_sum = (self.m_Moving * (Length.v - 1)) + series
        self.m_Moving = _fdiv(self.m_sum, Length.v)
        smma = self.m_Moving
        if self.BarCheck4(rates_total, bar, set_):
            self.m_SUM = self.m_sum
            self.m_MOVING = self.m_Moving
        if self.BarCheck5(rates_total, bar, set_):
            self.m_sum = self.m_SUM
            self.m_Moving = self.m_MOVING
        return smma
    def LWMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        lwma = 0.0
        iii = 0
        kkk = 0
        Length_ = Length.v + 1
        self.LengthCheck_1(Length)
        if bar == begin and (not self.SeriesArrayResize('CMoving_Average::LWMASeries', Length_, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck2(begin, bar, set_, Length_):
            self.m_sum = 0.0
            self.m_lsum = 0.0
            self.m_weight = 0
            rrr = Length.v
            iii = 1
            while iii <= Length.v:
                kkk = self.Recount_ArrayNumber(self.m_count, Length_, iii)
                self.m_sum += self.m_SeriesArray[kkk] * rrr
                self.m_lsum += self.m_SeriesArray[kkk]
                self.m_weight += iii
                iii += 1
                rrr -= 1
        elif self.BarCheck3(begin, bar, set_, Length_):
            return EMPTY_VALUE
        self.m_sum += (series * Length.v) - self.m_lsum
        kkk = self.Recount_ArrayNumber(self.m_count, Length_, Length.v)
        self.m_lsum += series - self.m_SeriesArray[kkk]
        lwma = _fdiv(self.m_sum, self.m_weight)
        if self.BarCheck4(rates_total, bar, set_):
            self.m_SUM = self.m_sum
            self.m_LSUM = self.m_lsum
        if self.BarCheck5(rates_total, bar, set_):
            self.m_sum = self.m_SUM
            self.m_lsum = self.m_LSUM
        return lwma

class CStdDeviation(CMovSeriesTools):
    _q_fields = ('m_Size_', 'm_count', 'm_Sum', 'm_SUM', 'm_Sum2', 'm_SUM2', 'm_SeriesArray')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_Sum = 0.0
        self.m_SUM = 0.0
        self.m_Sum2 = 0.0
        self.m_SUM2 = 0.0
        self.m_SeriesArray = Arr(0, 0.0)
    def StdDevSeries(self, begin, prev_calculated, rates_total, Length, deviation, series, MovSeries, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        iii = 0
        kkk = 0
        StdDev = 0.0
        m_SumX2 = 0.0
        if bar == begin and (not self.SeriesArrayResize('CStdDeviation::StdDevSeries', Length.v, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.LengthCheck_1(Length)
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length.v, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck2(begin, bar, set_, Length.v):
            self.m_Sum = 0.0
            self.m_Sum2 = 0.0
            iii = 1
            for iii in range(iii, Length.v):
                kkk = self.Recount_ArrayNumber(self.m_count, Length.v, iii)
                self.m_Sum += self.m_SeriesArray[kkk]
                self.m_Sum2 += MathPow(self.m_SeriesArray[kkk], 2)
            else:
                iii = _range_end(iii, Length.v, 1)
        elif self.BarCheck3(begin, bar, set_, Length.v):
            return EMPTY_VALUE
        self.m_Sum += series
        self.m_Sum2 += MathPow(series, 2)
        m_SumX2 = (Length.v * MathPow(MovSeries, 2)) - (2 * MovSeries * self.m_Sum) + self.m_Sum2
        kkk = self.Recount_ArrayNumber(self.m_count, Length.v, Length.v - 1)
        self.m_Sum2 -= MathPow(self.m_SeriesArray[kkk], 2)
        self.m_Sum -= self.m_SeriesArray[kkk]
        StdDev = deviation * MathSqrt(_fdiv(m_SumX2, Length.v))
        if self.BarCheck5(rates_total, bar, set_):
            self.m_Sum = self.m_SUM
            self.m_Sum2 = self.m_SUM2
        if self.BarCheck4(rates_total, bar, set_):
            self.m_SUM = self.m_Sum
            self.m_SUM2 = self.m_Sum2
        return StdDev

class CJJMA(CMovSeriesTools):
    _q_fields = ('m_start', 'm_array', 'm_degree', 'm_Phase', 'm_sense', 'm_Krx', 'm_Kfd', 'm_Krj', 'm_Kct', 'm_var1', 'm_var2', 'm_pos2', 'm_pos1', 'm_Loop1', 'm_Loop2', 'm_midd1', 'm_midd2', 'm_count1', 'm_count2', 'm_count3', 'm_ser1', 'm_ser2', 'm_Sum1', 'm_Sum2', 'm_JMA', 'm_storage1', 'm_storage2', 'm_djma', 'm_hoop1', 'm_hoop2', 'm_data', 'm_pos2_', 'm_pos1_', 'm_Loop1_', 'm_Loop2_', 'm_midd1_', 'm_midd2_', 'm_count1_', 'm_count2_', 'm_count3_', 'm_ser1_', 'm_ser2_', 'm_Sum1_', 'm_Sum2_', 'm_JMA_', 'm_storage1_', 'm_storage2_', 'm_djma_', 'm_hoop1_', 'm_hoop2_', 'm_data_', 'm_bhoop1', 'm_bhoop2', 'm_bdata')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_start = False
        self.m_array = Arr(62, 0.0, dyn=False)
        self.m_degree = 0.0
        self.m_Phase = 0.0
        self.m_sense = 0.0
        self.m_Krx = 0.0
        self.m_Kfd = 0.0
        self.m_Krj = 0.0
        self.m_Kct = 0.0
        self.m_var1 = 0.0
        self.m_var2 = 0.0
        self.m_pos2 = 0
        self.m_pos1 = 0
        self.m_Loop1 = 0
        self.m_Loop2 = 0
        self.m_midd1 = 0
        self.m_midd2 = 0
        self.m_count1 = 0
        self.m_count2 = 0
        self.m_count3 = 0
        self.m_ser1 = 0.0
        self.m_ser2 = 0.0
        self.m_Sum1 = 0.0
        self.m_Sum2 = 0.0
        self.m_JMA = 0.0
        self.m_storage1 = 0.0
        self.m_storage2 = 0.0
        self.m_djma = 0.0
        self.m_hoop1 = Arr(128, 0.0, dyn=False)
        self.m_hoop2 = Arr(11, 0.0, dyn=False)
        self.m_data = Arr(128, 0.0, dyn=False)
        self.m_pos2_ = 0
        self.m_pos1_ = 0
        self.m_Loop1_ = 0
        self.m_Loop2_ = 0
        self.m_midd1_ = 0
        self.m_midd2_ = 0
        self.m_count1_ = 0
        self.m_count2_ = 0
        self.m_count3_ = 0
        self.m_ser1_ = 0.0
        self.m_ser2_ = 0.0
        self.m_Sum1_ = 0.0
        self.m_Sum2_ = 0.0
        self.m_JMA_ = 0.0
        self.m_storage1_ = 0.0
        self.m_storage2_ = 0.0
        self.m_djma_ = 0.0
        self.m_hoop1_ = Arr(128, 0.0, dyn=False)
        self.m_hoop2_ = Arr(11, 0.0, dyn=False)
        self.m_data_ = Arr(128, 0.0, dyn=False)
        self.m_bhoop1 = Arr(128, False, dyn=False)
        self.m_bhoop2 = Arr(11, False, dyn=False)
        self.m_bdata = Arr(128, False, dyn=False)
    def JJMASeries(self, begin, prev_calculated, rates_total, Din, Phase, Length, series, bar, set_):
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        self.JJMAInit(begin, Din, Phase, Length, series, bar)
        posA = 0
        posB = 0
        back = 0
        shift2 = 0
        shift1 = 0
        numb = 0
        Res = 0.0
        ResPow = 0.0
        dser3 = 0.0
        dser4 = 0.0
        jjma = 0.0
        ratio = 0.0
        Extr = 0.0
        ser0 = 0.0
        resalt = 0.0
        newvel = 0.0
        dSupr = 0.0
        Pow1 = 0.0
        hoop1 = 0.0
        SmVel = 0.0
        Pow2 = 0.0
        Pow2x2 = 0.0
        Suprem1 = 0.0
        Suprem2 = 0.0
        dser1 = 0.0
        dser2 = 0.0
        extent = 0.0
        factor = 0.0
        if self.m_Loop1 < 61:
            self.m_Loop1 += 1
            self.m_array[self.m_Loop1] = series
        if self.m_Loop1 > 30:
            if not self.m_start:
                self.m_start = True
                shift1 = 1
                back = 29
                self.m_ser2 = self.m_array[1]
                self.m_ser1 = self.m_ser2
            else:
                back = 0
            for rrr in range(back, 0 - 1, -1):
                if rrr == 0:
                    ser0 = series
                else:
                    ser0 = self.m_array[31 - rrr]
                dser1 = ser0 - self.m_ser1
                dser2 = ser0 - self.m_ser2
                if MathAbs(dser1) > MathAbs(dser2):
                    self.m_var2 = MathAbs(dser1)
                else:
                    self.m_var2 = MathAbs(dser2)
                Res = self.m_var2
                newvel = Res + 1e-10
                if self.m_count1 <= 1:
                    self.m_count1 = 127
                else:
                    self.m_count1 -= 1
                if self.m_count2 <= 1:
                    self.m_count2 = 10
                else:
                    self.m_count2 -= 1
                if self.m_count3 < 128:
                    self.m_count3 += 1
                self.m_Sum1 += newvel - self.m_hoop2[self.m_count2]
                self.m_hoop2[self.m_count2] = newvel
                self.m_bhoop2[self.m_count2] = True
                if self.m_count3 > 10:
                    SmVel = self.m_Sum1 / 10.0
                else:
                    SmVel = _fdiv(self.m_Sum1, self.m_count3)
                if self.m_count3 > 127:
                    hoop1 = self.m_hoop1[self.m_count1]
                    self.m_hoop1[self.m_count1] = SmVel
                    self.m_bhoop1[self.m_count1] = True
                    numb = 64
                    posB = numb
                    while numb > 1:
                        if self.m_data[posB] < hoop1:
                            numb = _int(numb / 2.0)
                            posB += numb
                        elif self.m_data[posB] <= hoop1:
                            numb = 1
                        else:
                            numb = _int(numb / 2.0)
                            posB -= numb
                else:
                    self.m_hoop1[self.m_count1] = SmVel
                    self.m_bhoop1[self.m_count1] = True
                    if (self.m_midd1 + self.m_midd2) > 127:
                        self.m_midd2 -= 1
                        posB = self.m_midd2
                    else:
                        self.m_midd1 += 1
                        posB = self.m_midd1
                    if self.m_midd1 > 96:
                        self.m_pos2 = 96
                    else:
                        self.m_pos2 = self.m_midd1
                    if self.m_midd2 < 32:
                        self.m_pos1 = 32
                    else:
                        self.m_pos1 = self.m_midd2
                numb = 64
                posA = numb
                while numb > 1:
                    if self.m_data[posA] >= SmVel:
                        if self.m_data[posA - 1] <= SmVel:
                            numb = 1
                        else:
                            numb = _int(numb / 2.0)
                            posA -= numb
                    else:
                        numb = _int(numb / 2.0)
                        posA += numb
                    if posA == 127:
                        if SmVel > self.m_data[127]:
                            posA = 128
                if self.m_count3 > 127:
                    if posB >= posA:
                        if (self.m_pos2 + 1) > posA:
                            if (self.m_pos1 - 1) < posA:
                                self.m_Sum2 += SmVel
                            elif (self.m_pos1 + 0) > posA:
                                if (self.m_pos1 - 1) < posB:
                                    self.m_Sum2 += self.m_data[self.m_pos1 - 1]
                    elif self.m_pos1 >= posA:
                        if (self.m_pos2 + 1) < posA:
                            if (self.m_pos2 + 1) > posB:
                                self.m_Sum2 += self.m_data[self.m_pos2 + 1]
                    elif (self.m_pos2 + 2) > posA:
                        self.m_Sum2 += SmVel
                    elif (self.m_pos2 + 1) < posA:
                        if (self.m_pos2 + 1) > posB:
                            self.m_Sum2 += self.m_data[self.m_pos2 + 1]
                    if posB > posA:
                        if (self.m_pos1 - 1) < posB:
                            if (self.m_pos2 + 1) > posB:
                                self.m_Sum2 -= self.m_data[posB]
                            elif self.m_pos2 < posB:
                                if (self.m_pos2 + 1) > posA:
                                    self.m_Sum2 -= self.m_data[self.m_pos2]
                    else:
                        if (self.m_pos2 + 1) > posB and (self.m_pos1 - 1) < posB:
                            self.m_Sum2 -= self.m_data[posB]
                        elif (self.m_pos1 + 0) > posB:
                            if (self.m_pos1 - 0) < posA:
                                self.m_Sum2 -= self.m_data[self.m_pos1]
                if posB <= posA:
                    if posB == posA:
                        self.m_data[posA] = SmVel
                        self.m_bdata[posA] = True
                    else:
                        numb = posB + 1
                        for numb in range(numb, posA - 1 + 1):
                            self.m_data[numb - 1] = self.m_data[numb]
                            self.m_bdata[numb - 1] = True
                        else:
                            numb = _range_end(numb, posA - 1 + 1, 1)
                        self.m_data[posA - 1] = SmVel
                        self.m_bdata[posA - 1] = True
                else:
                    numb = posB - 1
                    for numb in range(numb, posA - 1, -1):
                        self.m_data[numb + 1] = self.m_data[numb]
                        self.m_bdata[numb + 1] = True
                    else:
                        numb = _range_end(numb, posA - 1, -1)
                    self.m_data[posA] = SmVel
                    self.m_bdata[posA] = True
                if self.m_count3 <= 127:
                    self.m_Sum2 = 0.0
                    numb = self.m_pos1
                    for numb in range(numb, self.m_pos2 + 1):
                        self.m_Sum2 += self.m_data[numb]
                    else:
                        numb = _range_end(numb, self.m_pos2 + 1, 1)
                resalt = _fdiv(self.m_Sum2, self.m_pos2 - self.m_pos1 + 1.0)
                if self.m_Loop2 > 30:
                    self.m_Loop2 = 31
                else:
                    self.m_Loop2 += 1
                if self.m_Loop2 <= 30:
                    if dser1 > 0.0:
                        self.m_ser1 = ser0
                    else:
                        self.m_ser1 = ser0 - (dser1 * self.m_Kct)
                    if dser2 < 0.0:
                        self.m_ser2 = ser0
                    else:
                        self.m_ser2 = ser0 - (dser2 * self.m_Kct)
                    self.m_JMA = series
                    if self.m_Loop2 != 30:
                        continue
                    else:
                        self.m_storage1 = series
                        if MathCeil(self.m_Krx) >= 1:
                            dSupr = MathCeil(self.m_Krx)
                        else:
                            dSupr = 1.0
                        if dSupr > 0:
                            Suprem2 = MathFloor(dSupr)
                        else:
                            if dSupr < 0:
                                Suprem2 = MathCeil(dSupr)
                            else:
                                Suprem2 = 0.0
                        if MathFloor(self.m_Krx) >= 1:
                            self.m_var2 = MathFloor(self.m_Krx)
                        else:
                            self.m_var2 = 1.0
                        if self.m_var2 > 0:
                            Suprem1 = MathFloor(self.m_var2)
                        else:
                            if self.m_var2 < 0:
                                Suprem1 = MathCeil(self.m_var2)
                            else:
                                Suprem1 = 0.0
                        if Suprem2 == Suprem1:
                            factor = 1.0
                        else:
                            dSupr = Suprem2 - Suprem1
                            factor = _fdiv(self.m_Krx - Suprem1, dSupr)
                        if Suprem1 <= 29:
                            shift1 = _int(Suprem1)
                        else:
                            shift1 = 29
                        if Suprem2 <= 29:
                            shift2 = _int(Suprem2)
                        else:
                            shift2 = 29
                        dser3 = series - self.m_array[self.m_Loop1 - shift1]
                        dser4 = series - self.m_array[self.m_Loop1 - shift2]
                        self.m_djma = _fdiv(dser3 * (1.0 - factor), Suprem1) + _fdiv(dser4 * factor, Suprem2)
                else:
                    if resalt:
                        ResPow = MathPow(_fdiv(Res, resalt), self.m_degree)
                    else:
                        ResPow = 0.0
                    if self.m_Kfd >= ResPow:
                        self.m_var1 = ResPow
                    else:
                        self.m_var1 = self.m_Kfd
                    if self.m_var1 < 1.0:
                        self.m_var2 = 1.0
                    else:
                        if self.m_Kfd >= ResPow:
                            self.m_sense = ResPow
                        else:
                            self.m_sense = self.m_Kfd
                        self.m_var2 = self.m_sense
                    extent = self.m_var2
                    Pow1 = MathPow(self.m_Kct, MathSqrt(extent))
                    if dser1 > 0.0:
                        self.m_ser1 = ser0
                    else:
                        self.m_ser1 = ser0 - (dser1 * Pow1)
                    if dser2 < 0.0:
                        self.m_ser2 = ser0
                    else:
                        self.m_ser2 = ser0 - (dser2 * Pow1)
            if self.m_Loop2 > 30:
                Pow2 = MathPow(self.m_Krj, extent)
                self.m_storage1 *= Pow2
                self.m_storage1 += (1.0 - Pow2) * series
                self.m_storage2 *= self.m_Krj
                self.m_storage2 += (series - self.m_storage1) * (1.0 - self.m_Krj)
                Extr = (self.m_Phase * self.m_storage2) + self.m_storage1
                Pow2x2 = Pow2 * Pow2
                ratio = Pow2x2 - (2.0 * Pow2) + 1.0
                self.m_djma *= Pow2x2
                self.m_djma += (Extr - self.m_JMA) * ratio
                self.m_JMA += self.m_djma
        if self.m_Loop1 <= 30:
            return EMPTY_VALUE
        jjma = self.m_JMA
        if self.BarCheck5(rates_total, bar, set_):
            numb = 0
            for numb in range(numb, 128):
                if self.m_bhoop1[numb]:
                    self.m_hoop1[numb] = self.m_hoop1_[numb]
            else:
                numb = _range_end(numb, 128, 1)
            numb = 0
            for numb in range(numb, 11):
                if self.m_bhoop2[numb]:
                    self.m_hoop2[numb] = self.m_hoop2_[numb]
            else:
                numb = _range_end(numb, 11, 1)
            numb = 0
            for numb in range(numb, 128):
                if self.m_bdata[numb]:
                    self.m_data[numb] = self.m_data_[numb]
            else:
                numb = _range_end(numb, 128, 1)
            ArrayInitialize(self.m_bhoop1, False)
            ArrayInitialize(self.m_bhoop2, False)
            ArrayInitialize(self.m_bdata, False)
            self.m_JMA = self.m_JMA_
            self.m_djma = self.m_djma_
            self.m_ser1 = self.m_ser1_
            self.m_ser2 = self.m_ser2_
            self.m_Sum2 = self.m_Sum2_
            self.m_pos1 = self.m_pos1_
            self.m_pos2 = self.m_pos2_
            self.m_Sum1 = self.m_Sum1_
            self.m_Loop1 = self.m_Loop1_
            self.m_Loop2 = self.m_Loop2_
            self.m_count1 = self.m_count1_
            self.m_count2 = self.m_count2_
            self.m_count3 = self.m_count3_
            self.m_storage1 = self.m_storage1_
            self.m_storage2 = self.m_storage2_
            self.m_midd1 = self.m_midd1_
            self.m_midd2 = self.m_midd2_
        if self.BarCheck4(rates_total, bar, set_):
            numb = 0
            for numb in range(numb, 128):
                if self.m_bhoop1[numb]:
                    self.m_hoop1_[numb] = self.m_hoop1[numb]
            else:
                numb = _range_end(numb, 128, 1)
            numb = 0
            for numb in range(numb, 11):
                if self.m_bhoop2[numb]:
                    self.m_hoop2_[numb] = self.m_hoop2[numb]
            else:
                numb = _range_end(numb, 11, 1)
            numb = 0
            for numb in range(numb, 128):
                if self.m_bdata[numb]:
                    self.m_data_[numb] = self.m_data[numb]
            else:
                numb = _range_end(numb, 128, 1)
            ArrayInitialize(self.m_bhoop1, False)
            ArrayInitialize(self.m_bhoop2, False)
            ArrayInitialize(self.m_bdata, False)
            self.m_JMA_ = self.m_JMA
            self.m_djma_ = self.m_djma
            self.m_Sum2_ = self.m_Sum2
            self.m_ser1_ = self.m_ser1
            self.m_ser2_ = self.m_ser2
            self.m_pos1_ = self.m_pos1
            self.m_pos2_ = self.m_pos2
            self.m_Sum1_ = self.m_Sum1
            self.m_Loop1_ = self.m_Loop1
            self.m_Loop2_ = self.m_Loop2
            self.m_count1_ = self.m_count1
            self.m_count2_ = self.m_count2
            self.m_count3_ = self.m_count3
            self.m_storage1_ = self.m_storage1
            self.m_storage2_ = self.m_storage2
            self.m_midd1_ = self.m_midd1
            self.m_midd2_ = self.m_midd2
        return jjma
    def JJMALengthCheck(self, LengthName, ExternLength):
        if ExternLength < 1:
            word = Box("")
            StringConcatenate(word, 'CJJMA::JJMALengthCheck', ' (): Параметр ', LengthName, ' должен быть не менее 1. Вы ввели недопустимое ', ExternLength, ' будет использовано  1')
            Print(word.v)
            return
    def JJMAPhaseCheck(self, PhaseName, ExternPhase):
        if ExternPhase < -100:
            word = Box("")
            StringConcatenate(word, 'CJJMA::JJMAPhaseCheck', ' (): Параметр ', PhaseName, ' должен быть не менее -100. Вы ввели недопустимое ', ExternPhase, ' будет использовано  -100')
            Print(word.v)
            return
        if ExternPhase > 100:
            word = Box("")
            StringConcatenate(word, 'CJJMA::JJMAPhaseCheck', ' (): Параметр ', PhaseName, ' должен быть не более +100. Вы ввели недопустимое ', ExternPhase, ' будет использовано  +100')
            Print(word.v)
            return
    def JJMAInit(self, begin, Din, Phase, Length, series, bar):
        if bar == begin or Din != 0:
            if bar == begin:
                self.m_midd1 = 63
                self.m_midd2 = 64
                self.m_start = False
                for numb in range(0, self.m_midd1 + 1):
                    self.m_data[numb] = -1000000.0
                for numb in range(self.m_midd2, 127 + 1):
                    self.m_data[numb] = 1000000.0
                ArrayInitialize(self.m_bhoop1, True)
                ArrayInitialize(self.m_bhoop2, True)
                ArrayInitialize(self.m_bdata, True)
                ArrayInitialize(self.m_hoop1_, 0.0)
                ArrayInitialize(self.m_hoop2_, 0.0)
                ArrayInitialize(self.m_hoop1, 0.0)
                ArrayInitialize(self.m_hoop2, 0.0)
                ArrayInitialize(self.m_array, 0.0)
                self.m_djma = 0.0
                self.m_Sum1 = 0.0
                self.m_Sum2 = 0.0
                self.m_ser1 = 0.0
                self.m_ser2 = 0.0
                self.m_pos1 = _int(0.0)
                self.m_pos2 = _int(0.0)
                self.m_Loop1 = _int(0.0)
                self.m_Loop2 = _int(0.0)
                self.m_count1 = _int(0.0)
                self.m_count2 = _int(0.0)
                self.m_count3 = _int(0.0)
                self.m_storage1 = 0.0
                self.m_storage2 = 0.0
                self.m_JMA = series
            if Phase >= -100 and Phase <= 100:
                self.m_Phase = (Phase / 100.0) + 1.5
            if Phase > 100:
                self.m_Phase = 2.5
            if Phase < -100:
                self.m_Phase = 0.5
            velA = 0.0
            velB = 0.0
            velC = 0.0
            velD = 0.0
            if Length >= 1.0000000002:
                velA = (Length - 1.0) / 2.0
            else:
                velA = 1e-10
            velA *= 0.9
            self.m_Krj = _fdiv(velA, velA + 2.0)
            velC = MathSqrt(velA)
            velD = MathLog(velC)
            self.m_var1 = velD
            self.m_var2 = self.m_var1
            velB = MathLog(2.0)
            self.m_sense = _fdiv(self.m_var2, velB) + 2.0
            if self.m_sense < 0.0:
                self.m_sense = 0.0
            self.m_Kfd = self.m_sense
            if self.m_Kfd >= 2.5:
                self.m_degree = self.m_Kfd - 2.0
            else:
                self.m_degree = 0.5
            self.m_Krx = velC * self.m_Kfd
            self.m_Kct = _fdiv(self.m_Krx, self.m_Krx + 1.0)

class CT3(CMovSeriesTools):
    _q_fields = ('m_b2', 'm_b3', 'm_e1', 'm_e2', 'm_e3', 'm_e4', 'm_e5', 'm_e6', 'm_E1', 'm_E2', 'm_E3', 'm_E4', 'm_E5', 'm_E6', 'm_c1', 'm_c2', 'm_c3', 'm_c4', 'm_w1', 'm_w2')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_b2 = 0.0
        self.m_b3 = 0.0
        self.m_e1 = 0.0
        self.m_e2 = 0.0
        self.m_e3 = 0.0
        self.m_e4 = 0.0
        self.m_e5 = 0.0
        self.m_e6 = 0.0
        self.m_E1 = 0.0
        self.m_E2 = 0.0
        self.m_E3 = 0.0
        self.m_E4 = 0.0
        self.m_E5 = 0.0
        self.m_E6 = 0.0
        self.m_c1 = 0.0
        self.m_c2 = 0.0
        self.m_c3 = 0.0
        self.m_c4 = 0.0
        self.m_w1 = 0.0
        self.m_w2 = 0.0
    def T3Series(self, begin, prev_calculated, rates_total, Din, Curvature, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        e0 = 0.0
        T3_ = 0.0
        self.LengthCheck_2(Length)
        self.T3Init(begin, Din, Curvature, Length.v, series, bar)
        e0 = series
        self.m_e1 = (self.m_w1 * e0) + (self.m_w2 * self.m_e1)
        self.m_e2 = (self.m_w1 * self.m_e1) + (self.m_w2 * self.m_e2)
        self.m_e3 = (self.m_w1 * self.m_e2) + (self.m_w2 * self.m_e3)
        self.m_e4 = (self.m_w1 * self.m_e3) + (self.m_w2 * self.m_e4)
        self.m_e5 = (self.m_w1 * self.m_e4) + (self.m_w2 * self.m_e5)
        self.m_e6 = (self.m_w1 * self.m_e5) + (self.m_w2 * self.m_e6)
        T3_ = (self.m_c1 * self.m_e6) + (self.m_c2 * self.m_e5) + (self.m_c3 * self.m_e4) + (self.m_c4 * self.m_e3)
        if self.BarCheck5(rates_total, bar, set_):
            self.m_e1 = self.m_E1
            self.m_e2 = self.m_E2
            self.m_e3 = self.m_E3
            self.m_e4 = self.m_E4
            self.m_e5 = self.m_E5
            self.m_e6 = self.m_E6
        if self.BarCheck4(rates_total, bar, set_):
            self.m_E1 = self.m_e1
            self.m_E2 = self.m_e2
            self.m_E3 = self.m_e3
            self.m_E4 = self.m_e4
            self.m_E5 = self.m_e5
            self.m_E6 = self.m_e6
        return T3_
    def T3Init(self, begin, Din, Curvature, Length, series, bar):
        if bar == begin or Din != 0:
            b = Curvature / 100.0
            self.m_b2 = b * b
            self.m_b3 = self.m_b2 * b
            self.m_c1 = -self.m_b3
            self.m_c2 = 3 * (self.m_b2 + self.m_b3)
            self.m_c3 = -3 * ((2 * self.m_b2) + b + self.m_b3)
            self.m_c4 = 1 + (3 * b) + self.m_b3 + (3 * self.m_b2)
            n = 1 + (0.5 * (Length - 1))
            self.m_w1 = _fdiv(2, n + 1)
            self.m_w2 = 1 - self.m_w1
            if bar == begin:
                self.m_e1 = series
                self.m_e2 = series
                self.m_e3 = series
                self.m_e4 = series
                self.m_e5 = series
                self.m_e6 = series

class CJurX(CMovSeriesTools):
    _q_fields = ('m_AB', 'm_AC', 'm_f1', 'm_f2', 'm_f3', 'm_f4', 'm_f5', 'm_f6', 'm_Kg', 'm_Hg', 'm_F1', 'm_F2', 'm_F3', 'm_F4', 'm_F5', 'm_F6', 'm_w')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_AB = 0.0
        self.m_AC = 0.0
        self.m_f1 = 0.0
        self.m_f2 = 0.0
        self.m_f3 = 0.0
        self.m_f4 = 0.0
        self.m_f5 = 0.0
        self.m_f6 = 0.0
        self.m_Kg = 0.0
        self.m_Hg = 0.0
        self.m_F1 = 0.0
        self.m_F2 = 0.0
        self.m_F3 = 0.0
        self.m_F4 = 0.0
        self.m_F5 = 0.0
        self.m_F6 = 0.0
        self.m_w = 0.0
    def JurXSeries(self, begin, prev_calculated, rates_total, Din, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        V1 = 0.0
        V2 = 0.0
        JurX_ = 0.0
        self.LengthCheck_2(Length)
        self.JurXInit(begin, Din, Length.v, series, bar)
        self.m_f1 = (self.m_Hg * self.m_f1) + (self.m_Kg * series)
        self.m_f2 = (self.m_Kg * self.m_f1) + (self.m_Hg * self.m_f2)
        V1 = (self.m_AC * self.m_f1) - (self.m_AB * self.m_f2)
        self.m_f3 = (self.m_Hg * self.m_f3) + (self.m_Kg * V1)
        self.m_f4 = (self.m_Kg * self.m_f3) + (self.m_Hg * self.m_f4)
        V2 = (self.m_AC * self.m_f3) - (self.m_AB * self.m_f4)
        self.m_f5 = (self.m_Hg * self.m_f5) + (self.m_Kg * V2)
        self.m_f6 = (self.m_Kg * self.m_f5) + (self.m_Hg * self.m_f6)
        JurX_ = (self.m_AC * self.m_f5) - (self.m_AB * self.m_f6)
        if self.BarCheck5(rates_total, bar, set_):
            self.m_f1 = self.m_F1
            self.m_f2 = self.m_F2
            self.m_f3 = self.m_F3
            self.m_f4 = self.m_F4
            self.m_f5 = self.m_F5
            self.m_f6 = self.m_F6
        if self.BarCheck4(rates_total, bar, set_):
            self.m_F1 = self.m_f1
            self.m_F2 = self.m_f2
            self.m_F3 = self.m_f3
            self.m_F4 = self.m_f4
            self.m_F5 = self.m_f5
            self.m_F6 = self.m_f6
        return JurX_
    def JurXInit(self, begin, Din, Length, series, bar):
        if bar == begin or Din != 0:
            if Length >= 6:
                self.m_w = Length - 1
            else:
                self.m_w = 5.0
            self.m_Kg = _fdiv(3, Length + 2.0)
            self.m_Hg = 1.0 - self.m_Kg
            if bar == begin:
                self.m_f1 = series
                self.m_f2 = series
                self.m_f3 = series
                self.m_f4 = series
                self.m_f5 = series
                self.m_f6 = series
                self.m_AB = 0.5
                self.m_AC = 1.5

class CCMO(CMovSeriesTools):
    _q_fields = ('m_dSeriesArray', 'm_Size_', 'm_count', 'm_UpSum_', 'm_UpSum', 'm_DnSum_', 'm_DnSum', 'm_Vidya', 'm_Vidya_', 'm_AbsCMO_', 'm_AbsCMO', 'm_series1', 'm_series1_', 'm_SmoothFactor')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_dSeriesArray = Arr(0, 0.0)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_UpSum_ = 0.0
        self.m_UpSum = 0.0
        self.m_DnSum_ = 0.0
        self.m_DnSum = 0.0
        self.m_Vidya = 0.0
        self.m_Vidya_ = 0.0
        self.m_AbsCMO_ = 0.0
        self.m_AbsCMO = 0.0
        self.m_series1 = 0.0
        self.m_series1_ = 0.0
        self.m_SmoothFactor = 0.0
    def VIDYASeries(self, begin, prev_calculated, rates_total, CMO_Length, EMA_Length, series, bar, set_):
        vidya = 0.0
        CMO_ = self.CMOSeries(begin, prev_calculated, rates_total, CMO_Length, series, bar, set_)
        if self.BarCheck2(begin, bar, set_, CMO_Length + 3):
            self.m_Vidya = series
            self.m_SmoothFactor = _fdiv(2.0, EMA_Length + 1.0)
        elif self.BarCheck3(begin, bar, set_, CMO_Length + 3):
            return EMPTY_VALUE
        CMO_ *= self.m_SmoothFactor
        self.m_Vidya = (CMO_ * series) + ((1 - CMO_) * self.m_Vidya)
        vidya = self.m_Vidya
        if self.BarCheck5(rates_total, bar, set_):
            self.m_Vidya = self.m_Vidya_
        if self.BarCheck4(rates_total, bar, set_):
            self.m_Vidya_ = self.m_Vidya
        return vidya
    def CMOSeries(self, begin, prev_calculated, rates_total, CMO_Length, series, bar, set_):
        CMO_Length = Box(CMO_Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        dseries = 0.0
        abcmo = 0.0
        iii = 0
        rrr = 0
        size = CMO_Length.v + 1
        if bar == begin and (not self.SeriesArrayResize('CCMO::CMOSeries', size, self.m_dSeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.LengthCheck_1(CMO_Length)
        if self.BarCheck1(begin + 1, bar, set_):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), size, prev_calculated, rates_total, series - self.m_series1, bar, self.m_dSeriesArray, set_)
        if self.BarCheck2(begin, bar, set_, CMO_Length.v + 3):
            self.m_UpSum = 0.0
            self.m_DnSum = 0.0
            iii = 1
            for iii in range(iii, CMO_Length.v):
                rrr = self.Recount_ArrayNumber(self.m_count, size, iii)
                dseries = self.m_dSeriesArray[rrr]
                if dseries > 0:
                    self.m_UpSum += dseries
                if dseries < 0:
                    self.m_DnSum -= dseries
            else:
                iii = _range_end(iii, CMO_Length.v, 1)
            self.m_AbsCMO = 1e-09
        elif self.BarCheck3(begin, bar, set_, CMO_Length.v + 3):
            self.m_series1 = series
            return EMPTY_VALUE
        dseries = self.m_dSeriesArray[self.m_count]
        if dseries > 0:
            self.m_UpSum += dseries
        if dseries < 0:
            self.m_DnSum -= dseries
        if (self.m_UpSum + self.m_DnSum) > 0:
            self.m_AbsCMO = MathAbs(_fdiv(self.m_UpSum - self.m_DnSum, self.m_UpSum + self.m_DnSum))
        abcmo = self.m_AbsCMO
        rrr = self.Recount_ArrayNumber(self.m_count, size, CMO_Length.v - 1)
        dseries = self.m_dSeriesArray[rrr]
        if dseries > 0:
            self.m_UpSum -= dseries
        if dseries < 0:
            self.m_DnSum += dseries
        if self.BarCheck5(rates_total, bar, set_):
            self.m_AbsCMO = self.m_AbsCMO_
            self.m_UpSum = self.m_UpSum_
            self.m_DnSum = self.m_DnSum_
            self.m_series1 = self.m_series1_
        else:
            self.m_series1 = series
        if self.BarCheck4(rates_total, bar, set_):
            self.m_AbsCMO_ = self.m_AbsCMO
            self.m_UpSum_ = self.m_UpSum
            self.m_DnSum_ = self.m_DnSum
            self.m_series1_ = self.m_series1
        return abcmo

class CAMA(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_dSeriesArray', 'm_NOISE', 'm_noise', 'm_Ama', 'm_AMA_', 'm_slowSC', 'm_fastSC', 'm_dSC', 'm_Size_1', 'm_Size_2', 'm_count')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(0, 0.0)
        self.m_dSeriesArray = Arr(0, 0.0)
        self.m_NOISE = 0.0
        self.m_noise = 0.0
        self.m_Ama = 0.0
        self.m_AMA_ = 0.0
        self.m_slowSC = 0.0
        self.m_fastSC = 0.0
        self.m_dSC = 0.0
        self.m_Size_1 = 0
        self.m_Size_2 = 0
        self.m_count = 0
    def AMASeries(self, begin, prev_calculated, rates_total, Length, Fast_Length, Slow_Length, Rate, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        signal = 0.0
        ER = 0.0
        ERSC = 0.0
        SSC = 0.0
        dprice = 0.0
        ama = 0.0
        iii = 0
        kkk = 0
        rrr = 0
        size = Length.v + 1
        if bar == begin:
            if (not self.SeriesArrayResize('CAMA::AMASeries', size, self.m_SeriesArray, _AttrRef(self, 'm_Size_1'))) or (not self.SeriesArrayResize('CAMA::AMASeries', size, self.m_dSeriesArray, _AttrRef(self, 'm_Size_2'))):
                return EMPTY_VALUE
        self.LengthCheck_1(Length)
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), size, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck1(begin + 1, bar, set_):
            return EMPTY_VALUE
        kkk = self.Recount_ArrayNumber(self.m_count, size, 1)
        dprice = series - self.m_SeriesArray[kkk]
        self.m_dSeriesArray[self.m_count] = dprice
        if self.BarCheck2(begin, bar, set_, Length.v + 3):
            rrr = self.Recount_ArrayNumber(self.m_count, size, 1)
            self.m_Ama = self.m_SeriesArray[rrr]
            self.m_slowSC = _fdiv(2.0, Slow_Length + 1)
            self.m_fastSC = _fdiv(2.0, Fast_Length + 1)
            self.m_dSC = self.m_fastSC - self.m_slowSC
            self.m_noise = 1e-09
            iii = 1
            for iii in range(iii, Length.v):
                rrr = self.Recount_ArrayNumber(self.m_count, size, iii)
                self.m_noise += MathAbs(self.m_dSeriesArray[rrr])
            else:
                iii = _range_end(iii, Length.v, 1)
        elif self.BarCheck3(begin, bar, set_, Length.v + 3):
            return EMPTY_VALUE
        self.m_noise += MathAbs(dprice)
        rrr = self.Recount_ArrayNumber(self.m_count, size, Length.v)
        signal = MathAbs(series - self.m_SeriesArray[rrr])
        ER = _fdiv(signal, self.m_noise)
        ERSC = ER * self.m_dSC
        SSC = ERSC + self.m_slowSC
        self.m_Ama = self.m_Ama + (MathPow(SSC, Rate) * (series - self.m_Ama))
        ama = self.m_Ama
        kkk = self.Recount_ArrayNumber(self.m_count, size, Length.v - 1)
        self.m_noise -= MathAbs(self.m_dSeriesArray[kkk])
        if self.BarCheck5(rates_total, bar, set_):
            self.m_noise = self.m_NOISE
            self.m_Ama = self.m_AMA_
        if self.BarCheck4(rates_total, bar, set_):
            self.m_AMA_ = self.m_Ama
            self.m_NOISE = self.m_noise
        return ama

class CParMA(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count', 'm_sum_x', 'm_sum_x2', 'm_sum_x3', 'm_sum_x4')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(0, 0.0)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_sum_x = 0
        self.m_sum_x2 = 0
        self.m_sum_x3 = 0
        self.m_sum_x4 = 0
    def ParMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        iii = 0
        kkk = 0
        S = 0.0
        B0 = 0.0
        B1 = 0.0
        B2 = 0.0
        parma = 0.0
        A = 0.0
        B = 0.0
        C = 0.0
        D = 0.0
        E = 0.0
        F = 0.0
        K = 0.0
        L = 0.0
        M = 0.0
        P = 0.0
        Q = 0.0
        R = 0.0
        sum_y = 0.0
        sum_xy = 0.0
        sum_x2y = 0.0
        var_tmp = 0.0
        if bar == begin and (not self.SeriesArrayResize('CParMA::ParMASeries', Length.v, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.LengthCheck_1(Length)
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length.v, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck2(begin, bar, set_, Length.v):
            self.ParMAInit(Length.v)
        elif self.BarCheck3(begin, bar, set_, Length.v):
            return EMPTY_VALUE
        sum_y = 0.0
        sum_xy = 0.0
        sum_x2y = 0.0
        iii = 1
        for iii in range(iii, Length.v + 1):
            kkk = self.Recount_ArrayNumber(self.m_count, Length.v, Length.v - iii)
            var_tmp = self.m_SeriesArray[kkk]
            sum_y += var_tmp
            sum_xy += iii * var_tmp
            sum_x2y += iii * iii * var_tmp
        else:
            iii = _range_end(iii, Length.v + 1, 1)
        A = Length.v
        B = self.m_sum_x
        C = self.m_sum_x2
        F = self.m_sum_x3
        M = self.m_sum_x4
        P = sum_y
        R = sum_xy
        S = sum_x2y
        D = B
        E = C
        K = C
        L = F
        Q = _fdiv(D, A)
        E = E - (Q * B)
        F = F - (Q * C)
        R = R - (Q * P)
        Q = _fdiv(K, A)
        L = L - (Q * B)
        M = M - (Q * C)
        S = S - (Q * P)
        Q = _fdiv(L, E)
        B2 = _fdiv(S - (R * Q), M - (F * Q))
        B1 = _fdiv(R - (F * B2), E)
        B0 = _fdiv(P - (B * B1) - (C * B2), A)
        parma = B0 + ((B1 + (B2 * A)) * A)
        return parma
    def ParMAInit(self, Length):
        var_tmp = 0
        self.m_sum_x = 0
        self.m_sum_x2 = 0
        self.m_sum_x3 = 0
        self.m_sum_x4 = 0
        iii = 1
        while iii <= Length:
            var_tmp = iii
            self.m_sum_x += var_tmp
            var_tmp *= iii
            self.m_sum_x2 += var_tmp
            var_tmp *= iii
            self.m_sum_x3 += var_tmp
            var_tmp *= iii
            self.m_sum_x4 += var_tmp
            iii += 1

class CMomentum(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(0, 0.0)
        self.m_Size_ = 0
        self.m_count = 0
    def MomentumSeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        kkk = 0
        Length_ = Length.v + 1
        Momentum = 0.0
        self.LengthCheck_1(Length)
        if bar == begin and (not self.SeriesArrayResize('CMomentum::MomentumSeries', Length_, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck3(begin, bar, set_, Length_):
            return EMPTY_VALUE
        kkk = self.Recount_ArrayNumber(self.m_count, Length_, Length.v)
        Momentum = series - self.m_SeriesArray[kkk]
        return Momentum

class CnMomentum(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(0, 0.0)
        self.m_Size_ = 0
        self.m_count = 0
    def nMomentumSeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        kkk = 0
        Length_ = Length.v + 1
        nMomentum = 0.0
        self.LengthCheck_1(Length)
        if bar == begin and (not self.SeriesArrayResize('CnMomentum::nMomentumSeries', Length_, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck3(begin, bar, set_, Length_):
            return EMPTY_VALUE
        kkk = self.Recount_ArrayNumber(self.m_count, Length_, Length.v)
        nMomentum = _fdiv(series - self.m_SeriesArray[kkk], self.m_SeriesArray[kkk])
        return nMomentum

class CROC(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count')
    def __init__(self, *args):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(0, 0.0)
        self.m_Size_ = 0
        self.m_count = 0
    def ROCSeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        Length = Box(Length)
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        kkk = 0
        Length_ = Length.v + 1
        ROC = 0.0
        self.LengthCheck_1(Length)
        if bar == begin and (not self.SeriesArrayResize('CROC::ROCSeries', Length_, self.m_SeriesArray, _AttrRef(self, 'm_Size_'))):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), Length_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck3(begin, bar, set_, Length_):
            return EMPTY_VALUE
        kkk = self.Recount_ArrayNumber(self.m_count, Length_, Length.v)
        ROC = _fdiv(100 * series, self.m_SeriesArray[kkk])
        return ROC

class CFATL(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count', 'm_FATL', 'm_FATLTable')
    def __init__(self):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(39, 0.0, dyn=False)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_FATL = 0.0
        self.m_FATLTable = Arr(39, 0.0, dyn=False)
        self.m_Size_ = 39
        FATLTable = Arr.of([0.436040945, 0.3658689069, 0.2460452079, 0.1104506886, -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374, -0.0190795053, 0.0259609206, 0.0502044896, 0.0477818607, 0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838, 0.0128149838, 0.0226522218, 0.0208778257, 0.0100299086, -0.0036771622, -0.013674485, -0.0160483392, -0.0108597376, -0.0016060704, 0.0069480557, 0.0110573605, 0.0095711419, 0.0040444064, -0.0023824623, -0.0067093714, -0.00720034, -0.004771771, 0.0005541115, 0.000786016, 0.0130129076, 0.0040364019], fill=0.0)
        ArrayCopy(self.m_FATLTable, FATLTable, 0, 0, WHOLE_ARRAY)
    def FATLSeries(self, begin, prev_calculated, rates_total, series, bar, set_):
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), self.m_Size_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck3(begin, bar, set_, self.m_Size_):
            return EMPTY_VALUE
        FATL = 0.0
        if self.BarCheck5(rates_total, bar, set_):
            if prev_calculated != rates_total:
                self.m_FATL = 0.0
                iii = 1
                while iii < self.m_Size_:
                    self.m_FATL += self.m_FATLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                    iii += 1
            FATL = self.m_FATL + (self.m_FATLTable[0] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, 0)])
        else:
            iii = 0
            while iii < self.m_Size_:
                FATL += self.m_FATLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                iii += 1
        return FATL

class CSATL(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count', 'm_SATL', 'm_SATLTable')
    def __init__(self):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(65, 0.0, dyn=False)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_SATL = 0.0
        self.m_SATLTable = Arr(65, 0.0, dyn=False)
        self.m_Size_ = 65
        SATLTable = Arr.of([0.0982862174, 0.0975682269, 0.0961401078, 0.0940230544, 0.091243709, 0.0878391006, 0.0838544303, 0.079340635, 0.0743569346, 0.0689666682, 0.0632381578, 0.0572428925, 0.0510534242, 0.0447468229, 0.038395995, 0.0320735368, 0.0258537721, 0.0198005183, 0.0139807863, 0.0084512448, 0.0032639979, -0.0015350359, -0.0059060082, -0.0098190256, -0.0132507215, -0.0161875265, -0.0186164872, -0.0205446727, -0.0219739146, -0.0229204861, -0.0234080863, -0.0234566315, -0.0231017777, -0.02237969, -0.0213300463, -0.0199924534, -0.0184126992, -0.0166377699, -0.0147139428, -0.0126796776, -0.0105938331, -0.008473677, -0.006384185, -0.0043466731, -0.0023956944, -0.000553518, 0.0011421469, 0.0026845693, 0.0040471369, 0.0052380201, 0.0062194591, 0.0070340085, 0.0076266453, 0.0080376628, 0.0083037666, 0.0083694798, 0.0082901022, 0.0080741359, 0.007754382, 0.0073260526, 0.0068163569, 0.0062325477, 0.0056078229, 0.0049516078, 0.0161380976], fill=0.0)
        ArrayCopy(self.m_SATLTable, SATLTable, 0, 0, WHOLE_ARRAY)
    def SATLSeries(self, begin, prev_calculated, rates_total, series, bar, set_):
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), self.m_Size_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck3(begin, bar, set_, self.m_Size_):
            return EMPTY_VALUE
        SATL = 0.0
        if self.BarCheck5(rates_total, bar, set_):
            if prev_calculated != rates_total:
                self.m_SATL = 0.0
                iii = 1
                while iii < self.m_Size_:
                    self.m_SATL += self.m_SATLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                    iii += 1
            SATL = self.m_SATL + (self.m_SATLTable[0] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, 0)])
        else:
            iii = 0
            while iii < self.m_Size_:
                SATL += self.m_SATLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                iii += 1
        return SATL

class CRFTL(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count', 'm_RFTL', 'm_RFTLTable')
    def __init__(self):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(44, 0.0, dyn=False)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_RFTL = 0.0
        self.m_RFTLTable = Arr(44, 0.0, dyn=False)
        self.m_Size_ = 44
        RFTLTable = Arr.of([-0.0025097319, 0.0513007762, 0.1142800493, 0.169934286, 0.2025269304, 0.2025269304, 0.169934286, 0.1142800493, 0.0513007762, -0.0025097319, -0.0353166244, -0.0433375629, -0.0311244617, -0.0088618137, 0.0120580088, 0.0233183633, 0.0221931304, 0.0115769653, -0.0022157966, -0.0126536111, -0.0157416029, -0.011339583, -0.002590561, 0.0059521459, 0.0105212252, 0.0096970755, 0.0046585685, -0.001707923, -0.0063513565, -0.007453935, -0.0050439973, -0.0007459678, 0.0032271474, 0.0051357867, 0.0044454862, 0.0018784961, -0.0011065767, -0.0031162862, -0.0033443253, -0.0022163335, 0.0002573669, 0.000365079, 0.0060440751, 0.0018747783], fill=0.0)
        ArrayCopy(self.m_RFTLTable, RFTLTable, 0, 0, WHOLE_ARRAY)
    def RFTLSeries(self, begin, prev_calculated, rates_total, series, bar, set_):
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), self.m_Size_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck3(begin, bar, set_, self.m_Size_):
            return EMPTY_VALUE
        RFTL = 0.0
        if self.BarCheck5(rates_total, bar, set_):
            if prev_calculated != rates_total:
                self.m_RFTL = 0.0
                iii = 1
                while iii < self.m_Size_:
                    self.m_RFTL += self.m_RFTLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                    iii += 1
            RFTL = self.m_RFTL + (self.m_RFTLTable[0] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, 0)])
        else:
            iii = 0
            while iii < self.m_Size_:
                RFTL += self.m_RFTLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                iii += 1
        return RFTL

class CRSTL(CMovSeriesTools):
    _q_fields = ('m_SeriesArray', 'm_Size_', 'm_count', 'm_RSTL', 'm_RSTLTable')
    def __init__(self):
        CMovSeriesTools.__init__(self)
        self.m_SeriesArray = Arr(99, 0.0, dyn=False)
        self.m_Size_ = 0
        self.m_count = 0
        self.m_RSTL = 0.0
        self.m_RSTLTable = Arr(99, 0.0, dyn=False)
        self.m_Size_ = 99
        RSTLTable = Arr.of([-0.00514293, -0.00398417, -0.00262594, -0.00107121, 0.00066887, 0.00258172, 0.00465269, 0.00686394, 0.00919334, 0.0116172, 0.01411056, 0.01664635, 0.01919533, 0.02172747, 0.0242132, 0.02662203, 0.02892446, 0.03109071, 0.03309496, 0.03490921, 0.03651145, 0.03788045, 0.03899804, 0.03984915, 0.04042329, 0.04071263, 0.04071263, 0.04042329, 0.03984915, 0.03899804, 0.03788045, 0.03651145, 0.03490921, 0.03309496, 0.03109071, 0.02892446, 0.02662203, 0.0242132, 0.02172747, 0.01919533, 0.01664635, 0.01411056, 0.0116172, 0.00919334, 0.00686394, 0.00465269, 0.00258172, 0.00066887, -0.00107121, -0.00262594, -0.00398417, -0.00514293, -0.00609634, -0.00684602, -0.00739452, -0.00774847, -0.0079163, -0.0079094, -0.00774085, -0.00742482, -0.00697718, -0.00641613, -0.00576108, -0.00502957, -0.00423873, -0.00340812, -0.00255923, -0.00170217, -0.00085902, -4.113e-05, 0.000737, 0.00146422, 0.00213007, 0.00272649, 0.00324752, 0.00368922, 0.00405, 0.00433024, 0.00453068, 0.00465046, 0.00469058, 0.00466041, 0.00457855, 0.00442491, 0.00423019, 0.00399201, 0.00372169, 0.00342736, 0.00311822, 0.00280309, 0.00249088, 0.00219089, 0.00191283, 0.00166683, 0.00146419, 0.00131867, 0.00124645, 0.00126836, -0.00401854], fill=0.0)
        ArrayCopy(self.m_RSTLTable, RSTLTable, 0, 0, WHOLE_ARRAY)
    def RSTLSeries(self, begin, prev_calculated, rates_total, series, bar, set_):
        if self.BarCheck1(begin, bar, set_):
            return EMPTY_VALUE
        self.Recount_ArrayZeroPos(_AttrRef(self, 'm_count'), self.m_Size_, prev_calculated, rates_total, series, bar, self.m_SeriesArray, set_)
        if self.BarCheck3(begin, bar, set_, self.m_Size_):
            return EMPTY_VALUE
        RSTL = 0.0
        if self.BarCheck5(rates_total, bar, set_):
            if prev_calculated != rates_total:
                self.m_RSTL = 0.0
                iii = 1
                while iii < self.m_Size_:
                    self.m_RSTL += self.m_RSTLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                    iii += 1
            RSTL = self.m_RSTL + (self.m_RSTLTable[0] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, 0)])
        else:
            iii = 0
            while iii < self.m_Size_:
                RSTL += self.m_RSTLTable[iii] * self.m_SeriesArray[self.Recount_ArrayNumber(self.m_count, self.m_Size_, iii)]
                iii += 1
        return RSTL

class CXMA(MqlObject):
    _q_fields = ('SMA', 'EMA', 'SMMA', 'LWMA', 'JJMA', 'JurX', 'ParMA', 'T3', 'VIDYA', 'AMA', 'm_init', 'm_Method')
    _q_ptrs = ('SMA', 'EMA', 'SMMA', 'LWMA', 'JJMA', 'JurX', 'ParMA', 'T3', 'VIDYA', 'AMA',)
    def __init__(self):
        self.SMA = None
        self.EMA = None
        self.SMMA = None
        self.LWMA = None
        self.JJMA = None
        self.JurX = None
        self.ParMA = None
        self.T3 = None
        self.VIDYA = None
        self.AMA = None
        self.m_init = False
        self.m_Method = 0
        self.m_init = False
    def _q_dtor(self):
        _sw2 = self.m_Method
        if _sw2 == MODE_SMA_:
            if self.SMA is not None:
                _delete(self.SMA)
        elif _sw2 == MODE_EMA_:
            if self.EMA is not None:
                _delete(self.EMA)
        elif _sw2 == MODE_SMMA_:
            if self.SMMA is not None:
                _delete(self.SMMA)
        elif _sw2 == MODE_LWMA_:
            if self.LWMA is not None:
                _delete(self.LWMA)
        elif _sw2 == MODE_JJMA:
            if self.JJMA is not None:
                _delete(self.JJMA)
        elif _sw2 == MODE_JurX:
            if self.JurX is not None:
                _delete(self.JurX)
        elif _sw2 == MODE_ParMA:
            if self.ParMA is not None:
                _delete(self.ParMA)
        elif _sw2 == MODE_T3:
            if self.T3 is not None:
                _delete(self.T3)
        elif _sw2 == MODE_VIDYA:
            if self.VIDYA is not None:
                _delete(self.VIDYA)
        elif _sw2 == MODE_AMA:
            if self.AMA is not None:
                _delete(self.AMA)
    def XMASeries(self, begin, prev_calculated, rates_total, Method, Phase, Length, series, bar, set_):
        self.XMAInit(Method)
        _sw3 = Method
        if _sw3 == MODE_SMA_:
            return self.SMA.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw3 == MODE_EMA_:
            return self.EMA.EMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw3 == MODE_SMMA_:
            return self.SMMA.SMMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw3 == MODE_LWMA_:
            return self.LWMA.LWMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw3 == MODE_JJMA:
            return self.JJMA.JJMASeries(begin, prev_calculated, rates_total, 0, Phase, Length, series, bar, set_)
        elif _sw3 == MODE_JurX:
            return self.JurX.JurXSeries(begin, prev_calculated, rates_total, 0, Length, series, bar, set_)
        elif _sw3 == MODE_ParMA:
            return self.ParMA.ParMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        elif _sw3 == MODE_T3:
            return self.T3.T3Series(begin, prev_calculated, rates_total, 0, Phase, Length, series, bar, set_)
        elif _sw3 == MODE_VIDYA:
            return self.VIDYA.VIDYASeries(begin, prev_calculated, rates_total, Phase, Length, series, bar, set_)
        elif _sw3 == MODE_AMA:
            return self.AMA.AMASeries(begin, prev_calculated, rates_total, Length, 2, Phase, 2.0, series, bar, set_)
        return 0.0
    def GetStartBars(self, Method, Length, Phase):
        _sw4 = Method
        if _sw4 == MODE_SMA_:
            return Length
        elif _sw4 == MODE_EMA_:
            return 0
        elif _sw4 == MODE_SMMA_:
            return Length + 1
        elif _sw4 == MODE_LWMA_:
            return Length
        elif _sw4 == MODE_JJMA:
            return 30
        elif _sw4 == MODE_JurX:
            return 0
        elif _sw4 == MODE_ParMA:
            return Length
        elif _sw4 == MODE_T3:
            return 0
        elif _sw4 == MODE_VIDYA:
            return Phase + 2
        elif _sw4 == MODE_AMA:
            return Length + 2
        return 0
    def GetString_MA_Method(self, Method):
        _sw5 = Method
        if _sw5 == MODE_SMA_:
            return 'SMA'
        elif _sw5 == MODE_EMA_:
            return 'EMA'
        elif _sw5 == MODE_SMMA_:
            return 'SMMA'
        elif _sw5 == MODE_LWMA_:
            return 'LWMA'
        elif _sw5 == MODE_JJMA:
            return 'JJMA'
        elif _sw5 == MODE_JurX:
            return 'JurX'
        elif _sw5 == MODE_ParMA:
            return 'ParMA'
        elif _sw5 == MODE_T3:
            return 'T3'
        elif _sw5 == MODE_VIDYA:
            return ' VIDYA'
        elif _sw5 == MODE_AMA:
            return 'AMA'
        return ''
    def XMAPhaseCheck(self, PhaseName, ExternPhase, Method):
        _sw6 = Method
        _k7 = 0 if _sw6 == MODE_SMA_ else 1 if _sw6 == MODE_EMA_ else 2 if _sw6 == MODE_SMMA_ else 3 if _sw6 == MODE_LWMA_ else 4 if _sw6 == MODE_JJMA else 5 if _sw6 == MODE_JurX else 6 if _sw6 == MODE_ParMA else 7 if _sw6 == MODE_T3 else 8 if _sw6 == MODE_VIDYA else 9 if _sw6 == MODE_AMA else 10
        try:
            if _k7 <= 0:
                raise _SwitchBreak
            if _k7 <= 1:
                raise _SwitchBreak
            if _k7 <= 2:
                raise _SwitchBreak
            if _k7 <= 3:
                raise _SwitchBreak
            if _k7 <= 4:
                if ExternPhase < -100:
                    word = Box("")
                    StringConcatenate(word, 'CXMA::XMAPhaseCheck', ' (): Параметр ', PhaseName, ' должен быть не менее -100. Вы ввели недопустимое ', ExternPhase, ' будет использовано -100')
                    Print(word.v)
                    raise _SwitchBreak
                if ExternPhase > 100:
                    word = Box("")
                    StringConcatenate(word, 'CXMA::XMAPhaseCheck', ' (): Параметр ', PhaseName, ' должен быть не более +100. Вы ввели недопустимое ', ExternPhase, ' будет использовано +100')
                    Print(word.v)
                    raise _SwitchBreak
                raise _SwitchBreak
            if _k7 <= 5:
                raise _SwitchBreak
            if _k7 <= 6:
                raise _SwitchBreak
            if _k7 <= 7:
                raise _SwitchBreak
                if ExternPhase < 1:
                    word = Box("")
                    StringConcatenate(word, 'CXMA::XMAPhaseCheck', ' (): Параметр ', PhaseName, ' должен быть не менее 1. Вы ввели недопустимое ', ExternPhase, ' будет использовано 1')
                    Print(word.v)
                    raise _SwitchBreak
            if _k7 <= 8:
                if ExternPhase < 1:
                    word = Box("")
                    StringConcatenate(word, 'CXMA::XMAPhaseCheck', ' (): Параметр ', PhaseName, ' должен быть не менее 1. Вы ввели недопустимое ', ExternPhase, ' будет использовано 1')
                    Print(word.v)
                    raise _SwitchBreak
            if _k7 <= 9:
                if ExternPhase < 1:
                    word = Box("")
                    StringConcatenate(word, 'CXMA::XMAPhaseCheck', ' (): Параметр ', PhaseName, ' должен быть не менее 1. Вы ввели недопустимое ', ExternPhase, ' будет использовано 1')
                    Print(word.v)
                    raise _SwitchBreak
        except _SwitchBreak:
            pass
    def XMALengthCheck(self, LengthName, ExternLength):
        if ExternLength < 1:
            word = Box("")
            StringConcatenate(word, 'CXMA::XMALengthCheck', ' (): Параметр ', LengthName, ' должен быть не менее 1. Вы ввели недопустимое ', ExternLength, ' будет использовано  1')
            Print(word.v)
            return
    def XMAInit(self, Method):
        if self.m_init:
            return
        else:
            self.m_init = True
            self.m_Method = Method
        _sw8 = Method
        if _sw8 == MODE_SMA_:
            self.SMA = CMoving_Average()
        elif _sw8 == MODE_EMA_:
            self.EMA = CMoving_Average()
        elif _sw8 == MODE_SMMA_:
            self.SMMA = CMoving_Average()
        elif _sw8 == MODE_LWMA_:
            self.LWMA = CMoving_Average()
        elif _sw8 == MODE_JJMA:
            self.JJMA = CJJMA()
        elif _sw8 == MODE_JurX:
            self.JurX = CJurX()
        elif _sw8 == MODE_ParMA:
            self.ParMA = CParMA()
        elif _sw8 == MODE_T3:
            self.T3 = CT3()
        elif _sw8 == MODE_VIDYA:
            self.VIDYA = CCMO()
        elif _sw8 == MODE_AMA:
            self.AMA = CAMA()
        else:
            pass

def GetStartBars(Method, Length, Phase):
    _sw9 = Method
    if _sw9 == MODE_SMA_:
        return Length
    elif _sw9 == MODE_EMA_:
        return 0
    elif _sw9 == MODE_SMMA_:
        return Length + 1
    elif _sw9 == MODE_LWMA_:
        return Length
    elif _sw9 == MODE_JJMA:
        return 30
    elif _sw9 == MODE_JurX:
        return 0
    elif _sw9 == MODE_ParMA:
        return Length
    elif _sw9 == MODE_T3:
        return 0
    elif _sw9 == MODE_VIDYA:
        return Phase + 2
    elif _sw9 == MODE_AMA:
        return Length + 2
    return 0

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw10 = applied_price
    if _sw10 == PRICE_CLOSE:
        return Close[bar]
    elif _sw10 == PRICE_OPEN:
        return Open[bar]
    elif _sw10 == PRICE_HIGH:
        return High[bar]
    elif _sw10 == PRICE_LOW:
        return Low[bar]
    elif _sw10 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw10 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw10 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw10 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw10 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw10 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw10 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw10 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]

def iPriceSeries(symbol, timeframe, applied_price, bar, set_):
    Bar = 0
    diPriceSeries = 0.0
    price = Arr(1, 0.0, dyn=False)
    if not set_:
        Bar = Bars(symbol, timeframe) - 1 - bar
    else:
        Bar = bar
    _sw11 = applied_price
    if _sw11 == 1:
        CopyClose(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
    elif _sw11 == 2:
        CopyOpen(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
    elif _sw11 == 3:
        CopyHigh(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
    elif _sw11 == 4:
        CopyLow(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
    elif _sw11 == 5:
        CopyHigh(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
        CopyLow(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        diPriceSeries = diPriceSeries / 2.0
    elif _sw11 == 6:
        CopyClose(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
        CopyHigh(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        CopyLow(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        diPriceSeries = diPriceSeries / 3.0
    elif _sw11 == 7:
        CopyClose(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0] * 2
        CopyHigh(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        CopyLow(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        diPriceSeries = diPriceSeries / 4.0
    elif _sw11 == 8:
        CopyClose(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
        CopyOpen(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        diPriceSeries = diPriceSeries / 2.0
    elif _sw11 == 9:
        CopyClose(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
        CopyOpen(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        CopyHigh(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        CopyLow(symbol, timeframe, Bar, 1, price)
        diPriceSeries += price[0]
        diPriceSeries = diPriceSeries / 4.0
    elif _sw11 == 10:
        Open_ = Arr(1, 0.0, dyn=False)
        Low_ = Arr(1, 0.0, dyn=False)
        High_ = Arr(1, 0.0, dyn=False)
        Close_ = Arr(1, 0.0, dyn=False)
        CopyClose(symbol, timeframe, Bar, 1, Close_)
        CopyOpen(symbol, timeframe, Bar, 1, Open_)
        CopyHigh(symbol, timeframe, Bar, 1, High_)
        CopyLow(symbol, timeframe, Bar, 1, Low_)
        if Close_[0] > Open_[0]:
            diPriceSeries = High_[0]
        else:
            if Close_[0] < Open_[0]:
                diPriceSeries = Low_[0]
            else:
                diPriceSeries = Close_[0]
    elif _sw11 == 11:
        Open_ = Arr(1, 0.0, dyn=False)
        Low_ = Arr(1, 0.0, dyn=False)
        High_ = Arr(1, 0.0, dyn=False)
        Close_ = Arr(1, 0.0, dyn=False)
        CopyClose(symbol, timeframe, Bar, 1, Close_)
        CopyOpen(symbol, timeframe, Bar, 1, Open_)
        CopyHigh(symbol, timeframe, Bar, 1, High_)
        CopyLow(symbol, timeframe, Bar, 1, Low_)
        if Close_[0] > Open_[0]:
            diPriceSeries = (High_[0] + Close_[0]) / 2.0
        else:
            if Close_[0] < Open_[0]:
                diPriceSeries = (Low_[0] + Close_[0]) / 2.0
            else:
                diPriceSeries = Close_[0]
    elif _sw11 == 12:
        Open_ = Arr(1, 0.0, dyn=False)
        Low_ = Arr(1, 0.0, dyn=False)
        High_ = Arr(1, 0.0, dyn=False)
        Close_ = Arr(1, 0.0, dyn=False)
        CopyClose(symbol, timeframe, Bar, 1, Close_)
        CopyOpen(symbol, timeframe, Bar, 1, Open_)
        CopyHigh(symbol, timeframe, Bar, 1, High_)
        CopyLow(symbol, timeframe, Bar, 1, Low_)
        res = High_[0] + Low_[0] + Close_[0]
        if Close_[0] < Open_[0]:
            res = (res + Low_[0]) / 2
        if Close_[0] > Open_[0]:
            res = (res + High_[0]) / 2
        if Close_[0] == Open_[0]:
            res = (res + Close_[0]) / 2
        diPriceSeries = (res - Low_[0] + (res - High_[0])) / 2
    else:
        CopyClose(symbol, timeframe, Bar, 1, price)
        diPriceSeries = price[0]
    return diPriceSeries

def bPriceSeries(symbol, timeframe, rates_total, applied_price, bar, set_, Price_):
    Bar = 0
    series = Arr(0, 0.0)
    ArraySetAsSeries(series, True)
    if not set_:
        Bar = rates_total - 1 - bar
    else:
        Bar = bar
    _sw12 = applied_price
    if _sw12 == 1:
        if CopyClose(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
    elif _sw12 == 2:
        if CopyOpen(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
    elif _sw12 == 3:
        if CopyHigh(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
    elif _sw12 == 4:
        if CopyLow(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
    elif _sw12 == 5:
        if CopyHigh(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
        if CopyLow(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        Price_.v = Price_.v / 2.0
    elif _sw12 == 6:
        if CopyClose(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
        if CopyHigh(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        if CopyLow(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        Price_.v = Price_.v / 3.0
    elif _sw12 == 7:
        if CopyClose(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0] * 2
        if CopyHigh(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        if CopyLow(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        Price_.v = Price_.v / 4.0
    elif _sw12 == 8:
        if CopyClose(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
        if CopyOpen(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        Price_.v = Price_.v / 2.0
    elif _sw12 == 9:
        if CopyClose(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
        if CopyOpen(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        if CopyHigh(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        if CopyLow(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v += series[0]
        Price_.v = Price_.v / 4.0
    elif _sw12 == 10:
        Open_ = Arr(1, 0.0, dyn=False)
        Low_ = Arr(1, 0.0, dyn=False)
        High_ = Arr(1, 0.0, dyn=False)
        Close_ = Arr(1, 0.0, dyn=False)
        if CopyClose(symbol, timeframe, Bar, 1, Close_) < 0:
            return False
        if CopyOpen(symbol, timeframe, Bar, 1, Open_) < 0:
            return False
        if CopyHigh(symbol, timeframe, Bar, 1, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, Bar, 1, Low_) < 0:
            return False
        if Close_[0] > Open_[0]:
            Price_.v = High_[0]
        else:
            if Close_[0] < Open_[0]:
                Price_.v = Low_[0]
            else:
                Price_.v = Close_[0]
    elif _sw12 == 11:
        Open_ = Arr(1, 0.0, dyn=False)
        Low_ = Arr(1, 0.0, dyn=False)
        High_ = Arr(1, 0.0, dyn=False)
        Close_ = Arr(1, 0.0, dyn=False)
        if CopyClose(symbol, timeframe, Bar, 1, Close_) < 0:
            return False
        if CopyOpen(symbol, timeframe, Bar, 1, Open_) < 0:
            return False
        if CopyHigh(symbol, timeframe, Bar, 1, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, Bar, 1, Low_) < 0:
            return False
        if Close_[0] > Open_[0]:
            Price_.v = (High_[0] + Close_[0]) / 2.0
        else:
            if Close_[0] < Open_[0]:
                Price_.v = (Low_[0] + Close_[0]) / 2.0
            else:
                Price_.v = Close_[0]
    elif _sw12 == 12:
        Open_ = Arr(1, 0.0, dyn=False)
        Low_ = Arr(1, 0.0, dyn=False)
        High_ = Arr(1, 0.0, dyn=False)
        Close_ = Arr(1, 0.0, dyn=False)
        if CopyClose(symbol, timeframe, Bar, 1, Close_) < 0:
            return False
        if CopyOpen(symbol, timeframe, Bar, 1, Open_) < 0:
            return False
        if CopyHigh(symbol, timeframe, Bar, 1, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, Bar, 1, Low_) < 0:
            return False
        res = High_[0] + Low_[0] + Close_[0]
        if Close_[0] < Open_[0]:
            res = (res + Low_[0]) / 2
        if Close_[0] > Open_[0]:
            res = (res + High_[0]) / 2
        if Close_[0] == Open_[0]:
            res = (res + Close_[0]) / 2
        Price_.v = (res - Low_[0] + (res - High_[0])) / 2
    else:
        if CopyClose(symbol, timeframe, Bar, 1, series) < 0:
            return False
        Price_.v = series[0]
    return True

def bPriceSeriesOnArray(symbol, timeframe, applied_price, start_pos, count, series):
    ArraySetAsSeries(series, True)
    _sw13 = applied_price
    if _sw13 == 1:
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
    elif _sw13 == 2:
        if CopyOpen(symbol, timeframe, start_pos, count, series) < 0:
            return False
    elif _sw13 == 3:
        if CopyHigh(symbol, timeframe, start_pos, count, series) < 0:
            return False
    elif _sw13 == 4:
        if CopyLow(symbol, timeframe, start_pos, count, series) < 0:
            return False
    elif _sw13 == 5:
        Low_ = Arr(0, 0.0)
        ArraySetAsSeries(Low_, True)
        if CopyHigh(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyLow(symbol, timeframe, start_pos, count, Low_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            series[kkk] = (series[kkk] + Low_[kkk]) / 2.0
    elif _sw13 == 6:
        Low_ = Arr(0, 0.0)
        High_ = Arr(0, 0.0)
        ArraySetAsSeries(Low_, True)
        ArraySetAsSeries(High_, True)
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyHigh(symbol, timeframe, start_pos, count, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, start_pos, count, Low_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            series[kkk] = (series[kkk] + High_[kkk] + Low_[kkk]) / 3.0
    elif _sw13 == 7:
        Low_ = Arr(0, 0.0)
        High_ = Arr(0, 0.0)
        ArraySetAsSeries(Low_, True)
        ArraySetAsSeries(High_, True)
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyHigh(symbol, timeframe, start_pos, count, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, start_pos, count, Low_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            series[kkk] = ((2 * series[kkk]) + High_[kkk] + Low_[kkk]) / 4.0
    elif _sw13 == 8:
        Open_ = Arr(0, 0.0)
        ArraySetAsSeries(Open_, True)
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyOpen(symbol, timeframe, start_pos, count, Open_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            series[kkk] = (series[kkk] + Open_[kkk]) / 2.0
    elif _sw13 == 9:
        Open_ = Arr(0, 0.0)
        Low_ = Arr(0, 0.0)
        High_ = Arr(0, 0.0)
        ArraySetAsSeries(Open_, True)
        ArraySetAsSeries(Low_, True)
        ArraySetAsSeries(High_, True)
        if CopyOpen(symbol, timeframe, start_pos, count, Open_) < 0:
            return False
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyHigh(symbol, timeframe, start_pos, count, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, start_pos, count, Low_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            series[kkk] = (Open_[kkk] + series[kkk] + High_[kkk] + Low_[kkk]) / 4.0
    elif _sw13 == 10:
        Open_ = Arr(0, 0.0)
        Low_ = Arr(0, 0.0)
        High_ = Arr(0, 0.0)
        ArraySetAsSeries(Open_, True)
        ArraySetAsSeries(Low_, True)
        ArraySetAsSeries(High_, True)
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyOpen(symbol, timeframe, start_pos, count, Open_) < 0:
            return False
        if CopyHigh(symbol, timeframe, start_pos, count, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, start_pos, count, Low_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            if series[kkk] > Open_[kkk]:
                series[kkk] = High_[kkk]
            else:
                if series[kkk] < Open_[kkk]:
                    series[kkk] = Low_[kkk]
    elif _sw13 == 11:
        Open_ = Arr(0, 0.0)
        Low_ = Arr(0, 0.0)
        High_ = Arr(0, 0.0)
        ArraySetAsSeries(Open_, True)
        ArraySetAsSeries(Low_, True)
        ArraySetAsSeries(High_, True)
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyOpen(symbol, timeframe, start_pos, count, Open_) < 0:
            return False
        if CopyHigh(symbol, timeframe, start_pos, count, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, start_pos, count, Low_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            if series[kkk] > Open_[kkk]:
                series[kkk] = (High_[kkk] + series[kkk]) / 2.0
            else:
                if series[kkk] < Open_[kkk]:
                    series[kkk] = (Low_[kkk] + series[kkk]) / 2.0
    elif _sw13 == 12:
        Open_ = Arr(0, 0.0)
        Low_ = Arr(0, 0.0)
        High_ = Arr(0, 0.0)
        ArraySetAsSeries(Open_, True)
        ArraySetAsSeries(Low_, True)
        ArraySetAsSeries(High_, True)
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
        if CopyOpen(symbol, timeframe, start_pos, count, Open_) < 0:
            return False
        if CopyHigh(symbol, timeframe, start_pos, count, High_) < 0:
            return False
        if CopyLow(symbol, timeframe, start_pos, count, Low_) < 0:
            return False
        for kkk in range(start_pos, start_pos + count):
            res = High_[kkk] + Low_[kkk] + series[kkk]
            if series[kkk] < Open_[kkk]:
                res = (res + Low_[kkk]) / 2
            if series[kkk] > Open_[kkk]:
                res = (res + High_[kkk]) / 2
            if series[kkk] == Open_[kkk]:
                res = (res + series[kkk]) / 2
            series[kkk] = (res - Low_[kkk] + (res - High_[kkk])) / 2
    else:
        if CopyClose(symbol, timeframe, start_pos, count, series) < 0:
            return False
    return True

def iPriceSeriesAlert(applied_price):
    if applied_price < 1:
        Alert('Параметр applied_price должен быть не менее 1. Вы ввели недопустимое ', applied_price, ' будет использовано 1')
    if applied_price > 12:
        Alert('Параметр applied_price должен быть не более 12. Вы ввели недопустимое ', applied_price, ' будет использовано 1')

__all__ = ['MODE_SMA_', 'MODE_EMA_', 'MODE_SMMA_', 'MODE_LWMA_', 'MODE_JJMA', 'MODE_JurX', 'MODE_ParMA', 'MODE_T3', 'MODE_VIDYA', 'MODE_AMA', 'CMovSeriesTools', 'CMoving_Average', 'CStdDeviation', 'CJJMA', 'CT3', 'CJurX', 'CCMO', 'CAMA', 'CParMA', 'CMomentum', 'CnMomentum', 'CROC', 'CFATL', 'CSATL', 'CRFTL', 'CRSTL', 'CXMA', 'GetStartBars', 'PriceSeries', 'iPriceSeries', 'bPriceSeries', 'bPriceSeriesOnArray', 'iPriceSeriesAlert']
