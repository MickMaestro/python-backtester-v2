"""DeleteTradeArrows — converted from MQL5: MQL5 Indicators/DeleteTradeArrows/DeleteTradeArrows.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'DeleteTradeArrows', 'source': 'MQL5 Indicators/DeleteTradeArrows/DeleteTradeArrows.mq5', 'folder': 'DeleteTradeArrows', 'inputs': [{'mql': 'del_pending', 'py': 'del_pending', 'param': 'del_pending', 'type': 'bool', 'default': True, 'label': 'удалять отложенники?', 'sinput': False}, {'mql': 'del_before_date', 'py': 'del_before_date', 'param': None, 'type': 'datetime', 'default': 0, 'label': 'удалять объекты до даты', 'sinput': False}, {'mql': 'del_after_date', 'py': 'del_after_date', 'param': None, 'type': 'datetime', 'default': 0, 'label': 'удалять объекты после даты', 'sinput': False}, {'mql': 'print_every_deletion', 'py': 'print_every_deletion', 'param': 'print_every_deletion', 'type': 'bool', 'default': False, 'label': 'сообщать об удаленных объектах?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
del_pending = _input('del_pending', True)  # удалять отложенники?
del_before_date = _input('del_before_date', 0)  # удалять объекты до даты
del_after_date = _input('del_after_date', 0)  # удалять объекты после даты
print_every_deletion = _input('print_every_deletion', False)  # сообщать об удаленных объектах?
bool_del_before = False
bool_del_after = False
object_names = Arr(0, "")

def OnInit():
    global bool_del_after, bool_del_before
    PrintFormat('%s: удалять отложенные - %s', 'OnInit', _str(del_pending))
    PrintFormat('%s:  del_before_date=%s', 'OnInit', TimeToString(del_before_date))
    PrintFormat('%s:  del_after_date=%s', 'OnInit', TimeToString(del_after_date))
    Comment('Objects on chart=', ObjectsTotal(0))
    bool_del_before = (del_before_date != 0)
    bool_del_after = (del_after_date != 0)
    Print('bool_del_before=', bool_del_before)
    Print('bool_del_after=', bool_del_after)
    ArrayResize(object_names, ObjectsTotal(0))
    ZeroMemory(object_names)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_first_run
    if _s_OnCalculate_first_run:
        _s_OnCalculate_first_run = False
    else:
        return 0
    pending_deleted = 0
    to_delete_object_name_count = 0
    total = ObjectsTotal(0)
    name = ""
    if del_pending:
        for i in range(total, -0, -1):
            name = ObjectName(0, i)
            type_ = ObjectGetInteger(0, name, OBJPROP_TYPE)
            if type_ == OBJ_ARROW:
                if ((StringFind(name, 'buy limit') != -1 or StringFind(name, 'buy stop') != -1) or StringFind(name, 'sell limit') != -1) or StringFind(name, 'sell stop') != -1:
                    order_id = GetOrderID(name)
                    if order_id != '':
                        object_names[to_delete_object_name_count] = order_id
                        to_delete_object_name_count += 1
                    if ObjectDelete(0, name):
                        if print_every_deletion:
                            Print('OnCalculate', ': ', pending_deleted, '. deleted ', name, '   type=', type_, '   id=', order_id)
                        pending_deleted += 1
        PrintFormat('Deleted %d arrows', pending_deleted)
        pending_deleted = 0
        if to_delete_object_name_count > 0:
            for i in range(to_delete_object_name_count, 0 - 1, -1):
                if DeleteObjectByPrefix(object_names[i]):
                    pending_deleted += 1
            PrintFormat('Deleted %d trendlines', pending_deleted)
    if bool_del_before:
        arrow_deleted = 0
        total = ObjectsTotal(0)
        arrow_time = 0
        for i in range(total, -0, -1):
            name = ObjectName(0, i)
            arrow_time = ObjectGetInteger(0, name, OBJPROP_TIME)
            if arrow_time < del_before_date:
                if ObjectDelete(0, name):
                    if print_every_deletion:
                        PrintFormat('%s: %d. deleted %s - %s', 'OnCalculate', i, TimeToString(arrow_time), name)
                        arrow_deleted += 1
        PrintFormat('Deleted before %s => %d objects', TimeToString(del_before_date), arrow_deleted)
    if bool_del_after:
        arrow_deleted = 0
        total = ObjectsTotal(0)
        arrow_time = 0
        for i in range(total, -0, -1):
            name = ObjectName(0, i)
            arrow_time = ObjectGetInteger(0, name, OBJPROP_TIME)
            if arrow_time > del_after_date:
                if ObjectDelete(0, name):
                    if print_every_deletion:
                        PrintFormat('%s: %d. deleted %s - %s', 'OnCalculate', i, TimeToString(arrow_time), name)
                        arrow_deleted += 1
        PrintFormat('Deleted after %s => %d objects', TimeToString(del_before_date), arrow_deleted)
    comment = StringFormat('Objects on chart=%d', ObjectsTotal(0))
    comment = comment + '\r\n' + StringFormat('delete pending==%s', _str(del_pending))
    if bool_del_before:
        comment = comment + '\r\n' + StringFormat('delete before %s', TimeToString(del_before_date))
    if bool_del_after:
        comment = comment + '\r\n' + StringFormat('delete after %s', TimeToString(del_after_date))
    comment = comment + '\r\n' + StringFormat('delete pending==%s', _str(del_pending))
    Comment(comment)
    return rates_total

def GetOrderID(arrow_name):
    id_ = ''
    id_pos = -1
    if (id_pos := StringFind(arrow_name, '#')) != -1:
        pos = StringFind(arrow_name, ' ', id_pos)
        id_ = StringSubstr(arrow_name, 0, pos)
    return id_

def DeleteObjectByPrefix(prefix):
    res = False
    total = ObjectsTotal(0)
    name = ""
    for i in range(total, -0, -1):
        name = ObjectName(0, i)
        if StringFind(name, prefix) == 0:
            if (res := ObjectDelete(0, name)):
                if print_every_deletion:
                    Print('DeleteObjectByPrefix', ':  deleted ', name)
    return res

# ---- static local variables
_s_OnCalculate_first_run = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeleteTradeArrows(_MQL5Indicator):
    name = 'DeleteTradeArrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'del_pending': True,  # удалять отложенники?
        'print_every_deletion': False,  # сообщать об удаленных объектах?
    }

