"""jma — converted from MQL5: MQL5 Indicators/Background_JMACandle_HTF/jma.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JMA'}, 'levels': [], 'description': [], 'name': 'jma', 'source': 'MQL5 Indicators/Background_JMACandle_HTF/jma.mq5', 'folder': 'Background_JMACandle_HTF', 'inputs': [{'mql': 'Length_', 'py': 'Length_', 'param': 'Length_', 'type': 'int', 'default': 7, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Length_ = _input('Length_', 7)  # Глубина сглаживания
Phase_ = _input('Phase_', 100)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
m_start = False
m_array = Arr(62, 0.0, dyn=False)
m_degree = 0.0
m_Phase = 0.0
m_sense = 0.0
m_Krx = 0.0
m_Kfd = 0.0
m_Krj = 0.0
m_Kct = 0.0
m_var1 = 0.0
m_var2 = 0.0
m_pos2 = 0
m_pos1 = 0
m_Loop1 = 0
m_Loop2 = 0
m_midd1 = 0
m_midd2 = 0
m_count1 = 0
m_count2 = 0
m_count3 = 0
m_ser1 = 0.0
m_ser2 = 0.0
m_Sum1 = 0.0
m_Sum2 = 0.0
m_JMA = 0.0
m_storage1 = 0.0
m_storage2 = 0.0
m_djma = 0.0
m_hoop1 = Arr(128, 0.0, dyn=False)
m_hoop2 = Arr(11, 0.0, dyn=False)
m_data = Arr(128, 0.0, dyn=False)
m_pos2_ = 0
m_pos1_ = 0
m_Loop1_ = 0
m_Loop2_ = 0
m_midd1_ = 0
m_midd2_ = 0
m_count1_ = 0
m_count2_ = 0
m_count3_ = 0
m_ser1_ = 0.0
m_ser2_ = 0.0
m_Sum1_ = 0.0
m_Sum2_ = 0.0
m_JMA_ = 0.0
m_storage1_ = 0.0
m_storage2_ = 0.0
m_djma_ = 0.0
m_hoop1_ = Arr(128, 0.0, dyn=False)
m_hoop2_ = Arr(11, 0.0, dyn=False)
m_data_ = Arr(128, 0.0, dyn=False)
m_bhoop1 = Arr(128, False, dyn=False)
m_bhoop2 = Arr(11, False, dyn=False)
m_bdata = Arr(128, False, dyn=False)

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = 30 + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JMA( Length = ', Length_, ', Phase = ', Phase_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_JMA, m_JMA_, m_Loop1, m_Loop1_, m_Loop2, m_Loop2_, m_Sum1, m_Sum1_, m_Sum2, m_Sum2_, m_count1, m_count1_, m_count2, m_count2_, m_count3, m_count3_, m_djma, m_djma_, m_midd1, m_midd1_, m_midd2, m_midd2_, m_pos1, m_pos1_, m_pos2, m_pos2_, m_sense, m_ser1, m_ser1_, m_ser2, m_ser2_, m_start, m_storage1, m_storage1_, m_storage2, m_storage2_, m_var1, m_var2
    if rates_total < min_rates_total:
        return 0
    posA = 0
    posB = 0
    back = 0
    first = 0
    bar = 0
    shift2 = 0
    shift1 = 0
    numb = 0
    Res = 0.0
    ResPow = 0.0
    dser3 = 0.0
    dser4 = 0.0
    jjma = 0.0
    series = 0.0
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
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        JJMAInit(Phase_, Length_, PriceSeries(IPC, 0, open, low, high, close))
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        if m_Loop1 < 61:
            m_Loop1 += 1
            m_array[m_Loop1] = series
        if m_Loop1 > 30:
            if not m_start:
                m_start = True
                shift1 = 1
                back = 29
                m_ser2 = m_array[1]
                m_ser1 = m_ser2
            else:
                back = 0
            for rrr in range(back, 0 - 1, -1):
                if rrr == 0:
                    ser0 = series
                else:
                    ser0 = m_array[31 - rrr]
                dser1 = ser0 - m_ser1
                dser2 = ser0 - m_ser2
                if MathAbs(dser1) > MathAbs(dser2):
                    m_var2 = MathAbs(dser1)
                else:
                    m_var2 = MathAbs(dser2)
                Res = m_var2
                newvel = Res + 1e-10
                if m_count1 <= 1:
                    m_count1 = 127
                else:
                    m_count1 -= 1
                if m_count2 <= 1:
                    m_count2 = 10
                else:
                    m_count2 -= 1
                if m_count3 < 128:
                    m_count3 += 1
                m_Sum1 += newvel - m_hoop2[m_count2]
                m_hoop2[m_count2] = newvel
                m_bhoop2[m_count2] = True
                if m_count3 > 10:
                    SmVel = m_Sum1 / 10.0
                else:
                    SmVel = _fdiv(m_Sum1, m_count3)
                if m_count3 > 127:
                    hoop1 = m_hoop1[m_count1]
                    m_hoop1[m_count1] = SmVel
                    m_bhoop1[m_count1] = True
                    numb = 64
                    posB = numb
                    while numb > 1:
                        if m_data[posB] < hoop1:
                            numb = _int(numb / 2.0)
                            posB += numb
                        elif m_data[posB] <= hoop1:
                            numb = 1
                        else:
                            numb = _int(numb / 2.0)
                            posB -= numb
                else:
                    m_hoop1[m_count1] = SmVel
                    m_bhoop1[m_count1] = True
                    if (m_midd1 + m_midd2) > 127:
                        m_midd2 -= 1
                        posB = m_midd2
                    else:
                        m_midd1 += 1
                        posB = m_midd1
                    if m_midd1 > 96:
                        m_pos2 = 96
                    else:
                        m_pos2 = m_midd1
                    if m_midd2 < 32:
                        m_pos1 = 32
                    else:
                        m_pos1 = m_midd2
                numb = 64
                posA = numb
                while numb > 1:
                    if m_data[posA] >= SmVel:
                        if m_data[posA - 1] <= SmVel:
                            numb = 1
                        else:
                            numb = _int(numb / 2.0)
                            posA -= numb
                    else:
                        numb = _int(numb / 2.0)
                        posA += numb
                    if posA == 127:
                        if SmVel > m_data[127]:
                            posA = 128
                if m_count3 > 127:
                    if posB >= posA:
                        if (m_pos2 + 1) > posA:
                            if (m_pos1 - 1) < posA:
                                m_Sum2 += SmVel
                            elif (m_pos1 + 0) > posA:
                                if (m_pos1 - 1) < posB:
                                    m_Sum2 += m_data[m_pos1 - 1]
                    elif m_pos1 >= posA:
                        if (m_pos2 + 1) < posA:
                            if (m_pos2 + 1) > posB:
                                m_Sum2 += m_data[m_pos2 + 1]
                    elif (m_pos2 + 2) > posA:
                        m_Sum2 += SmVel
                    elif (m_pos2 + 1) < posA:
                        if (m_pos2 + 1) > posB:
                            m_Sum2 += m_data[m_pos2 + 1]
                    if posB > posA:
                        if (m_pos1 - 1) < posB:
                            if (m_pos2 + 1) > posB:
                                m_Sum2 -= m_data[posB]
                            elif m_pos2 < posB:
                                if (m_pos2 + 1) > posA:
                                    m_Sum2 -= m_data[m_pos2]
                    else:
                        if (m_pos2 + 1) > posB and (m_pos1 - 1) < posB:
                            m_Sum2 -= m_data[posB]
                        elif (m_pos1 + 0) > posB:
                            if (m_pos1 - 0) < posA:
                                m_Sum2 -= m_data[m_pos1]
                if posB <= posA:
                    if posB == posA:
                        m_data[posA] = SmVel
                        m_bdata[posA] = True
                    else:
                        numb = posB + 1
                        for numb in range(numb, posA - 1 + 1):
                            m_data[numb - 1] = m_data[numb]
                            m_bdata[numb - 1] = True
                        else:
                            numb = _range_end(numb, posA - 1 + 1, 1)
                        m_data[posA - 1] = SmVel
                        m_bdata[posA - 1] = True
                else:
                    numb = posB - 1
                    for numb in range(numb, posA - 1, -1):
                        m_data[numb + 1] = m_data[numb]
                        m_bdata[numb + 1] = True
                    else:
                        numb = _range_end(numb, posA - 1, -1)
                    m_data[posA] = SmVel
                    m_bdata[posA] = True
                if m_count3 <= 127:
                    m_Sum2 = 0.0
                    numb = m_pos1
                    for numb in range(numb, m_pos2 + 1):
                        m_Sum2 += m_data[numb]
                    else:
                        numb = _range_end(numb, m_pos2 + 1, 1)
                resalt = _fdiv(m_Sum2, m_pos2 - m_pos1 + 1.0)
                if m_Loop2 > 30:
                    m_Loop2 = 31
                else:
                    m_Loop2 += 1
                if m_Loop2 <= 30:
                    if dser1 > 0.0:
                        m_ser1 = ser0
                    else:
                        m_ser1 = ser0 - (dser1 * m_Kct)
                    if dser2 < 0.0:
                        m_ser2 = ser0
                    else:
                        m_ser2 = ser0 - (dser2 * m_Kct)
                    m_JMA = series
                    if m_Loop2 != 30:
                        continue
                    else:
                        m_storage1 = series
                        if MathCeil(m_Krx) >= 1:
                            dSupr = MathCeil(m_Krx)
                        else:
                            dSupr = 1.0
                        if dSupr > 0:
                            Suprem2 = MathFloor(dSupr)
                        else:
                            if dSupr < 0:
                                Suprem2 = MathCeil(dSupr)
                            else:
                                Suprem2 = 0.0
                        if MathFloor(m_Krx) >= 1:
                            m_var2 = MathFloor(m_Krx)
                        else:
                            m_var2 = 1.0
                        if m_var2 > 0:
                            Suprem1 = MathFloor(m_var2)
                        else:
                            if m_var2 < 0:
                                Suprem1 = MathCeil(m_var2)
                            else:
                                Suprem1 = 0.0
                        if Suprem2 == Suprem1:
                            factor = 1.0
                        else:
                            dSupr = Suprem2 - Suprem1
                            factor = _fdiv(m_Krx - Suprem1, dSupr)
                        if Suprem1 <= 29:
                            shift1 = _int(Suprem1)
                        else:
                            shift1 = 29
                        if Suprem2 <= 29:
                            shift2 = _int(Suprem2)
                        else:
                            shift2 = 29
                        dser3 = series - m_array[m_Loop1 - shift1]
                        dser4 = series - m_array[m_Loop1 - shift2]
                        m_djma = _fdiv(dser3 * (1.0 - factor), Suprem1) + _fdiv(dser4 * factor, Suprem2)
                else:
                    ResPow = MathPow(_fdiv(Res, resalt), m_degree)
                    if m_Kfd >= ResPow:
                        m_var1 = ResPow
                    else:
                        m_var1 = m_Kfd
                    if m_var1 < 1.0:
                        m_var2 = 1.0
                    else:
                        if m_Kfd >= ResPow:
                            m_sense = ResPow
                        else:
                            m_sense = m_Kfd
                        m_var2 = m_sense
                    extent = m_var2
                    Pow1 = MathPow(m_Kct, MathSqrt(extent))
                    if dser1 > 0.0:
                        m_ser1 = ser0
                    else:
                        m_ser1 = ser0 - (dser1 * Pow1)
                    if dser2 < 0.0:
                        m_ser2 = ser0
                    else:
                        m_ser2 = ser0 - (dser2 * Pow1)
            if m_Loop2 > 30:
                Pow2 = MathPow(m_Krj, extent)
                m_storage1 *= Pow2
                m_storage1 += (1.0 - Pow2) * series
                m_storage2 *= m_Krj
                m_storage2 += (series - m_storage1) * (1.0 - m_Krj)
                Extr = (m_Phase * m_storage2) + m_storage1
                Pow2x2 = Pow2 * Pow2
                ratio = Pow2x2 - (2.0 * Pow2) + 1.0
                m_djma *= Pow2x2
                m_djma += (Extr - m_JMA) * ratio
                m_JMA += m_djma
        if m_Loop1 <= 30:
            continue
        jjma = m_JMA
        if bar == (rates_total - 1):
            numb = 0
            for numb in range(numb, 128):
                if m_bhoop1[numb]:
                    m_hoop1[numb] = m_hoop1_[numb]
            else:
                numb = _range_end(numb, 128, 1)
            numb = 0
            for numb in range(numb, 11):
                if m_bhoop2[numb]:
                    m_hoop2[numb] = m_hoop2_[numb]
            else:
                numb = _range_end(numb, 11, 1)
            numb = 0
            for numb in range(numb, 128):
                if m_bdata[numb]:
                    m_data[numb] = m_data_[numb]
            else:
                numb = _range_end(numb, 128, 1)
            ArrayInitialize(m_bhoop1, False)
            ArrayInitialize(m_bhoop2, False)
            ArrayInitialize(m_bdata, False)
            m_JMA = m_JMA_
            m_djma = m_djma_
            m_ser1 = m_ser1_
            m_ser2 = m_ser2_
            m_Sum2 = m_Sum2_
            m_pos1 = m_pos1_
            m_pos2 = m_pos2_
            m_Sum1 = m_Sum1_
            m_Loop1 = m_Loop1_
            m_Loop2 = m_Loop2_
            m_count1 = m_count1_
            m_count2 = m_count2_
            m_count3 = m_count3_
            m_storage1 = m_storage1_
            m_storage2 = m_storage2_
            m_midd1 = m_midd1_
            m_midd2 = m_midd2_
        if bar == (rates_total - 2):
            numb = 0
            for numb in range(numb, 128):
                if m_bhoop1[numb]:
                    m_hoop1_[numb] = m_hoop1[numb]
            else:
                numb = _range_end(numb, 128, 1)
            numb = 0
            for numb in range(numb, 11):
                if m_bhoop2[numb]:
                    m_hoop2_[numb] = m_hoop2[numb]
            else:
                numb = _range_end(numb, 11, 1)
            numb = 0
            for numb in range(numb, 128):
                if m_bdata[numb]:
                    m_data_[numb] = m_data[numb]
            else:
                numb = _range_end(numb, 128, 1)
            ArrayInitialize(m_bhoop1, False)
            ArrayInitialize(m_bhoop2, False)
            ArrayInitialize(m_bdata, False)
            m_JMA_ = m_JMA
            m_djma_ = m_djma
            m_Sum2_ = m_Sum2
            m_ser1_ = m_ser1
            m_ser2_ = m_ser2
            m_pos1_ = m_pos1
            m_pos2_ = m_pos2
            m_Sum1_ = m_Sum1
            m_Loop1_ = m_Loop1
            m_Loop2_ = m_Loop2
            m_count1_ = m_count1
            m_count2_ = m_count2
            m_count3_ = m_count3
            m_storage1_ = m_storage1
            m_storage2_ = m_storage2
            m_midd1_ = m_midd1
            m_midd2_ = m_midd2
        IndBuffer[bar] = jjma + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def JJMAInit(Phase, Length, series):
    global m_JMA, m_Kct, m_Kfd, m_Krj, m_Krx, m_Loop1, m_Loop2, m_Phase, m_Sum1, m_Sum2, m_count1, m_count2, m_count3, m_degree, m_djma, m_midd1, m_midd2, m_pos1, m_pos2, m_sense, m_ser1, m_ser2, m_start, m_storage1, m_storage2, m_var1, m_var2
    m_midd1 = 63
    m_midd2 = 64
    m_start = False
    for numb in range(0, m_midd1 + 1):
        m_data[numb] = -1000000.0
    for numb in range(m_midd2, 127 + 1):
        m_data[numb] = 1000000.0
    ArrayInitialize(m_bhoop1, True)
    ArrayInitialize(m_bhoop2, True)
    ArrayInitialize(m_bdata, True)
    ArrayInitialize(m_hoop1_, 0.0)
    ArrayInitialize(m_hoop2_, 0.0)
    ArrayInitialize(m_hoop1, 0.0)
    ArrayInitialize(m_hoop2, 0.0)
    ArrayInitialize(m_array, 0.0)
    m_djma = 0.0
    m_Sum1 = 0.0
    m_Sum2 = 0.0
    m_ser1 = 0.0
    m_ser2 = 0.0
    m_pos1 = _int(0.0)
    m_pos2 = _int(0.0)
    m_Loop1 = _int(0.0)
    m_Loop2 = _int(0.0)
    m_count1 = _int(0.0)
    m_count2 = _int(0.0)
    m_count3 = _int(0.0)
    m_storage1 = 0.0
    m_storage2 = 0.0
    m_JMA = series
    if Phase >= -100 and Phase <= 100:
        m_Phase = (Phase / 100.0) + 1.5
    if Phase > 100:
        m_Phase = 2.5
    if Phase < -100:
        m_Phase = 0.5
    velA = 0.0
    velB = 0.0
    velC = 0.0
    velD = 0.0
    if Length >= 1.0000000002:
        velA = (Length - 1.0) / 2.0
    else:
        velA = 1e-10
    velA *= 0.9
    m_Krj = _fdiv(velA, velA + 2.0)
    velC = MathSqrt(velA)
    velD = MathLog(velC)
    m_var1 = velD
    m_var2 = m_var1
    velB = MathLog(2.0)
    m_sense = _fdiv(m_var2, velB) + 2.0
    if m_sense < 0.0:
        m_sense = 0.0
    m_Kfd = m_sense
    if m_Kfd >= 2.5:
        m_degree = m_Kfd - 2.0
    else:
        m_degree = 0.5
    m_Krx = velC * m_Kfd
    m_Kct = _fdiv(m_Krx, m_Krx + 1.0)

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jma(_MQL5Indicator):
    name = 'jma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length_': 7,  # Глубина сглаживания
        'Phase_': 100,  # Параметр сглаживания
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

