"""demo_filereaddouble — converted from MQL5: MQL5 Indicators/Demo_FileReadDouble/demo_filereaddouble.mq5

Copyright: Copyright 2013, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MA'}, 'levels': [], 'description': [], 'name': 'demo_filereaddouble', 'source': 'MQL5 Indicators/Demo_FileReadDouble/demo_filereaddouble.mq5', 'folder': 'Demo_FileReadDouble', 'inputs': [{'mql': 'InpFileName', 'py': 'InpFileName', 'param': None, 'type': 'string', 'default': 'MA.csv', 'label': 'file name', 'sinput': False}, {'mql': 'InpDirectoryName', 'py': 'InpDirectoryName', 'param': None, 'type': 'string', 'default': 'Data', 'label': 'directory name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFileName = _input('InpFileName', 'MA.csv')  # file name
InpDirectoryName = _input('InpDirectoryName', 'Data')  # directory name
ind = 0
size = 0
ma_buff = Arr(0, 0.0)
time_buff = Arr(0, 0)
buff = Arr(0, 0.0)

def OnInit():
    global size
    ResetLastError()
    file_handle = FileOpen(InpDirectoryName + '//' + InpFileName, FILE_READ | FILE_BIN)
    if file_handle != INVALID_HANDLE:
        PrintFormat('%s file is available for reading', InpFileName)
        PrintFormat('File path: %s\\Files\\', TerminalInfoString(TERMINAL_DATA_PATH))
        size = _int(FileReadDouble(file_handle))
        ArrayResize(ma_buff, size)
        ArrayResize(time_buff, size)
        for i in range(0, size):
            time_buff[i] = _long(FileReadDouble(file_handle))
            ma_buff[i] = FileReadDouble(file_handle)
        FileClose(file_handle)
        PrintFormat('Data is written, %s file is closed', InpFileName)
    else:
        PrintFormat('Failed to open %s file, Error code = %d', InpFileName, GetLastError())
        return INIT_FAILED
    SetIndexBuffer(0, buff, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ind
    ArraySetAsSeries(time, False)
    for i in range(prev_calculated, rates_total):
        buff[i] = 0.0
        if ind < size:
            for j in range(ind, size):
                if time[i] == time_buff[j]:
                    buff[i] = ma_buff[j]
                    ind = j + 1
                    break
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemoFilereaddouble(_MQL5Indicator):
    name = 'demo_filereaddouble'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

