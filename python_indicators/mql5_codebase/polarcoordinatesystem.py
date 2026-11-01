"""PolarCoordinateSystem — converted from MQL5: MQL5 Indicators/Price in polar coordinate system/PolarCoordinateSystem.mq5

Copyright: Copyright 2018, Nikolai Semko; Link: SemkoNV@bk.ru; Version: 1.35

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: FileReadFloat, FileReadLong, FileReadStruct, FileWriteFloat, FileWriteLong, FileWriteStruct, FolderClean, FolderDelete
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.controls_rect import *  # #include Rect.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, Nikolai Semko', 'link': 'SemkoNV@bk.ru', 'version': '1.35', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'PolarCoordinateSystem', 'source': 'MQL5 Indicators/Price in polar coordinate system/PolarCoordinateSystem.mq5', 'folder': 'Price in polar coordinate system', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh', 'Rect.mqh']}

# enum ENUM_LINE_END
LINE_END_ROUND = 0
LINE_END_BUTT = 1
LINE_END_SQUARE = 2
_enum('ENUM_LINE_END', {0: 'LINE_END_ROUND', 1: 'LINE_END_BUTT', 2: 'LINE_END_SQUARE'})

# enum mouse_status
NO_PRESSED = 0
LEFT_BUTTON_PRESSED = 1
RIGHT_BUTTON_PRESSED = 2
LEFT_AND_RIGHT_BUTTONS_PRESSED = 3
KEY_PRESSED = 4
_enum('mouse_status', {0: 'NO_PRESSED', 1: 'LEFT_BUTTON_PRESSED', 2: 'RIGHT_BUTTON_PRESSED', 3: 'LEFT_AND_RIGHT_BUTTONS_PRESSED', 4: 'KEY_PRESSED'})

# ---- inputs and global variables
OnChart = False  # Sign of the presence in the program's body of the OnChartEvent event handler
OnZ = True
WidOld = 0
HeiOld = Arr(0, 0)
sizeArr = 0
StartBar = -1
iC = Arr(0, None)
cl = Arr(0, 0.0)
ti = Arr(0, 0)
per = 0
N = 0.3
day = False
mouse = True
min_ = 0.0
max_ = 0.0
start = 0

class CFile(CObject):
    _q_fields = ('m_handle', 'm_name', 'm_flags')
    def __init__(self):
        CObject.__init__(self)
        self.m_handle = 0
        self.m_name = ""
        self.m_flags = 0
        self.m_handle = INVALID_HANDLE
        self.m_name = ''
        self.m_flags = FILE_ANSI
    def _q_dtor(self):
        if self.m_handle != INVALID_HANDLE:
            self.Close()
    def Handle(self):
        return self.m_handle
    def FileName(self):
        return self.m_name
    def Flags(self):
        return self.m_flags
    def SetUnicode(self, unicode):
        if self.m_handle == INVALID_HANDLE:
            if unicode:
                self.m_flags |= FILE_UNICODE
            else:
                self.m_flags &= ~FILE_UNICODE
    def SetCommon(self, common):
        if self.m_handle == INVALID_HANDLE:
            if common:
                self.m_flags |= FILE_COMMON
            else:
                self.m_flags &= ~FILE_COMMON
    def Open(self, file_name, open_flags, delimiter=9):
        if self.m_handle != INVALID_HANDLE:
            self.Close()
        if (open_flags & (FILE_BIN | FILE_CSV)) == 0:
            open_flags |= FILE_TXT
        self.m_handle = FileOpen(file_name, open_flags | self.m_flags, delimiter)
        if self.m_handle != INVALID_HANDLE:
            self.m_flags |= open_flags
            self.m_name = file_name
        return self.m_handle
    def Close(self):
        if self.m_handle != INVALID_HANDLE:
            FileClose(self.m_handle)
            self.m_handle = INVALID_HANDLE
            self.m_name = ''
            self.m_flags &= FILE_ANSI | FILE_UNICODE
    def Delete_0(self):
        if self.m_handle != INVALID_HANDLE:
            file_name = self.m_name
            common_flag = self.m_flags & FILE_COMMON
            self.Close()
            FileDelete(file_name, common_flag)
    def Delete_2(self, file_name, common_flag=0):
        if file_name == self.m_name:
            flag = self.m_flags & FILE_COMMON
            if flag == common_flag:
                self.Close()
        FileDelete(file_name, common_flag)
    def Size(self):
        if self.m_handle != INVALID_HANDLE:
            return FileSize(self.m_handle)
        return 0
    def Tell(self):
        if self.m_handle != INVALID_HANDLE:
            return FileTell(self.m_handle)
        return 0
    def Seek(self, offset, origin):
        if self.m_handle != INVALID_HANDLE:
            FileSeek(self.m_handle, offset, origin)
    def Flush(self):
        if self.m_handle != INVALID_HANDLE:
            FileFlush(self.m_handle)
    def IsEnding(self):
        if self.m_handle != INVALID_HANDLE:
            return FileIsEnding(self.m_handle)
        return False
    def IsLineEnding(self):
        if self.m_handle != INVALID_HANDLE:
            if (self.m_flags & FILE_BIN) == 0:
                return FileIsLineEnding(self.m_handle)
        return False
    def IsExist(self, file_name, common_flag=0):
        return FileIsExist(file_name, common_flag)
    def Copy(self, src_name, common_flag, dst_name, mode_flags):
        return _bool(FileCopy(src_name, common_flag, dst_name, mode_flags))
    def Move(self, src_name, common_flag, dst_name, mode_flags):
        return _bool(FileMove(src_name, common_flag, dst_name, mode_flags))
    def FolderCreate(self, folder_name):
        return FolderCreate(folder_name, self.m_flags)
    def FolderDelete(self, folder_name):
        return _bool(_missing('FolderDelete')(folder_name, self.m_flags))
    def FolderClean(self, folder_name):
        return _bool(_missing('FolderClean')(folder_name, self.m_flags))
    def FileFindFirst(self, file_filter, returned_filename):
        return FileFindFirst(file_filter, returned_filename.v, self.m_flags)
    def FileFindNext(self, search_handle, returned_filename):
        return FileFindNext(search_handle, returned_filename.v)
    def FileFindClose(self, search_handle):
        FileFindClose(search_handle)

class CFileBin(CFile):
    _q_fields = ()
    def __init__(self):
        CFile.__init__(self)
    def _q_dtor(self):
        pass
    def Open(self, file_name, open_flags):
        return CFile.Open(self, file_name, open_flags | FILE_BIN)
    def WriteChar(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteInteger(self.m_handle, value, 1)
        return 0
    def WriteShort(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteInteger(self.m_handle, value, 2)
        return 0
    def WriteInteger(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteInteger(self.m_handle, value, 4)
        return 0
    def WriteLong(self, value):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileWriteLong')(self.m_handle, value))
        return 0
    def WriteFloat(self, value):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileWriteFloat')(self.m_handle, value))
        return 0
    def WriteDouble(self, value):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteDouble(self.m_handle, value)
        return 0
    def WriteString_1(self, value):
        if self.m_handle != INVALID_HANDLE:
            size = StringLen(value)
            if FileWriteInteger(self.m_handle, size) == 4:
                return FileWriteString(self.m_handle, value, size)
        return 0
    def WriteString_2(self, value, size):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteString(self.m_handle, value, size)
        return 0
    def WriteCharArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteShortArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteIntegerArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteLongArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteFloatArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteDoubleArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileWriteArray(self.m_handle, array, start_item, items_count)
        return 0
    def WriteStruct(self, data):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileWriteStruct')(self.m_handle, data.v))
        return 0
    def WriteObject(self, object_):
        if self.m_handle != INVALID_HANDLE:
            if CheckPointer(object_):
                return object_.Save(self.m_handle)
        return False
    def WriteEnum(self, value):
        return self.WriteInteger(_int(value))
    def ReadChar(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _char(FileReadInteger(self.m_handle, 1))
            return GetLastError() == 0
        return False
    def ReadShort(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _short(FileReadInteger(self.m_handle, 2))
            return GetLastError() == 0
        return False
    def ReadInteger(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = FileReadInteger(self.m_handle, 4)
            return GetLastError() == 0
        return False
    def ReadLong(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _long(_missing('FileReadLong')(self.m_handle))
            return GetLastError() == 0
        return False
    def ReadFloat(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = _missing('FileReadFloat')(self.m_handle)
            return GetLastError() == 0
        return False
    def ReadDouble(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            value.v = FileReadDouble(self.m_handle)
            return GetLastError() == 0
        return False
    def ReadString_1(self, value):
        if self.m_handle != INVALID_HANDLE:
            ResetLastError()
            size = FileReadInteger(self.m_handle)
            if GetLastError() == 0:
                value.v = FileReadString(self.m_handle, size)
                return size == StringLen(value.v)
        return False
    def ReadString_2(self, value, size):
        if self.m_handle != INVALID_HANDLE:
            value.v = FileReadString(self.m_handle, size)
            return size == StringLen(value.v)
        return False
    def ReadCharArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadShortArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadIntegerArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadLongArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadFloatArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadDoubleArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadArray(self, array, start_item=0, items_count=WHOLE_ARRAY):
        if self.m_handle != INVALID_HANDLE:
            return FileReadArray(self.m_handle, array, start_item, items_count)
        return 0
    def ReadStruct(self, data):
        if self.m_handle != INVALID_HANDLE:
            return _uint(_missing('FileReadStruct')(self.m_handle, data.v))
        return 0
    def ReadObject(self, object_):
        if self.m_handle != INVALID_HANDLE:
            if CheckPointer(object_):
                return object_.Load(self.m_handle)
        return False
    def ReadEnum(self, value):
        val = Box(0)
        if not self.ReadInteger(val):
            return False
        value.v = val.v
        return True

class CCanvas(MqlObject):
    _q_fields = ('m_style', 'm_style_idx', 'm_chart_id', 'm_objname', 'm_objtype', 'm_rcname', 'm_width', 'm_height', 'm_format', 'm_fontname', 'm_fontsize', 'm_fontflags', 'm_fontangle', 'm_pixels')
    m_default_colors = None
    def __init__(self):
        self.m_style = 0
        self.m_style_idx = 0
        self.m_chart_id = 0
        self.m_objname = ""
        self.m_objtype = 0
        self.m_rcname = ""
        self.m_width = 0
        self.m_height = 0
        self.m_format = 0
        self.m_fontname = ""
        self.m_fontsize = 0
        self.m_fontflags = 0
        self.m_fontangle = 0
        self.m_pixels = Arr(0, 0)
        self.m_chart_id = 0
        self.m_objname = ""
        self.m_objtype = WRONG_VALUE
        self.m_rcname = ""
        self.m_width = 0
        self.m_height = 0
        self.m_format = COLOR_FORMAT_XRGB_NOALPHA
        self.m_fontname = 'arial'
        self.m_fontsize = -120
        self.m_fontflags = 0
        self.m_fontangle = 0
        self.m_style = UINT_MAX
        self.m_style_idx = 0
    def _q_dtor(self):
        pass
    def Create(self, name, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        self.Destroy()
        if (width > 0 and height > 0) and ArrayResize(self.m_pixels, width * height) > 0:
            uniq = _str(ChartID()) + _str(GetTickCount()) + '.' + _str(GetMicrosecondCount() & 0x3FF)
            self.m_rcname = '::' + StringSubstr(name, 0, 63 - StringLen(uniq)) + uniq
            ArrayInitialize(self.m_pixels, 0)
            if ResourceCreate(self.m_rcname, self.m_pixels, width, height, 0, 0, 0, clrfmt):
                self.m_width = width
                self.m_height = height
                self.m_format = clrfmt
                return True
        self.Destroy()
        return False
    def CreateBitmap_6(self, name, time, price, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        return self.CreateBitmap_8(0, 0, name, time, price, width, height, clrfmt)
    def CreateBitmap_8(self, chart_id, subwin, name, time, price, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if self.Create(name, width, height, clrfmt):
            if ObjectCreate(chart_id, name, OBJ_BITMAP, subwin, time, price):
                if ObjectSetString(chart_id, name, OBJPROP_BMPFILE, self.m_rcname):
                    self.m_chart_id = chart_id
                    self.m_objname = name
                    self.m_objtype = OBJ_BITMAP
                    return True
        return False
    def CreateBitmapLabel_6(self, name, x, y, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        return self.CreateBitmapLabel_8(0, 0, name, x, y, width, height, clrfmt)
    def CreateBitmapLabel_8(self, chart_id, subwin, name, x, y, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if self.Create(name, width, height, clrfmt):
            if ObjectCreate(chart_id, name, OBJ_BITMAP_LABEL, subwin, 0, 0):
                if (ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x) and ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y)) and ObjectSetString(chart_id, name, OBJPROP_BMPFILE, self.m_rcname):
                    self.m_chart_id = chart_id
                    self.m_objname = name
                    self.m_objtype = OBJ_BITMAP_LABEL
                    return True
        return False
    def Attach_3(self, chart_id, objname, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if OBJ_BITMAP_LABEL == ObjectGetInteger(chart_id, objname, OBJPROP_TYPE):
            rcname = ObjectGetString(chart_id, objname, OBJPROP_BMPFILE)
            rcname = StringSubstr(rcname, StringFind(rcname, '::'))
            if ResourceReadImage(rcname, self.m_pixels, _uint(self.m_width), _uint(self.m_height)):
                self.m_chart_id = chart_id
                self.m_objname = objname
                self.m_rcname = rcname
                self.m_format = clrfmt
                self.m_objtype = OBJ_BITMAP_LABEL
                return True
        return False
    def Attach_5(self, chart_id, objname, width, height, clrfmt=COLOR_FORMAT_XRGB_NOALPHA):
        if OBJ_BITMAP_LABEL == ObjectGetInteger(chart_id, objname, OBJPROP_TYPE):
            rcname = ObjectGetString(chart_id, objname, OBJPROP_BMPFILE)
            if ((StringLen(rcname) == 0 and width > 0) and height > 0) and ArrayResize(self.m_pixels, width * height) > 0:
                ZeroMemory(self.m_pixels)
                if ResourceCreate('::' + objname, self.m_pixels, width, height, 0, 0, 0, clrfmt) and ObjectSetString(chart_id, objname, OBJPROP_BMPFILE, '::' + objname):
                    self.m_chart_id = chart_id
                    self.m_width = width
                    self.m_height = height
                    self.m_objname = objname
                    self.m_rcname = '::' + objname
                    self.m_format = clrfmt
                    self.m_objtype = OBJ_BITMAP_LABEL
                    return True
        return False
    def Destroy(self):
        if self.m_objname != "":
            ObjectDelete(self.m_chart_id, self.m_objname)
            self.m_chart_id = 0
            self.m_objname = ""
            self.m_objtype = WRONG_VALUE
        ArrayFree(self.m_pixels)
        if self.m_rcname != "":
            ResourceFree(self.m_rcname)
            self.m_rcname = ""
        self.m_width = 0
        self.m_height = 0
    def ChartObjectName(self):
        return self.m_objname
    def ResourceName(self):
        return self.m_rcname
    def Width(self):
        return self.m_width
    def Height(self):
        return self.m_height
    def Update(self, redraw=True):
        if self.m_rcname == "":
            return
        if ResourceCreate(self.m_rcname, self.m_pixels, self.m_width, self.m_height, 0, 0, 0, self.m_format) and redraw:
            ChartRedraw(self.m_chart_id)
    def Resize(self, width, height):
        if (self.m_rcname != "" and width > 0) and height > 0:
            if ArrayResize(self.m_pixels, width * height) > 0:
                self.m_width = width
                self.m_height = height
                ArrayInitialize(self.m_pixels, 0)
                if ResourceCreate(self.m_rcname, self.m_pixels, self.m_width, self.m_height, 0, 0, 0, self.m_format):
                    if self.m_objname != "" and ObjectSetString(self.m_chart_id, self.m_objname, OBJPROP_BMPFILE, self.m_rcname):
                        return True
        return False
    def Erase(self, clr=0):
        ArrayInitialize(self.m_pixels, clr)
    def PixelGet(self, x, y):
        if ((x >= 0 and x < self.m_width) and y >= 0) and y < self.m_height:
            return self.m_pixels[(y * self.m_width) + x]
        return 0
    def PixelSet(self, x, y, clr):
        if ((x >= 0 and x < self.m_width) and y >= 0) and y < self.m_height:
            self.m_pixels[(y * self.m_width) + x] = clr
    def LineVertical(self, x, y1, y2, clr):
        tmp = 0
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        if ((y2 < 0 or y1 >= self.m_height) or x < 0) or x >= self.m_width:
            return
        if y1 < 0:
            y1 = 0
        if y2 >= self.m_height:
            y2 = self.m_height - 1
        index = (y1 * self.m_width) + x
        i = y1
        while i <= y2:
            self.m_pixels[index] = clr
            i += 1
            index += self.m_width
    def LineHorizontal(self, x1, x2, y, clr):
        tmp = 0
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if ((x2 < 0 or x1 >= self.m_width) or y < 0) or y >= self.m_height:
            return
        if x1 < 0:
            x1 = 0
        if x2 >= self.m_width:
            x2 = self.m_width - 1
        ArrayFill(self.m_pixels, (y * self.m_width) + x1, x2 - x1 + 1, clr)
    def Line(self, x1, y1, x2, y2, clr):
        if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
            return
        if x1 >= self.m_width and x2 >= self.m_width:
            return
        if y1 >= self.m_height and y2 >= self.m_height:
            return
        dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
        dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
        if dx == 0:
            self.LineVertical(x1, y1, y2, clr)
            return
        if dy == 0:
            self.LineHorizontal(x1, x2, y1, clr)
            return
        sx = (1 if (x1 < x2) else -1)
        sy = (1 if (y1 < y2) else -1)
        er = dx - dy
        draw = False
        while x1 != x2 or y1 != y2:
            if ((x1 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                if draw:
                    return
            else:
                self.m_pixels[(y1 * self.m_width) + x1] = clr
                draw = True
            er2 = _int(er << 1)
            if er2 > (-dy):
                er -= dy
                x1 += sx
            if er2 < dx:
                er += dx
                y1 += sy
        self.PixelSet(x2, y2, clr)
    def Polyline(self, x, y, clr):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        for i in range(0, total):
            self.Line(x[i], y[i], x[i + 1], y[i + 1], clr)
    def Polygon(self, x, y, clr):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        for i in range(0, total):
            self.Line(x[i], y[i], x[i + 1], y[i + 1], clr)
        self.Line(x[total], y[total], x[0], y[0], clr)
    def Rectangle(self, x1, y1, x2, y2, clr):
        self.LineHorizontal(x1, x2, y1, clr)
        self.LineVertical(x2, y1, y2, clr)
        self.LineHorizontal(x2, x1, y2, clr)
        self.LineVertical(x1, y2, y1, clr)
    def Triangle(self, x1, y1, x2, y2, x3, y3, clr):
        self.Line(x1, y1, x2, y2, clr)
        self.Line(x2, y2, x3, y3, clr)
        self.Line(x3, y3, x1, y1, clr)
    def Circle(self, x, y, r, clr):
        f = 1 - r
        dd_x = 1
        dd_y = -2 * r
        dx = 0
        dy = r
        xx = 0
        yy = 0
        while dy >= dx:
            xx = x + dx
            if xx >= 0 and xx < self.m_width:
                yy = y + dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            xx = x - dx
            if xx >= 0 and xx < self.m_width:
                yy = y + dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dy
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            xx = x + dy
            if xx >= 0 and xx < self.m_width:
                yy = y + dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            xx = x - dy
            if xx >= 0 and xx < self.m_width:
                yy = y + dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
                yy = y - dx
                if yy >= 0 and yy < self.m_height:
                    self.m_pixels[(yy * self.m_width) + xx] = clr
            if f >= 0:
                dy -= 1
                dd_y += 2
                f += dd_y
            dx += 1
            dd_x += 2
            f += dd_x
    def Ellipse(self, x1, y1, x2, y2, clr):
        x = 0
        y = 0
        rx = 0
        ry = 0
        dx = 0
        dy = 0
        xx = 0
        yy = 0
        rx_sq = 0
        ry_sq = 0
        f = 0
        tmp = 0
        if x1 == x2:
            if y1 == y2:
                self.PixelSet(x1, y1, clr)
            else:
                self.LineVertical(x1, y1, y2, clr)
            return
        if y1 == y2:
            self.LineHorizontal(x1, x2, y1, clr)
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        rx = (x2 - x1) >> 1
        ry = (y2 - y1) >> 1
        dx = 0
        dy = ry
        rx_sq = rx * rx
        ry_sq = ry * ry
        f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
        while (rx_sq * dy) > (ry_sq * dx):
            yy = y + dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            yy = y - dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            if f >= 0:
                dy -= 1
                f -= _int(rx_sq << 2) * dy
            f += _int(ry_sq << 1) * (3 + _int(dx << 1))
            dx += 1
        f = (_int(ry_sq << 1) * (dx + 1) * dx) + (_int(rx_sq << 1) * ((dy * (dy - 2)) + 1)) + ((1 - _int(rx_sq << 1)) * ry_sq)
        while dy >= 0:
            yy = y + dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            yy = y - dy
            if yy >= 0 and yy < self.m_height:
                yy *= self.m_width
                xx = x + dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
                xx = x - dx
                if xx >= 0 and xx < self.m_width:
                    self.m_pixels[yy + xx] = clr
            if f <= 0:
                dx += 1
                f += _int(ry_sq << 2) * dx
            dy -= 1
            f += _int(rx_sq << 1) * (3 - _int(dy << 1))
    def Arc_9(self, x1, y1, x2, y2, x3, y3, x4, y4, clr):
        tmp = 0
        x = 0
        y = 0
        fi3 = 0.0
        fi4 = 0.0
        if x1 == x2 or y1 == y2:
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        if x3 == x and y3 == y:
            return
        if x4 == x and y4 == y:
            return
        fi3 = self.AngleCalc(x, y, x3, y3)
        fi4 = self.AngleCalc(x, y, x4, y4)
        self.Arc_7(x, y, x2 - x, y2 - y, fi3, fi4, clr)
    def Arc_7(self, x, y, rx, ry, fi3, fi4, clr):
        x3 = Box(0)
        y3 = Box(0)
        x4 = Box(0)
        y4 = Box(0)
        if rx < 10 or ry < 10:
            return
        if rx < 0:
            rx = -rx
        if ry < 0:
            ry = -ry
        if fi3 == fi4:
            return
        if fi4 < fi3:
            fi4 += 2 * M_PI
        self.Arc_11(x, y, rx, ry, fi3, fi4, x3, y3, x4, y4, clr)
    def Arc_11(self, x, y, rx, ry, fi3, fi4, x3, y3, x4, y4, clr):
        if rx < 10 or ry < 10:
            return
        dx = 0
        dy = 0
        xx = 0
        yy = 0
        rx_sq = 0
        ry_sq = 0
        f = 0
        fi = 0.0
        ray3 = False
        ray4 = False
        ckw = False
        xx_c = 0
        yy_c = 0
        fi_c = 0.0
        ackw = False
        xx_a = 0
        yy_a = 0
        fi_a = 0.0
        rx_sq = rx * rx
        ry_sq = ry * ry
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 < M_PI and fi3 > 0) or (fi < M_PI and fi > 0)) or (fi4 - fi3) >= M_PI:
            dx = 0
            dy = ry
            f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
            while (rx_sq * dy) >= (ry_sq * dx):
                yy = y - dy
                if dx == 0:
                    fi = self.AngleCalc(0, 0, 0, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(x, yy, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = x
                    yy_c = yy
                    fi_c = fi
                    xx_a = x
                    yy_a = yy
                    fi_a = fi
                else:
                    xx = x + dx
                    fi = self.AngleCalc(0, 0, dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    xx = x - dx
                    fi = self.AngleCalc(0, 0, -dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(fi_a - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dy -= 1
                    f -= _int(rx_sq << 2) * dy
                f += _int(ry_sq << 1) * (3 + _int(dx << 1))
                dx += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, dx, -dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x + dx), _box_set(y3, y - dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, -dx, -dy)
                if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x - dx), _box_set(y4, y - dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 > M_PI_2 and fi3 < (3 * M_PI_2)) or (fi > M_PI_2 and fi < (3 * M_PI_2))) or (fi4 - fi3) >= M_PI:
            dx = rx
            dy = 0
            f = (_int(ry_sq << 1) * ((dx - 1) * dx)) + ry_sq + (_int(rx_sq << 1) * (1 - ry_sq))
            while (ry_sq * dx) >= (rx_sq * dy):
                xx = x - dx
                if dy == 0:
                    fi = self.AngleCalc(0, 0, -dx, 0)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, y, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = xx
                    yy_c = y
                    fi_c = fi
                    xx_a = xx
                    yy_a = y
                    fi_a = fi
                else:
                    yy = y - dy
                    fi = self.AngleCalc(0, 0, -dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    yy = y + dy
                    fi = self.AngleCalc(0, 0, -dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(fi_a - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dx -= 1
                    f -= _int(ry_sq << 2) * dx
                f += _int(rx_sq << 1) * (3 + _int(dy << 1))
                dy += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, -dx, -dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x - dx), _box_set(y3, y - dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, -dx, dy)
                if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x - dx), _box_set(y4, y + dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 > M_PI and fi3 < (2 * M_PI)) or (fi > M_PI and fi < (2 * M_PI))) or (fi4 - fi3) >= M_PI:
            dx = 0
            dy = ry
            f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
            while (rx_sq * dy) >= (ry_sq * dx):
                yy = y + dy
                if dx == 0:
                    fi = self.AngleCalc(0, 0, 0, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(x, yy, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = x
                    yy_c = yy
                    fi_c = fi
                    xx_a = x
                    yy_a = yy
                    fi_a = fi
                else:
                    xx = x - dx
                    fi = self.AngleCalc(0, 0, -dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    xx = x + dx
                    fi = self.AngleCalc(0, 0, dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(fi_a - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dy -= 1
                    f -= _int(rx_sq << 2) * dy
                f += _int(ry_sq << 1) * (3 + _int(dx << 1))
                dx += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, -dx, dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x - dx), _box_set(y3, y + dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, dx, dy)
                if MathAbs(fi_a - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x + dx), _box_set(y4, y + dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
        fi = MathMod(fi4, 2 * M_PI)
        if ((fi3 < M_PI_2 or fi3 > (3 * M_PI_2)) or (fi < M_PI_2 or fi > (3 * M_PI_2))) or (fi4 - fi3) >= M_PI:
            dx = rx
            dy = 0
            f = (_int(ry_sq << 1) * ((dx - 1) * dx)) + ry_sq + (_int(rx_sq << 1) * (1 - ry_sq))
            while (ry_sq * dx) >= (rx_sq * dy):
                xx = x + dx
                if dy == 0:
                    fi = self.AngleCalc(0, 0, dx, 0)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, y, clr)
                        ackw = True
                        ckw = ackw
                    else:
                        ackw = False
                        ckw = ackw
                    xx_c = xx
                    yy_c = y
                    fi_c = fi
                    xx_a = xx
                    yy_a = y
                    fi_a = fi
                else:
                    yy = y + dy
                    fi = self.AngleCalc(0, 0, dx, dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ckw:
                            ckw = True
                            if not ray4:
                                if MathAbs(fi_c - MathMod(fi4, 2 * M_PI)) < MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                    self.PixelSet(_box_set(x4, xx_c), _box_set(y4, yy_c), clr)
                                else:
                                    x4.v = xx
                                    y4.v = yy
                                ray4 = True
                    else:
                        if ckw and (not ray3):
                            if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                                self.PixelSet(_box_set(x3, xx), _box_set(y3, yy), clr)
                            else:
                                x3.v = xx_c
                                y3.v = yy_c
                            ray3 = True
                        ckw = False
                    xx_c = xx
                    yy_c = yy
                    fi_c = fi
                    yy = y - dy
                    fi = self.AngleCalc(0, 0, dx, -dy)
                    if (fi <= fi4 and fi3 <= fi) or (fi4 >= (2 * M_PI) and fi <= (fi4 - (2 * M_PI))):
                        self.PixelSet(xx, yy, clr)
                        if not ackw:
                            ackw = True
                            if not ray3:
                                if MathAbs(MathMod(fi_a, 2 * M_PI) - fi3) < MathAbs(fi - fi3):
                                    self.PixelSet(_box_set(x3, xx_a), _box_set(y3, yy_a), clr)
                                else:
                                    x3.v = xx
                                    y3.v = yy
                                ray3 = True
                    else:
                        if ackw and (not ray4):
                            if MathAbs(MathMod(fi_a, 2 * M_PI) - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                                self.PixelSet(_box_set(x4, xx), _box_set(y4, yy), clr)
                            else:
                                x4.v = xx_a
                                y4.v = yy_a
                            ray4 = True
                        ackw = False
                    xx_a = xx
                    yy_a = yy
                    fi_a = fi
                if f >= 0:
                    dx -= 1
                    f -= _int(ry_sq << 2) * dx
                f += _int(rx_sq << 1) * (3 + _int(dy << 1))
                dy += 1
            if ckw and (not ray3):
                fi = self.AngleCalc(0, 0, dx, dy)
                if MathAbs(fi_c - fi3) > MathAbs(fi - fi3):
                    self.PixelSet(_box_set(x3, x + dx), _box_set(y3, y + dy), clr)
                else:
                    x3.v = xx_c
                    y3.v = yy_c
            if ackw and (not ray4):
                fi = self.AngleCalc(0, 0, dx, -dy)
                if MathAbs(MathMod(fi_a, 2 * M_PI) - MathMod(fi4, 2 * M_PI)) > MathAbs(fi - MathMod(fi4, 2 * M_PI)):
                    self.PixelSet(_box_set(x4, x + dx), _box_set(y4, y - dy), clr)
                else:
                    x4.v = xx_a
                    y4.v = yy_a
    def Pie_10(self, x1, y1, x2, y2, x3, y3, x4, y4, clr, fill_clr):
        tmp = 0
        x = 0
        y = 0
        fi3 = 0.0
        fi4 = 0.0
        if x1 == x2 or y1 == y2:
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        if x3 == x and y3 == y:
            return
        if x4 == x and y4 == y:
            return
        fi3 = self.AngleCalc(x, y, x3, y3)
        fi4 = self.AngleCalc(x, y, x4, y4)
        self.Pie_8(x, y, x2 - x, y2 - y, fi3, fi4, clr, fill_clr)
    def Pie_8(self, x, y, rx, ry, fi3, fi4, clr, fill_clr):
        x3 = Box(x)
        y3 = Box(y)
        x4 = Box(x)
        y4 = Box(y)
        if rx == 0 or ry == 0:
            return
        if rx < 0:
            rx = -rx
        if ry < 0:
            ry = -ry
        if fi3 == fi4:
            return
        if fi4 < fi3:
            fi4 += 2 * M_PI
        self.Arc_11(x, y, rx, ry, fi3, fi4, x3, y3, x4, y4, clr)
        if (x == x3.v and y == y3.v) or (x == x4.v and y == y4.v):
            return
        self.Line(x, y, x3.v, y3.v, clr)
        self.Line(x, y, x4.v, y4.v, clr)
        if rx > ry:
            rx = ry
        fi = (fi3 + fi4) / 2
        xf = x + _int(0.9 * rx * cos(fi))
        yf = y - _int(0.9 * rx * sin(fi))
        self.Fill_3(xf, yf, fill_clr)
    def FillRectangle(self, x1, y1, x2, y2, clr):
        tmp = 0
        if x2 < x1:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y2 < y1:
            tmp = y1
            y1 = y2
            y2 = tmp
        if ((x2 < 0 or y2 < 0) or x1 >= self.m_width) or y1 >= self.m_height:
            return
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 >= self.m_width:
            x2 = self.m_width - 1
        if y2 >= self.m_height:
            y2 = self.m_height - 1
        len_ = x2 - x1 + 1
        while y1 <= y2:
            ArrayFill(self.m_pixels, (y1 * self.m_width) + x1, len_, clr)
            y1 += 1
    def FillTriangle(self, x1, y1, x2, y2, x3, y3, clr):
        xx1 = 0
        xx2 = 0
        tmp = 0
        k1 = 0.0
        k2 = 0.0
        xd1 = 0.0
        xd2 = 0.0
        if y1 > y2:
            tmp = y2
            y2 = y1
            y1 = tmp
            tmp = x2
            x2 = x1
            x1 = tmp
        if y1 > y3:
            tmp = y1
            y1 = y3
            y3 = tmp
            tmp = x1
            x1 = x3
            x3 = tmp
        if y2 > y3:
            tmp = y2
            y2 = y3
            y3 = tmp
            tmp = x2
            x2 = x3
            x3 = tmp
        if y3 < 0 or y1 > self.m_height:
            return
        if (x1 < 0 and x2 < 0) and x3 < 0:
            return
        if (x1 > self.m_width and x2 > self.m_width) and x3 > self.m_width:
            return
        if (tmp := y1 - y2) != 0:
            k1 = _fdiv(x1 - x2, float(tmp))
        if (tmp := y1 - y3) != 0:
            k2 = _fdiv(x1 - x3, float(tmp))
        xd1 = x1
        xd2 = x1
        for i in range(y1, y3 + 1):
            if i == y2:
                if (tmp := y2 - y3) != 0:
                    k1 = _fdiv(x2 - x3, float(tmp))
                xd1 = x2
            xx1 = _int(xd1)
            xd1 += k1
            xx2 = _int(xd2)
            xd2 += k2
            if i < 0 or i >= self.m_height:
                continue
            if xx1 > xx2:
                tmp = xx1
                xx1 = xx2
                xx2 = tmp
            if xx2 < 0 or xx1 >= self.m_width:
                continue
            if xx1 < 0:
                xx1 = 0
            if xx2 >= self.m_width:
                xx2 = self.m_width - 1
            ArrayFill(self.m_pixels, (i * self.m_width) + xx1, xx2 - xx1, clr)
    def FillPolygon(self, x, y, clr):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 3:
            return
        ArrayResize(_s_CCanvas_FillPolygon_p, total)
        imin = 0
        xmin = x[0]
        ymin = y[0]
        for i in range(1, total):
            if y[i] > ymin:
                continue
            if y[i] == ymin:
                if x[i] < xmin:
                    xmin = x[i]
                    imin = i
                continue
            xmin = x[i]
            ymin = y[i]
            imin = i
        i = 0
        while i < total:
            _s_CCanvas_FillPolygon_p[i].x = x[_imod(imin, total)]
            _s_CCanvas_FillPolygon_p[i].y = y[_imod(imin, total)]
            i += 1
            imin += 1
        self.PolygonFill(_s_CCanvas_FillPolygon_p, clr)
        ArrayFree(_s_CCanvas_FillPolygon_p)
    def FillCircle(self, x, y, r, clr):
        f = 1 - r
        dd_x = 1
        dd_y = -2 * r
        dx = 0
        dy = r
        while dy >= dx:
            self.LineHorizontal(x - dy, x + dy, y - dx, clr)
            self.LineHorizontal(x - dy, x + dy, y + dx, clr)
            if f >= 0:
                self.LineHorizontal(x - dx, x + dx, y - dy, clr)
                self.LineHorizontal(x - dx, x + dx, y + dy, clr)
                dy -= 1
                dd_y += 2
                f += dd_y
            dx += 1
            dd_x += 2
            f += dd_x
    def FillEllipse(self, x1, y1, x2, y2, clr):
        x = 0
        y = 0
        rx = 0
        ry = 0
        dx = 0
        dy = 0
        rx_sq = 0
        ry_sq = 0
        f = 0
        tmp = 0
        if x1 == x2:
            if y1 == y2:
                self.PixelSet(x1, y1, clr)
            else:
                self.LineVertical(x1, y1, y2, clr)
            return
        if y1 == y2:
            self.LineHorizontal(x1, x2, y1, clr)
            return
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1 = y2
            y2 = tmp
        x = (x2 + x1) >> 1
        y = (y2 + y1) >> 1
        rx = (x2 - x1) >> 1
        ry = (y2 - y1) >> 1
        dx = 0
        dy = ry
        rx_sq = rx * rx
        ry_sq = ry * ry
        f = (_int(rx_sq << 1) * ((dy - 1) * dy)) + rx_sq + (_int(ry_sq << 1) * (1 - rx_sq))
        while (rx_sq * dy) > (ry_sq * dx):
            self.LineHorizontal(x - dx, x + dx, y + dy, clr)
            self.LineHorizontal(x - dx, x + dx, y - dy, clr)
            if f >= 0:
                dy -= 1
                f -= _int(rx_sq << 2) * dy
            f += _int(ry_sq << 1) * (3 + _int(dx << 1))
            dx += 1
        f = (_int(ry_sq << 1) * (dx + 1) * dx) + (_int(rx_sq << 1) * ((dy * (dy - 2)) + 1)) + ((1 - _int(rx_sq << 1)) * ry_sq)
        while dy >= 0:
            self.LineHorizontal(x - dx, x + dx, y + dy, clr)
            self.LineHorizontal(x - dx, x + dx, y - dy, clr)
            if f <= 0:
                dx += 1
                f += _int(ry_sq << 2) * dx
            dy -= 1
            f += _int(rx_sq << 1) * (3 - _int(dy << 1))
    def Fill_3(self, x, y, clr):
        if ((x < 0 or x >= self.m_width) or y < 0) or y >= self.m_height:
            return
        index = (y * self.m_width) + x
        old_clr = self.m_pixels[index]
        if old_clr == clr:
            return
        stack = Arr(0, 0)
        count = 1
        idx = 0
        total = ArraySize(self.m_pixels)
        if ArrayResize(stack, total) == -1:
            return
        stack[0] = index
        self.m_pixels[index] = clr
        i = 0
        while i < count:
            index = stack[i]
            x = _imod(index, self.m_width)
            idx = index - 1
            if x > 0 and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index - self.m_width
            if idx >= 0 and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + 1
            if x < (self.m_width - 1) and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + self.m_width
            if idx < total and self.m_pixels[idx] == old_clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            i += 1
        ArrayFree(stack)
    def Fill_4(self, x, y, clr, threshould):
        if threshould == 0.0:
            self.Fill_3(x, y, clr)
            return
        if (((x < 0 or x >= self.m_width) or y < 0) or y >= self.m_height) or threshould > 255:
            return
        index = (y * self.m_width) + x
        old_clr = self.m_pixels[index]
        if old_clr == clr:
            return
        stack = Arr(0, 0)
        count = 1
        idx = 0
        total = ArraySize(self.m_pixels)
        if ArrayResize(stack, total) == -1:
            return
        stack[0] = index
        self.m_pixels[index] = clr
        i = 0
        while i < count:
            index = stack[i]
            x = _imod(index, self.m_width)
            idx = index - 1
            if (x > 0 and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index - self.m_width
            if (idx >= 0 and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + 1
            if (x < (self.m_width - 1) and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            idx = index + self.m_width
            if (idx < total and self.PixelsSimilar(self.m_pixels[idx], old_clr, threshould)) and self.m_pixels[idx] != clr:
                self.m_pixels[idx] = clr
                stack[((count := count + 1) - 1)] = idx
            i += 1
        ArrayFree(stack)
    def PixelSetAA(self, x, y, clr):
        ix = _int(MathRound(x))
        iy = _int(MathRound(y))
        rrr = 0.0
        k = 0.0
        dx = x - ix
        dy = y - iy
        a = 0
        r = 0
        g = 0
        b = 0
        c = 0
        if dx == 0.0 and dy == 0.0:
            self.PixelSet(ix, iy, clr)
            return
        _s_CCanvas_PixelSetAA_xx[2] = ix
        _s_CCanvas_PixelSetAA_xx[0] = _s_CCanvas_PixelSetAA_xx[2]
        _s_CCanvas_PixelSetAA_yy[1] = iy
        _s_CCanvas_PixelSetAA_yy[0] = _s_CCanvas_PixelSetAA_yy[1]
        if dx < 0.0:
            _s_CCanvas_PixelSetAA_xx[3] = ix - 1
            _s_CCanvas_PixelSetAA_xx[1] = _s_CCanvas_PixelSetAA_xx[3]
        if dx == 0.0:
            _s_CCanvas_PixelSetAA_xx[3] = ix
            _s_CCanvas_PixelSetAA_xx[1] = _s_CCanvas_PixelSetAA_xx[3]
        if dx > 0.0:
            _s_CCanvas_PixelSetAA_xx[3] = ix + 1
            _s_CCanvas_PixelSetAA_xx[1] = _s_CCanvas_PixelSetAA_xx[3]
        if dy < 0.0:
            _s_CCanvas_PixelSetAA_yy[3] = iy - 1
            _s_CCanvas_PixelSetAA_yy[2] = _s_CCanvas_PixelSetAA_yy[3]
        if dy == 0.0:
            _s_CCanvas_PixelSetAA_yy[3] = iy
            _s_CCanvas_PixelSetAA_yy[2] = _s_CCanvas_PixelSetAA_yy[3]
        if dy > 0.0:
            _s_CCanvas_PixelSetAA_yy[3] = iy + 1
            _s_CCanvas_PixelSetAA_yy[2] = _s_CCanvas_PixelSetAA_yy[3]
        for i in range(0, 4):
            dx = _s_CCanvas_PixelSetAA_xx[i] - x
            dy = _s_CCanvas_PixelSetAA_yy[i] - y
            _s_CCanvas_PixelSetAA_rr[i] = _fdiv(1, (dx * dx) + (dy * dy))
            rrr += _s_CCanvas_PixelSetAA_rr[i]
        for i in range(0, 4):
            k = _fdiv(_s_CCanvas_PixelSetAA_rr[i], rrr)
            c = self.PixelGet(_s_CCanvas_PixelSetAA_xx[i], _s_CCanvas_PixelSetAA_yy[i])
            a = _uchar((k * _uchar(clr >> 24)) + ((1 - k) * _uchar(c >> 24)))
            r = _uchar((k * _uchar(clr >> 16)) + ((1 - k) * _uchar(c >> 16)))
            g = _uchar((k * _uchar(clr >> 8)) + ((1 - k) * _uchar(c >> 8)))
            b = _uchar((k * _uchar(clr)) + ((1 - k) * _uchar(c)))
            self.PixelSet(_s_CCanvas_PixelSetAA_xx[i], _s_CCanvas_PixelSetAA_yy[i], (((_uchar(a) << 24) | (_uchar(r) << 16)) | (_uchar(g) << 8)) | _uchar(b))
    def LineAA(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
            return
        if x1 >= self.m_width and x2 >= self.m_width:
            return
        if y1 >= self.m_height and y2 >= self.m_height:
            return
        if x1 == x2 and y1 == y2:
            self.PixelSet(x1, y1, clr)
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        dx = x2 - x1
        dy = y2 - y1
        xy = sqrt((dx * dx) + (dy * dy))
        xx = x1
        yy = y1
        mask = _int(1 << self.m_style_idx)
        dx = _fdiv(dx, xy)
        dy = _fdiv(dy, xy)
        while True:
            if (self.m_style & mask) == mask:
                self.PixelSetAA(xx, yy, clr)
            xx += dx
            yy += dy
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            if not (fabs(x2 - xx) >= fabs(dx) and fabs(y2 - yy) >= fabs(dy)):
                break
        if (self.m_style & mask) == mask:
            self.PixelSetAA(x2, y2, clr)
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineAA(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            y1 = y[i]
            x2 = x[i + 1]
            y2 = y[i + 1]
            if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 >= self.m_width and x2 >= self.m_width:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if y1 >= self.m_height and y2 >= self.m_height:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 == x2 and y1 == y2:
                self.PixelSet(x1, y1, clr)
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            dx = x2 - x1
            dy = y2 - y1
            xy = sqrt((dx * dx) + (dy * dy))
            xx = x1
            yy = y1
            dx = _fdiv(dx, xy)
            dy = _fdiv(dy, xy)
            while True:
                if (self.m_style & mask) == mask:
                    self.PixelSetAA(xx, yy, clr)
                xx += dx
                yy += dy
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                if not (fabs(x2 - xx) >= fabs(dx) and fabs(y2 - yy) >= fabs(dy)):
                    break
            if (self.m_style & mask) == mask:
                self.PixelSetAA(x2, y2, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolygonAA(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            y1 = y[i]
            x2 = (x[i + 1] if ((i + 1) != total) else x[0])
            y2 = (y[i + 1] if ((i + 1) != total) else y[0])
            if (x1 < 0 and x2 < 0) or (y1 < 0 and y2 < 0):
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 >= self.m_width and x2 >= self.m_width:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if y1 >= self.m_height and y2 >= self.m_height:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 == x2 and y1 == y2:
                self.PixelSet(x1, y1, clr)
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            dx = x2 - x1
            dy = y2 - y1
            xy = sqrt((dx * dx) + (dy * dy))
            xx = x1
            yy = y1
            dx = _fdiv(dx, xy)
            dy = _fdiv(dy, xy)
            while True:
                if (self.m_style & mask) == mask:
                    self.PixelSetAA(xx, yy, clr)
                xx += dx
                yy += dy
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                if not (fabs(x2 - xx) >= fabs(dx) and fabs(y2 - yy) >= fabs(dy)):
                    break
            if (self.m_style & mask) == mask:
                self.PixelSetAA(x2, y2, clr)
        if style != UINT_MAX:
            self.m_style = prev_style
    def TriangleAA(self, x1, y1, x2, y2, x3, y3, clr, style=UINT_MAX):
        x = Arr(3, 0, dyn=False)
        y = Arr(3, 0, dyn=False)
        x[0] = x1
        x[1] = x2
        x[2] = x3
        y[0] = y1
        y[1] = y2
        y[2] = y3
        self.PolygonAA(x, y, clr, style)
    def CircleAA(self, x, y, r, clr, style=UINT_MAX):
        if r <= 0:
            return
        xx = x + r
        yy = y
        fi = 0.0
        df = _fdiv(M_PI_2, MathCeil(r))
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        if r > M_PI:
            df = df / 2
        while True:
            xx = x + (r * cos(fi))
            yy = y - (r * sin(fi))
            if (self.m_style & mask) == mask:
                self.PixelSetAA(xx, yy, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            fi += df
            if not (fabs((2 * M_PI) - fi) >= (df / 2)):
                break
        if style != UINT_MAX:
            self.m_style = prev_style
    def EllipseAA(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        rx = (x2 - x1) / 2
        ry = (y2 - y1) / 2
        x = ((x1 + rx) if (x2 > x1) else (x2 + rx))
        y = ((y1 + ry) if (y2 > y1) else (y2 + ry))
        rx2 = rx * rx
        ry2 = ry * ry
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        quarter = round(_fdiv(rx2, sqrt(rx2 + ry2)))
        dx = 0.0
        while dx <= quarter:
            dy = ry * sqrt(1 - _fdiv(dx * dx, rx2))
            if (self.m_style & mask) == mask:
                self.PixelSet4AA(x, y, dx, dy, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dx += 1
        quarter = round(_fdiv(ry2, sqrt(rx2 + ry2)))
        dy = 0.0
        while dy <= quarter:
            dx = rx * sqrt(1 - _fdiv(dy * dy, ry2))
            if (self.m_style & mask) == mask:
                self.PixelSet4AA(x, y, dx, dy, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dy += 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineWu(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
        dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        tmp = 0
        if dx == 0:
            if y1 > y2:
                tmp = y1
                y1 = y2
                y2 = tmp
            if ((y2 < 0 or y1 >= self.m_height) or x1 < 0) or x1 >= self.m_width:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if y1 < 0:
                y1 = 0
            if y2 >= (self.m_height - 1):
                y2 = self.m_height - 1
            index = (y1 * self.m_width) + x1
            i = y1
            while i <= y2:
                if (self.m_style & mask) == mask:
                    self.m_pixels[index] = clr
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                i += 1
                index += self.m_width
            if style != UINT_MAX:
                self.m_style = prev_style
            return
        if dy == 0:
            if x1 > x2:
                tmp = x1
                x1 = x2
                x2 = tmp
            if ((x2 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                if style != UINT_MAX:
                    self.m_style = prev_style
                return
            if x1 < 0:
                x1 = 0
            if x2 >= self.m_width:
                x2 = self.m_width - 1
            i = 0
            index = (y1 * self.m_width) + x1
            while i < (x2 - x1):
                if (self.m_style & mask) == mask:
                    self.m_pixels[index] = clr
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                i += 1
                index += 1
            if style != UINT_MAX:
                self.m_style = prev_style
            return
        if dx == 0 and dy == 0:
            self.PixelSet(x1, y1, clr)
            if style != UINT_MAX:
                self.m_style = prev_style
            return
        if dy < dx:
            if x2 < x1:
                x2 += x1
                x1 = x2 - x1
                x2 -= x1
                y2 += y1
                y1 = y2 - y1
                y2 -= y1
            if y2 < y1:
                dy *= -1
            grad = _fdiv(float(dy), dx)
            intery = y1 + grad
            if (self.m_style & mask) == mask:
                self.PixelSet(x1, y1, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            for x in range(x1 + 1, x2):
                alpha1 = 1 - (intery - _int(intery))
                alpha2 = intery - _int(intery)
                if (self.m_style & mask) == mask:
                    self.PixelTransform(x, _int(intery), clr, alpha1)
                    self.PixelTransform(x, _int(intery) + 1, clr, alpha2)
                intery += grad
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if (self.m_style & mask) == mask:
                self.PixelSet(x2, y2, clr)
        else:
            if y2 < y1:
                x2 += x1
                x1 = x2 - x1
                x2 -= x1
                y2 += y1
                y1 = y2 - y1
                y2 -= y1
            if x2 < x1:
                dx *= -1
            grad = _fdiv(float(dx), dy)
            interx = x1 + grad
            if (self.m_style & mask) == mask:
                self.PixelSet(x1, y1, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            for y in range(y1 + 1, y2):
                alpha1 = 1 - (interx - _int(interx))
                alpha2 = interx - _int(interx)
                if (self.m_style & mask) == mask:
                    self.PixelTransform(_int(interx), y, clr, alpha1)
                    self.PixelTransform(_int(interx) + 1, y, clr, alpha2)
                interx += grad
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if (self.m_style & mask) == mask:
                self.PixelSet(x2, y2, clr)
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineWu(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            x2 = x[i + 1]
            y1 = y[i]
            y2 = y[i + 1]
            dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
            dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
            tmp = 0
            if dx == 0:
                if y1 > y2:
                    tmp = y1
                    y1 = y2
                    y2 = tmp
                if ((y2 < 0 or y1 >= self.m_height) or x1 < 0) or x1 >= self.m_width:
                    continue
                if y1 < 0:
                    y1 = 0
                if y2 >= (self.m_height - 1):
                    y2 = self.m_height - 1
                index = (y1 * self.m_width) + x1
                j = y1
                while j <= y2:
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += self.m_width
                continue
            if dy == 0:
                if x1 > x2:
                    tmp = x1
                    x1 = x2
                    x2 = tmp
                if ((x2 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                    continue
                if x1 < 0:
                    x1 = 0
                if x2 >= self.m_width:
                    x2 = self.m_width - 1
                j = 0
                index = (y1 * self.m_width) + x1
                while j < (x2 - x1):
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += 1
                continue
            if dx == 0 and dy == 0:
                self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                continue
            if dy < dx:
                if x2 < x1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if y2 < y1:
                    dy *= -1
                grad = _fdiv(float(dy), dx)
                intery = y1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for xc in range(x1 + 1, x2):
                    alpha1 = 1 - (intery - _int(intery))
                    alpha2 = intery - _int(intery)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(xc, _int(intery), clr, alpha1)
                        self.PixelTransform(xc, _int(intery) + 1, clr, alpha2)
                    intery += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            else:
                if y2 < y1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if x2 < x1:
                    dx *= -1
                grad = _fdiv(float(dx), dy)
                interx = x1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for yc in range(y1 + 1, y2):
                    alpha1 = 1 - (interx - _int(interx))
                    alpha2 = interx - _int(interx)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(_int(interx), yc, clr, alpha1)
                        self.PixelTransform(_int(interx) + 1, yc, clr, alpha2)
                    interx += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolygonWu(self, x, y, clr, style=UINT_MAX):
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for i in range(0, total):
            x1 = x[i]
            y1 = y[i]
            x2 = (x[i + 1] if ((i + 1) != total) else x[0])
            y2 = (y[i + 1] if ((i + 1) != total) else y[0])
            dx = ((x2 - x1) if (x2 > x1) else (x1 - x2))
            dy = ((y2 - y1) if (y2 > y1) else (y1 - y2))
            tmp = 0
            if dx == 0:
                if y1 > y2:
                    tmp = y1
                    y1 = y2
                    y2 = tmp
                if ((y2 < 0 or y1 >= self.m_height) or x1 < 0) or x1 >= self.m_width:
                    continue
                if y1 < 0:
                    y1 = 0
                if y2 >= (self.m_height - 1):
                    y2 = self.m_height - 1
                index = (y1 * self.m_width) + x1
                j = y1
                while j <= y2:
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += self.m_width
                continue
            if dy == 0:
                if x1 > x2:
                    tmp = x1
                    x1 = x2
                    x2 = tmp
                if ((x2 < 0 or x1 >= self.m_width) or y1 < 0) or y1 >= self.m_height:
                    continue
                if x1 < 0:
                    x1 = 0
                if x2 >= self.m_width:
                    x2 = self.m_width - 1
                j = 0
                index = (y1 * self.m_width) + x1
                while j < (x2 - x1):
                    if (self.m_style & mask) == mask:
                        self.m_pixels[index] = clr
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                    j += 1
                    index += 1
                continue
            if dx == 0 and dy == 0:
                self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                continue
            if dy < dx:
                if x2 < x1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if y2 < y1:
                    dy *= -1
                grad = _fdiv(float(dy), dx)
                intery = y1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for xc in range(x1 + 1, x2):
                    alpha1 = 1 - (intery - _int(intery))
                    alpha2 = intery - _int(intery)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(xc, _int(intery), clr, alpha1)
                        self.PixelTransform(xc, _int(intery) + 1, clr, alpha2)
                    intery += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            else:
                if y2 < y1:
                    x2 += x1
                    x1 = x2 - x1
                    x2 -= x1
                    y2 += y1
                    y1 = y2 - y1
                    y2 -= y1
                if x2 < x1:
                    dx *= -1
                grad = _fdiv(float(dx), dy)
                interx = x1 + grad
                if (self.m_style & mask) == mask:
                    self.PixelSet(x1, y1, clr)
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
                for yc in range(y1 + 1, y2):
                    alpha1 = 1 - (interx - _int(interx))
                    alpha2 = interx - _int(interx)
                    if (self.m_style & mask) == mask:
                        self.PixelTransform(_int(interx), yc, clr, alpha1)
                        self.PixelTransform(_int(interx) + 1, yc, clr, alpha2)
                    interx += grad
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if (self.m_style & mask) == mask:
                    self.PixelSet(x2, y2, clr)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def TriangleWu(self, x1, y1, x2, y2, x3, y3, clr, style=UINT_MAX):
        x = Arr(3, 0, dyn=False)
        y = Arr(3, 0, dyn=False)
        x[0] = x1
        x[1] = x2
        x[2] = x3
        y[0] = y1
        y[1] = y2
        y[2] = y3
        self.PolygonWu(x, y, clr, style)
    def CircleWu(self, x, y, r, clr, style=UINT_MAX):
        if r <= 0:
            return
        r2 = r * r
        quarter = round(_fdiv(r, sqrt(2.0)))
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        d1 = 0
        while d1 <= quarter:
            d2 = sqrt(r2 - (d1 * d1))
            alpha1 = d2 - floor(d2)
            alpha2 = 1 - alpha1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, _int(d2) + 1, d1, clr, alpha1)
                self.PixelTransform4(x, y, d1, _int(d2) + 1, clr, alpha1)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, d1, _int(d2), clr, alpha2)
                self.PixelTransform4(x, y, _int(d2), d1, clr, alpha2)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            d1 += 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def EllipseWu(self, x1, y1, x2, y2, clr, style=UINT_MAX):
        rx = _idiv(x2 - x1, 2)
        ry = _idiv(y2 - y1, 2)
        x = ((x1 + rx) if (x2 > x1) else (x2 + rx))
        y = ((y1 + ry) if (y2 > y1) else (y2 + ry))
        if rx <= 0 or ry <= 0:
            return
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        rx2 = rx * rx
        ry2 = ry * ry
        quarter = round(_fdiv(rx2, sqrt(rx2 + ry2)))
        dx = 0
        while dx <= quarter:
            dy = ry * sqrt(1 - _fdiv(dx * dx, rx2))
            alpha1 = dy - floor(dy)
            alpha2 = 1 - alpha1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, dx, _int(dy) + 1, clr, alpha1)
                self.PixelTransform4(x, y, dx, _int(dy), clr, alpha2)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dx += 1
        quarter = round(_fdiv(ry2, sqrt(rx2 + ry2)))
        dy = 0
        while dy <= quarter:
            dx = rx * sqrt(1 - _fdiv(dy * dy, ry2))
            alpha1 = dx - floor(dx)
            alpha2 = 1 - alpha1
            if (self.m_style & mask) == mask:
                self.PixelTransform4(x, y, _int(dx) + 1, dy, clr, alpha1)
                self.PixelTransform4(x, y, _int(dx), dy, clr, alpha2)
            mask = _uint(mask << 1)
            if mask == 0x1000000:
                mask = 1
            dy += 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineThickVertical(self, x, y1, y2, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.LineWu(x, y1, x, y2, clr, style)
            return
        r = size / 2.0
        dy = MathAbs(y2 - y1)
        sign = (1 if (y1 < y2) else -1)
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        if style == STYLE_SOLID:
            self.SegmentVertical(x, y1, y2, sign, r, clr, end_style)
        else:
            ys = 0
            ye = 0
            steps = _int(MathRound(_fdiv(dy, r)))
            segment = False
            for i in range(0, steps + 1):
                if (self.m_style & mask) == mask and (not segment):
                    ys = y1 + (sign * _int(i * r))
                    segment = True
                elif (self.m_style & mask) != mask and segment:
                    ye = y1 + (sign * _int(i * r))
                    self.SegmentVertical(x, ys, ye, sign, r, clr, end_style)
                    segment = False
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if segment:
                self.SegmentVertical(x, ys, y2, sign, r, clr, end_style)
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineThickHorizontal(self, x1, x2, y, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.LineWu(x1, y, x2, y, clr, style)
            return
        r = size / 2.0
        dx = MathAbs(x2 - x1)
        sign = (1 if (x1 < x2) else -1)
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        if style == STYLE_SOLID:
            self.SegmentHorizontal(x1, x2, y, sign, r, clr, end_style)
        else:
            xs = 0
            xe = 0
            steps = _int(MathRound(_fdiv(dx, r)))
            segment = False
            for i in range(0, steps + 1):
                if (self.m_style & mask) == mask and (not segment):
                    xs = x1 + (sign * _int(i * r))
                    segment = True
                elif (self.m_style & mask) != mask and segment:
                    xe = x1 + (sign * _int(i * r))
                    self.SegmentHorizontal(xs, xe, y, sign, r, clr, end_style)
                    segment = False
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if segment:
                self.SegmentHorizontal(xs, x2, y, sign, r, clr, end_style)
        if style != UINT_MAX:
            self.m_style = prev_style
    def LineThick(self, x1, y1, x2, y2, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.LineWu(x1, y1, x2, y2, clr, style)
            return
        r = size / 2.0
        dx = MathAbs(x2 - x1)
        dy = MathAbs(y2 - y1)
        if dx == 0:
            self.LineThickVertical(x1, y1, y2, clr, size, style, end_style)
            return
        if dy == 0:
            self.LineThickHorizontal(x1, x2, y1, clr, size, style, end_style)
            return
        k = MathArctan(_fdiv(dx, dy))
        rcos_k = r * cos(k)
        rsin_k = r * sin(k)
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        xsign = (1 if (x1 < x2) else -1)
        ysign = (1 if (y1 < y2) else -1)
        kp0 = (-xsign) * ysign * _fdiv(dx, dy)
        kp1 = _fdiv(-1, kp0)
        if style == STYLE_SOLID:
            self.Segment(x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
        else:
            xs = 0
            ys = 0
            xe = 0
            ye = 0
            length = MathSqrt((dx * dx) + (dy * dy))
            steps = _int(MathRound(_fdiv(length, r)))
            segment = False
            for i in range(0, steps + 1):
                if (self.m_style & mask) == mask and (not segment):
                    xs = x1 + (xsign * _int(i * rsin_k))
                    ys = y1 + (ysign * _int(i * rcos_k))
                    segment = True
                elif (self.m_style & mask) != mask and segment:
                    xe = x1 + (xsign * _int(i * rsin_k))
                    ye = y1 + (ysign * _int(i * rcos_k))
                    self.Segment(xs, ys, xe, ye, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                    segment = False
                mask = _uint(mask << 1)
                if mask == 0x1000000:
                    mask = 1
            if segment:
                self.Segment(xs, ys, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineThick(self, x, y, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.PolylineWu(x, y, clr, style)
            return
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        total -= 1
        r = size / 2.0
        gap = 1.0
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for index in range(0, total):
            x1 = x[index]
            y1 = y[index]
            x2 = x[index + 1]
            y2 = y[index + 1]
            dx = MathAbs(x2 - x1)
            dy = MathAbs(y2 - y1)
            if dx == 0:
                sign = (1 if (y1 < y2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentVertical(x1, y1, y2, sign, r, clr, end_style)
                else:
                    ys = y1
                    ye = 0
                    steps = _fdiv(dy, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            ys = y1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            ye = y1 + (sign * _int(i * r))
                            self.SegmentVertical(x1, ys, ye, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentVertical(x1, ys, y2, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            if dy == 0:
                sign = (1 if (x1 < x2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentHorizontal(x1, x2, y1, sign, r, clr, end_style)
                else:
                    xs = x1
                    xe = 0
                    steps = _fdiv(dx, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            xs = x1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            xe = x1 + (sign * _int(i * r))
                            self.SegmentHorizontal(xs, xe, y1, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentHorizontal(xs, x2, y1, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            k = MathArctan(_fdiv(dx, dy))
            rcos_k = r * cos(k)
            rsin_k = r * sin(k)
            xsign = (1 if (x1 < x2) else -1)
            ysign = (1 if (y1 < y2) else -1)
            kp0 = (-xsign) * ysign * _fdiv(dx, dy)
            kp1 = _fdiv(-1, kp0)
            if style == STYLE_SOLID:
                self.Segment(x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
            else:
                xs = x1
                ys = y1
                xe = 0
                ye = 0
                length = MathSqrt((dx * dx) + (dy * dy))
                steps = _fdiv(length, r)
                isteps = _int(steps)
                segment = False
                for i in range(0, isteps):
                    if (self.m_style & mask) == mask and (not segment):
                        xs = x1 + (xsign * _int(i * rsin_k))
                        ys = y1 + (ysign * _int(i * rcos_k))
                        segment = True
                    elif (self.m_style & mask) != mask and segment:
                        xe = x1 + (xsign * _int(i * rsin_k))
                        ye = y1 + (ysign * _int(i * rcos_k))
                        self.Segment(xs, ys, xe, ye, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                        segment = False
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if segment or (steps < 1 and (self.m_style & mask) == mask):
                    self.Segment(xs, ys, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                gap -= steps - isteps
                if gap < 0:
                    gap += 1
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolygonThick(self, x, y, clr, size, style, end_style):
        if size <= 2:
            if size > 0:
                self.PolylineWu(x, y, clr, style)
            return
        total = ArraySize(x)
        if total > ArraySize(y):
            total = ArraySize(y)
        if total < 2:
            return
        r = size / 2.0
        gap = 1.0
        prev_style = self.m_style
        if style != UINT_MAX:
            self.LineStyleSet(style)
        mask = _int(1 << self.m_style_idx)
        for index in range(0, total):
            x1 = x[index]
            y1 = y[index]
            x2 = (x[index + 1] if (index != (total - 1)) else x[0])
            y2 = (y[index + 1] if (index != (total - 1)) else y[0])
            dx = MathAbs(x2 - x1)
            dy = MathAbs(y2 - y1)
            if dx == 0:
                sign = (1 if (y1 < y2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentVertical(x1, y1, y2, sign, r, clr, end_style)
                else:
                    ys = y1
                    ye = 0
                    steps = _fdiv(dy, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            ys = y1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            ye = y1 + (sign * _int(i * r))
                            self.SegmentVertical(x1, ys, ye, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentVertical(x1, ys, y2, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            if dy == 0:
                sign = (1 if (x1 < x2) else -1)
                if style == STYLE_SOLID:
                    self.SegmentHorizontal(x1, x2, y1, sign, r, clr, end_style)
                else:
                    xs = x1
                    xe = 0
                    steps = _fdiv(dx, r)
                    isteps = _int(steps)
                    segment = False
                    for i in range(0, isteps):
                        if (self.m_style & mask) == mask and (not segment):
                            xs = x1 + (sign * _int(i * r))
                            segment = True
                        elif (self.m_style & mask) != mask and segment:
                            xe = x1 + (sign * _int(i * r))
                            self.SegmentHorizontal(xs, xe, y1, sign, r, clr, end_style)
                            segment = False
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                    if segment or (steps < 1 and (self.m_style & mask) == mask):
                        self.SegmentHorizontal(xs, x2, y1, sign, r, clr, end_style)
                    gap -= steps - isteps
                    if gap < 0:
                        gap += 1
                        mask = _uint(mask << 1)
                        if mask == 0x1000000:
                            mask = 1
                continue
            k = MathArctan(_fdiv(dx, dy))
            rcos_k = r * cos(k)
            rsin_k = r * sin(k)
            xsign = (1 if (x1 < x2) else -1)
            ysign = (1 if (y1 < y2) else -1)
            kp0 = (-xsign) * ysign * _fdiv(dx, dy)
            kp1 = _fdiv(-1, kp0)
            if style == STYLE_SOLID:
                self.Segment(x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
            else:
                xs = x1
                ys = y1
                xe = 0
                ye = 0
                length = MathSqrt((dx * dx) + (dy * dy))
                steps = _fdiv(length, r)
                isteps = _int(steps)
                segment = False
                for i in range(0, isteps):
                    if (self.m_style & mask) == mask and (not segment):
                        xs = x1 + (xsign * _int(i * rsin_k))
                        ys = y1 + (ysign * _int(i * rcos_k))
                        segment = True
                    elif (self.m_style & mask) != mask and segment:
                        xe = x1 + (xsign * _int(i * rsin_k))
                        ye = y1 + (ysign * _int(i * rcos_k))
                        self.Segment(xs, ys, xe, ye, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                        segment = False
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
                if segment or (steps < 1 and (self.m_style & mask) == mask):
                    self.Segment(xs, ys, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style)
                gap -= steps - isteps
                if gap < 0:
                    gap += 1
                    mask = _uint(mask << 1)
                    if mask == 0x1000000:
                        mask = 1
        if style != UINT_MAX:
            self.m_style = prev_style
    def PolylineSmooth(self, x, y, clr, size, style=STYLE_SOLID, end_style=LINE_END_ROUND, tension=0.5, step=10.0):
        arr_size = ArraySize(x)
        if arr_size != ArraySize(y):
            return
        x1 = Box(0.0)
        x2 = Box(0.0)
        y1 = Box(0.0)
        y2 = Box(0.0)
        tension *= 0.3
        xc = Arr(0, 0)
        yc = Arr(0, 0)
        ptX = Arr(0, 0.0)
        ptY = Arr(0, 0.0)
        size_pt = (arr_size * 3) - 2
        ArrayResize(ptX, size_pt)
        ArrayResize(ptY, size_pt)
        self.CalcCurveBezierEndp(x[0], y[0], x[1], y[1], tension, x1, y1)
        ptX[0] = x[0]
        ptY[0] = y[0]
        ptX[1] = x1.v
        ptY[1] = y1.v
        for i in range(0, arr_size - 2):
            self.CalcCurveBezier(x, y, i, tension, x1, y1, x2, y2)
            ptX[(3 * i) + 2] = x1.v
            ptY[(3 * i) + 2] = y1.v
            ptX[(3 * i) + 3] = x[i + 1]
            ptY[(3 * i) + 3] = y[i + 1]
            ptX[(3 * i) + 4] = x2.v
            ptY[(3 * i) + 4] = y2.v
        self.CalcCurveBezierEndp(x[arr_size - 1], y[arr_size - 1], x[arr_size - 2], y[arr_size - 2], tension, x1, y1)
        ptX[size_pt - 2] = x1.v
        ptY[size_pt - 2] = y1.v
        ptX[size_pt - 1] = x[arr_size - 1]
        ptY[size_pt - 1] = y[arr_size - 1]
        index = 0
        for i in range(0, arr_size - 1):
            distance = MathSqrt(((x[i + 1] - x[i]) * (x[i + 1] - x[i])) + ((y[i + 1] - y[i]) * (y[i + 1] - y[i])))
            size_i = (_int(_fdiv(distance, step)) if (step > 0.0) else 1)
            if size_i < 1:
                size_i = 2
            ArrayResize(xc, ArraySize(xc) + size_i, 1024)
            ArrayResize(yc, ArraySize(yc) + size_i, 1024)
            t = 0
            while t < size_i:
                xc[index] = _int(MathRound(self.CalcBezierX(_fdiv(float(t), size_i), ptX[3 * i], ptX[(3 * i) + 1], ptX[(3 * i) + 2], ptX[(3 * i) + 3])))
                yc[index] = _int(MathRound(self.CalcBezierY(_fdiv(float(t), size_i), ptY[3 * i], ptY[(3 * i) + 1], ptY[(3 * i) + 2], ptY[(3 * i) + 3])))
                t += 1
                index += 1
        self.PolylineThick(xc, yc, clr, size, style, LINE_END_ROUND)
    def PolygonSmooth(self, x, y, clr, size, style=STYLE_SOLID, end_style=LINE_END_ROUND, tension=0.5, step=10.0):
        size_arr = ArraySize(x)
        if size_arr != ArraySize(y):
            return
        x1 = Box(0.0)
        x2 = Box(0.0)
        y1 = Box(0.0)
        y2 = Box(0.0)
        tension *= 0.3
        xc = Arr(0, 0)
        yc = Arr(0, 0)
        ptX = Arr(0, 0.0)
        ptY = Arr(0, 0.0)
        size_pt = ((size_arr + 1) * 3) - 3
        ArrayResize(ptX, size_pt)
        ArrayResize(ptY, size_pt)
        xe = Arr(0, 0)
        ye = Arr(0, 0)
        ArrayResize(xe, size_arr + 2)
        ArrayResize(ye, size_arr + 2)
        xe[0] = x[size_arr - 1]
        ye[0] = y[size_arr - 1]
        xe[size_arr + 1] = x[0]
        ye[size_arr + 1] = y[0]
        ArrayCopy(xe, x, 1, 0, size_arr)
        ArrayCopy(ye, y, 1, 0, size_arr)
        for i in range(0, size_arr):
            self.CalcCurveBezier(xe, ye, i, tension, x1, y1, x2, y2)
            ptX[(3 * i) + 0] = x1.v
            ptY[(3 * i) + 0] = y1.v
            ptX[(3 * i) + 1] = xe[i + 1]
            ptY[(3 * i) + 1] = ye[i + 1]
            ptX[(3 * i) + 2] = x2.v
            ptY[(3 * i) + 2] = y2.v
        index = 0
        for i in range(0, size_arr - 1):
            distance = MathSqrt(((x[i] - x[i + 1]) * (x[i] - x[i + 1])) + ((y[i] - y[i + 1]) * (y[i] - y[i + 1])))
            size_i = (_int(_fdiv(distance, step)) if (step > 0.0) else 1)
            if size_i < 1:
                size_i = 2
            ArrayResize(xc, ArraySize(xc) + size_i, 1024)
            ArrayResize(yc, ArraySize(yc) + size_i, 1024)
            t = 0
            while t < size_i:
                xc[index] = _int(MathRound(self.CalcBezierX(_fdiv(float(t), size_i), ptX[1 + (i * 3)], ptX[2 + (i * 3)], ptX[3 + (i * 3)], ptX[4 + (i * 3)])))
                yc[index] = _int(MathRound(self.CalcBezierY(_fdiv(float(t), size_i), ptY[1 + (i * 3)], ptY[2 + (i * 3)], ptY[3 + (i * 3)], ptY[4 + (i * 3)])))
                t += 1
                index += 1
        distance = MathSqrt(((x[size_arr - 1] - x[0]) * (x[size_arr - 1] - x[0])) + ((y[size_arr - 1] - y[0]) * (y[size_arr - 1] - y[0])))
        size_i = (_int(_fdiv(distance, step)) if (step > 0.0) else 1)
        if size_i < 1:
            size_i = 2
        ArrayResize(xc, ArraySize(xc) + size_i, 1024)
        ArrayResize(yc, ArraySize(yc) + size_i, 1024)
        t = 0
        while t < size_i:
            xc[index] = _int(MathRound(self.CalcBezierX(_fdiv(float(t), size_i), ptX[size_pt - 2], ptX[size_pt - 1], ptX[0], ptX[1])))
            yc[index] = _int(MathRound(self.CalcBezierY(_fdiv(float(t), size_i), ptY[size_pt - 2], ptY[size_pt - 1], ptY[0], ptY[1])))
            t += 1
            index += 1
        self.PolygonThick(xc, yc, clr, size, style, LINE_END_ROUND)
    def BitBlt(self, dst_x, dst_y, src, src_width, src_height, src_x, src_y, src_dx, src_dy, mode=0):
        for y in range(0, src_dy):
            for x in range(0, src_dx):
                self.PixelSet(dst_x + x, dst_y + y, src[((src_y + y) * src_width) + src_x + x])
    def FontSet_4(self, name, size, flags=0, angle=0):
        if not TextSetFont(name, size, flags, angle):
            return False
        self.m_fontname = name
        self.m_fontsize = size
        self.m_fontflags = flags
        self.m_fontangle = angle
        return True
    def FontSet_0(self):
        return TextSetFont(self.m_fontname, self.m_fontsize, self.m_fontflags, self.m_fontangle)
    def FontNameSet(self, name):
        if not TextSetFont(name, self.m_fontsize, self.m_fontflags, self.m_fontangle):
            return False
        self.m_fontname = name
        return True
    def FontSizeSet(self, size):
        if not TextSetFont(self.m_fontname, size, self.m_fontflags, self.m_fontangle):
            return False
        self.m_fontsize = size
        return True
    def FontFlagsSet(self, flags):
        if not TextSetFont(self.m_fontname, self.m_fontsize, flags, self.m_fontangle):
            return False
        self.m_fontflags = flags
        return True
    def FontAngleSet(self, angle):
        if not TextSetFont(self.m_fontname, self.m_fontsize, self.m_fontflags, angle):
            return False
        self.m_fontangle = angle
        return True
    def FontGet(self, name, size, flags, angle):
        name.v = self.m_fontname
        size.v = self.m_fontsize
        flags.v = self.m_fontflags
        angle.v = self.m_fontangle
    def FontNameGet(self):
        return self.m_fontname
    def FontSizeGet(self):
        return self.m_fontsize
    def FontFlagsGet(self):
        return self.m_fontflags
    def FontAngleGet(self):
        return self.m_fontangle
    def TextOut(self, x, y, text, clr, alignment=0):
        if self.FontSet_0():
            TextOut(text, x, y, alignment, self.m_pixels, self.m_width, self.m_height, clr, self.m_format)
    def TextWidth(self, text):
        if not self.FontSet_0():
            return 0
        w = 0
        h = 0
        TextGetSize(text, _ValRef(w), _ValRef(h))
        return _int(w)
    def TextHeight(self, text):
        if not self.FontSet_0():
            return 0
        w = 0
        h = 0
        TextGetSize(text, _ValRef(w), _ValRef(h))
        return _int(h)
    def TextSize(self, text, width, height):
        if self.FontSet_0():
            TextGetSize(text, _ValRef(_uint(width.v)), _ValRef(_uint(height.v)))
    @staticmethod
    def GetDefaultColor(i):
        if i < 0:
            return 0
        if i < ArraySize(CCanvas.m_default_colors):
            return CCanvas.m_default_colors[i]
        return ((0xFF000000 | (_uchar((_imod(i, 3) * 60) + (i * 50)) << 16)) | (_uchar((_imod(i + 1, 3) * 60) + (i * 60)) << 8)) | _uchar((_imod(i + 2, 3) * 60) + (i * 50))
    def TransparentLevelSet(self, value):
        total = ArraySize(self.m_pixels)
        value24 = _uint(value << 24)
        for i in range(0, total):
            self.m_pixels[i] = value24 | (self.m_pixels[i] & 0xFFFFFF)
    def LoadFromFile(self, filename):
        if not CCanvas.LoadBitmap(filename, self.m_pixels, _AttrRef(self, 'm_width'), _AttrRef(self, 'm_height')):
            return False
        if self.m_format == COLOR_FORMAT_ARGB_RAW:
            a = 0
            r = 0
            g = 0
            b = 0
            img_size = self.m_width * self.m_height
            for i in range(0, img_size):
                _sw1 = (a := _uchar(self.m_pixels[i] >> 24))
                if _sw1 == 0xFF:
                    pass
                elif _sw1 == 0x00:
                    self.m_pixels[i] = 0
                else:
                    r = _idiv(_uchar(self.m_pixels[i] >> 16) * a, 255)
                    g = _idiv(_uchar(self.m_pixels[i] >> 8) * a, 255)
                    b = _idiv(_uchar(self.m_pixels[i]) * a, 255)
                    self.m_pixels[i] = (((_uchar(a) << 24) | (_uchar(r) << 16)) | (_uchar(g) << 8)) | _uchar(b)
        return True
    def LineStyleGet(self):
        _sw2 = self.m_style
        if _sw2 == 0xFFFFFF:
            return STYLE_SOLID
        elif _sw2 == 0x3FFFF:
            return STYLE_DASH
        elif _sw2 == 0x1C71C7:
            return STYLE_DOT
        elif _sw2 == 0x381FF:
            return STYLE_DASHDOT
        elif _sw2 == 0x1C71FF:
            return STYLE_DASHDOTDOT
        else:
            return self.m_style
    def LineStyleSet(self, style):
        _sw3 = style
        if _sw3 == STYLE_SOLID:
            self.m_style = 0xFFFFFF
        elif _sw3 == STYLE_DASH:
            self.m_style = 0x3FFFF
        elif _sw3 == STYLE_DOT:
            self.m_style = 0x1C71C7
        elif _sw3 == STYLE_DASHDOT:
            self.m_style = 0x381FF
        elif _sw3 == STYLE_DASHDOTDOT:
            self.m_style = 0x1C71FF
        else:
            if (style & 0x80000000) != 0:
                self.m_style = style
        self.m_style_idx = 0
    @staticmethod
    def LoadBitmap(filename, data, width, height):
        header = BitmapHeader()
        result = True
        file = CFileBin()
        img_size = 0
        no_alpha = False
        no_flip = False
        r = 0
        g = 0
        b = 0
        if file.Open(filename, FILE_READ) == INVALID_HANDLE:
            Print('File not found')
            return False
        if file.ReadStruct(_ValRef(header)) != 8:
            Print('Failed to read file header')
            file.Close()
            return False
        width.v = _int(header.imgWidth)
        height.v = _int(header.imgHeight)
        if height.v < 0:
            height.v = -height.v
            no_flip = True
        if header.imgBitCount == 32:
            no_alpha = True
            img_size = file.ReadArray(data)
            if not no_flip:
                for i in range(0, _idiv(height.v, 2)):
                    tmp = Arr(0, 0)
                    ArrayCopy(tmp, data, 0, width.v * i, width.v)
                    ArrayCopy(data, data, width.v * i, width.v * (height.v - i - 1), width.v)
                    ArrayCopy(data, tmp, width.v * (height.v - i - 1), 0, width.v)
            for i in range(0, img_size):
                if _uchar(data[i] >> 24) != 0:
                    no_alpha = False
                    break
            if no_alpha:
                for i in range(0, img_size):
                    data[i] |= 0xFF000000
        else:
            byte_width = 0
            if ArrayResize(data, width.v * height.v) != -1:
                byte_width = width.v * 3
                byte_width = (byte_width + 3) & (~3)
                tmp = Arr(0, 0)
                for i in range(0, height.v):
                    if file.ReadArray(tmp, 0, byte_width) != byte_width:
                        result = False
                        break
                    j = 0
                    k = 0
                    p = width.v * (height.v - i - 1)
                    while j < width.v:
                        r = tmp[k + 2]
                        g = tmp[k + 1]
                        b = tmp[k]
                        data[p] = ((0xFF000000 | (_uchar(r) << 16)) | (_uchar(g) << 8)) | _uchar(b)
                        j += 1
                        p += 1
                        k += 3
            else:
                result = False
        file.Close()
        return result
    def TextOutFast(self, x, y, text, clr, alignment=0):
        TextOut(text, x, y, alignment, self.m_pixels, self.m_width, self.m_height, clr, self.m_format)
    def PixelsSimilar(self, clr0, clr1, threshould):
        dr = MathAbs(((clr0 >> 16) & 0xff) - ((clr1 >> 16) & 0xff))
        dg = MathAbs(((clr0 >> 8) & 0xff) - ((clr1 >> 8) & 0xff))
        db = MathAbs(((clr0 >> 0) & 0xff) - ((clr1 >> 0) & 0xff))
        return (dr <= threshould or dg <= threshould) or db <= threshould
    def PixelTransform(self, x, y, clr, alpha):
        index = (y * self.m_width) + x
        if (((x < 0 or y < 0) or x > self.m_width) or y > self.m_height) or index >= ArraySize(self.m_pixels):
            return
        if alpha == 1:
            self.m_pixels[index] = clr
            return
        clr0 = self.m_pixels[index]
        r0 = ((clr0 >> 16) & 0xFF) * (1.0 - alpha)
        g0 = ((clr0 >> 8) & 0xFF) * (1.0 - alpha)
        b0 = ((clr0 >> 0) & 0xFF) * (1.0 - alpha)
        r1 = ((clr >> 16) & 0xFF) * alpha
        g1 = ((clr >> 8) & 0xFF) * alpha
        b1 = ((clr >> 0) & 0xFF) * alpha
        r = _int(r0 + r1)
        g = _int(g0 + g1)
        b = _int(b0 + b1)
        self.m_pixels[(y * self.m_width) + x] = ((_int(r << 16) | _int(g << 8)) | _int(b << 0)) | _int(255 << 24)
    def PixelTransform4(self, x, y, dx, dy, clr, alpha):
        self.PixelTransform(x + dx, y + dy, clr, alpha)
        self.PixelTransform(x - dx, y + dy, clr, alpha)
        self.PixelTransform(x + dx, y - dy, clr, alpha)
        self.PixelTransform(x - dx, y - dy, clr, alpha)
    def PixelSet4AA(self, x, y, dx, dy, clr):
        self.PixelSetAA(x + dx, y + dy, clr)
        self.PixelSetAA(x - dx, y + dy, clr)
        self.PixelSetAA(x + dx, y - dy, clr)
        self.PixelSetAA(x - dx, y - dy, clr)
    def SegmentVertical(self, x, y1, y2, ysign, r, clr, end_style):
        ye1 = 0
        ye2 = 0
        ys1 = 0
        ys2 = 0
        _sw4 = end_style
        if _sw4 == LINE_END_ROUND:
            ye1 = y1
            ye2 = y2
            ys1 = y1 - _int(ysign * r)
            ys2 = y2 + _int(ysign * r)
        elif _sw4 == LINE_END_BUTT:
            ye1 = y1
            ye2 = y2
            ys1 = y1
            ys2 = y2
        elif _sw4 == LINE_END_SQUARE:
            ye1 = y1 - _int(ysign * r)
            ye2 = y2 + _int(ysign * r)
            ys1 = ye1
            ys2 = ye2
        else:
            return
        for i in range(0, MathAbs(ys2 - ys1) + 1):
            yi = ys1 + (ysign * i)
            j = 0
            while j < (2 * r):
                xi = x - r + j
                dist = self.DistancePointSegment(xi, yi, x, ye1, x, ye2)
                val = MathAbs(_fdiv(dist, r))
                self.PixelTransform(_int(xi), _int(yi), clr, self.FilterFunction(val))
                j += 1
    def SegmentHorizontal(self, x1, x2, y, xsign, r, clr, end_style):
        xe1 = 0
        xe2 = 0
        xs1 = 0
        xs2 = 0
        _sw5 = end_style
        if _sw5 == LINE_END_ROUND:
            xe1 = x1
            xe2 = x2
            xs1 = x1 - _int(xsign * r)
            xs2 = x2 + _int(xsign * r)
        elif _sw5 == LINE_END_BUTT:
            xe1 = x1
            xe2 = x2
            xs1 = x1
            xs2 = x2
        elif _sw5 == LINE_END_SQUARE:
            xe1 = x1 - _int(xsign * r)
            xe2 = x2 + _int(xsign * r)
            xs1 = xe1
            xs2 = xe2
        else:
            return
        for i in range(0, MathAbs(xs2 - xs1) + 1):
            xi = xs1 + (xsign * i)
            j = 0
            while j < (2 * r):
                yi = y - r + j
                dist = self.DistancePointSegment(xi, yi, xe1, y, xe2, y)
                val = MathAbs(_fdiv(dist, r))
                self.PixelTransform(_int(xi), _int(yi), clr, self.FilterFunction(val))
                j += 1
    def Segment(self, x1, y1, x2, y2, kp0, kp1, xsign, ysign, rcos_k, rsin_k, r, clr, end_style):
        if x1 == x2 and y1 == y2:
            return
        if x1 == x2:
            self.SegmentVertical(x1, y1, y2, ysign, r, clr, end_style)
            return
        if y1 == y2:
            self.SegmentHorizontal(x1, x2, y1, xsign, r, clr, end_style)
            return
        xe1 = 0
        ye1 = 0
        xe2 = 0
        ye2 = 0
        xs1 = 0
        ys1 = 0
        xs2 = 0
        ys2 = 0
        _sw6 = end_style
        if _sw6 == LINE_END_ROUND:
            xe1 = x1
            ye1 = y1
            xe2 = x2
            ye2 = y2
            xs1 = x1 - (xsign * _int(rsin_k))
            ys1 = y1 - (ysign * _int(rcos_k))
            xs2 = x2 + (xsign * _int(rsin_k))
            ys2 = y2 + (ysign * _int(rcos_k))
        elif _sw6 == LINE_END_BUTT:
            xe1 = x1
            ye1 = y1
            xe2 = x2
            ye2 = y2
            xs1 = x1
            ys1 = y1
            xs2 = x2
            ys2 = y2
        elif _sw6 == LINE_END_SQUARE:
            xe1 = x1 - (xsign * _int(rsin_k))
            ye1 = y1 - (ysign * _int(rcos_k))
            xe2 = x2 + (xsign * _int(rsin_k))
            ye2 = y2 + (ysign * _int(rcos_k))
            xs1 = xe1
            ys1 = ye1
            xs2 = xe2
            ys2 = ye2
        else:
            return
        p0x = xs1 + (xsign * rcos_k)
        p0y = ys1 - (ysign * rsin_k)
        p1x = xs1 - (xsign * rcos_k)
        p1y = ys1 + (ysign * rsin_k)
        p2x = xs2 + (xsign * rcos_k)
        p2y = ys2 - (ysign * rsin_k)
        p3x = xs2 - (xsign * rcos_k)
        p3y = ys2 + (ysign * rsin_k)
        if MathAbs(kp0) >= 1:
            xi0 = 0.0
            xi1 = 0.0
            height = MathAbs(p3y - p0y)
            i = 0
            while i <= height:
                y = p0y + (ysign * i)
                xi00 = MathRound(p0x + _fdiv(y - p0y, kp0))
                xi01 = MathRound(p1x + _fdiv(y - p1y, kp1))
                xi02 = MathRound(p2x + _fdiv(y - p2y, kp1))
                xi03 = MathRound(p3x + _fdiv(y - p3y, kp0))
                if xsign == 1:
                    xi0 = MathMax(xi00, xi01)
                    xi1 = MathMin(xi02, xi03)
                else:
                    xi0 = MathMin(xi00, xi01)
                    xi1 = MathMax(xi02, xi03)
                width = MathAbs(MathRound(xi1 - xi0))
                j = 0
                while j <= width:
                    xi = xi0 + (xsign * j)
                    dist = self.DistancePointSegment(xi, y, xe1, ye1, xe2, ye2)
                    val = MathAbs(_fdiv(dist, r))
                    self.PixelTransform(_int(xi), _int(y), clr, self.FilterFunction(val))
                    j += 1
                i += 1
        else:
            yi0 = 0.0
            yi1 = 0.0
            width = MathAbs(p2x - p1x)
            i = 0
            while i <= width:
                x = p1x + (xsign * i)
                yi00 = MathRound(p0y + ((x - p0x) * kp0))
                yi01 = MathRound(p1y + ((x - p1x) * kp1))
                yi02 = MathRound(p2y + ((x - p2x) * kp1))
                yi03 = MathRound(p3y + ((x - p3x) * kp0))
                if ysign == 1:
                    yi0 = MathMax(yi00, yi02)
                    yi1 = MathMin(yi01, yi03)
                else:
                    yi0 = MathMin(yi00, yi02)
                    yi1 = MathMax(yi01, yi03)
                height = MathAbs(yi1 - yi0)
                j = 0
                while j <= height:
                    yi = yi0 + (ysign * j)
                    dist = self.DistancePointSegment(x, yi, xe1, ye1, xe2, ye2)
                    val = MathAbs(_fdiv(dist, r))
                    self.PixelTransform(_int(x), _int(yi), clr, self.FilterFunction(val))
                    j += 1
                i += 1
    def DistancePointSegment(self, px, py, x1, y1, x2, y2):
        a = ((px - x1) * (px - x1)) + ((py - y1) * (py - y1))
        b = ((px - x2) * (px - x2)) + ((py - y2) * (py - y2))
        c = ((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1))
        if a >= (b + c):
            return MathSqrt(b)
        if b >= (a + c):
            return MathSqrt(a)
        a = MathSqrt(a)
        b = MathSqrt(b)
        c = MathSqrt(c)
        p = (a + b + c) / 2
        s = MathSqrt((p - a) * (p - b) * (p - c) * p)
        if MathIsValidNumber(s):
            return _fdiv(s * 2.0, c)
        else:
            return 0.0
    def AngleCalc(self, x1, y1, x2, y2):
        fi = 0.0
        if x1 == x2:
            if y1 == y2:
                return EMPTY_VALUE
            fi = (M_PI_2 if (y2 < y1) else (3 * M_PI_2))
        else:
            fi = atan(_fdiv(float(y1 - y2), x2 - x1))
            if x2 < x1:
                fi += M_PI
            else:
                if fi < 0:
                    fi += 2 * M_PI
        return fi
    def PointClassify(self, p0, p1, p2):
        return ((p1.x - p0.x) * (p2.y - p0.y)) - ((p2.x - p0.x) * (p1.y - p0.y))
    def PolygonClassify(self, p):
        total = ArraySize(p)
        im = 0
        xm = p[0].x
        ym = p[0].y
        for i in range(1, total):
            if p[i].y > ym:
                continue
            if p[i].y == ym and p[i].x > xm:
                continue
            im = i
            xm = p[i].x
            ym = p[i].y
        return self.PointClassify(p[_imod(im - 1 + total, total)], p[im], p[_imod(im + 1, total)])
    def IsPolygonConvex(self, p):
        total = ArraySize(p)
        if total == 3:
            return True
        res = (-1 if (self.PointClassify(p[0], p[1], p[2]) < 0) else 1)
        for i in range(1, total):
            res1 = (-1 if (self.PointClassify(p[i], p[_imod(i + 1, total)], p[_imod(i + 2, total)]) < 0) else 1)
            if res != res1:
                return False
        return True
    def PolygonNormalize(self, p):
        total = ArraySize(p)
        imin = 0
        xmin = p[0].x
        ymin = p[0].y
        for i in range(1, total):
            if p[i].y > ymin:
                continue
            if p[i].y == ymin:
                if p[i].x < xmin:
                    xmin = p[i].x
                    imin = i
                continue
            xmin = p[i].x
            ymin = p[i].y
            imin = i
        if imin == 0:
            return
        for i in range(0, imin):
            tmp = _copy(p[0])
            ArrayCopy(p, p, 0, 1)
            _assign(p[total - 1], tmp)
    def PolygonIntersect(self, p, add):
        total = ArraySize(p)
        res = (-1 if (self.PolygonClassify(p) < 0) else 1)
        for i in range(0, total):
            rr = (-1 if (self.PointClassify(p[i], p[_imod(i + 1, total)], p[_imod(i + 2, total)]) < 0) else 1)
            rl = (-1 if (self.PointClassify(p[_imod(total - i - 2, total)], p[_imod(total - i - 1, total)], p[_imod(total - i, total)]) < 0) else 1)
            if rl != res or rr != res:
                res = total - i - 1 - (i + 1)
                if res < 0:
                    return
                if res < 2:
                    ArrayResize(add, total - i)
                    _assign(add[0], p[0])
                    ArrayCopy(add, p, 1, i + 1, total - i - 1)
                    ArrayResize(p, i + 2)
                else:
                    ArrayResize(add, res + 1)
                    ArrayCopy(add, p, 0, i + 1, res + 1)
                    ArrayCopy(p, p, i + 2, i + res + 1, total - res - i - 1)
                    ArrayResize(p, total - res + 1)
                break
    def PolygonFill(self, p, clr):
        il = 0
        ir = 0
        xl = 0.0
        xr = 0.0
        yy = 0
        dl = 0.0
        dr = 0.0
        total = ArraySize(p)
        if total < 3:
            return
        while not self.IsPolygonConvex(p):
            add = Arr(0, 0, factory=CPoint)
            self.PolygonIntersect(p, add)
            self.PolygonNormalize(add)
            self.PolygonFill(add, clr)
            ArrayFree(add)
        total = ArraySize(p)
        ir = 0
        il = ir
        xr = p[0].x
        xl = xr
        yy = p[0].y
        if yy == p[1].y:
            xr = p[(ir := 1)].x
        self.LineHorizontal(_int(MathCeil(xl)), _int(MathFloor(xr)), yy, clr)
        while True:
            while yy == p[il].y:
                il = _imod(il - 1 + total, total)
                if yy > p[il].y:
                    return
                if yy != p[il].y:
                    dl = _fdiv(p[il].x - xl, p[il].y - yy)
                    self.LineHorizontal(_int(MathCeil(xl + (dl / 2))), _int(MathFloor(xl)), yy, clr)
                    xl += dl / 2
                else:
                    self.LineHorizontal(_int(MathCeil(xl)), _int(MathFloor(p[il].x)), yy, clr)
            while yy == p[ir].y:
                ir = _imod(ir + 1, total)
                if yy > p[ir].y:
                    return
                if yy != p[ir].y:
                    dr = _fdiv(p[ir].x - xr, p[ir].y - yy)
                    self.LineHorizontal(_int(MathCeil(xr)), _int(MathFloor(xr + (dr / 2))), yy, clr)
                    xr += dr / 2
                else:
                    self.LineHorizontal(_int(MathCeil(p[ir].x)), _int(MathFloor(xr)), yy, clr)
            yy += 1
            if yy == p[il].y:
                xl = p[il].x
            else:
                xl += dl
            if yy == p[ir].y:
                xr = p[ir].x
            else:
                xr += dr
            self.LineHorizontal(_int(MathCeil(xl)), _int(MathFloor(xr)), yy, clr)
            if not (il >= ir and ir != 0):
                break
    def CalcCurveBezierEndp(self, xend, yend, xadj, yadj, tension, x, y):
        x.v = (tension * (xadj - xend)) + xend
        y.v = (tension * (yadj - yend)) + yend
    def CalcCurveBezier(self, x, y, i, tension, x1, y1, x2, y2):
        xdiff = 0.0
        ydiff = 0.0
        xdiff = x[i + 2] - x[i]
        ydiff = y[i + 2] - y[i]
        x1.v = x[i + 1] - (tension * xdiff)
        y1.v = y[i + 1] - (tension * ydiff)
        x2.v = x[i + 1] + (tension * xdiff)
        y2.v = y[i + 1] + (tension * ydiff)
    def CalcBezierX(self, t, x0, x1, x2, x3):
        return (x0 * ((1 - t) * (1 - t) * (1 - t))) + (x1 * 3 * t * ((1 - t) * (1 - t))) + (x2 * 3 * (t * t) * (1 - t)) + (x3 * (t * t * t))
    def CalcBezierY(self, t, y0, y1, y2, y3):
        return (y0 * ((1 - t) * (1 - t) * (1 - t))) + (y1 * 3 * t * ((1 - t) * (1 - t))) + (y2 * 3 * (t * t) * (1 - t)) + (y3 * (t * t * t))
    def FilterFunction(self, x):
        if x <= 0.8:
            return 1.0
        else:
            return MathExp((-(x - 0.8)) * (x - 0.8) * 50)
CCanvas.m_default_colors = Arr.of([((0xFF000000 | (_uchar(0) << 16)) | (_uchar(0) << 8)) | _uchar(255), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(0) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(0) << 16)) | (_uchar(128) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(242) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(0) << 8)) | _uchar(128), ((0xFF000000 | (_uchar(0) << 16)) | (_uchar(255) << 8)) | _uchar(0), ((0xFF000000 | (_uchar(185) << 16)) | (_uchar(0) << 8)) | _uchar(61), ((0xFF000000 | (_uchar(0) << 16)) | (_uchar(183) << 8)) | _uchar(239), ((0xFF000000 | (_uchar(255) << 16)) | (_uchar(128) << 8)) | _uchar(0)], fill=0, dyn=False, size=9)

class argb(MqlObject):
    _q_fields = ('clr', 'c')
    def __init__(self, *args):
        self.clr = 0
        self.c = Arr(4, 0, dyn=False)

class Window(MqlObject):
    _q_fields = ('ChartId', 'Color', 'Width', 'Height', 'height', 'Left_bar', 'Right_bar', 'Total_bars', 'BarsInWind', 'Y_min', 'Y_max', 'dy_pix', 'dx_pix', 'MouseX', 'MouseY', 'MouseBar', 'MousePrice', 'MouseTime', 'MouseStatus', 'IdEvent', 'lparam', 'MouseSubWin', 'WindowsTotal', 'SubWin', 'time')
    def __init__(self, *args):
        self.ChartId = 0
        self.Color = 0
        self.Width = 0
        self.Height = 0
        self.height = Arr(0, 0)
        self.Left_bar = 0
        self.Right_bar = 0.0
        self.Total_bars = 0.0
        self.BarsInWind = 0
        self.Y_min = 0.0
        self.Y_max = 0.0
        self.dy_pix = 0.0
        self.dx_pix = 0
        self.MouseX = 0
        self.MouseY = 0
        self.MouseBar = 0.0
        self.MousePrice = 0.0
        self.MouseTime = 0
        self.MouseStatus = 0
        self.IdEvent = 0
        self.lparam = 0
        self.MouseSubWin = 0
        self.WindowsTotal = 0
        self.SubWin = 0
        self.time = Arr(0, 0)

class B17(MqlObject):
    _q_fields = ()
    def __init__(self):
        pass
    def _q_dtor(self):
        if CheckPointer(Canvas) != POINTER_INVALID:
            _delete(Canvas)
        for i in range(0, ArraySize(iC)):
            if CheckPointer(iC[i]) != POINTER_INVALID:
                _delete(iC[i])

class iCanvas(CCanvas):
    _q_fields = ('T', 'Pr', 'FullWinCanvW', 'FullWinCanvH', 'TextPosX', 'TextPosY', 'StepTextLine', 'TextColor', 'ProgType', 'SubWin', 'Handle')
    def __init__(self, chart_id=0, Xpos=0, Ypos=0, Name='iCanvas', width=0, height=0, formatCF=COLOR_FORMAT_ARGB_NORMALIZE, subwin=-1):
        global WidOld
        CCanvas.__init__(self)
        self.T = Arr(1, 0, dyn=False)
        self.Pr = Arr(1, 0.0, dyn=False)
        self.FullWinCanvW = False
        self.FullWinCanvH = False
        self.TextPosX = 0
        self.TextPosY = 0
        self.StepTextLine = 0
        self.TextColor = 0
        self.ProgType = 0
        self.SubWin = 0
        self.Handle = 0
        ResetLastError()
        self.ProgType = MQLInfoInteger(MQL_PROGRAM_TYPE)
        if chart_id == 0:
            chart_id = ChartID()
        size_iC = ArraySize(iC)
        if size_iC > 0:
            if CheckPointer(iC[size_iC - 1]) == POINTER_INVALID:
                ArrayResize(iC, size_iC - 1)
                size_iC -= 1
        W.WindowsTotal = _int(ChartGetInteger(W.ChartId, CHART_WINDOWS_TOTAL))
        if subwin < 0:
            if self.ProgType == PROGRAM_INDICATOR:
                self.SubWin = ChartWindowFind()
            else:
                self.SubWin = 0
        elif subwin < W.WindowsTotal:
            self.SubWin = subwin
        else:
            self.SubWin = 0
        if CheckPointer(Canvas) == POINTER_INVALID:
            W.ChartId = chart_id
            ChartSetInteger(W.ChartId, CHART_EVENT_MOUSE_MOVE, True)
            GetWindowProperties(W)
            W.SubWin = self.SubWin
            W.MouseX = _idiv(W.Width, 2)
            W.MouseY = _idiv(W.Height, 2)
            W.MouseBar = self.Bar(W.MouseX)
            W.MousePrice = self.Close(W.MouseX)
            WidOld = W.Width
            HeiOld[self.SubWin] = W.height[self.SubWin]
            W.MouseSubWin = XYToTimePrice(W.MouseX, W.MouseY, _AttrRef(W, 'MouseTime'), _AttrRef(W, 'MousePrice'))
        if width == 0:
            width = W.Width
            self.FullWinCanvW = True
            Xpos = 0
        else:
            self.FullWinCanvW = False
        if height == 0:
            height = W.height[self.SubWin]
            self.FullWinCanvH = True
            Ypos = 0
        else:
            self.FullWinCanvH = False
        Name += IntegerToString(rand()) + IntegerToString(rand())
        self.Handle = ChartGetInteger(chart_id, CHART_WINDOW_HANDLE, self.SubWin)
        if not self.CreateBitmapLabel_8(chart_id, self.SubWin, Name, Xpos, Ypos, width, height, formatCF):
            Print('Error creating canvas: ', GetLastError())
        else:
            ArrayResize(iC, size_iC + 1)
            iC[size_iC] = self
        ChartSetInteger(self.m_chart_id, CHART_FOREGROUND, self.SubWin, False)
        ObjectSetInteger(self.m_chart_id, self.m_objname, OBJPROP_BACK, False)
        self.TextPosX = 20
        self.TextPosY = 100
        self.StepTextLine = 22
        self.TextColor = clrDarkOrchid
        self.CurentFont()
        self.Erase(0)
    def _q_dtor(self):
        self.Destroy()
        ChartRedraw()
    def X_1(self, bar):
        return (float(W.Left_bar) - bar) * W.dx_pix
    def X_2(self, Time):
        b = wBarShift(Time, W.time, Period())
        return self.X_1(b)
    def Y(self, Price):
        if W.dy_pix == 0:
            W.dy_pix = 1.0
        return _fdiv(W.Y_max - Price, W.dy_pix)
    def Price(self, y):
        return W.Y_max - _fdiv(y * (W.Y_max - W.Y_min), W.Height)
    def Bar(self, x):
        return float(W.Left_bar) + 1 - _fdiv(x, float(W.dx_pix))
    def TimePos(self, x):
        B = self.Bar(x)
        if B < 0:
            self.T[0] = W.time[W.BarsInWind - 1] - (_long(B) * PeriodSeconds())
        elif B < W.Right_bar or B > W.Left_bar:
            self.T[0] = iTime(Symbol(), Period(), _int(B))
        else:
            self.T[0] = W.time[W.BarsInWind - Floor(B) - 1 + _int(W.Right_bar)]
        return self.T[0] + _int(float(PeriodSeconds()) * (1 - B + _int(B)))
    def Close(self, x):
        CopyClose(Symbol(), Period(), _int(self.Bar(x)), 1, self.Pr)
        return self.Pr[0]
    def Open(self, x):
        CopyOpen(Symbol(), Period(), _int(self.Bar(x)), 1, self.Pr)
        return self.Pr[0]
    def High(self, x):
        CopyHigh(Symbol(), Period(), _int(self.Bar(x)), 1, self.Pr)
        return self.Pr[0]
    def Low(self, x):
        CopyLow(Symbol(), Period(), _int(self.Bar(x)), 1, self.Pr)
        return self.Pr[0]
    def FullWinCanvWidth(self):
        return self.FullWinCanvW
    def FullWinCanvHeight(self):
        return self.FullWinCanvH
    def Comm(self, text):
        self.TextOut(self.TextPosX, self.TextPosY, text, self.TextColor)
        self.TextPosY += self.StepTextLine
    def TextPosition_1(self, x, y):
        self.TextPosX = x
        self.TextPosY = y
    def TextPosition_2(self, x, y):
        if x > 100:
            x = 100.0
        elif x < 0:
            x = 0.0
        self.TextPosX = Round((x * W.Width) / 100)
        if y > 100:
            y = 100.0
        elif y < 0:
            y = 0.0
        self.TextPosY = Round((y * W.Height) / 100)
    def CurentFont(self, FontName='Courier New', size=18, LineStep=20, clr=clrDarkOrchid, transp=1.0):
        self.FontSet_4(FontName, size)
        if transp > 1:
            transp = 1.0
        if transp < 0:
            transp = 0.0
        self.StepTextLine = LineStep
        self.TextColor = ColorToARGB(clr, _uchar((255 * transp) + 0.5))
    def LineD(self, x1, y1, x2, y2, clr):
        if fabs(x2 - x1) < 1.1 and fabs(y2 - y1) < 1.1:
            self.PixelSet(Round(x2), Round(y2), clr)
            return
        if ((x1 != x1 or x2 != x2) or y1 != y1) or y2 != y2:
            return
        if Round(x1) == Round(x2):
            self.LineVertical(Round(x1), Round(y1), Round(y2), clr)
            return
        if Round(y1) == Round(y2):
            self.LineHorizontal(Round(x1), Round(x2), Round(y1), clr)
            return
        if x1 > x2:
            temp = x1
            x1 = x2
            x2 = temp
            temp = y1
            y1 = y2
            y2 = temp
        if ((x1 >= self.m_width or x2 < 0) or (y1 >= self.m_height and y2 >= self.m_height)) or (y1 < 0 and y2 < 0):
            return
        dx = _fdiv(x2 - x1, y2 - y1)
        dy = _fdiv(y2 - y1, x2 - x1)
        if x1 < 0:
            y1 = y1 - (dy * x1)
            x1 = 0.0
        if x2 >= (self.m_width - 0.5):
            y2 = y2 - (dy * (x2 - self.m_width + 1))
            x2 = self.m_width - 1
        if y2 > y1:
            if y1 < 0:
                x1 = x1 - (dx * y1)
                y1 = 0.0
            if y2 >= (self.m_height - 0.5):
                x2 = x2 - (dx * (y2 - self.m_height + 1))
                y2 = self.m_height - 1
        else:
            if y2 < 0:
                x2 = x2 - (dx * y2)
                y2 = 0.0
            if y1 >= (self.m_height - 0.5):
                x1 = x1 - (dx * (y1 - self.m_height + 1))
                y1 = self.m_height - 1
        if fabs(dx) >= 1:
            x = x1
            y = y1
            while x <= x2:
                self.PixelSet(Round(x), Round(y), clr)
                x += 1
                y += dy
        elif y2 > y1:
            y = y1
            x = x1
            while y <= y2:
                self.PixelSet(Round(x), Round(y), clr)
                y += 1
                x += dx
        else:
            y = y2
            x = x2
            while y <= y1:
                self.PixelSet(Round(x), Round(y), clr)
                y += 1
                x += dx
    def SetBack(self, bck):
        ObjectSetInteger(self.m_chart_id, self.m_objname, OBJPROP_BACK, bck)
    def MoveCanvas(self, x, y):
        if ObjectSetInteger(self.m_chart_id, self.m_objname, OBJPROP_XDISTANCE, x) and ObjectSetInteger(self.m_chart_id, self.m_objname, OBJPROP_YDISTANCE, y):
            return True
        else:
            return False

class BitmapHeader(MqlObject):
    _q_fields = ('type', 'size', 'reserv', 'offbits', 'imgSSize', 'imgWidth', 'imgHeight', 'imgPlanes', 'imgBitCount', 'imgCompression', 'imgSizeImage', 'imgXPelsPerMeter', 'imgYPelsPerMeter', 'imgClrUsed', 'imgClrImportant')
    def __init__(self, *args):
        self.type = 0
        self.size = 0
        self.reserv = 0
        self.offbits = 0
        self.imgSSize = 0
        self.imgWidth = 0
        self.imgHeight = 0
        self.imgPlanes = 0
        self.imgBitCount = 0
        self.imgCompression = 0
        self.imgSizeImage = 0
        self.imgXPelsPerMeter = 0
        self.imgYPelsPerMeter = 0
        self.imgClrUsed = 0
        self.imgClrImportant = 0

def Ceil(x):
    return ((_int(x) + 1) if ((x - _int(x)) > 0) else _int(x))

def Round(x):
    return (_int(x + 0.5) if (x > 0) else _int(x - 0.5))

def Floor(x):
    return (_int(x) if (x > 0) else (_int(x) - 1) if ((_int(x) - x) > 0) else _int(x))

def XYToTimePrice(x, y, Time, Price, id_=0):
    global _s_XYToTimePrice_ChartChange, _s_XYToTimePrice_Cur_wind, _s_XYToTimePrice_nofirst
    if sizeArr > W.BarsInWind or sizeArr < 1:
        return _s_XYToTimePrice_Cur_wind
    if not _s_XYToTimePrice_nofirst:
        _s_XYToTimePrice_ChartChange = True
        _s_XYToTimePrice_nofirst = True
    if id_ == CHARTEVENT_CHART_CHANGE:
        _s_XYToTimePrice_ChartChange = True
        return _s_XYToTimePrice_Cur_wind
    if _s_XYToTimePrice_ChartChange:
        if W.WindowsTotal > 10:
            Print('Too many subwindows')
            return -1
        _s_XYToTimePrice_Hei[0] = W.height[0]
        for i in range(1, W.WindowsTotal):
            _s_XYToTimePrice_Hei[i] = W.height[i] + _s_XYToTimePrice_Hei[i - 1] + 2
        _s_XYToTimePrice_y_min[0] = W.Y_min
        _s_XYToTimePrice_y_max[0] = W.Y_max
        if W.WindowsTotal > 0:
            for i in range(1, W.WindowsTotal):
                _s_XYToTimePrice_y_min[i] = (W.Y_min if (i == W.SubWin) else ChartGetDouble(W.ChartId, CHART_PRICE_MIN, i))
                _s_XYToTimePrice_y_max[i] = (W.Y_max if (i == W.SubWin) else ChartGetDouble(W.ChartId, CHART_PRICE_MAX, i))
    if ((x > (W.Width + 1) or x < 0) or y < 0) or y >= (_s_XYToTimePrice_Hei[W.WindowsTotal - 1] + 1):
        return -1
    _s_XYToTimePrice_Cur_wind = -1
    if y >= 0 and y <= _s_XYToTimePrice_Hei[0]:
        _s_XYToTimePrice_Cur_wind = 0
    elif W.WindowsTotal > 1:
        for i in range(1, W.WindowsTotal):
            if y > (_s_XYToTimePrice_Hei[i - 1] + 1) and y <= _s_XYToTimePrice_Hei[i]:
                _s_XYToTimePrice_Cur_wind = i
                break
    if _s_XYToTimePrice_Cur_wind >= 0:
        if _s_XYToTimePrice_Cur_wind > 0:
            y = y - _s_XYToTimePrice_Hei[_s_XYToTimePrice_Cur_wind - 1] - 2
        hh = _s_XYToTimePrice_Hei[_s_XYToTimePrice_Cur_wind]
        if _s_XYToTimePrice_Cur_wind > 0:
            hh -= _s_XYToTimePrice_Hei[_s_XYToTimePrice_Cur_wind - 1] + 2
        if hh != 0:
            Price.v = _s_XYToTimePrice_y_min[_s_XYToTimePrice_Cur_wind] + _fdiv((hh - y) * (_s_XYToTimePrice_y_max[_s_XYToTimePrice_Cur_wind] - _s_XYToTimePrice_y_min[_s_XYToTimePrice_Cur_wind]), hh)
        B = W.Left_bar + 1 - _fdiv(x, float(W.dx_pix))
        TT = 0
        if B < 0:
            TT = W.time[W.BarsInWind - 1] - (_long(B) * PeriodSeconds())
        elif B < W.Right_bar or B > W.Left_bar:
            TT = iTime(Symbol(), Period(), _int(B))
        else:
            i = W.BarsInWind - Floor(B) - 1 + _int(W.Right_bar)
            if i >= 0 and i < ArraySize(W.time):
                TT = W.time[i]
            else:
                TT = iTime(Symbol(), Period(), _int(B))
        Time.v = TT + _int(float(PeriodSeconds()) * (1 - B + _int(B)))
    _s_XYToTimePrice_ChartChange = False
    return _s_XYToTimePrice_Cur_wind

def GetWindowProperties(w):
    global _s_GetWindowProperties_lastTF, _s_GetWindowProperties_oldLB, _s_GetWindowProperties_oldRB, sizeArr
    if _s_GetWindowProperties_oldLB is _UNSET:
        _s_GetWindowProperties_oldLB = w.Left_bar
    if _s_GetWindowProperties_oldRB is _UNSET:
        _s_GetWindowProperties_oldRB = w.Right_bar
    max_bars = TerminalInfoInteger(TERMINAL_MAXBARS)
    W.WindowsTotal = _int(ChartGetInteger(W.ChartId, CHART_WINDOWS_TOTAL))
    w.Color = _uint(ChartGetInteger(W.ChartId, CHART_COLOR_BACKGROUND))
    w.Width = _int(ChartGetInteger(W.ChartId, CHART_WIDTH_IN_PIXELS))
    w.Left_bar = _int(ChartGetInteger(W.ChartId, CHART_FIRST_VISIBLE_BAR))
    if w.Left_bar >= max_bars:
        w.Left_bar = max_bars - 1
    w.Y_min = ChartGetDouble(W.ChartId, CHART_PRICE_MIN)
    w.Y_max = ChartGetDouble(W.ChartId, CHART_PRICE_MAX)
    if w.Y_max == 0:
        w.Y_max = 1.0
    ArrayResize(w.height, W.WindowsTotal)
    ArrayResize(HeiOld, W.WindowsTotal)
    for i in range(0, W.WindowsTotal):
        w.height[i] = _int(ChartGetInteger(W.ChartId, CHART_HEIGHT_IN_PIXELS, i))
    w.Height = w.height[0]
    if (w.Y_max - w.Y_min) != 0 and w.Height != 0:
        w.dy_pix = _fdiv(w.Y_max - w.Y_min, w.Height)
    w.dx_pix = _int(1 << ChartGetInteger(W.ChartId, CHART_SCALE))
    w.Total_bars = _fdiv(float(w.Width), w.dx_pix)
    w.Right_bar = w.Left_bar - w.Total_bars
    if w.Right_bar < 0:
        w.Right_bar = 0.0
    oldBIW = w.BarsInWind
    w.BarsInWind = w.Left_bar - _int(w.Right_bar) + 1
    if (_s_GetWindowProperties_oldRB != w.Right_bar or _s_GetWindowProperties_oldLB != w.Left_bar) or _s_GetWindowProperties_lastTF != Period():
        sizeArr = CopyTime(None, Period(), _int(w.Right_bar), w.BarsInWind, w.time)
    _s_GetWindowProperties_lastTF = Period()
    _s_GetWindowProperties_oldLB = w.Left_bar
    _s_GetWindowProperties_oldRB = w.Right_bar

def MyChartEvent_1(id_, lparam, dparam, sparam):
    pass

def MyChartEvent_2(id_, lparam, dparam, sparam):
    global N, _s_MyChartEvent_click, day, mouse, per
    if sparam == '1':
        if not _s_MyChartEvent_click:
            if mouse:
                mouse = False
            else:
                mouse = True
            _s_MyChartEvent_click = True
    else:
        _s_MyChartEvent_click = False
    if sparam == '32':
        if not _s_MyChartEvent_click:
            if day:
                day = False
            else:
                day = True
            _s_MyChartEvent_click = True
            Draw()
    else:
        _s_MyChartEvent_click = False
    if id_ == CHARTEVENT_MOUSE_MOVE and mouse:
        if not day:
            per = (24 * 60) + (W.MouseY * 60)
        else:
            per = 24 * 60 * PeriodSeconds()
        N = _fdiv(float(W.MouseX), W.Width)
        Draw()
    if id_ == CHARTEVENT_MOUSE_MOVE:
        X = _idiv(W.Width, 2)
        Y = _idiv(W.Height, 2) - 5
        r = _idiv(W.Height, 2) - 7
        dd = sqrt(((W.MouseX - X) * (W.MouseX - X)) + ((W.MouseY - Y) * (W.MouseY - Y)))
        info.Erase(0)
        if dd < r and dd > (r * 0.3):
            info.MoveCanvas(W.MouseX + 3, W.MouseY - 10)
            info.TextPosition_1(0, 0)
            info.Comm(DoubleToString(min_ + _fdiv((max_ - min_) * (dd - (r * 0.3)), r * 0.7), _int(SymbolInfoInteger(Symbol(), SYMBOL_DIGITS))))
        elif W.MouseY > (W.Height - 20):
            xx = (W.MouseX if (W.MouseX < (W.Width - 160)) else (W.MouseX - 160))
            info.MoveCanvas(xx, W.Height - 25)
            info.TextPosition_1(0, 0)
            info.Comm(TimeToString(ti[start + _int(_fdiv((ArraySize(ti) - start) * float(W.MouseX), W.Width))]))
        info.Update()

def SetOnChart_1(x):
    global OnChart, OnZ
    OnChart = False
    OnZ = False

def SetOnChart_2(x):
    global OnChart, OnZ
    OnChart = True
    OnZ = False

def OnChartEvent(id_, lparam, dparam, sparam):
    if sparam == '0':
        W.MouseStatus = NO_PRESSED
    elif sparam == '1':
        W.MouseStatus = LEFT_BUTTON_PRESSED
    elif sparam == '2':
        W.MouseStatus = RIGHT_BUTTON_PRESSED
    elif sparam == '3':
        W.MouseStatus = LEFT_AND_RIGHT_BUTTONS_PRESSED
    else:
        W.MouseStatus = KEY_PRESSED
    W.IdEvent = id_
    W.lparam = lparam
    if id_ == CHARTEVENT_MOUSE_MOVE:
        W.MouseX = _int(lparam)
        W.MouseY = _int(dparam)
        W.MouseBar = float(W.Left_bar) + 1 - _fdiv(float(W.MouseX), float(W.dx_pix))
        W.MouseSubWin = XYToTimePrice(W.MouseX, W.MouseY, _AttrRef(W, 'MouseTime'), _AttrRef(W, 'MousePrice'), id_)
        if W.MouseSubWin > 0:
            for i in range(0, W.MouseSubWin):
                W.MouseY = W.MouseY - W.height[i] - 2
    if id_ == CHARTEVENT_CHART_CHANGE:
        ChartChanged()
    if OnZ:
        SetOnChart_2(sizeArr)
    if OnChart:
        MyChartEvent_2(id_, lparam, dparam, sparam)

def ChartChanged():
    global WidOld, _s_ChartChanged_preWinTotal
    if _s_ChartChanged_preWinTotal is _UNSET:
        _s_ChartChanged_preWinTotal = W.WindowsTotal
    GetWindowProperties(W)
    if _s_ChartChanged_preWinTotal != W.WindowsTotal:
        for i in range(ArraySize(iC) - 1, 0 - 1, -1):
            if CheckPointer(iC[i]) != POINTER_INVALID:
                if iC[i].SubWin >= W.WindowsTotal:
                    iC[i].SubWin -= 1
    for i in range(ArraySize(iC) - 1, 0 - 1, -1):
        if CheckPointer(iC[i]) != POINTER_INVALID:
            if iC[i].FullWinCanvWidth():
                if iC[i].FullWinCanvHeight():
                    if W.Width != WidOld or W.height[iC[i].SubWin] != HeiOld[iC[i].SubWin]:
                        iC[i].Resize(W.Width, W.height[iC[i].SubWin])
                        HeiOld[iC[i].SubWin] = W.height[iC[i].SubWin]
                else:
                    if W.Width != WidOld:
                        iC[i].Resize(W.Width, iC[i].Height())
            else:
                if iC[i].FullWinCanvHeight():
                    if W.height[iC[i].SubWin] != HeiOld[iC[i].SubWin]:
                        iC[i].Resize(iC[i].Width(), W.height[iC[i].SubWin])
                        HeiOld[iC[i].SubWin] = W.height[iC[i].SubWin]
        else:
            ArrayRemove(iC, i, 1)
    WidOld = W.Width
    _s_ChartChanged_preWinTotal = W.WindowsTotal
    XYToTimePrice(0, 0, _AttrRef(W, 'MouseTime'), _AttrRef(W, 'MousePrice'), CHARTEVENT_CHART_CHANGE)

def wBarShift(t, arr, tf):
    global _s_wBarShift_lastTF, _s_wBarShift_last_t
    if _s_wBarShift_lastTF is _UNSET:
        _s_wBarShift_lastTF = tf
    size = ArraySize(arr)
    PerSec = PeriodSeconds(tf)
    cur = 0
    Start = 0
    fin = size - 1
    if _s_wBarShift_last_t is _UNSET:
        _s_wBarShift_last_t = (arr[fin] if (W.Right_bar == 0 and tf == Period()) else (TimeCurrent() - _idiv(GetTickCount(), 1000)))
    if (t > arr[0] and t < arr[fin]) and tf == Period():
        if tf > PERIOD_D1:
            while True:
                cur = _idiv(Start + fin, 2)
                if t < arr[cur]:
                    if t >= arr[cur - 1]:
                        return size + _int(W.Right_bar) - cur - _fdiv(float(t - arr[cur - 1]), PerSec)
                    fin = cur
                else:
                    if t < arr[cur + 1]:
                        return size - 1 + _int(W.Right_bar) - cur - _fdiv(float(t - arr[cur]), PerSec)
                    if Start == cur:
                        return 0.0
                    Start = cur
        else:
            while True:
                cur = _idiv(Start + fin, 2)
                if t < arr[cur]:
                    if t >= arr[cur - 1]:
                        return size + _int(W.Right_bar) - cur - _fdiv(float(_imod(t, PerSec)), PerSec)
                    fin = cur
                else:
                    if t < arr[cur + 1]:
                        return size - 1 + _int(W.Right_bar) - cur - _fdiv(float(_imod(t, PerSec)), PerSec)
                    if Start == cur:
                        return 0.0
                    Start = cur
                if (arr[fin] - arr[Start]) == ((fin - Start) * PerSec):
                    return size - 1 + _int(W.Right_bar) - Start - _fdiv(float(t - arr[Start]), PerSec)
    tc1 = 0
    if W.Right_bar == 0 and tf == Period():
        tc1 = arr[fin]
    else:
        if tf == _s_wBarShift_lastTF:
            tc1 = _idiv(GetTickCount(), 1000) + _s_wBarShift_last_t
        else:
            tc1 = TimeCurrent()
            _s_wBarShift_last_t = tc1 - _idiv(GetTickCount(), 1000)
            _s_wBarShift_lastTF = tf
        tc1 = tc1 - _imod(tc1, PerSec)
    if t >= tc1:
        return _fdiv(float(tc1 - t), PerSec)
    ib = iBarShift(Symbol(), tf, t)
    if tf < PERIOD_W1:
        return ib - _fdiv(float(_imod(t, PerSec)), PerSec)
    else:
        return ib - _fdiv(float(t - iTime(Symbol(), tf, ib)), PerSec)

def OnInit():
    global per
    per = 24 * 60
    ChartSetInteger(0, CHART_SHOW, False)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ChartSetInteger(0, CHART_SHOW, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    d = rates_total - prev_calculated
    if d > 1 or d < 0:
        ArrayCopy(cl, close)
        ArrayCopy(ti, time)
        Draw()
    else:
        if d == 1:
            ArrayResize(cl, rates_total)
            ArrayResize(ti, rates_total)
        cl[rates_total - 1] = close[rates_total - 1]
        ti[rates_total - 1] = time[rates_total - 1]
    return rates_total

def Draw():
    global max_, min_, start
    X = _idiv(W.Width, 2)
    Y = _idiv(W.Height, 2) - 5
    size = ArraySize(cl)
    Canvas.Erase()
    start = _int(size * N)
    if start >= size:
        start = size - 1
    max_ = cl[ArrayMaximum(cl, start)]
    min_ = cl[ArrayMinimum(cl, start)]
    if (max_ - min_) <= 0:
        return
    nn = 0
    c = 0.0
    for i in range(start, size):
        r = (_idiv(W.Height, 2) - 7) * (0.3 + _fdiv(0.7 * (cl[i] - min_), max_ - min_))
        a = 0.0
        if day:
            a = _fdiv(2 * M_PI * float(_imod(ti[i], per)), per) - M_PI_2
        else:
            a = _fdiv(2 * M_PI * float(_imod(i, per)), per) - M_PI_2
        cc = cos(a)
        if c < 0 and cc >= 0:
            nn += 1
        c = cc
        x = Round(X + (c * r))
        y = Round(Y + (sin(a) * r))
        Canvas.PixelSet(x, y, Grad(_fdiv(float(i - start), size - start)))
    Canvas.TextPosition_1(50, 70)
    Canvas.Comm(Symbol())
    Canvas.Comm('Total ' + _str(nn) + ' Circles')
    if day:
        Canvas.Comm('Circle period = ' + _str(_idiv(per, 86400)) + ' days')
    else:
        Canvas.Comm('Circle period = ' + _str(per) + ' bars')
    Canvas.Comm('Start date = ' + _str(ti[start]))
    i = 0
    while i < W.Width:
        Canvas.LineVertical(i, W.Height - 1, W.Height - 10, Grad(_fdiv(float(i), W.Width)))
        i += 1
    Canvas.Update()

def Grad(p):
    if p > 0.9999:
        return _s_Grad_Col[5]
    if p < 0.0001:
        return _s_Grad_Col[0]
    p = p * 5
    n = _int(p)
    k = p - n
    c1 = argb()
    c2 = argb()
    c1.clr = _s_Grad_Col[n]
    c2.clr = _s_Grad_Col[n + 1]
    return (((_uchar(255) << 24) | (_uchar(c1.c[2] + _uchar((k * (c2.c[2] - c1.c[2])) + 0.5)) << 16)) | (_uchar(c1.c[1] + _uchar((k * (c2.c[1] - c1.c[1])) + 0.5)) << 8)) | _uchar(c1.c[0] + _uchar((k * (c2.c[0] - c1.c[0])) + 0.5))

# ---- global variables initialised from expressions
W = _alloc(Window)
W.__init__()
Canvas = iCanvas()
d17 = _alloc(B17)
d17.__init__()
info = _alloc(iCanvas)
info.__init__(0, 0, 0, 'iCanvas_info', 200, 20)

# ---- static local variables
_s_CCanvas_FillPolygon_p = Arr(0, 0, factory=CPoint)
_s_CCanvas_PixelSetAA_rr = Arr(4, 0.0, dyn=False)
_s_CCanvas_PixelSetAA_xx = Arr(4, 0, dyn=False)
_s_CCanvas_PixelSetAA_yy = Arr(4, 0, dyn=False)
_s_XYToTimePrice_Hei = Arr(10, 0, dyn=False)
_s_XYToTimePrice_y_min = Arr(10, 0.0, dyn=False)
_s_XYToTimePrice_y_max = Arr(10, 0.0, dyn=False)
_s_XYToTimePrice_ChartChange = True
_s_XYToTimePrice_nofirst = False
_s_XYToTimePrice_Cur_wind = -1
_s_GetWindowProperties_lastTF = 0
_s_GetWindowProperties_oldLB = _UNSET
_s_GetWindowProperties_oldRB = _UNSET
_s_MyChartEvent_click = False
_s_ChartChanged_preWinTotal = _UNSET
_s_wBarShift_lastTF = _UNSET
_s_wBarShift_last_t = _UNSET
_s_Grad_Col = Arr.of([0xFF0000FF, 0xFFFF00FF, 0xFFFF0000, 0xFFFFFF00, 0xFF00FF00, 0xFF00FFFF], fill=0, dyn=False, size=6)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PolarCoordinateSystem(_MQL5Indicator):
    name = 'PolarCoordinateSystem'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

