"""mycextremum.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh

# enum looling_for
Pike = 1
Sill = -1
_enum('looling_for', {1: 'Pike', -1: 'Sill'})


class MyCExtremum(CObject):
    _q_fields = ('HighMapBuffer', 'LowMapBuffer', 'ZigzagBuffer')
    def __init__(self):
        CObject.__init__(self)
        self.HighMapBuffer = Arr(0, 0.0)
        self.LowMapBuffer = Arr(0, 0.0)
        self.ZigzagBuffer = Arr(0, 0.0)
    def _q_dtor(self):
        pass
    def GetHighMapZigzag(self, in_, ExtDepth, ExtDeviation, ExtBackstep):
        shift = 0
        back = 0
        lasthigh = 0.0
        res = 0.0
        val = 0.0
        rates_total = ArrayRange(in_, 0)
        deviation = ExtDeviation * Point()
        if rates_total < 100:
            Print('MyCExtremum::GetHighMapZigzag', ' ERROR: the small size of the buffer!')
            return -1
        ArrayResize(self.HighMapBuffer, rates_total, 1000)
        ArrayFill(self.HighMapBuffer, 0, rates_total, 0.0)
        shift = ExtDepth
        for shift in range(shift, rates_total):
            val = in_[self.iHighest(in_, ExtDepth, shift)]
            if val == lasthigh:
                val = 0.0
            else:
                lasthigh = val
                if (val - in_[shift]) > deviation:
                    val = 0.0
                else:
                    back = 1
                    for back in range(back, ExtBackstep + 1):
                        res = self.HighMapBuffer[shift - back]
                        if res != 0 and res < val:
                            self.HighMapBuffer[shift - back] = 0.0
                    else:
                        back = _range_end(back, ExtBackstep + 1, 1)
            if in_[shift] == val:
                self.HighMapBuffer[shift] = val
            else:
                self.HighMapBuffer[shift] = 0.0
        else:
            shift = _range_end(shift, rates_total, 1)
        return rates_total
    def GetLowMapZigzag(self, in_, ExtDepth, ExtDeviation, ExtBackstep):
        shift = 0
        back = 0
        val = 0.0
        lastlow = 0.0
        res = 0.0
        rates_total = ArrayRange(in_, 0)
        deviation = ExtDeviation * Point()
        if rates_total < 100:
            Print('MyCExtremum::GetLowMapZigzag', ' ERROR: the small size of the buffer!')
            return -1
        ArrayResize(self.LowMapBuffer, rates_total, 1000)
        ArrayFill(self.LowMapBuffer, 0, rates_total, 0.0)
        shift = ExtDepth
        for shift in range(shift, rates_total):
            val = in_[self.iLowest(in_, ExtDepth, shift)]
            if val == lastlow:
                val = 0.0
            else:
                lastlow = val
                if (in_[shift] - val) > deviation:
                    val = 0.0
                else:
                    back = 1
                    for back in range(back, ExtBackstep + 1):
                        res = self.LowMapBuffer[shift - back]
                        if res != 0 and res > val:
                            self.LowMapBuffer[shift - back] = 0.0
                    else:
                        back = _range_end(back, ExtBackstep + 1, 1)
            if in_[shift] == val:
                self.LowMapBuffer[shift] = val
            else:
                self.LowMapBuffer[shift] = 0.0
        else:
            shift = _range_end(shift, rates_total, 1)
        return rates_total
    def GetClassicZigzag(self, high, low, ExtDepth, ExtDeviation, ExtBackstep):
        if ArrayIsSeries(high):
            ArraySetAsSeries(high, False)
        if ArrayIsSeries(low):
            ArraySetAsSeries(low, False)
        rates_total = ArrayRange(high, 0)
        if rates_total > ArrayRange(low, 0):
            rates_total = ArrayRange(low, 0)
        limit = rates_total - ExtDepth
        shift = 0
        whatlookfor = 0
        lasthighpos = 0
        lastlowpos = 0
        res = 0.0
        curlow = 0.0
        curhigh = 0.0
        lasthigh = 0.0
        lastlow = 0.0
        if rates_total < 100:
            Print('MyCExtremum::GetClassicZigzag', ' ERROR: the small size of the buffer!')
            return -1
        ArrayResize(self.ZigzagBuffer, rates_total, 1000)
        ArrayFill(self.ZigzagBuffer, 0, rates_total, 0.0)
        if self.GetHighMapZigzag(high, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        if self.GetLowMapZigzag(low, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        if whatlookfor == 0:
            lastlow = 0.0
            lasthigh = 0.0
        else:
            lastlow = curlow
            lasthigh = curhigh
        shift = ExtDepth
        for shift in range(shift, rates_total):
            res = 0.0
            _sw1 = whatlookfor
            if _sw1 == 0:
                if lastlow == 0 and lasthigh == 0:
                    if self.HighMapBuffer[shift] != 0:
                        lasthigh = high[shift]
                        lasthighpos = shift
                        whatlookfor = Sill
                        self.ZigzagBuffer[shift] = lasthigh
                        res = 1.0
                    if self.LowMapBuffer[shift] != 0:
                        lastlow = low[shift]
                        lastlowpos = shift
                        whatlookfor = Pike
                        self.ZigzagBuffer[shift] = lastlow
                        res = 1.0
            elif _sw1 == Pike:
                if (self.LowMapBuffer[shift] != 0.0 and self.LowMapBuffer[shift] < lastlow) and self.HighMapBuffer[shift] == 0.0:
                    self.ZigzagBuffer[lastlowpos] = 0.0
                    lastlowpos = shift
                    lastlow = self.LowMapBuffer[shift]
                    self.ZigzagBuffer[shift] = lastlow
                    res = 1.0
                if self.HighMapBuffer[shift] != 0.0 and self.LowMapBuffer[shift] == 0.0:
                    lasthigh = self.HighMapBuffer[shift]
                    lasthighpos = shift
                    self.ZigzagBuffer[shift] = lasthigh
                    whatlookfor = Sill
                    res = 1.0
            elif _sw1 == Sill:
                if (self.HighMapBuffer[shift] != 0.0 and self.HighMapBuffer[shift] > lasthigh) and self.LowMapBuffer[shift] == 0.0:
                    self.ZigzagBuffer[lasthighpos] = 0.0
                    lasthighpos = shift
                    lasthigh = self.HighMapBuffer[shift]
                    self.ZigzagBuffer[shift] = lasthigh
                if self.LowMapBuffer[shift] != 0.0 and self.HighMapBuffer[shift] == 0.0:
                    lastlow = self.LowMapBuffer[shift]
                    lastlowpos = shift
                    self.ZigzagBuffer[shift] = lastlow
                    whatlookfor = Pike
            else:
                self.CorrectMapClassicZigzag()
                return rates_total
        else:
            shift = _range_end(shift, rates_total, 1)
        self.CorrectMapClassicZigzag()
        return rates_total
    def _GetHighMapZigzag(self, in_, ExtDepth, ExtDeviation, ExtBackstep):
        shift = 0
        back = 0
        lasthigh = 0.0
        res = 0.0
        val = 0.0
        rates_total = ArrayRange(in_, 0)
        limit = rates_total - ExtDepth
        deviation = ExtDeviation * Point()
        if rates_total < 100:
            Print('MyCExtremum::_GetHighMapZigzag', ' ERROR: the small size of the buffer!')
            return -1
        ArrayResize(self.HighMapBuffer, rates_total, 1000)
        ArrayFill(self.HighMapBuffer, 0, rates_total, 0.0)
        shift = limit
        for shift in range(shift, 0 - 1, -1):
            val = in_[self.iHighest(in_, ExtDepth, shift)]
            if val == lasthigh:
                val = 0.0
            else:
                lasthigh = val
                if (val - in_[shift]) > deviation:
                    val = 0.0
                else:
                    back = 1
                    for back in range(back, ExtBackstep + 1):
                        res = self.HighMapBuffer[shift + back]
                        if res != 0 and res < val:
                            self.HighMapBuffer[shift + back] = 0.0
                    else:
                        back = _range_end(back, ExtBackstep + 1, 1)
            if in_[shift] == val:
                self.HighMapBuffer[shift + 1] = val
            else:
                self.HighMapBuffer[shift + 1] = 0.0
        else:
            shift = _range_end(shift, 0 - 1, -1)
        self.CorrectMapHigh(in_)
        return rates_total
    def _GetLowMapZigzag(self, in_, ExtDepth, ExtDeviation, ExtBackstep):
        shift = 0
        back = 0
        val = 0.0
        lastlow = 0.0
        res = 0.0
        rates_total = ArrayRange(in_, 0)
        limit = rates_total - ExtDepth
        deviation = ExtDeviation * Point()
        if rates_total < 100:
            Print('MyCExtremum::_GetLowMapZigzag', ' ERROR: the small size of the buffer!')
            return -1
        ArrayResize(self.LowMapBuffer, rates_total, 1000)
        ArrayFill(self.LowMapBuffer, 0, rates_total, 0.0)
        shift = limit
        for shift in range(shift, 0 - 1, -1):
            val = in_[self.iLowest(in_, ExtDepth, shift)]
            if val == lastlow:
                val = 0.0
            else:
                lastlow = val
                if (in_[shift] - val) > deviation:
                    val = 0.0
                else:
                    back = 1
                    for back in range(back, ExtBackstep + 1):
                        res = self.LowMapBuffer[shift + back]
                        if res != 0 and res > val:
                            self.LowMapBuffer[shift + back] = 0.0
                    else:
                        back = _range_end(back, ExtBackstep + 1, 1)
            if in_[shift] == val:
                self.LowMapBuffer[shift + 1] = val
            else:
                self.LowMapBuffer[shift + 1] = 0.0
        else:
            shift = _range_end(shift, 0 - 1, -1)
        self.CorrectMapLow(in_)
        return rates_total
    def GetModZigzag(self, high, low, ExtDepth, ExtDeviation, ExtBackstep):
        rates_total = ArrayRange(high, 0)
        if rates_total > ArrayRange(low, 0):
            rates_total = ArrayRange(low, 0)
        limit = rates_total - ExtDepth
        shift = 0
        whatlookfor = 0
        lasthighpos = 0
        lastlowpos = 0
        res = 0.0
        curlow = 0.0
        curhigh = 0.0
        lasthigh = 0.0
        lastlow = 0.0
        if rates_total < 100:
            Print('MyCExtremum::GetModZigzag', ' ERROR: the small size of the buffer!')
            return -1
        ArrayResize(self.ZigzagBuffer, rates_total, 1000)
        ArrayFill(self.ZigzagBuffer, 0, rates_total, 0.0)
        if self._GetHighMapZigzag(high, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        if self._GetLowMapZigzag(low, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        self.CorrectMapZigzag()
        if whatlookfor == 0:
            lastlow = 0.0
            lasthigh = 0.0
        else:
            lastlow = curlow
            lasthigh = curhigh
        shift = limit
        for shift in range(shift, 0 - 1, -1):
            res = 0.0
            _sw2 = whatlookfor
            if _sw2 == 0:
                if lastlow == 0 and lasthigh == 0:
                    if self.HighMapBuffer[shift] != 0:
                        lasthigh = high[shift]
                        lasthighpos = shift
                        whatlookfor = Sill
                        self.ZigzagBuffer[shift] = lasthigh
                        res = 1.0
                    if self.LowMapBuffer[shift] != 0:
                        lastlow = low[shift]
                        lastlowpos = shift
                        whatlookfor = Pike
                        self.ZigzagBuffer[shift] = lastlow
                        res = 1.0
            elif _sw2 == Pike:
                if (self.LowMapBuffer[shift] != 0.0 and self.LowMapBuffer[shift] < lastlow) and self.HighMapBuffer[shift] == 0.0:
                    self.ZigzagBuffer[lastlowpos] = 0.0
                    lastlowpos = shift
                    lastlow = self.LowMapBuffer[shift]
                    self.ZigzagBuffer[shift] = lastlow
                    res = 1.0
                if self.HighMapBuffer[shift] != 0.0 and self.LowMapBuffer[shift] == 0.0:
                    lasthigh = self.HighMapBuffer[shift]
                    lasthighpos = shift
                    self.ZigzagBuffer[shift] = lasthigh
                    whatlookfor = Sill
                    res = 1.0
            elif _sw2 == Sill:
                if (self.HighMapBuffer[shift] != 0.0 and self.HighMapBuffer[shift] > lasthigh) and self.LowMapBuffer[shift] == 0.0:
                    self.ZigzagBuffer[lasthighpos] = 0.0
                    lasthighpos = shift
                    lasthigh = self.HighMapBuffer[shift]
                    self.ZigzagBuffer[shift] = lasthigh
                if self.LowMapBuffer[shift] != 0.0 and self.HighMapBuffer[shift] == 0.0:
                    lastlow = self.LowMapBuffer[shift]
                    lastlowpos = shift
                    self.ZigzagBuffer[shift] = lastlow
                    whatlookfor = Pike
            else:
                return rates_total
        else:
            shift = _range_end(shift, 0 - 1, -1)
        return rates_total
    def iHighest(self, array, depth, startPos):
        index = startPos
        if startPos < 0:
            Print('MyCExtremum::iHighest', ' ERROR: Invalid parameter in the function iHighest(...)')
            return 0
        if (startPos - depth) < 0:
            depth = startPos
        max_ = array[startPos]
        for i in range(startPos, startPos - depth, -1):
            if array[i] > max_:
                index = i
                max_ = array[i]
        return index
    def iLowest(self, array, depth, startPos):
        index = startPos
        if startPos < 0:
            Print('MyCExtremum::iLowest', ' ERROR: Invalid parameter in the function iLowest(...)')
            return 0
        if (startPos - depth) < 0:
            depth = startPos
        min_ = array[startPos]
        for i in range(startPos, startPos - depth, -1):
            if array[i] < min_:
                index = i
                min_ = array[i]
        return index
    def CorrectMapHigh(self, in_):
        rates_total = ArrayRange(self.HighMapBuffer, 0)
        for i in range(0, rates_total):
            if self.HighMapBuffer[i] != 0:
                self.HighMapBuffer[i] = in_[i]
    def CorrectMapLow(self, in_):
        rates_total = ArrayRange(self.LowMapBuffer, 0)
        for i in range(0, rates_total):
            if self.LowMapBuffer[i] != 0:
                self.LowMapBuffer[i] = in_[i]
    def CorrectMapZigzag(self):
        rates_total = ArrayRange(self.HighMapBuffer, 0)
        for i in range(0, rates_total):
            if self.HighMapBuffer[i] != 0 and self.LowMapBuffer[i] != 0:
                self.HighMapBuffer[i] = 0.0
                self.LowMapBuffer[i] = 0.0
    def CorrectMapClassicZigzag(self):
        rates_total = ArrayRange(self.ZigzagBuffer, 0)
        for i in range(0, rates_total - 1):
            if self.ZigzagBuffer[i] != 0:
                if self.LowMapBuffer[i] != 0:
                    for a in range(i, 0, -1):
                        if self.HighMapBuffer[a] != 0:
                            self.ZigzagBuffer[a] = self.HighMapBuffer[a]
                            return
                    return
                if self.HighMapBuffer[i] != 0:
                    for a in range(i, 0, -1):
                        if self.LowMapBuffer[a] != 0:
                            self.ZigzagBuffer[a] = self.LowMapBuffer[a]
                            return
                    return

__all__ = ['Pike', 'Sill', 'MyCExtremum']
