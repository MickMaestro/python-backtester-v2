"""Ticks — converted from MQL5: MQL5 Indicators/Ticks indicator/Ticks.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.fxsaber_pointer import *  # #include Pointer.mqh
from backtester.mql5.lib.fxsaber_chartobjects_ticks_bars import *  # #include Bars.mqh
from backtester.mql5.lib.fxsaber_chartobjects_ticks_bar import *  # #include Bar.mqh
from backtester.mql5.lib.fxsaber_chartobjects_ticks_tick import *  # #include Tick.mqh

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Ticks', 'source': 'MQL5 Indicators/Ticks indicator/Ticks.mq5', 'folder': 'Ticks indicator', 'inputs': [{'mql': 'exColorBid', 'py': 'exColorBid', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет Bid', 'sinput': False}, {'mql': 'exColorAsk', 'py': 'exColorAsk', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет Ask', 'sinput': False}, {'mql': 'exColorSpread', 'py': 'exColorSpread', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет Spread', 'sinput': False}, {'mql': 'exTransparency', 'py': 'exTransparency', 'param': 'exTransparency', 'type': 'uchar', 'default': 127, 'label': 'Прозрачность (0 - 255)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Pointer.mqh', 'Bars.mqh', 'Bar.mqh', 'Tick.mqh']}

# enum ENUM_PRICE_TYPE
BID = 0
ASK = 1
AVG = 2
_enum('ENUM_PRICE_TYPE', {0: 'BID', 1: 'ASK', 2: 'AVG'})

# ---- inputs and global variables
exTransparency = _input('exTransparency', 0x7F)  # Прозрачность (0 - 255)

class EVENTBASE(MqlObject):
    _q_fields = ('EventCustom',)
    AllEventClasses = None
    TimerInterval = None
    EventCustoms = 0
    def __init__(self, Add=True):
        self.EventCustom = 0
        self.EventCustom = -1
        if Add:
            Pos = EVENTBASE.GetAllEventClassesSize(self)
            ArrayResize(EVENTBASE.AllEventClasses, Pos + 1)
            EVENTBASE.AllEventClasses[Pos] = self
            self.EventCustom = EVENTBASE.EventCustoms
            EVENTBASE.EventCustoms += 1
    def _q_dtor(self):
        ArrayResize(EVENTBASE.AllEventClasses, EVENTBASE.GetAllEventClassesSize(self))
    @staticmethod
    def GetAllEventClassesSize(This):
        Size = ArraySize(EVENTBASE.AllEventClasses)
        Pos = 0
        for i in range(0, Size):
            EVENTBASE.AllEventClasses[Pos] = EVENTBASE.AllEventClasses[i]
            if CheckPointer(EVENTBASE.AllEventClasses[i]) != POINTER_INVALID and EVENTBASE.AllEventClasses[i] != This:
                Pos += 1
        return Pos
    @staticmethod
    def CalcTimerInterval():
        global _s_EVENTBASE_CalcTimerInterval_PrevTime
        CurrTime = GetTickCount()
        EVENTBASE.TimerInterval = CurrTime - _s_EVENTBASE_CalcTimerInterval_PrevTime
        _s_EVENTBASE_CalcTimerInterval_PrevTime = CurrTime
        return
    def Event(self, id_, lparam, dparam, sparam):
        return
    def EventTick(self):
        return
    def EventTimer(self):
        return
    @staticmethod
    def MyEvent(id_, lparam, dparam, sparam):
        Size = ArraySize(EVENTBASE.AllEventClasses)
        for i in range(0, Size):
            if CheckPointer(EVENTBASE.AllEventClasses[i]) != POINTER_INVALID:
                EVENTBASE.AllEventClasses[i].Event(id_, lparam, dparam, sparam)
        return
    @staticmethod
    def MyEventTick():
        Size = ArraySize(EVENTBASE.AllEventClasses)
        for i in range(0, Size):
            if CheckPointer(EVENTBASE.AllEventClasses[i]) != POINTER_INVALID:
                EVENTBASE.AllEventClasses[i].EventTick()
        return
    @staticmethod
    def MyEventTimer():
        EVENTBASE.CalcTimerInterval()
        Size = ArraySize(EVENTBASE.AllEventClasses)
        for i in range(0, Size):
            if CheckPointer(EVENTBASE.AllEventClasses[i]) != POINTER_INVALID:
                EVENTBASE.AllEventClasses[i].EventTimer()
        return
    @staticmethod
    def GetTimerInterval():
        return EVENTBASE.TimerInterval
    def GetEventCustom(self):
        return _int(self.EventCustom + CHARTEVENT_CUSTOM)
    @staticmethod
    def GetEventCustoms():
        return EVENTBASE.EventCustoms
EVENTBASE.AllEventClasses = Arr(0, None)
EVENTBASE.TimerInterval = _uint(INT_MAX)

class CHARTOBJECT(EVENTBASE):
    _q_fields = ('Name', 'Chart', 'Type')
    def __init__(self, Add, chart_id, object_name, object_type, sub_window, time1, price1, time2=0, price2=0.0, time3=0, price3=0.0):
        EVENTBASE.__init__(self, Add)
        self.Name = ""
        self.Chart = 0
        self.Type = 0
        self.Name = object_name
        self.Chart = (ChartID() if (chart_id == 0) else chart_id)
        self.Type = object_type
        ObjectCreate(chart_id, object_name, object_type, sub_window, time1, price1, time2, price2, time3, price3)
    def _q_dtor(self):
        ObjectDelete(self.Chart, self.Name)
        CHARTOBJECT.Visual(self)
    def ChartXYToTimePrice(self, x, y, sub_window, time, price, Add=True):
        Res = x < CHARTOBJECT.GetProperty_1(self, _int(CHART_WIDTH_IN_PIXELS), sub_window.v)
        TmpTime = 0
        ChartXYToTimePrice(self.Chart, x, ((y - 1) if (y > 0) else (y + 1)), sub_window, _ValRef(TmpTime), price)
        ChartXYToTimePrice(self.Chart, x, y, sub_window, time, price)
        if (Res and TmpTime == time.v) and time.v > 0:
            if Add:
                time.v += PeriodSeconds(ChartPeriod(self.Chart)) >> 1
        else:
            time.v = 0
        return Res
    @staticmethod
    def IsMouseLeftDown(sparam):
        return (StringToInteger(sparam) & 1 != 0)
    @staticmethod
    def IsMouseShiftDown(sparam):
        return (StringToInteger(sparam) & 4 != 0)
    @staticmethod
    def TimeToString(uTime, mode=TIME_DATE | TIME_SECONDS):
        return TimeToString(_idiv(uTime, 1000), mode) + '.' + IntegerToString(_imod(uTime, 1000), 3, 48)
    def GetPrice(self, Num=0):
        return ObjectGetDouble(self.Chart, self.Name, OBJPROP_PRICE, Num)
    def GetTime(self, Num=0):
        return ObjectGetInteger(self.Chart, self.Name, OBJPROP_TIME, Num)
    def SetProperty_1(self, id_, Value, Modifier=0):
        return ObjectSetInteger(self.Chart, self.Name, id_, Modifier, Value)
    def SetProperty_2(self, id_, Value, Modifier=0):
        return ObjectSetDouble(self.Chart, self.Name, id_, Modifier, Value)
    def SetProperty_3(self, id_, Value, Modifier=0):
        return ObjectSetString(self.Chart, self.Name, id_, Modifier, Value)
    def SetProperty_4(self, id_, Value):
        return ChartSetInteger(self.Chart, id_, Value)
    def SetProperty_5(self, id_, Value):
        return ChartSetDouble(self.Chart, id_, Value)
    def SetProperty_6(self, id_, Value):
        return ChartSetString(self.Chart, id_, Value)
    def GetProperty_1(self, Property, Modifier=0):
        return ObjectGetInteger(self.Chart, self.Name, Property, Modifier)
    def GetProperty_2(self, Property, Modifier=0):
        return ObjectGetDouble(self.Chart, self.Name, Property, Modifier)
    def GetProperty_3(self, Property, Modifier=0):
        return ObjectGetString(self.Chart, self.Name, Property, Modifier)
    def GetProperty_4(self, Property, SubWindow=0):
        return ChartGetInteger(self.Chart, Property, self.GetSubWindow())
    def GetProperty_5(self, Property, SubWindow=0):
        return ChartGetDouble(self.Chart, Property, self.GetSubWindow())
    def GetProperty_1(self, Property):
        return ChartGetString(self.Chart, Property)
    def GetSubWindow(self):
        return ObjectFind(self.Chart, self.Name)
    def Comment(self, Str=''):
        CHARTOBJECT.SetProperty_6(self, _int(CHART_COMMENT), Str)
        return
    def GetXY(self, X, Y, Num=0):
        TmpX = 0
        Res = False
        _sw1 = self.Type
        if _sw1 == OBJ_HLINE:
            Res = ChartTimePriceToXY(self.Chart, self.GetSubWindow(), 0, self.GetPrice(Num), _ValRef(TmpX), Y)
        return Res
    def _q_assign(self, Value):
        return
    def _q_assign(self, Value):
        return
    def _q_assign(self, Value):
        return
    def _q_assign(self, Value):
        self.SetProperty_6(_int(OBJPROP_TEXT), Value)
        return
    def GetMe(self):
        return self
    def Visual(self):
        ChartRedraw(self.Chart)
        return

class RESOURCE(EVENTBASE):
    _q_fields = ('Name',)
    def __init__(self, Add=False):
        EVENTBASE.__init__(self, Add)
        self.Name = ""
        self.Name = '::' + _str(MathRand())
    def _q_dtor(self):
        ResourceFree(self.Name)
    def Set(self, Data, Width):
        return ResourceCreate(self.Name, Data, Width, (ArraySize(Data) if (Width == 0) else _idiv(ArraySize(Data), Width)), 0, 0, Width, COLOR_FORMAT_ARGB_NORMALIZE)

class CHARTOBJECTRESOURCE(CHARTOBJECT):
    _q_fields = ('Resource',)
    _q_ptrs = ('Resource',)
    def __init__(self, chart_id=0, sub_window=0, Add=False):
        CHARTOBJECT.__init__(self, Add, chart_id, _str(MathRand()), _int(OBJ_BITMAP_LABEL), sub_window, 0, 0.0)
        self.Resource = None
        self.Resource = RESOURCE()
        if CheckPointer(self.Resource) == POINTER_DYNAMIC:
            self = self.Resource.Name
        self.SetProperty_4(_int(OBJPROP_HIDDEN), True)
        self.SetProperty_4(_int(OBJPROP_SELECTABLE), False)
    def _q_dtor(self):
        POINTER.DeleteObject_1(self.Resource)
    def _q_assign(self, Value):
        self.SetProperty_6(_int(OBJPROP_BMPFILE), Value)
        return

class TICKSPICTURE(MqlObject):
    _q_fields = ('bars', 'Amount', 'PriceMin', 'PriceMax', 'WidthBar', 'X0', 'Y0', 'Width', 'Height', 'Step', 'Pixels')
    _q_ptrs = ('bars',)
    def __init__(self, Chart_ID, bBars, x0, y0):
        self.bars = None
        self.Amount = 0
        self.PriceMin = 0.0
        self.PriceMax = 0.0
        self.WidthBar = 0
        self.X0 = 0
        self.Y0 = 0
        self.Width = 0
        self.Height = 0
        self.Step = 0
        self.Pixels = Arr(0, 0)
        self.bars = bBars
        self.Amount = (0 if (CheckPointer(self.bars) == POINTER_INVALID) else self.bars.GetAmount())
        self.PriceMin = (self.bars.GetMin() if (self.Amount > 0) else 0)
        self.PriceMax = (self.bars.GetMax() if (self.Amount > 0) else 0)
        self.WidthBar = TICKSPICTURE.GetBarWidth(Chart_ID)
        self.X0 = ((TICKSPICTURE.PriceToX(_long(self.bars[0].time), Chart_ID) - (self.WidthBar >> 1)) if (self.Amount > 0) else 0)
        self.Y0 = TICKSPICTURE.PriceToY_2(self.PriceMax, Chart_ID)
        self.Width = self.WidthBar * self.Amount
        self.Height = TICKSPICTURE.PriceToY_2(self.PriceMin, Chart_ID) - self.Y0 + 1
        self.Step = _idiv(PeriodSeconds(ChartPeriod(Chart_ID)) * 1000, self.WidthBar)
        if self.Amount > 0:
            if ArrayResize(self.Pixels, self.Width * self.Height) > 0:
                ArrayFill(self.Pixels, 0, ArraySize(self.Pixels), 0)
        x0.v = self.X0
        y0.v = self.Y0
    @staticmethod
    def GetBarWidth(Chart_ID=0):
        return _int(1 << ChartGetInteger(Chart_ID, CHART_SCALE))
    @staticmethod
    def GetVisibleTime(Chart_ID=0):
        TmpTime = 0
        TmpPrice = 0.0
        TmpSubWindow = 0
        ChartXYToTimePrice(Chart_ID, 0, 0, _ValRef(TmpSubWindow), _ValRef(TmpTime), _ValRef(TmpPrice))
        return TmpTime
    @staticmethod
    def GetVisiblePrice(Chart_ID=0):
        return ChartGetDouble(Chart_ID, CHART_PRICE_MAX)
    @staticmethod
    def PriceToX(dtime, Chart_ID=0):
        X = 0
        Y = 0
        ChartTimePriceToXY(Chart_ID, 0, dtime, TICKSPICTURE.GetVisiblePrice(), _ValRef(X), _ValRef(Y))
        return X
    @staticmethod
    def PriceToY_2(Price, Chart_ID):
        X = 0
        Y = 0
        ChartTimePriceToXY(Chart_ID, 0, TICKSPICTURE.GetVisibleTime(Chart_ID), Price, _ValRef(X), _ValRef(Y))
        return Y
    def PriceToY_1(self, Price):
        return (0 if (self.PriceMax == self.PriceMin) else _int(_fdiv((self.PriceMax - Price) * (self.Height - 1), self.PriceMax - self.PriceMin)))
    def Fill(self, Color, PriceType=_int(BID)):
        AmountPixels = ArraySize(self.Pixels)
        if (self.Amount <= 0 or Color == 0) or AmountPixels < _uint(self.Width * self.Height):
            return
        Pos = 0
        high = DBL_MIN
        low = DBL_MAX
        PriceHigh = 0.0
        PriceLow = 0.0
        X = 0
        while X < self.Width:
            Bar = self.bars[_idiv(X, self.WidthBar)]
            Interval = (Bar.time * 1000) + (self.Step * _imod(X, self.WidthBar))
            Size = Bar.GetAmount()
            if _imod(X, self.WidthBar) == 0:
                Pos = 0
            while Pos < Size:
                if Bar[Pos].time > Interval:
                    break
                PriceLow = (Bar[Pos].ask if (PriceType == ASK) else Bar[Pos].bid)
                PriceHigh = (Bar[Pos].bid if (PriceType == BID) else Bar[Pos].ask)
                if PriceHigh > high:
                    high = PriceHigh
                if PriceLow < low:
                    low = PriceLow
                Pos += 1
            if PriceHigh != 0 and PriceLow != 0:
                MinY = self.PriceToY_1(high)
                MaxY = self.PriceToY_1(low)
                j = X + (MinY * self.Width)
                Y = MinY
                while Y <= MaxY and j < AmountPixels:
                    if PriceType != AVG:
                        self.Pixels[j] |= Color
                    elif self.Pixels[j] == 0:
                        self.Pixels[j] = Color
                    j += self.Width
                    Y += 1
                high = PriceHigh
                low = PriceLow
            X += 1
        return
    def SendToResource(self, Resource):
        return Resource.Set(self.Pixels, self.Width)

class CHARTOBJECTTICKS(CHARTOBJECTRESOURCE):
    _q_fields = ('ColorBid', 'ColorAsk', 'ColorSpread')
    def __init__(self, lChart_ID=0, cColorBid=_uint(clrBlue), cColorAsk=_uint(clrRed), cColorSpread=_uint(clrYellow), Transparency=0x7F):
        CHARTOBJECTRESOURCE.__init__(self, lChart_ID, 0, True)
        self.ColorBid = 0
        self.ColorAsk = 0
        self.ColorSpread = 0
        self.ColorBid = (0 if (cColorBid == clrNONE) else ColorToARGB(cColorBid, Transparency))
        self.ColorAsk = (0 if (cColorAsk == clrNONE) else ColorToARGB(cColorAsk, Transparency))
        self.ColorSpread = (0 if (cColorSpread == clrNONE) else ColorToARGB(cColorSpread, Transparency))
    def _q_dtor(self):
        Comment('')
        ChartRedraw()
    def Visual(self):
        StartTime = GetMicrosecondCount()
        X0 = 0
        Y0 = 0
        bars = BARS(self.Chart)
        TicksPicture = TICKSPICTURE(self.Chart, bars, _ValRef(X0), _ValRef(Y0))
        self.SetProperty_4(_int(OBJPROP_XDISTANCE), X0)
        self.SetProperty_4(_int(OBJPROP_YDISTANCE), Y0)
        TicksPicture.Fill(self.ColorBid, _int(BID))
        TicksPicture.Fill(self.ColorAsk, _int(ASK))
        TicksPicture.Fill(self.ColorSpread, _int(AVG))
        TicksPicture.SendToResource(self.Resource)
        Comment('LastCalcTime = ' + _str(TimeLocal()) + ', Ticks = ' + _str(bars.GetAmountTicks()) + ', CalcLength = ' + _str(_idiv(GetMicrosecondCount() - StartTime, 1000)) + ' ms.')
        ChartRedraw(self.Chart)
        return
    def Event(self, id_, lparam, dparam, sparam):
        if id_ == CHARTEVENT_CHART_CHANGE:
            self.Visual()
        return

def OnChartEvent(id_, lparam, dparam, sparam):
    EVENTBASE.MyEvent(id_, lparam, dparam, sparam)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR) <= ChartGetInteger(0, CHART_VISIBLE_BARS):
        ChartObject.Visual()
    return rates_total

# ---- global variables initialised from expressions
exColorBid = _input('exColorBid', _uint(clrBlue))  # Цвет Bid
exColorAsk = _input('exColorAsk', _uint(clrRed))  # Цвет Ask
exColorSpread = _input('exColorSpread', _uint(clrYellow))  # Цвет Spread
ChartObject = _alloc(CHARTOBJECTTICKS)
ChartObject.__init__(0, exColorBid, exColorAsk, exColorSpread, exTransparency)

# ---- static local variables
_s_EVENTBASE_CalcTimerInterval_PrevTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ticks(_MQL5Indicator):
    name = 'Ticks'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'exTransparency': 127,  # Прозрачность (0 - 255)
    }

