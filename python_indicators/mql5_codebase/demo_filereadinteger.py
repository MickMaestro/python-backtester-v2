"""demo_filereadinteger — converted from MQL5: MQL5 Indicators/Demo_FileReadInteger/demo_filereadinteger.mq5

Copyright: Copyright 2013, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Trends'}, 'levels': [], 'description': [], 'name': 'demo_filereadinteger', 'source': 'MQL5 Indicators/Demo_FileReadInteger/demo_filereadinteger.mq5', 'folder': 'Demo_FileReadInteger', 'inputs': [{'mql': 'InpFileName', 'py': 'InpFileName', 'param': None, 'type': 'string', 'default': 'Trend.bin', 'label': 'file name', 'sinput': False}, {'mql': 'InpDirectoryName', 'py': 'InpDirectoryName', 'param': None, 'type': 'string', 'default': 'Data', 'label': 'directory name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
InpFileName = _input('InpFileName', 'Trend.bin')  # file name
InpDirectoryName = _input('InpDirectoryName', 'Data')  # directory name
ind = 0
size = 0
time_buff = Arr(0, 0)
buff = Arr(0, 0.0)

def OnInit():
    global size
    def_size = 100
    ArrayResize(time_buff, def_size)
    ResetLastError()
    file_handle = FileOpen(InpDirectoryName + '//' + InpFileName, FILE_READ | FILE_BIN)
    if file_handle != INVALID_HANDLE:
        PrintFormat('%s file is available for reading', InpFileName)
        PrintFormat('File path: %s\\Files\\', TerminalInfoString(TERMINAL_DATA_PATH))
        arr_size = 0
        arr = Arr(0, 0)
        while not FileIsEnding(file_handle):
            arr_size = FileReadInteger(file_handle, INT_VALUE)
            ArrayResize(arr, arr_size)
            for i in range(0, arr_size):
                arr[i] = _char(FileReadInteger(file_handle, CHAR_VALUE))
            time_buff[size] = StringToTime(CharArrayToString(arr))
            size += 1
            if size == def_size:
                def_size += 100
                ArrayResize(time_buff, def_size)
        FileClose(file_handle)
        PrintFormat('Data is read, %s file is closed', InpFileName)
    else:
        PrintFormat('Failed to open %s file, Error code = %d', InpFileName, GetLastError())
        return INIT_FAILED
    SetIndexBuffer(0, buff, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ind
    ArraySetAsSeries(time, False)
    ArraySetAsSeries(close, False)
    for i in range(prev_calculated, rates_total):
        buff[i] = 0.0
        if ind < size:
            for j in range(ind, size):
                if time[i] == time_buff[j]:
                    buff[i] = close[i]
                    ind = j + 1
                    break
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemoFilereadinteger(_MQL5Indicator):
    name = 'demo_filereadinteger'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

