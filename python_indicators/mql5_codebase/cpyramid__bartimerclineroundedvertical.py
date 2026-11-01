"""CPyramid — converted from MQL5: MQL5 Indicators/BarTimerCLineRoundedVertical/CPyramid.mq5

Copyright: Copyright 2017, Alexander Fedosov; Link: https://www.mql5.com/ru/users/alex2356; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: FileReadFloat, FileReadLong, FileReadStruct, FileWriteFloat, FileWriteLong, FileWriteStruct, FolderClean, FolderDelete
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.controls_rect import *  # #include Rect.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2017, Alexander Fedosov', 'link': 'https://www.mql5.com/ru/users/alex2356', 'version': '1.00', 'indicator_plots': 0, 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'CPyramid', 'source': 'MQL5 Indicators/BarTimerCLineRoundedVertical/CPyramid.mq5', 'folder': 'BarTimerCLineRoundedVertical', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 10, 'label': 'ADX Period', 'sinput': False}, {'mql': 'maxval', 'py': 'maxval', 'param': 'maxval', 'type': 'double', 'default': 50.0, 'label': 'Max value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh', 'Rect.mqh']}

# enum ENUM_LINE_END
LINE_END_ROUND = 0
LINE_END_BUTT = 1
LINE_END_SQUARE = 2
_enum('ENUM_LINE_END', {0: 'LINE_END_ROUND', 1: 'LINE_END_BUTT', 2: 'LINE_END_SQUARE'})

# enum ENUM_ORIENTATION
VERTICAL = 1
HORIZONTAL = 2
_enum('ENUM_ORIENTATION', {1: 'VERTICAL', 2: 'HORIZONTAL'})

# enum ENUM_TYPE_HISTOGRAM
SIMPLE = 1
TRIANGLE = 2
RECTANGLE = 3
_enum('ENUM_TYPE_HISTOGRAM', {1: 'SIMPLE', 2: 'TRIANGLE', 3: 'RECTANGLE'})

# enum ENUM_POSITION
TOPRIGHT = 1
TOPLEFT = 2
BOTTOMRIGHT = 3
BOTTOMLEFT = 4
BOTHRIGHT = 5
BOTHLEFT = 6
_enum('ENUM_POSITION', {1: 'TOPRIGHT', 2: 'TOPLEFT', 3: 'BOTTOMRIGHT', 4: 'BOTTOMLEFT', 5: 'BOTHRIGHT', 6: 'BOTHLEFT'})

# ---- inputs and global variables
period = _input('period', 10)  # ADX Period
maxval = _input('maxval', 50.0)  # Max value
InpInd_Handle = 0
adx = Arr(0, 0.0)

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

class CCanvasBase(MqlObject):
    _q_fields = ('m_canvas_name', 'm_x', 'm_y', 'm_x_size', 'm_y_size', 'm_canvas')
    def __init__(self):
        self.m_canvas_name = ""
        self.m_x = 0
        self.m_y = 0
        self.m_x_size = 0
        self.m_y_size = 0
        self.m_canvas = CCanvas()
        self.m_x = 0
        self.m_y = 0
        self.m_x_size = 200
        self.m_y_size = 200
    def _q_dtor(self):
        pass
    def CreateCanvas(self):
        ObjectDelete(0, self.m_canvas_name)
        if not self.m_canvas.CreateBitmapLabel_6(self.m_canvas_name, self.m_x, self.m_y, self.m_x_size, self.m_y_size, COLOR_FORMAT_ARGB_NORMALIZE):
            return False
        ObjectSetInteger(0, self.m_canvas_name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, self.m_canvas_name, OBJPROP_ANCHOR, ANCHOR_CENTER)
        ObjectSetInteger(0, self.m_canvas_name, OBJPROP_BACK, False)
        return True
    def DeleteCanvas(self):
        return (True if ObjectDelete(0, self.m_canvas_name) else False)
    def X_1(self, x):
        self.m_x = x
    def X_0(self):
        return self.m_x
    def Y_1(self, y):
        self.m_y = y
    def Y_0(self):
        return self.m_y
    def XSize_1(self, x_size):
        self.m_x_size = x_size
    def XSize_0(self):
        return self.m_x_size
    def YSize_1(self, y_size):
        self.m_y_size = y_size
    def YSize_0(self):
        return self.m_y_size
    def Name(self, canvas_name):
        self.m_canvas_name = canvas_name

class CCircleArc(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_arc_color', 'm_area_color', 'm_label_color', 'm_value_color', 'm_transparency', 'm_radius', 'm_scale_width', 'm_label_font_size', 'm_value_font_size', 'm_label_value', 'm_orientation')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_arc_color = 0
        self.m_area_color = 0
        self.m_label_color = 0
        self.m_value_color = 0
        self.m_transparency = 0
        self.m_radius = 0
        self.m_scale_width = 0
        self.m_label_font_size = 0
        self.m_value_font_size = 0
        self.m_label_value = ""
        self.m_orientation = 0
        self.m_bg_color = clrSilver
        self.m_arc_color = clrYellowGreen
        self.m_area_color = clrAliceBlue
        self.m_label_color = clrBlack
        self.m_value_color = clrBlack
        self.m_transparency = 255
        self.m_radius = 50
        self.m_scale_width = 10
        self.m_label_font_size = 20
        self.m_value_font_size = 20
        self.m_label_value = ''
        self.m_orientation = VERTICAL
    def _q_dtor(self):
        pass
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def ArcColor_0(self):
        return self.m_arc_color
    def ArcColor_1(self, clr):
        self.m_arc_color = clr
    def AreaColor_0(self):
        return self.m_area_color
    def AreaColor_1(self, clr):
        self.m_area_color = clr
    def LabelColor_0(self):
        return self.m_label_color
    def LabelColor_1(self, clr):
        self.m_label_color = clr
    def ValueColor_0(self):
        return self.m_value_color
    def ValueColor_1(self, clr):
        self.m_value_color = clr
    def Alpha_0(self):
        return self.m_transparency
    def Alpha_1(self, trn):
        self.m_transparency = trn
    def Radius_0(self):
        return self.m_radius
    def Radius_1(self, r):
        self.m_radius = r
    def Width_0(self):
        return self.m_scale_width
    def Width_1(self, w):
        self.m_scale_width = w
    def LabelSize_0(self):
        return self.m_label_font_size
    def LabelSize_1(self, sz):
        self.m_label_font_size = sz
    def ValueSize_0(self):
        return self.m_value_font_size
    def ValueSize_1(self, sz):
        self.m_value_font_size = sz
    def LabelValue_0(self):
        return self.m_label_value
    def LabelValue_1(self, str_):
        self.m_label_value = str_
    def Orientation_1(self, orietation):
        self.m_orientation = orietation
    def Orientation_0(self):
        return self.m_orientation
    def Create(self, name, x, y):
        r = self.m_radius
        a = 0.0
        b = 0.0
        a = (M_PI_2 if (self.m_orientation == VERTICAL) else 0)
        b = (M_PI_2 if (self.m_orientation == VERTICAL) else 0)
        b += (90 * M_PI) / 180
        x = (r if (x < r) else x)
        y = (r if (y < r) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1((2 * r) + 1)
        self.YSize_1((2 * r) + 1)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        self.m_canvas.FillCircle(r, r, r, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.Pie_8(r, r, _idiv(self.XSize_0(), 2), _idiv(self.YSize_0(), 2), a, b, ColorToARGB(self.m_arc_color, self.m_transparency), ColorToARGB(self.m_arc_color, self.m_transparency))
        self.m_canvas.FillCircle(r, r, r - self.m_scale_width, ColorToARGB(self.m_area_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(r, r, '0', ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_label_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def NewValue(self, value, maxvalue, digits=2):
        r = self.m_radius
        a = 0.0
        b = 0.0
        result = 0.0
        value = (maxvalue if (value > maxvalue) else value)
        value = (0 if (value < 0) else value)
        a = (M_PI_2 if (self.m_orientation == VERTICAL) else 0)
        b = (M_PI_2 if (self.m_orientation == VERTICAL) else 0)
        result = value * _fdiv(360.0, maxvalue)
        b += (result * M_PI) / 180
        if b >= (2 * M_PI):
            b = (2 * M_PI) - 0.02
        self.m_canvas.FillCircle(r, r, r, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.Pie_8(r, r, _idiv(self.XSize_0(), 2), _idiv(self.YSize_0(), 2), a, b, ColorToARGB(self.m_arc_color, self.m_transparency), ColorToARGB(self.m_arc_color, self.m_transparency))
        self.m_canvas.FillCircle(r, r, r - self.m_scale_width, ColorToARGB(self.m_area_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(r, r, DoubleToString(value, digits), ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_label_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()

class CCircleSection(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_area_color', 'm_border_color', 'm_label_color', 'm_value_color', 'm_scale_color_on', 'm_scale_color_off', 'm_transparency', 'm_radius', 'm_scale_width', 'm_border_size', 'm_label_font_size', 'm_value_font_size', 'm_label_value', 'm_orientation')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_area_color = 0
        self.m_border_color = 0
        self.m_label_color = 0
        self.m_value_color = 0
        self.m_scale_color_on = 0
        self.m_scale_color_off = 0
        self.m_transparency = 0
        self.m_radius = 0
        self.m_scale_width = 0
        self.m_border_size = 0
        self.m_label_font_size = 0
        self.m_value_font_size = 0
        self.m_label_value = ""
        self.m_orientation = 0
        self.m_bg_color = clrAliceBlue
        self.m_area_color = clrCornflowerBlue
        self.m_border_color = clrAliceBlue
        self.m_label_color = clrWhite
        self.m_value_color = clrWhite
        self.m_scale_color_on = clrForestGreen
        self.m_scale_color_off = clrSilver
        self.m_transparency = 255
        self.m_radius = 40
        self.m_scale_width = 10
        self.m_border_size = 5
        self.m_label_font_size = 20
        self.m_value_font_size = 20
        self.m_label_value = ''
        self.m_orientation = VERTICAL
    def _q_dtor(self):
        pass
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def AreaColor_0(self):
        return self.m_area_color
    def AreaColor_1(self, clr):
        self.m_area_color = clr
    def BorderColor_0(self):
        return self.m_border_color
    def BorderColor_1(self, clr):
        self.m_border_color = clr
    def LabelColor_0(self):
        return self.m_label_color
    def LabelColor_1(self, clr):
        self.m_label_color = clr
    def ValueColor_0(self):
        return self.m_value_color
    def ValueColor_1(self, clr):
        self.m_value_color = clr
    def ScaleColorOn(self, clr):
        self.m_scale_color_on = clr
    def ScaleColorOff(self, clr):
        self.m_scale_color_off = clr
    def Alpha_0(self):
        return self.m_transparency
    def Alpha_1(self, trn):
        self.m_transparency = trn
    def Radius_0(self):
        return self.m_radius
    def Radius_1(self, r):
        self.m_radius = r
    def ScaleWidth_0(self):
        return self.m_scale_width
    def ScaleWidth_1(self, scl):
        self.m_scale_width = scl
    def BorderSize_0(self):
        return self.m_border_size
    def BorderSize_1(self, sz):
        self.m_border_size = sz
    def LabelSize_0(self):
        return self.m_label_font_size
    def LabelSize_1(self, sz):
        self.m_label_font_size = sz
    def ValueSize_0(self):
        return self.m_value_font_size
    def ValueSize_1(self, sz):
        self.m_value_font_size = sz
    def LabelValue_0(self):
        return self.m_label_value
    def LabelValue_1(self, str_):
        self.m_label_value = str_
    def Orientation_1(self, orietation):
        self.m_orientation = orietation
    def Orientation_0(self):
        return self.m_orientation
    def Create(self, name, x, y):
        r = self.m_radius
        a = 0.0
        b = 0.0
        x = (r if (x < r) else x)
        y = (r if (y < r) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1((2 * r) + 1)
        self.YSize_1((2 * r) + 1)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        for i in range(0, 10):
            if self.m_orientation == HORIZONTAL:
                a = (36 * i * M_PI) / 180
                b = (36 * (i + 1) * M_PI) / 180
                if a > (2 * M_PI):
                    a -= 2 * M_PI
                if b > (2 * M_PI):
                    b -= 2 * M_PI
            else:
                a = M_PI_2 + ((36 * i * M_PI) / 180)
                b = M_PI_2 + ((36 * (i + 1) * M_PI) / 180)
                if a > (2 * M_PI):
                    a -= 2 * M_PI
                if b > (2 * M_PI):
                    b -= 2 * M_PI
            self.m_canvas.Pie_8(r, r, _idiv(self.XSize_0(), 2), _idiv(self.YSize_0(), 2), a, b, ColorToARGB(self.m_bg_color, self.m_transparency), ColorToARGB(self.m_scale_color_off, self.m_transparency))
        self.m_canvas.FillCircle(r, r, _idiv(self.XSize_0(), 2) - self.m_scale_width, ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillCircle(r, r, _idiv(self.XSize_0(), 2) - self.m_scale_width - self.m_border_size, ColorToARGB(self.m_area_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_value_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(r, r, '0', ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def NewValue(self, value, maxvalue=100.0, digits=2):
        r = self.m_radius
        a = 0.0
        b = 0.0
        clr = 0
        for i in range(0, 10):
            if self.m_orientation == HORIZONTAL:
                a = (36 * i * M_PI) / 180
                b = (36 * (i + 1) * M_PI) / 180
                if a > (2 * M_PI):
                    a -= 2 * M_PI
                if b > (2 * M_PI):
                    b -= 2 * M_PI
            else:
                a = M_PI_2 + ((36 * i * M_PI) / 180)
                b = M_PI_2 + ((36 * (i + 1) * M_PI) / 180)
                if a > (2 * M_PI):
                    a -= 2 * M_PI
                if b > (2 * M_PI):
                    b -= 2 * M_PI
            clr = (self.m_scale_color_on if (((maxvalue / 10) * (i + 1)) <= value) else self.m_scale_color_off)
            self.m_canvas.Pie_8(r, r, _idiv(self.XSize_0(), 2), _idiv(self.YSize_0(), 2), a, b, ColorToARGB(self.m_bg_color, self.m_transparency), ColorToARGB(clr, self.m_transparency))
        self.m_canvas.FillCircle(r, r, _idiv(self.XSize_0(), 2) - self.m_scale_width, ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillCircle(r, r, _idiv(self.XSize_0(), 2) - self.m_scale_width - self.m_border_size, ColorToARGB(self.m_area_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_value_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(r, r, DoubleToString(value, digits), ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()

class CCircleSimple(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_border_color', 'm_font_color', 'm_label_color', 'm_transparency', 'm_border', 'm_radius', 'm_font_size', 'm_label_font_size', 'm_digits', 'm_label')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_border_color = 0
        self.m_font_color = 0
        self.m_label_color = 0
        self.m_transparency = 0
        self.m_border = 0
        self.m_radius = 0
        self.m_font_size = 0
        self.m_label_font_size = 0
        self.m_digits = 0
        self.m_label = ""
        self.m_bg_color = clrAliceBlue
        self.m_border_color = clrRoyalBlue
        self.m_font_color = clrBlack
        self.m_label_color = clrBlack
        self.m_transparency = 255
        self.m_border = 5
        self.m_radius = 40
        self.m_font_size = 17
        self.m_label_font_size = 20
        self.m_digits = 2
        self.m_label = 'label'
    def _q_dtor(self):
        pass
    def Color_0(self):
        return self.m_bg_color
    def Color_1(self, clr):
        self.m_bg_color = clr
    def Radius_0(self):
        return self.m_radius
    def Radius_1(self, r):
        self.m_radius = r
    def FontSize_0(self):
        return self.m_font_size
    def FontSize_1(self, fontsize):
        self.m_font_size = fontsize
    def LabelSize_0(self):
        return self.m_label_font_size
    def LabelSize_1(self, fontsize):
        self.m_label_font_size = fontsize
    def FontColor_0(self):
        return self.m_font_color
    def FontColor_1(self, fontcolor):
        self.m_font_color = fontcolor
    def LabelColor_0(self):
        return self.m_label_color
    def LabelColor_1(self, fontcolor):
        self.m_label_color = fontcolor
    def BorderColor(self, clr):
        self.m_border_color = clr
    def BorderSize(self, border):
        self.m_border = border
    def Alpha_0(self):
        return self.m_transparency
    def Alpha_1(self, alpha):
        self.m_transparency = alpha
    def Label_0(self):
        return self.m_label
    def Label_1(self, label):
        self.m_label = label
    def Create(self, name, x, y):
        r = self.m_radius
        x = (r if (x < r) else x)
        y = (r if (y < r) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1((2 * r) + 1)
        self.YSize_1((2 * r) + 1)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        if self.m_border > 0:
            self.m_canvas.FillCircle(r, r, r, ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillCircle(r, r, r - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_font_size)
        self.m_canvas.TextOut(r, r, '0', ColorToARGB(self.m_font_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_label_font_size, self.m_label, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def NewValue_1(self, value):
        r = self.m_radius
        self.m_canvas.FillCircle(r, r, r - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_font_size)
        self.m_canvas.TextOut(r, r, IntegerToString(value), ColorToARGB(self.m_font_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_label_font_size, self.m_label, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()
    def NewValue_2(self, value):
        r = self.m_radius
        self.m_canvas.FillCircle(r, r, r - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_font_size)
        self.m_canvas.TextOut(r, r, DoubleToString(value, self.m_digits), ColorToARGB(self.m_font_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_label_font_size, self.m_label, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()

class CHexagon(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_label_color', 'm_value_color', 'm_transparency', 'm_size', 'm_label_font_size', 'm_value_font_size', 'm_label_value')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_label_color = 0
        self.m_value_color = 0
        self.m_transparency = 0
        self.m_size = 0
        self.m_label_font_size = 0
        self.m_value_font_size = 0
        self.m_label_value = ""
        self.m_bg_color = 0xF0C869
        self.m_label_color = clrWhite
        self.m_value_color = clrWhite
        self.m_transparency = 255
        self.m_size = 100
        self.m_label_font_size = 20
        self.m_value_font_size = 20
        self.m_label_value = 'Label'
    def _q_dtor(self):
        pass
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def LabelColor_0(self):
        return self.m_label_color
    def LabelColor_1(self, clr):
        self.m_label_color = clr
    def ValueColor_0(self):
        return self.m_value_color
    def ValueColor_1(self, clr):
        self.m_value_color = clr
    def Alpha_0(self):
        return self.m_transparency
    def Alpha_1(self, trn):
        self.m_transparency = trn
    def Size_0(self):
        return self.m_size
    def Size_1(self, r):
        self.m_size = r
    def LabelSize_0(self):
        return self.m_label_font_size
    def LabelSize_1(self, sz):
        self.m_label_font_size = sz
    def ValueSize_0(self):
        return self.m_value_font_size
    def ValueSize_1(self, sz):
        self.m_value_font_size = sz
    def LabelValue_0(self):
        return self.m_label_value
    def LabelValue_1(self, str_):
        self.m_label_value = str_
    def Create(self, name, x, y):
        a = 0
        r = 0
        r = self.m_size
        x = (_idiv(r, 2) if (x < _idiv(r, 2)) else x)
        y = (_idiv(r, 2) if (y < _idiv(r, 2)) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1(r)
        self.YSize_1(r)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        a = _int(_idiv(self.YSize_0(), 2) * MathSin((30 * M_PI) / 180))
        self.m_canvas.FillTriangle(_idiv(self.XSize_0(), 2), 0, 0, a, self.XSize_0(), a, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillRectangle(0, a, self.XSize_0(), a + _idiv(self.YSize_0(), 2), ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillTriangle(0, a + _idiv(self.YSize_0(), 2), self.XSize_0(), a + _idiv(self.YSize_0(), 2), _idiv(self.XSize_0(), 2), self.YSize_0(), ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FontNameSet('Trebuchet MS')
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(_idiv(r, 2), _idiv(r, 2), '-', ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(_idiv(r, 2), _idiv(r, 2) + self.m_value_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def NewValue(self, value, digits=2):
        a = 0
        r = 0
        r = self.m_size
        a = _int(_idiv(self.YSize_0(), 2) * MathSin((30 * M_PI) / 180))
        self.m_canvas.FillTriangle(_idiv(self.XSize_0(), 2), 0, 0, a, self.XSize_0(), a, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillRectangle(0, a, self.XSize_0(), a + _idiv(self.YSize_0(), 2), ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillTriangle(0, a + _idiv(self.YSize_0(), 2), self.XSize_0(), a + _idiv(self.YSize_0(), 2), _idiv(self.XSize_0(), 2), self.YSize_0(), ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FontNameSet('Trebuchet MS')
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(_idiv(r, 2), _idiv(r, 2), DoubleToString(value, digits), ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(_idiv(r, 2), _idiv(r, 2) + self.m_value_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()

class CHistogram(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_bg_graph_color', 'm_border_color', 'm_axis_color', 'm_grid_color', 'm_scale_color', 'm_graph_color1', 'm_graph_color2', 'm_graph_color3', 'm_value_color', 'm_label_color', 'm_x_size', 'm_y_size', 'm_gap', 'm_font_size', 'm_value_font_size', 'm_x', 'm_label_value', 'm_y_min', 'm_y_max', 'm_num_grid', 'm_transparency', 'm_type')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_bg_graph_color = 0
        self.m_border_color = 0
        self.m_axis_color = 0
        self.m_grid_color = 0
        self.m_scale_color = 0
        self.m_graph_color1 = 0
        self.m_graph_color2 = 0
        self.m_graph_color3 = 0
        self.m_value_color = 0
        self.m_label_color = 0
        self.m_x_size = 0
        self.m_y_size = 0
        self.m_gap = 0
        self.m_font_size = 0
        self.m_value_font_size = 0
        self.m_x = Arr(0, 0)
        self.m_label_value = Arr(0, "")
        self.m_y_min = 0.0
        self.m_y_max = 0.0
        self.m_num_grid = 0
        self.m_transparency = 0
        self.m_type = 0
        self.m_bg_color = clrWhite
        self.m_bg_graph_color = clrWhite
        self.m_border_color = clrBlack
        self.m_axis_color = clrNavy
        self.m_grid_color = clrGray
        self.m_scale_color = clrNavy
        self.m_graph_color1 = 0xE1D291
        self.m_graph_color2 = 0xD2B41E
        self.m_graph_color3 = 0xA59600
        self.m_value_color = clrWhite
        self.m_label_color = clrBlack
        self.m_x_size = 500
        self.m_y_size = 300
        self.m_gap = 40
        self.m_font_size = 16
        self.m_value_font_size = 16
        self.m_y_min = 0.0
        self.m_y_max = 100.0
        self.m_num_grid = 5
        self.m_transparency = 255
        self.m_type = TRIANGLE
    def _q_dtor(self):
        pass
    def Type_1(self, type_):
        self.m_type = type_
    def Type_0(self):
        return self.m_type
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def BgGraphColor_0(self):
        return self.m_bg_graph_color
    def BgGraphColor_1(self, clr):
        self.m_bg_graph_color = clr
    def BorderColor_0(self):
        return self.m_border_color
    def BorderColor_1(self, clr):
        self.m_border_color = clr
    def AxisColor_0(self):
        return self.m_axis_color
    def AxisColor_1(self, clr):
        self.m_axis_color = clr
    def GridColor_0(self):
        return self.m_grid_color
    def GridColor_1(self, clr):
        self.m_grid_color = clr
    def ScaleColor_0(self):
        return self.m_scale_color
    def ScaleColor_1(self, clr):
        self.m_scale_color = clr
    def GraphColor1_0(self):
        return self.m_graph_color1
    def GraphColor1_1(self, clr):
        self.m_graph_color1 = clr
    def GraphColor2_0(self):
        return self.m_graph_color2
    def GraphColor2_1(self, clr):
        self.m_graph_color2 = clr
    def GraphColor3_0(self):
        return self.m_graph_color3
    def GraphColor3_1(self, clr):
        self.m_graph_color3 = clr
    def ValueColor_0(self):
        return self.m_value_color
    def ValueColor_1(self, clr):
        self.m_value_color = clr
    def LabelColor_0(self):
        return self.m_label_color
    def LabelColor_1(self, clr):
        self.m_label_color = clr
    def XGraphSize_0(self):
        return self.m_x_size
    def XGraphSize_1(self, x_size):
        self.m_x_size = x_size
    def YGraphSize_0(self):
        return self.m_y_size
    def YGraphSize_1(self, y_size):
        self.m_y_size = y_size
    def FontSize_0(self):
        return self.m_font_size
    def FontSize_1(self, fontzise):
        self.m_font_size = fontzise
    def ValueSize_0(self):
        return self.m_value_font_size
    def ValueSize_1(self, size):
        self.m_value_font_size = size
    def Gap_0(self):
        return self.m_gap
    def Gap_1(self, g):
        self.m_gap = g
    def YMin_0(self):
        return self.m_y_min
    def YMin_1(self, ymin):
        self.m_y_min = ymin
    def YMax_0(self):
        return self.m_y_max
    def YMax_1(self, ymax):
        self.m_y_max = ymax
    def NumGrid_0(self):
        return self.m_num_grid
    def NumGrid_1(self, num):
        self.m_num_grid = num
    def Create(self, name, x, y):
        x = (_idiv(self.m_x_size, 2) if (x < _idiv(self.m_x_size, 2)) else x)
        y = (_idiv(self.m_y_size, 2) if (y < _idiv(self.m_y_size, 2)) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1(self.m_x_size)
        self.YSize_1(self.m_y_size)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        self.m_canvas.FillRectangle(0, 0, self.XSize_0(), self.YSize_0(), ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(1, 1, self.XSize_0() - 2, self.YSize_0() - 2, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap - 1, self.m_gap - 1, self.XSize_0() - self.m_gap + 1, self.YSize_0() - self.m_gap + 1, ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap, self.m_gap, self.XSize_0() - self.m_gap, self.YSize_0() - self.m_gap, ColorToARGB(self.m_bg_graph_color, self.m_transparency))
        self.VerticalScale(self.m_y_min, self.m_y_max, self.m_num_grid)
        self.HorizontalScale(3)
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def SetArrayValue(self, data):
        x = 0
        y = 0
        y1 = 0
        y2 = 0
        self.m_canvas.FillRectangle(0, 0, self.XSize_0(), self.YSize_0(), ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(1, 1, self.XSize_0() - 2, self.YSize_0() - 2, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap - 1, self.m_gap - 1, self.XSize_0() - self.m_gap + 1, self.YSize_0() - self.m_gap + 1, ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap, self.m_gap, self.XSize_0() - self.m_gap, self.YSize_0() - self.m_gap, ColorToARGB(self.m_bg_graph_color, self.m_transparency))
        if data[ArrayMaximum(data)] > self.m_y_max:
            self.m_y_max = data[ArrayMaximum(data)]
        self.VerticalScale(self.m_y_min, self.m_y_max, self.m_num_grid)
        self.HorizontalScale(ArraySize(data))
        ArrayResize(self.m_label_value, ArraySize(data))
        i = 0
        while i < ArraySize(data):
            if data[i] > 0:
                x = self.m_x[i] + _idiv(self.m_x[i + 1] - self.m_x[i], 2)
                y = _int(self.YSize_0() - self.m_gap - (_fdiv(self.YSize_0() - (2 * self.m_gap), self.m_y_max) * data[i]))
                y1 = _int(self.YSize_0() - self.m_gap - (_fdiv(self.YSize_0() - (2 * self.m_gap), self.m_y_max) * data[i] * 0.3))
                y2 = _int(self.YSize_0() - self.m_gap - (_fdiv(self.YSize_0() - (2 * self.m_gap), self.m_y_max) * data[i] * 0.1))
                y = (self.m_gap if (y < self.m_gap) else y)
                if self.m_type == SIMPLE:
                    self.m_canvas.FillTriangle(self.m_x[i], self.YSize_0() - self.m_gap, self.m_x[i + 1], self.YSize_0() - self.m_gap, x, y, ColorToARGB(self.m_graph_color1, self.m_transparency))
                elif self.m_type == TRIANGLE:
                    self.m_canvas.FillTriangle(self.m_x[i], self.YSize_0() - self.m_gap, x, y, x, y1, ColorToARGB(self.m_graph_color1, self.m_transparency))
                    self.m_canvas.FillTriangle(self.m_x[i], self.YSize_0() - self.m_gap, self.m_x[i + 1], self.YSize_0() - self.m_gap, x, y1, ColorToARGB(self.m_graph_color2, self.m_transparency))
                    self.m_canvas.FillTriangle(x, y, x, y1, self.m_x[i + 1], self.YSize_0() - self.m_gap, ColorToARGB(self.m_graph_color3, self.m_transparency))
                elif self.m_type == RECTANGLE:
                    x1 = 0
                    x2 = 0
                    x1 = self.m_x[i] + _idiv(self.m_x[i + 1] - self.m_x[i], 3)
                    x2 = self.m_x[i] + _idiv(2 * (self.m_x[i + 1] - self.m_x[i]), 3)
                    self.m_canvas.FillRectangle(x1, y, x2, self.YSize_0() - self.m_gap, ColorToARGB(self.m_graph_color1, self.m_transparency))
                self.m_canvas.FontNameSet('Trebuchet MS')
                self.m_canvas.FontSizeSet(self.m_value_font_size)
                self.m_canvas.TextOut(x, y2, DoubleToString(data[i], 2), ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
                self.m_canvas.TextOut(x, y - 5, self.m_label_value[i], ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
            i += 1
        self.m_canvas.Update()
    def SetArrayLabel(self, data):
        ArrayResize(self.m_label_value, ArraySize(data))
        for i in range(0, ArraySize(data)):
            self.m_label_value[i] = data[i]
    def VerticalScale(self, min_, max_, num_grid):
        s = 0.0
        v = 0.0
        scale = 0.0
        s = _idiv(self.YSize_0() - (2 * self.m_gap), num_grid)
        self.m_canvas.FontSizeSet(self.m_font_size)
        self.m_canvas.TextOut(self.m_gap - 20, self.YSize_0() - self.m_gap, DoubleToString(min_, 0), ColorToARGB(self.m_axis_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        for i in range(num_grid, 1 - 1, -1):
            scale = self.YSize_0() - self.m_gap - (s * i)
            v = _fdiv(max_ - min_, num_grid) * i
            self.m_canvas.TextOut(self.m_gap - 20, _int(scale), DoubleToString(v, 0), ColorToARGB(self.m_axis_color, self.m_transparency), TA_CENTER | TA_VCENTER)
            self.m_canvas.LineAA(self.m_gap, _int(scale), self.XSize_0() - self.m_gap, _int(scale), ColorToARGB(self.m_grid_color, self.m_transparency), STYLE_DOT)
            self.m_canvas.LineHorizontal(self.m_gap - 5, self.m_gap + 5, _int(scale), ColorToARGB(self.m_scale_color, self.m_transparency))
    def HorizontalScale(self, num_grid):
        if num_grid < 2:
            return
        ArrayResize(self.m_x, num_grid + 1)
        self.m_x[0] = self.m_gap
        s = 0.0
        scale = 0.0
        s = _idiv(self.XSize_0() - (2 * self.m_gap), num_grid)
        self.m_canvas.FontSizeSet(self.m_font_size)
        for i in range(num_grid, 1 - 1, -1):
            scale = self.m_gap + (s * i)
            scale = ((self.XSize_0() - self.m_gap) if (i == num_grid) else scale)
            self.m_canvas.LineVertical(_int(scale), self.YSize_0() - self.m_gap - 5, self.YSize_0() - self.m_gap + 5, ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.TextOut(_int(scale), self.YSize_0() - self.m_gap + 20, IntegerToString(i), ColorToARGB(self.m_axis_color, self.m_transparency), TA_CENTER | TA_VCENTER)
            self.m_x[i] = _int(scale)

class CLineGraph(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_bg_graph_color', 'm_border_color', 'm_axis_color', 'm_grid_color', 'm_scale_color', 'm_graph_color', 'm_x_size', 'm_y_size', 'm_gap', 'm_font_size', 'm_x', 'm_y_min', 'm_y_max', 'm_num_grid', 'm_transparency')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_bg_graph_color = 0
        self.m_border_color = 0
        self.m_axis_color = 0
        self.m_grid_color = 0
        self.m_scale_color = 0
        self.m_graph_color = 0
        self.m_x_size = 0
        self.m_y_size = 0
        self.m_gap = 0
        self.m_font_size = 0
        self.m_x = Arr(0, 0)
        self.m_y_min = 0.0
        self.m_y_max = 0.0
        self.m_num_grid = 0
        self.m_transparency = 0
        self.m_bg_color = clrWhite
        self.m_bg_graph_color = clrWhite
        self.m_border_color = clrBlack
        self.m_axis_color = clrNavy
        self.m_grid_color = clrGray
        self.m_scale_color = clrNavy
        self.m_graph_color = clrBlack
        self.m_x_size = 500
        self.m_y_size = 300
        self.m_gap = 40
        self.m_font_size = 16
        self.m_y_min = 0.0
        self.m_y_max = 100.0
        self.m_num_grid = 5
        self.m_transparency = 255
    def _q_dtor(self):
        pass
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def BgGraphColor_0(self):
        return self.m_bg_graph_color
    def BgGraphColor_1(self, clr):
        self.m_bg_graph_color = clr
    def BorderColor_0(self):
        return self.m_border_color
    def BorderColor_1(self, clr):
        self.m_border_color = clr
    def AxisColor_0(self):
        return self.m_axis_color
    def AxisColor_1(self, clr):
        self.m_axis_color = clr
    def GridColor_0(self):
        return self.m_grid_color
    def GridColor_1(self, clr):
        self.m_grid_color = clr
    def ScaleColor_0(self):
        return self.m_scale_color
    def ScaleColor_1(self, clr):
        self.m_scale_color = clr
    def GraphColor_0(self):
        return self.m_graph_color
    def GraphColor_1(self, clr):
        self.m_graph_color = clr
    def XGraphSize_0(self):
        return self.m_x_size
    def XGraphSize_1(self, x_size):
        self.m_x_size = x_size
    def YGraphSize_0(self):
        return self.m_y_size
    def YGraphSize_1(self, y_size):
        self.m_y_size = y_size
    def FontSize_0(self):
        return self.m_font_size
    def FontSize_1(self, fontzise):
        self.m_font_size = fontzise
    def Gap_0(self):
        return self.m_gap
    def Gap_1(self, g):
        self.m_gap = g
    def YMin_0(self):
        return self.m_y_min
    def YMin_1(self, ymin):
        self.m_y_min = ymin
    def YMax_0(self):
        return self.m_y_max
    def YMax_1(self, ymax):
        self.m_y_max = ymax
    def NumGrid_0(self):
        return self.m_num_grid
    def NumGrid_1(self, num):
        self.m_num_grid = num
    def Create(self, name, x, y):
        x = (_idiv(self.m_x_size, 2) if (x < _idiv(self.m_x_size, 2)) else x)
        y = (_idiv(self.m_y_size, 2) if (y < _idiv(self.m_y_size, 2)) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1(self.m_x_size)
        self.YSize_1(self.m_y_size)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        self.m_canvas.FillRectangle(0, 0, self.XSize_0(), self.YSize_0(), ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(1, 1, self.XSize_0() - 2, self.YSize_0() - 2, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap - 1, self.m_gap - 1, self.XSize_0() - self.m_gap + 1, self.YSize_0() - self.m_gap + 1, ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap, self.m_gap, self.XSize_0() - self.m_gap, self.YSize_0() - self.m_gap, ColorToARGB(self.m_bg_graph_color, self.m_transparency))
        self.VerticalScale(self.m_y_min, self.m_y_max, self.m_num_grid)
        self.HorizontalScale(5)
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def SetArrayValue(self, data):
        y0 = 0
        y1 = 0
        self.m_canvas.FillRectangle(0, 0, self.XSize_0(), self.YSize_0(), ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(1, 1, self.XSize_0() - 2, self.YSize_0() - 2, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap - 1, self.m_gap - 1, self.XSize_0() - self.m_gap + 1, self.YSize_0() - self.m_gap + 1, ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(self.m_gap, self.m_gap, self.XSize_0() - self.m_gap, self.YSize_0() - self.m_gap, ColorToARGB(self.m_bg_graph_color, self.m_transparency))
        if data[ArrayMaximum(data)] > self.m_y_max:
            self.m_y_max = data[ArrayMaximum(data)]
        self.VerticalScale(self.m_y_min, self.m_y_max, self.m_num_grid)
        self.HorizontalScale(ArraySize(data))
        i = 0
        while i < (ArraySize(data) - 1):
            y0 = _int((self.YSize_0() - (2 * self.m_gap)) * (1 - _fdiv(data[i], self.m_y_max)))
            y0 = _int(self.YSize_0() - self.m_gap - (_fdiv(self.YSize_0() - (2 * self.m_gap), self.m_y_max) * data[i]))
            y0 = (self.m_gap if (y0 < self.m_gap) else y0)
            y1 = _int(self.YSize_0() - self.m_gap - (_fdiv(self.YSize_0() - (2 * self.m_gap), self.m_y_max) * data[i + 1]))
            y1 = (self.m_gap if (y1 < self.m_gap) else y1)
            self.m_canvas.LineAA(self.m_x[i + 1], y0, self.m_x[i + 2], y1, ColorToARGB(self.m_graph_color, self.m_transparency), STYLE_SOLID)
            self.m_canvas.FillCircle(self.m_x[i + 1], y0, 2, ColorToARGB(self.m_graph_color, self.m_transparency))
            self.m_canvas.FillCircle(self.m_x[i + 2], y1, 2, ColorToARGB(self.m_graph_color, self.m_transparency))
            i += 1
        self.m_canvas.Update()
    def VerticalScale(self, min_, max_, num_grid):
        s = 0.0
        v = 0.0
        scale = 0.0
        s = _idiv(self.YSize_0() - (2 * self.m_gap), num_grid)
        self.m_canvas.FontSizeSet(self.m_font_size)
        self.m_canvas.TextOut(self.m_gap - 20, self.YSize_0() - self.m_gap, DoubleToString(min_, 0), ColorToARGB(self.m_axis_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        for i in range(num_grid, 1 - 1, -1):
            scale = self.YSize_0() - self.m_gap - (s * i)
            v = _fdiv(max_ - min_, num_grid) * i
            self.m_canvas.TextOut(self.m_gap - 20, _int(scale), DoubleToString(v, 0), ColorToARGB(self.m_axis_color, self.m_transparency), TA_CENTER | TA_VCENTER)
            self.m_canvas.LineAA(self.m_gap, _int(scale), self.XSize_0() - self.m_gap, _int(scale), ColorToARGB(self.m_grid_color, self.m_transparency), STYLE_DOT)
            self.m_canvas.LineHorizontal(self.m_gap - 5, self.m_gap + 5, _int(scale), ColorToARGB(self.m_scale_color, self.m_transparency))
    def HorizontalScale(self, num_grid):
        if num_grid < 2:
            return
        ArrayResize(self.m_x, num_grid + 1)
        self.m_x[0] = self.m_gap
        s = 0.0
        scale = 0.0
        s = _idiv(self.XSize_0() - (2 * self.m_gap), num_grid)
        self.m_canvas.FontSizeSet(self.m_font_size)
        for i in range(num_grid, 1 - 1, -1):
            scale = self.m_gap + (s * i)
            scale = ((self.XSize_0() - self.m_gap) if (i == num_grid) else scale)
            self.m_canvas.LineVertical(_int(scale), self.YSize_0() - self.m_gap - 5, self.YSize_0() - self.m_gap + 5, ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.TextOut(_int(scale), self.YSize_0() - self.m_gap + 20, IntegerToString(i), ColorToARGB(self.m_axis_color, self.m_transparency), TA_CENTER | TA_VCENTER)
            self.m_x[i] = _int(scale)

class CLineRounded(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_border_color', 'm_scale_color', 'm_value_color', 'm_x_size', 'm_y_size', 'm_border', 'm_font_size', 'm_transparency')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_border_color = 0
        self.m_scale_color = 0
        self.m_value_color = 0
        self.m_x_size = 0
        self.m_y_size = 0
        self.m_border = 0
        self.m_font_size = 0
        self.m_transparency = 0
        self.m_bg_color = clrGainsboro
        self.m_border_color = 0xFFC864
        self.m_scale_color = clrForestGreen
        self.m_x_size = 300
        self.m_y_size = 20
        self.m_border = 5
        self.m_font_size = 16
        self.m_transparency = 255
    def _q_dtor(self):
        pass
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def BorderColor_0(self):
        return self.m_border_color
    def BorderColor_1(self, clr):
        self.m_border_color = clr
    def ScaleColor_0(self):
        return self.m_scale_color
    def ScaleColor_1(self, clr):
        self.m_scale_color = clr
    def ValueColor_0(self):
        return self.m_value_color
    def ValueColor_1(self, clr):
        self.m_value_color = clr
    def XSizeInd_0(self):
        return self.m_x_size
    def XSizeInd_1(self, x_size):
        self.m_x_size = x_size
    def YSizeInd_0(self):
        return self.m_y_size
    def YSizeInd_1(self, y_size):
        self.m_y_size = y_size
    def Border_0(self):
        return self.m_border
    def Border_1(self, border):
        self.m_border = border
    def FontSize_0(self):
        return self.m_font_size
    def FontSize_1(self, fontzise):
        self.m_font_size = fontzise
    def Alpha_0(self):
        return self.m_transparency
    def Alpha_1(self, alpha):
        self.m_transparency = alpha
    def Create(self, name, x, y):
        x = (_idiv(self.m_x_size, 2) if (x < _idiv(self.m_x_size, 2)) else x)
        y = (_idiv(self.m_y_size, 2) if (y < _idiv(self.m_y_size, 2)) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1(self.m_x_size)
        self.YSize_1(self.m_y_size)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        self.m_canvas.FillRectangle(_idiv(self.YSize_0(), 2), 0, self.XSize_0() - _idiv(self.YSize_0(), 2), self.YSize_0(), ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillCircle(_idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - 1, _idiv(self.YSize_0(), 2), ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillCircle(self.XSize_0() - _idiv(self.YSize_0(), 2) - 1, _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), ColorToARGB(self.m_border_color, self.m_transparency))
        self.m_canvas.FillRectangle(_idiv(self.YSize_0(), 2), self.m_border, self.XSize_0() - _idiv(self.YSize_0(), 2), self.YSize_0() - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillCircle(_idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillCircle(self.XSize_0() - _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def NewValue(self, value, maxvalue, digits=0):
        v = 0
        v = _int(_fdiv(self.XSize_0() - _idiv(self.YSize_0(), 2), maxvalue) * value)
        self.m_canvas.FillRectangle(_idiv(self.YSize_0(), 2), self.m_border, self.XSize_0() - _idiv(self.YSize_0(), 2), self.YSize_0() - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillCircle(_idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FillCircle(self.XSize_0() - _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_bg_color, self.m_transparency))
        if v >= _idiv(self.YSize_0(), 2) and v <= (self.XSize_0() - _idiv(self.YSize_0(), 2)):
            self.m_canvas.FillRectangle(_idiv(self.YSize_0(), 2), self.m_border, v, self.YSize_0() - self.m_border, ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.FillCircle(_idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.FillCircle(v, _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_scale_color, self.m_transparency))
        elif v > (self.XSize_0() - _idiv(self.YSize_0(), 2)):
            self.m_canvas.FillRectangle(_idiv(self.YSize_0(), 2), self.m_border, self.XSize_0() - _idiv(self.YSize_0(), 2), self.YSize_0() - self.m_border, ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.FillCircle(_idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.FillCircle(self.XSize_0() - _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_scale_color, self.m_transparency))
        elif v > 0 and v < _idiv(self.YSize_0(), 2):
            self.m_canvas.FillCircle(_idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2), _idiv(self.YSize_0(), 2) - self.m_border, ColorToARGB(self.m_scale_color, self.m_transparency))
        self.m_canvas.FontSizeSet(self.m_font_size)
        self.m_canvas.TextOut(_idiv(self.XSize_0(), 2), _idiv(self.YSize_0(), 2), DoubleToString(value, digits), ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()

class CPetal(CCanvasBase):
    _q_fields = ('m_bg_color', 'm_label_color', 'm_value_color', 'm_transparency', 'm_orientation', 'm_radius', 'm_label_font_size', 'm_value_font_size', 'm_label_value')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_bg_color = 0
        self.m_label_color = 0
        self.m_value_color = 0
        self.m_transparency = 0
        self.m_orientation = 0
        self.m_radius = 0
        self.m_label_font_size = 0
        self.m_value_font_size = 0
        self.m_label_value = ""
        self.m_bg_color = clrDodgerBlue
        self.m_label_color = clrWhite
        self.m_value_color = clrWhite
        self.m_transparency = 255
        self.m_orientation = TOPLEFT
        self.m_radius = 50
        self.m_label_font_size = 20
        self.m_value_font_size = 20
        self.m_label_value = 'Label'
    def _q_dtor(self):
        pass
    def Orientation_1(self, orietation):
        self.m_orientation = orietation
    def Orientation_0(self):
        return self.m_orientation
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def LabelColor_0(self):
        return self.m_label_color
    def LabelColor_1(self, clr):
        self.m_label_color = clr
    def ValueColor_0(self):
        return self.m_value_color
    def ValueColor_1(self, clr):
        self.m_value_color = clr
    def Alpha_0(self):
        return self.m_transparency
    def Alpha_1(self, trn):
        self.m_transparency = trn
    def Radius_0(self):
        return self.m_radius
    def Radius_1(self, r):
        self.m_radius = r
    def LabelSize_0(self):
        return self.m_label_font_size
    def LabelSize_1(self, sz):
        self.m_label_font_size = sz
    def ValueSize_0(self):
        return self.m_value_font_size
    def ValueSize_1(self, sz):
        self.m_value_font_size = sz
    def LabelValue_0(self):
        return self.m_label_value
    def LabelValue_1(self, str_):
        self.m_label_value = str_
    def Create(self, name, x, y):
        r = self.m_radius
        x = (r if (x < r) else x)
        y = (r if (y < r) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1((2 * r) + 1)
        self.YSize_1((2 * r) + 1)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        self.m_canvas.FillCircle(r, r, r, ColorToARGB(self.m_bg_color, self.m_transparency))
        if self.m_orientation == TOPRIGHT:
            self.m_canvas.FillTriangle(_idiv(self.XSize_0(), 2), 0, self.XSize_0(), 0, self.XSize_0(), _idiv(self.YSize_0(), 2), ColorToARGB(self.m_bg_color, self.m_transparency))
        elif self.m_orientation == TOPLEFT:
            self.m_canvas.FillTriangle(0, 0, _idiv(self.XSize_0(), 2), 0, 0, _idiv(self.YSize_0(), 2), ColorToARGB(self.m_bg_color, self.m_transparency))
        elif self.m_orientation == BOTTOMRIGHT:
            self.m_canvas.FillTriangle(self.XSize_0(), self.YSize_0(), self.XSize_0(), _idiv(self.YSize_0(), 2), _idiv(self.XSize_0(), 2), self.YSize_0(), ColorToARGB(self.m_bg_color, self.m_transparency))
        elif self.m_orientation == BOTTOMLEFT:
            self.m_canvas.FillTriangle(0, self.YSize_0(), 0, _idiv(self.YSize_0(), 2), _idiv(self.XSize_0(), 2), self.YSize_0(), ColorToARGB(self.m_bg_color, self.m_transparency))
        elif self.m_orientation == BOTHRIGHT:
            self.m_canvas.FillTriangle(_idiv(self.XSize_0(), 2), 0, self.XSize_0(), 0, self.XSize_0(), _idiv(self.YSize_0(), 2), ColorToARGB(self.m_bg_color, self.m_transparency))
            self.m_canvas.FillTriangle(0, self.YSize_0(), 0, _idiv(self.YSize_0(), 2), _idiv(self.XSize_0(), 2), self.YSize_0(), ColorToARGB(self.m_bg_color, self.m_transparency))
        elif self.m_orientation == BOTHLEFT:
            self.m_canvas.FillTriangle(0, 0, _idiv(self.XSize_0(), 2), 0, 0, _idiv(self.YSize_0(), 2), ColorToARGB(self.m_bg_color, self.m_transparency))
            self.m_canvas.FillTriangle(self.XSize_0(), self.YSize_0(), self.XSize_0(), _idiv(self.YSize_0(), 2), _idiv(self.XSize_0(), 2), self.YSize_0(), ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FontNameSet('Trebuchet MS')
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(r, r, '-', ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_value_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def NewValue(self, value, digits):
        r = self.m_radius
        self.m_canvas.FillCircle(r, r, r, ColorToARGB(self.m_bg_color, self.m_transparency))
        self.m_canvas.FontNameSet('Trebuchet MS')
        self.m_canvas.FontSizeSet(self.m_value_font_size)
        self.m_canvas.TextOut(r, r, '-', ColorToARGB(self.m_value_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.FontSizeSet(self.m_label_font_size)
        self.m_canvas.TextOut(r, r + self.m_value_font_size, self.m_label_value, ColorToARGB(self.m_label_color, self.m_transparency), TA_CENTER | TA_VCENTER)
        self.m_canvas.Update()

class CPyramid(CCanvasBase):
    _q_fields = ('m_section_color', 'm_bg_color', 'm_scale_color', 'm_label_color', 'm_size', 'm_font_size', 'm_line1', 'm_line2', 'm_cross', 'm_transparency')
    def __init__(self):
        CCanvasBase.__init__(self)
        self.m_section_color = Arr(0, 0)
        self.m_bg_color = 0
        self.m_scale_color = 0
        self.m_label_color = 0
        self.m_size = 0
        self.m_font_size = 0
        self.m_line1 = Arr(0, 0.0)
        self.m_line2 = Arr(0, 0.0)
        self.m_cross = Arr(0, 0.0)
        self.m_transparency = 0
        self.m_bg_color = clrSilver
        self.m_scale_color = clrWhite
        self.m_label_color = clrWhite
        self.m_size = 400
        self.m_font_size = 14
        self.m_transparency = 255
        ArrayResize(self.m_section_color, 5)
        self.m_section_color[0] = 0x0000F0
        self.m_section_color[1] = 0x4696FA
        self.m_section_color[2] = 0x50AF00
        self.m_section_color[3] = 0xC87300
        self.m_section_color[4] = clrMidnightBlue
    def _q_dtor(self):
        pass
    def SectionColor(self, clr, number):
        number = (5 if (number > 5) else number)
        self.m_section_color[number - 1] = clr
    def BgColor_0(self):
        return self.m_bg_color
    def BgColor_1(self, clr):
        self.m_bg_color = clr
    def ScaleColor_0(self):
        return self.m_scale_color
    def ScaleColor_1(self, clr):
        self.m_scale_color = clr
    def LabelColor_0(self):
        return self.m_label_color
    def LabelColor_1(self, clr):
        self.m_label_color = clr
    def Size_0(self):
        return self.m_size
    def Size_1(self, size):
        self.m_size = size
    def FontSize_0(self):
        return self.m_font_size
    def FontSize_1(self, fontsize):
        self.m_font_size = fontsize
    def Alpha_0(self):
        return self.m_transparency
    def Alpha_1(self, trn):
        self.m_transparency = trn
    def Create(self, name, x, y):
        size = self.m_size
        x = (_idiv(size, 2) if (x < _idiv(size, 2)) else x)
        y = (_idiv(size, 2) if (y < _idiv(size, 2)) else y)
        self.Name(name)
        self.X_1(x)
        self.Y_1(y)
        self.XSize_1(size)
        self.YSize_1(size)
        if not self.CreateCanvas():
            Print('Error. Can not create Canvas.')
        self.m_canvas.FontNameSet('Trebuchet MS')
        self.m_canvas.FontSizeSet(self.m_font_size)
        self.m_canvas.FontAngleSet(200)
        x1 = 0.0
        x2 = 0.0
        y1 = 0.0
        y2 = 0.0
        x1 = _idiv(self.XSize_0(), 2)
        y1 = 0.0
        x2 = 0.0
        y2 = _idiv(4 * self.YSize_0(), 5)
        self.Equation(x1, y1, x2, y2, self.m_line1)
        for i in range(5, 0, -1):
            y1 = _idiv(i * self.YSize_0(), 5)
            y2 = _idiv((i - 1) * self.YSize_0(), 5)
            self.Equation(x1, y1, x2, y2, self.m_line2)
            self.Cross(self.m_line1[0], self.m_line1[1], self.m_line2[0], self.m_line2[1], self.m_cross)
            self.m_canvas.FillTriangle(_int(x1), 0, _int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(self.m_section_color[i - 1], self.m_transparency))
            self.m_canvas.LineAA(_int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(self.m_scale_color, self.m_transparency))
        x1 = _idiv(self.XSize_0(), 2)
        y1 = 0.0
        x2 = self.XSize_0()
        y2 = _idiv(4 * self.YSize_0(), 5)
        self.Equation(x1, y1, x2, y2, self.m_line1)
        for i in range(5, 0, -1):
            y1 = _idiv(i * self.YSize_0(), 5)
            y2 = _idiv((i - 1) * self.YSize_0(), 5)
            self.Equation(x1, y1, x2, y2, self.m_line2)
            self.Cross(self.m_line1[0], self.m_line1[1], self.m_line2[0], self.m_line2[1], self.m_cross)
            self.m_canvas.FillTriangle(_int(x1), 0, _int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(self.m_section_color[i - 1]))
            self.m_canvas.LineAA(_int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.TextOut(_int(x1 + 2), _int(y2 + _idiv(self.YSize_0(), 6)), ' - ', ColorToARGB(self.m_label_color, self.m_transparency), TA_LEFT | TA_VCENTER)
        self.m_canvas.LineVertical(_idiv(self.XSize_0(), 2), 0, self.YSize_0(), ColorToARGB(self.m_scale_color, self.m_transparency))
        self.m_canvas.Update()
    def Delete(self):
        self.DeleteCanvas()
    def NewValue(self, value, maxvalue):
        s = 0.0
        col = 0
        x1 = 0.0
        x2 = 0.0
        y1 = 0.0
        y2 = 0.0
        x1 = _idiv(self.XSize_0(), 2)
        y1 = 0.0
        x2 = 0.0
        y2 = _idiv(4 * self.YSize_0(), 5)
        self.Equation(x1, y1, x2, y2, self.m_line1)
        for i in range(5, 0, -1):
            s = maxvalue - (((i - 1) * maxvalue) / 5)
            col = (self.m_section_color[i - 1] if (value >= s) else self.m_bg_color)
            y1 = _idiv(i * self.YSize_0(), 5)
            y2 = _idiv((i - 1) * self.YSize_0(), 5)
            self.Equation(x1, y1, x2, y2, self.m_line2)
            self.Cross(self.m_line1[0], self.m_line1[1], self.m_line2[0], self.m_line2[1], self.m_cross)
            self.m_canvas.FillTriangle(_int(x1), 0, _int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(self.m_section_color[i - 1], self.m_transparency))
            self.m_canvas.FillTriangle(_int(x1), 0, _int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(col, self.m_transparency))
            self.m_canvas.LineAA(_int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(clrWhite))
        x1 = _idiv(self.XSize_0(), 2)
        y1 = 0.0
        x2 = self.XSize_0()
        y2 = _idiv(4 * self.YSize_0(), 5)
        self.Equation(x1, y1, x2, y2, self.m_line1)
        for i in range(5, 0, -1):
            s = maxvalue - (((i - 1) * maxvalue) / 5)
            col = (self.m_section_color[i - 1] if (value >= s) else self.m_bg_color)
            y1 = _idiv(i * self.YSize_0(), 5)
            y2 = _idiv((i - 1) * self.YSize_0(), 5)
            self.Equation(x1, y1, x2, y2, self.m_line2)
            self.Cross(self.m_line1[0], self.m_line1[1], self.m_line2[0], self.m_line2[1], self.m_cross)
            self.m_canvas.FillTriangle(_int(x1), 0, _int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(self.m_section_color[i - 1], self.m_transparency))
            self.m_canvas.FillTriangle(_int(x1), 0, _int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(col, self.m_transparency))
            self.m_canvas.LineAA(_int(x1), _int(y1), _int(self.m_cross[0]), _int(self.m_cross[1]), ColorToARGB(self.m_scale_color, self.m_transparency))
            self.m_canvas.TextOut(_int(x1 + 2), _int(y2 + _idiv(self.YSize_0(), 6)), DoubleToString(s, 0), ColorToARGB(self.m_label_color, self.m_transparency), TA_LEFT | TA_VCENTER)
        self.m_canvas.LineVertical(_idiv(self.XSize_0(), 2), 0, self.YSize_0(), ColorToARGB(self.m_scale_color, self.m_transparency))
        self.m_canvas.Update()
    def Equation(self, x1, y1, x2, y2, arr):
        ArrayResize(arr, 2)
        arr[0] = _fdiv(y1 - y2, x1 - x2)
        arr[1] = y2 - (arr[0] * x2)
    def Cross(self, k1, b1, k2, b2, arr):
        x = 0.0
        y = 0.0
        ArrayResize(arr, 2)
        y = _fdiv((b1 * k2) - (b2 * k1), k2 - k1)
        x = _fdiv(y - b2, k2)
        arr[0] = x
        arr[1] = y

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

def OnInit():
    global InpInd_Handle
    InpInd_Handle = iADX(Symbol(), PERIOD_CURRENT, period)
    if InpInd_Handle == INVALID_HANDLE:
        Print('Failed to get indicator handle')
        return INIT_FAILED
    ArraySetAsSeries(adx, True)
    ind1.Size_1(250)
    ind1.Create('pyramid', 200, 0)
    ind2.FontSize_1(ind1.FontSize_0())
    ind2.LabelSize_1(ind1.FontSize_0())
    ind2.Label_1('ADX')
    ind2.Radius_1(30)
    ind2.Create('label', ind1.X_0() - _idiv(ind1.Size_0(), 3), ind1.Y_0() - _idiv(ind1.Size_0(), 4))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if CopyBuffer(InpInd_Handle, 0, 0, 2, adx) <= 0:
        return 0
    ind1.NewValue(adx[0], maxval)
    ind2.NewValue_2(adx[0])
    return rates_total

def OnDeinit(reason):
    ind1.Delete()
    ind2.Delete()
    ChartRedraw()

# ---- global variables initialised from expressions
ind1 = _alloc(CPyramid)
ind1.__init__()
ind2 = _alloc(CCircleSimple)
ind2.__init__()

# ---- static local variables
_s_CCanvas_FillPolygon_p = Arr(0, 0, factory=CPoint)
_s_CCanvas_PixelSetAA_rr = Arr(4, 0.0, dyn=False)
_s_CCanvas_PixelSetAA_xx = Arr(4, 0, dyn=False)
_s_CCanvas_PixelSetAA_yy = Arr(4, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CPyramidIndicator(_MQL5Indicator):
    name = 'CPyramid'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,  # ADX Period
        'maxval': 50.0,  # Max value
    }

