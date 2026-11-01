"""MetaCOT2 TFF Movement Index — converted from MQL5: MQL5 Indicators/MetaCOT 2 CFTC ToolBox (Set of Indicators) MT5/MetaCOT2 TFF Movement Index.mq5

MetaCOT 2 is designed for analize CFTC reports, data mining and for fundamental analysis.
See article 'MetaCOT Project - New horizons for CFTC report analysis in MetaTrader 4'
\\nFor work this indicator need download and install 'MetaCOT -  Install CFTC reports' tool.
Copyright: MetaCOT® 2009-2017, Vasiliy Sokolov, St.-Petersburg, Russia; Link: https://www.mql5.com/en/articles/1573; Version: VERSION

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Imports DLL/library functions: ..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5 (not available).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.metacot_version import *  # #include Version.mqh
from backtester.mql5.lib.metacot_enums import *  # #include Enums.mqh

MQL5_META = {'props': {'copyright': 'MetaCOT® 2009-2017, Vasiliy Sokolov, St.-Petersburg, Russia', 'link': 'https://www.mql5.com/en/articles/1573', 'version': 'VERSION', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [255], 2: [9470064]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['MetaCOT 2 is designed for analize CFTC reports, data mining and for fundamental analysis.', "See article 'MetaCOT Project - New horizons for CFTC report analysis in MetaTrader 4'", "\\nFor work this indicator need download and install 'MetaCOT -  Install CFTC reports' tool."], 'name': 'MetaCOT2 TFF Movement Index', 'source': 'MQL5 Indicators/MetaCOT 2 CFTC ToolBox (Set of Indicators) MT5/MetaCOT2 TFF Movement Index.mq5', 'folder': 'MetaCOT 2 CFTC ToolBox (Set of Indicators) MT5', 'inputs': [{'mql': 'Source', 'py': 'Source', 'param': 'Source', 'type': 'int', 'default': 0, 'label': 'Source of Report', 'sinput': False}, {'mql': 'Group', 'py': 'Group', 'param': 'Group', 'type': 'int', 'default': 0, 'label': 'Group of Traders', 'sinput': False}, {'mql': 'TffPeriod', 'py': 'TffPeriod', 'param': 'TffPeriod', 'type': 'int', 'default': 52, 'label': 'Period', 'sinput': False}, {'mql': 'DiffLag', 'py': 'DiffLag', 'param': 'DiffLag', 'type': 'int', 'default': 6, 'label': 'Movement Period', 'sinput': False}, {'mql': 'MovType', 'py': 'MovType', 'param': 'MovType', 'type': 'int', 'default': 0, 'label': 'Movement Type', 'sinput': False}, {'mql': 'critv', 'py': 'critv', 'param': 'critv', 'type': 'int', 'default': 40, 'label': 'Critical Value', 'sinput': False}, {'mql': 'ProffSettings', 'py': 'ProffSettings', 'param': None, 'type': 'string', 'default': '', 'label': '#      PROFESSIONAL SETTINGS:    #', 'sinput': False}, {'mql': 'ReleaseDay', 'py': 'ReleaseDay', 'param': 'ReleaseDay', 'type': 'int', 'default': 1, 'label': 'Release Day', 'sinput': False}, {'mql': 'DateType', 'py': 'DateType', 'param': 'DateType', 'type': 'int', 'default': 0, 'label': 'Data Type', 'sinput': False}, {'mql': 'AutoDetectReport', 'py': 'AutoDetectReport', 'param': 'AutoDetectReport', 'type': 'bool', 'default': True, 'label': 'Auto Detect Report Name', 'sinput': False}, {'mql': 'LoadReportName', 'py': 'LoadReportName', 'param': None, 'type': 'string', 'default': 'BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE', 'label': 'Report Name (If Auto Detect=false)', 'sinput': False}, {'mql': 'Mirror', 'py': 'Mirror', 'param': 'Mirror', 'type': 'bool', 'default': False, 'label': 'Mirror Mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': ['..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5'], 'libraries': ['Version.mqh', 'Enums.mqh']}

# ---- inputs and global variables
ReportType = CFTC_TFF
Source = _input('Source', FUTURES_ONLY)  # Source of Report
Group = _input('Group', TFF_NETTO_OI)  # Group of Traders
TffPeriod = _input('TffPeriod', 52)  # Period
DiffLag = _input('DiffLag', 6)  # Movement Period
MovType = _input('MovType', MOVMENT_ON_COT_INDEX)  # Movement Type
critv = _input('critv', 40)  # Critical Value
ProffSettings = _input('ProffSettings', '')  # #      PROFESSIONAL SETTINGS:    #
ReleaseDay = _input('ReleaseDay', COT_RELEASE_FRIDAY)  # Release Day
DateType = _input('DateType', COT_DATA_FUTURES)  # Data Type
AutoDetectReport = _input('AutoDetectReport', True)  # Auto Detect Report Name
LoadReportName = _input('LoadReportName', 'BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE')  # Report Name (If Auto Detect=false)
Mirror = _input('Mirror', False)  # Mirror Mode
cot_values = Arr(0, 0.0)
limit_values = Arr(0, 0.0)
Sign = 1
cvalues = Arr(0, 0.0)
ctimes = Arr(0, 0)
cindex = 0
prev_total = 0
wrong_combinated = False

class CotBaseSettings(MqlObject):
    _q_fields = ('report_name', 'source', 'subgroup', 'date_type', 'release_day')
    def __init__(self):
        self.report_name = ""
        self.source = 0
        self.subgroup = 0
        self.date_type = 0
        self.release_day = 0
        self.report_name = '# BRITISH POUND STERLING - CONCATENATE'
        self.source = FUTURES_AND_OPTIONS
        self.subgroup = COT_SUBGROUP_ALL
        self.date_type = COT_DATA_FUTURES
        self.release_day = COT_RELEASE_FRIDAY

class CftcReportInfo(MqlObject):
    _q_fields = ('reverse', 'report_name', 'short_name')
    def __init__(self, *args):
        self.reverse = False
        self.report_name = ""
        self.short_name = ""

class CftcIndParams(MqlObject):
    _q_fields = ('ind_type', 'group_traders', 'name_group_traders', 'period', 'mov_period', 'mov_type')
    def __init__(self, *args):
        self.ind_type = 0
        self.group_traders = 0
        self.name_group_traders = ""
        self.period = 0
        self.mov_period = 0
        self.mov_type = 0

def GetCftcReportInfo(*args):
    raise NotImplementedError('DLL/library function GetCftcReportInfo from ..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5')

def GetCotAbsoluteValues(*args):
    raise NotImplementedError('DLL/library function GetCotAbsoluteValues from ..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5')

def GetCotLargestValues(*args):
    raise NotImplementedError('DLL/library function GetCotLargestValues from ..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5')

def GetDCotAbsoluteValues(*args):
    raise NotImplementedError('DLL/library function GetDCotAbsoluteValues from ..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5')

def GetTffAbsoluteValues(*args):
    raise NotImplementedError('DLL/library function GetTffAbsoluteValues from ..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5')

def GetCitAbsoluteValues(*args):
    raise NotImplementedError('DLL/library function GetCitAbsoluteValues from ..\\\\Scripts\\\\Market\\\\MetaCOT 2 CFTC ToolBox Demo MT5.ex5')

def GetCotFromNetto(ngroup, lgroup, sgroup):
    _sw1 = ngroup
    if _sw1 == COT_NETTO_NCOMM:
        lgroup.v = COT_GROUP_NONCOMM_LONG
        sgroup.v = COT_GROUP_NONCOMM_SHORT
    elif _sw1 == COT_NETTO_OPERATORS:
        lgroup.v = COT_GROUP_OPERATORS_LONG
        sgroup.v = COT_GROUP_OPERATORS_SHORT
    elif _sw1 == COT_NETTO_NONREPORTABLE:
        lgroup.v = COT_GROUP_NONREP_LONG
        sgroup.v = COT_GROUP_NONREP_SHORT

def GetIndexValues(period, src_values, ind_values):
    max_ = 0.0
    min_ = 0.0
    index = 0.0
    curr = 0.0
    imax = 0
    imin = 0
    total = ArraySize(src_values)
    ArrayResize(ind_values, ArraySize(src_values))
    ArrayInitialize(ind_values, EMPTY_VALUE)
    for i in range(period - 1, total):
        imax = ArrayMaximum(src_values, i - period + 1, period)
        imin = ArrayMinimum(src_values, i - period + 1, period)
        max_ = src_values[imax]
        min_ = src_values[imin]
        curr = src_values[i]
        if (max_ - min_) != 0.0:
            index = _fdiv(curr - min_, max_ - min_) * 100.0
        else:
            index = 100.0
        ind_values[i] = index
    return ArraySize(ind_values) > 0

def GetRatioValues(netto_values, oi_values, ratio_values):
    ArrayResize(ratio_values, ArraySize(oi_values))
    for i in range(0, ArraySize(ratio_values)):
        if oi_values[i] != 0.0:
            ratio_values[i] = _fdiv(netto_values[i], oi_values[i])
        else:
            ratio_values[i] = 1.0
    return ArraySize(ratio_values) > 0

def GetDiffValues(src_values, diff_values, diff_type=DIFF_ABS, diff_lag=1):
    ArrayResize(diff_values, ArraySize(src_values))
    ArrayInitialize(diff_values, EMPTY_VALUE)
    for i in range(diff_lag, ArraySize(src_values)):
        delta = src_values[i] - src_values[i - diff_lag]
        if diff_type == DIFF_PERCENT:
            if src_values[i - diff_lag] != 0.0:
                delta = _fdiv(delta, src_values[i - diff_lag]) * 100.0
        diff_values[i] = delta
    return ArraySize(diff_values) > 0

def GetCotNettoValues(settings, group, times, values):
    if group == COT_NETTO_OI:
        return GetCotAbsoluteValues(settings, COT_GROUP_OI, times, values)
    long_group = Box(COT_GROUP_OI)
    short_group = Box(COT_GROUP_OI)
    GetCotFromNetto(group, long_group, short_group)
    long_values = Arr(0, 0.0)
    short_values = Arr(0, 0.0)
    GetCotAbsoluteValues(settings, long_group.v, times, long_values)
    GetCotAbsoluteValues(settings, short_group.v, times, short_values)
    ArrayResize(values, ArraySize(long_values))
    for i in range(0, ArraySize(long_values)):
        values[i] = long_values[i] - short_values[i]
    return ArraySize(values) > 0

def GetCotIndexValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    if not GetCotNettoValues(settings, group, times, netto_values):
        return False
    return GetIndexValues(period, netto_values, values)

def GetCotWillcoValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    oi_values = Arr(0, 0.0)
    if not GetCotNettoValues(settings, group, times, netto_values):
        return False
    if not GetCotAbsoluteValues(settings, COT_GROUP_OI, times, oi_values):
        return False
    ratio_values = Arr(0, 0.0)
    GetRatioValues(netto_values, oi_values, ratio_values)
    return GetIndexValues(period, ratio_values, values)

def GetDCotNettoValues(settings, group, times, values):
    if group == DCOT_NETTO_OI:
        return GetDCotAbsoluteValues(settings, DCOT_GROUP_OI, times, values)
    long_group = Box(DCOT_GROUP_OI)
    short_group = Box(DCOT_GROUP_OI)
    GetDCotFromNetto(group, long_group, short_group)
    long_values = Arr(0, 0.0)
    short_values = Arr(0, 0.0)
    GetDCotAbsoluteValues(settings, long_group.v, times, long_values)
    GetDCotAbsoluteValues(settings, short_group.v, times, short_values)
    ArrayResize(values, ArraySize(long_values))
    for i in range(0, ArraySize(long_values)):
        values[i] = long_values[i] - short_values[i]
    return ArraySize(values) > 0

def GetDCotIndexValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    if not GetDCotNettoValues(settings, group, times, netto_values):
        return False
    return GetIndexValues(period, netto_values, values)

def GetDCotWillcoValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    oi_values = Arr(0, 0.0)
    if not GetDCotNettoValues(settings, group, times, netto_values):
        return False
    if not GetDCotAbsoluteValues(settings, DCOT_GROUP_OI, times, oi_values):
        return False
    ratio_values = Arr(0, 0.0)
    GetRatioValues(netto_values, oi_values, ratio_values)
    return GetIndexValues(period, netto_values, values)

def GetDCotFromNetto(ngroup, lgroup, sgroup):
    _sw2 = ngroup
    if _sw2 == DCOT_NETTO_DEALERS:
        lgroup.v = DCOT_GROUP_DEALERS_LONG
        sgroup.v = DCOT_GROUP_DEALERS_SHORT
    elif _sw2 == DCOT_NETTO_MANAGED:
        lgroup.v = DCOT_GROUP_MANAGED_LONG
        sgroup.v = DCOT_GROUP_MANAGED_SHORT
    elif _sw2 == DCOT_NETTO_NONREP:
        lgroup.v = DCOT_GROUP_NONREP_LONG
        sgroup.v = DCOT_GROUP_NONREP_SHORT
    elif _sw2 == DCOT_NETTO_PRODUCER:
        lgroup.v = DCOT_GROUP_PRODUCER_LONG
        sgroup.v = DCOT_GROUP_PRODUCER_SHORT
    elif _sw2 == DCOT_NETTO_TOTAL:
        lgroup.v = DCOT_GROUP_TOTAL_LONG
        sgroup.v = DCOT_GROUP_TOTAL_SHORT
    elif _sw2 == DCOT_NETTO_REPORTABLE:
        lgroup.v = DCOT_GROUP_REPORTABLE_LONG
        sgroup.v = DCOT_GROUP_REPORTABLE_SHORT

def GetTffNettoValues(settings, group, times, values):
    if group == TFF_NETTO_OI:
        return GetTffAbsoluteValues(settings, TFF_GROUP_OI, times, values)
    long_group = Box(TFF_GROUP_OI)
    short_group = Box(TFF_GROUP_OI)
    GetTffFromNetto(group, long_group, short_group)
    long_values = Arr(0, 0.0)
    short_values = Arr(0, 0.0)
    GetTffAbsoluteValues(settings, long_group.v, times, long_values)
    GetTffAbsoluteValues(settings, short_group.v, times, short_values)
    ArrayResize(values, ArraySize(long_values))
    for i in range(0, ArraySize(long_values)):
        values[i] = long_values[i] - short_values[i]
    return ArraySize(values) > 0

def GetTffFromNetto(ngroup, lgroup, sgroup):
    _sw3 = ngroup
    if _sw3 == TFF_NETTO_DEALERS:
        lgroup.v = TFF_GROUP_DEALERS_LONG
        sgroup.v = TFF_GROUP_DEALERS_SHORT
    elif _sw3 == TFF_NETTO_INSTITUTIONAL:
        lgroup.v = TFF_GROUP_INSTITUTIONAL_LONG
        sgroup.v = TFF_GROUP_INSTITUTIONAL_SHORT
    elif _sw3 == TFF_NETTO_LEVERAGE:
        lgroup.v = TFF_GROUP_LEVERAGE_LONG
        sgroup.v = TFF_GROUP_LEVERAGE_SHORT
    elif _sw3 == TFF_NETTO_REPORTABLE:
        lgroup.v = TFF_GROUP_OTHER_REP_LONG
        sgroup.v = TFF_GROUP_OTHER_REP_SHORT
    elif _sw3 == TFF_NETTO_NONREPORT:
        lgroup.v = TFF_GROUP_NONREP_LONG
        sgroup.v = TFF_GROUP_NONREP_SHORT

def GetTffIndexValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    if not GetTffNettoValues(settings, group, times, netto_values):
        return False
    return GetIndexValues(period, netto_values, values)

def GetTffWillcoValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    oi_values = Arr(0, 0.0)
    if not GetTffNettoValues(settings, group, times, netto_values):
        return False
    if not GetTffAbsoluteValues(settings, TFF_GROUP_OI, times, oi_values):
        return False
    ratio_values = Arr(0, 0.0)
    GetRatioValues(netto_values, oi_values, ratio_values)
    return GetIndexValues(period, netto_values, values)

def GetCitNettoValues(settings, group, times, values):
    if group == CIT_NETTO_OI:
        return GetCitAbsoluteValues(settings, CIT_GROUP_OI, times, values)
    long_group = Box(CIT_GROUP_OI)
    short_group = Box(CIT_GROUP_OI)
    GetCitFromNetto(group, long_group, short_group)
    long_values = Arr(0, 0.0)
    short_values = Arr(0, 0.0)
    GetCitAbsoluteValues(settings, long_group.v, times, long_values)
    GetCitAbsoluteValues(settings, short_group.v, times, short_values)
    ArrayResize(values, ArraySize(long_values))
    for i in range(0, ArraySize(long_values)):
        values[i] = long_values[i] - short_values[i]
    return ArraySize(values) > 0

def GetCitFromNetto(ngroup, lgroup, sgroup):
    _sw4 = ngroup
    if _sw4 == CIT_NETTO_NONCOMM:
        lgroup.v = CIT_GROUP_NONCOMM_LONG
        sgroup.v = CIT_GROUP_NONCOMM_SHORT
    elif _sw4 == CIT_NETTO_NONREP:
        lgroup.v = CIT_GROUP_NONREP_LONG
        sgroup.v = CIT_GROUP_NONREP_SHORT
    elif _sw4 == CIT_NETTO_ALL:
        lgroup.v = CIT_GROUP_ALL_LONG
        sgroup.v = CIT_GROUP_ALL_SHORT
    elif _sw4 == CIT_NETTO_OPERATORS:
        lgroup.v = CIT_GROUP_OPERATORS_LONG
        sgroup.v = CIT_GROUP_OPERATORS_SHORT
    elif _sw4 == CIT_NETTO_REPORTABLE:
        lgroup.v = CIT_GROUP_REP_LONG
        sgroup.v = CIT_GROUP_REP_SHORT

def GetCitIndexValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    if not GetCitNettoValues(settings, group, times, netto_values):
        return False
    return GetIndexValues(period, netto_values, values)

def GetCitWillcoValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    oi_values = Arr(0, 0.0)
    if not GetCitNettoValues(settings, group, times, netto_values):
        return False
    if not GetCitAbsoluteValues(settings, CIT_GROUP_OI, times, oi_values):
        return False
    ratio_values = Arr(0, 0.0)
    GetRatioValues(netto_values, oi_values, ratio_values)
    return GetIndexValues(period, ratio_values, values)

def GetLCotFromNetto(ngroup, lgroup, sgroup):
    _sw5 = ngroup
    if _sw5 == LCOT_NETTO_4:
        lgroup.v = LCOT_GROSS_LONG_4
        sgroup.v = LCOT_GROSS_SHORT_4
    elif _sw5 == LCOT_NETTO_8:
        lgroup.v = LCOT_GROSS_LONG_8
        sgroup.v = LCOT_GROSS_SHORT_8
    elif _sw5 == LCOT_NETTO_NET_4:
        lgroup.v = LCOT_NET_LONG_4
        sgroup.v = LCOT_NET_SHORT_4
    elif _sw5 == LCOT_NETTO_NET_8:
        lgroup.v = LCOT_NET_LONG_8
        sgroup.v = LCOT_NET_SHORT_8

def GetLCotNettoValues(settings, group, times, values):
    long_group = Box(LCOT_GROSS_LONG_4)
    short_group = Box(LCOT_GROSS_SHORT_4)
    GetLCotFromNetto(group, long_group, short_group)
    long_values = Arr(0, 0.0)
    short_values = Arr(0, 0.0)
    GetCotLargestValues(settings, long_group.v, times, long_values)
    GetCotLargestValues(settings, short_group.v, times, short_values)
    ArrayResize(values, ArraySize(long_values))
    for i in range(0, ArraySize(long_values)):
        values[i] = long_values[i] - short_values[i]
    return ArraySize(values) > 0

def GetLCotIndexValues(settings, period, group, times, values):
    netto_values = Arr(0, 0.0)
    if not GetLCotNettoValues(settings, group, times, netto_values):
        return False
    return GetIndexValues(period, netto_values, values)

def GetCftcTotalGroupsOfInd(ind_type):
    _sw6 = ind_type
    if _sw6 in (CFTC_IND_COT_ABS_POS, CFTC_IND_COT_ABS_CHANGES):
        return 10
    elif _sw6 in (CFTC_IND_COT_NETTO_POS, CFTC_IND_COT_NETTO_CHANGES, CFTC_IND_COT_INDEX, CFTC_IND_COT_MOV_INDEX, CFTC_IND_COT_WILLCO_INDEX):
        return 5
    elif _sw6 in (CFTC_IND_DCOT_ABS_POS, CFTC_IND_DCOT_ABS_CHANGES):
        return 16
    elif _sw6 in (CFTC_IND_DCOT_NETTO_POS, CFTC_IND_DCOT_NETTO_CHANGES, CFTC_IND_DCOT_INDEX, CFTC_IND_DCOT_WILLCO, CFTC_IND_DCOT_MOV_INDEX):
        return 7
    elif _sw6 in (CFTC_IND_TFF_ABS_POS, CFTC_IND_TFF_ABS_CHANGES):
        return 15
    elif _sw6 in (CFTC_IND_TFF_NETTO_POS, CFTC_IND_TFF_NETTO_CHANGES, CFTC_IND_TFF_INDEX, CFTC_IND_TFF_MOV_INDEX, CFTC_IND_TFF_WILLCO):
        return 6
    elif _sw6 in (CFTC_IND_CIT_ABS_POS, CFTC_IND_CIT_ABS_CHANGES):
        return 12
    elif _sw6 in (CFTC_IND_CIT_NETTO_POS, CFTC_IND_CIT_NETTO_CHANGES, CFTC_IND_CIT_INDEX, CFTC_IND_CIT_MOV_INDEX, CFTC_IND_CIT_WILLCO):
        return 6
    elif _sw6 in (CFTC_IND_LCOT_ABS_POS, CFTC_IND_LCOT_ABS_CHANGES):
        return 8
    elif _sw6 in (CFTC_IND_LCOT_NETTO_POS, CFTC_IND_LCOT_NETTO_CHANGES, CFTC_IND_LCOT_MOV_INDEX, CFTC_IND_LCOT_WILLCO):
        return 4
    return 0

def GetCftcReportFromInd(ind_type):
    s_ind = EnumToString(ind_type, 'ENUM_CFTC_INDICATORS')
    if StringFind(s_ind, '_COT_', 8) != -1:
        return CFTC_COT
    if StringFind(s_ind, '_DCOT_', 8) != -1:
        return CFTC_DCOT
    if StringFind(s_ind, '_CIT_', 8) != -1:
        return CFTC_CIT
    if StringFind(s_ind, '_TFF_', 8) != -1:
        return CFTC_TFF
    if StringFind(s_ind, '_LCOT_', 8) != -1:
        return CFTC_LCOT
    return -1

def GetCftcValuesByIndType(settings, ind_params, times, values):
    _sw7 = ind_params.ind_type
    if _sw7 == CFTC_IND_COT_ABS_POS:
        ind_params.name_group_traders = EnumCotGroupToString(ind_params.group_traders)
        return GetCotAbsoluteValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_COT_ABS_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumCotGroupToString(ind_params.group_traders)
        GetCotAbsoluteValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_COT_NETTO_POS:
        ind_params.name_group_traders = EnumCotNetGroupToString(ind_params.group_traders)
        return GetCotNettoValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_COT_NETTO_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumCotNetGroupToString(ind_params.group_traders)
        GetCotNettoValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_COT_INDEX:
        ind_params.name_group_traders = EnumCotNetGroupToString(ind_params.group_traders)
        return GetCotIndexValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_COT_MOV_INDEX:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumCotNetGroupToString(ind_params.group_traders)
        if ind_params.mov_type == MOVMENT_ON_COT_INDEX:
            GetCotIndexValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        else:
            GetCotWillcoValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, DIFF_ABS, ind_params.mov_period)
    elif _sw7 == CFTC_IND_COT_WILLCO_INDEX:
        ind_params.name_group_traders = EnumCotNetGroupToString(ind_params.group_traders)
        return GetCotWillcoValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_DCOT_ABS_POS:
        ind_params.name_group_traders = EnumDCotGroupToString(ind_params.group_traders)
        return GetDCotAbsoluteValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_DCOT_ABS_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumDCotGroupToString(ind_params.group_traders)
        GetDCotAbsoluteValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_DCOT_NETTO_POS:
        ind_params.name_group_traders = EnumDCotNettoToString(ind_params.group_traders)
        return GetDCotNettoValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_DCOT_NETTO_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumDCotNettoToString(ind_params.group_traders)
        GetDCotNettoValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_DCOT_INDEX:
        ind_params.name_group_traders = EnumDCotNettoToString(ind_params.group_traders)
        return GetDCotIndexValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_DCOT_MOV_INDEX:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumDCotNettoToString(ind_params.group_traders)
        if ind_params.mov_type == MOVMENT_ON_COT_INDEX:
            GetDCotIndexValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        else:
            GetDCotWillcoValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, DIFF_ABS, ind_params.mov_period)
    elif _sw7 == CFTC_IND_DCOT_WILLCO:
        ind_params.name_group_traders = EnumDCotNettoToString(ind_params.group_traders)
        return GetDCotWillcoValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_TFF_ABS_POS:
        ind_params.name_group_traders = EnumTffGroupToString(ind_params.group_traders)
        return GetTffAbsoluteValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_TFF_ABS_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumTffGroupToString(ind_params.group_traders)
        GetTffAbsoluteValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_TFF_NETTO_POS:
        ind_params.name_group_traders = EnumTffNettoGroupToString(ind_params.group_traders)
        return GetTffNettoValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_TFF_NETTO_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumTffNettoGroupToString(ind_params.group_traders)
        GetTffNettoValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_TFF_INDEX:
        ind_params.name_group_traders = EnumTffNettoGroupToString(ind_params.group_traders)
        return GetTffIndexValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_TFF_MOV_INDEX:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumTffNettoGroupToString(ind_params.group_traders)
        if ind_params.mov_type == MOVMENT_ON_COT_INDEX:
            GetTffIndexValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        else:
            GetTffWillcoValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, DIFF_ABS, ind_params.mov_period)
    elif _sw7 == CFTC_IND_TFF_WILLCO:
        ind_params.name_group_traders = EnumTffNettoGroupToString(ind_params.group_traders)
        return GetTffWillcoValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_CIT_ABS_POS:
        ind_params.name_group_traders = EnumCitGroupToString(ind_params.group_traders)
        return GetCitAbsoluteValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_CIT_ABS_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumCitGroupToString(ind_params.group_traders)
        GetCitAbsoluteValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_CIT_NETTO_POS:
        ind_params.name_group_traders = EnumCitNettoGroupToString(ind_params.group_traders)
        return GetCitNettoValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_CIT_NETTO_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumCitNettoGroupToString(ind_params.group_traders)
        GetCitNettoValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_CIT_INDEX:
        ind_params.name_group_traders = EnumCitNettoGroupToString(ind_params.group_traders)
        return GetCitIndexValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_CIT_MOV_INDEX:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumCitNettoGroupToString(ind_params.group_traders)
        if ind_params.mov_type == MOVMENT_ON_COT_INDEX:
            GetCitIndexValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        else:
            GetCitWillcoValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, DIFF_ABS, ind_params.mov_period)
    elif _sw7 == CFTC_IND_CIT_WILLCO:
        ind_params.name_group_traders = EnumCitNettoGroupToString(ind_params.group_traders)
        return GetCitWillcoValues(settings, ind_params.period, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_LCOT_ABS_POS:
        ind_params.name_group_traders = EnumLCotToString(ind_params.group_traders)
        return GetCotLargestValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_LCOT_ABS_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumLCotToString(ind_params.group_traders)
        GetCotLargestValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_LCOT_NETTO_POS:
        ind_params.name_group_traders = EnumLCotNettoToString(ind_params.group_traders)
        return GetLCotNettoValues(settings, ind_params.group_traders, times, values)
    elif _sw7 == CFTC_IND_LCOT_NETTO_CHANGES:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumLCotNettoToString(ind_params.group_traders)
        GetLCotNettoValues(settings, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, ind_params.mov_type, ind_params.mov_period)
    elif _sw7 == CFTC_IND_LCOT_MOV_INDEX:
        src_values = Arr(0, 0.0)
        ind_params.name_group_traders = EnumLCotNettoToString(ind_params.group_traders)
        GetLCotIndexValues(settings, ind_params.period, ind_params.group_traders, times, src_values)
        return GetDiffValues(src_values, values, DIFF_ABS, ind_params.mov_period)
    elif _sw7 == CFTC_IND_LCOT_WILLCO:
        ind_params.name_group_traders = EnumLCotNettoToString(ind_params.group_traders)
        return GetLCotIndexValues(settings, ind_params.period, ind_params.group_traders, times, values)
    return True

def OnInit():
    global Sign, wrong_combinated
    if (not AutoDetectReport) or (not GetCftcReportInfo(Symbol(), ReportType, ReportInfo)):
        ReportInfo.reverse = Mirror
        ReportInfo.report_name = LoadReportName
        ReportInfo.short_name = LoadReportName
    if DateType == COT_DATA_NUMBERS_TRADES and Group == TFF_NETTO_NONREPORT:
        wrong_combinated = True
        return INIT_SUCCEEDED
    Sign = (-1 if Mirror else 1)
    SetIndexBuffer(0, cot_values, INDICATOR_DATA)
    SetIndexBuffer(1, limit_values, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 100.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, float(critv))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -1.0 * critv)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -100.0)
    mmode = (' (Mirror mode)' if Mirror else '')
    IndicatorSetString(INDICATOR_SHORTNAME, 'MetaCOT ' + '2.12' + ' Mov.Index, ' + ReportInfo.short_name + ' (' + _str(TffPeriod) + ',' + _str(DiffLag) + ') ' + EnumTffNettoGroupToString(Group) + mmode)
    CftcSet.report_name = ReportInfo.report_name
    CftcSet.source = Source
    CftcSet.date_type = DateType
    CftcSet.release_day = ReleaseDay
    CftcSet.report_name = ReportInfo.report_name
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global cindex, prev_total
    if (rates_total - prev_calculated) > 1:
        if MovType == MOVMENT_ON_COT_INDEX:
            GetTffIndexValues(CftcSet, TffPeriod, Group, ctimes, cvalues)
        else:
            GetTffWillcoValues(CftcSet, TffPeriod, Group, ctimes, cvalues)
    total = ArraySize(cvalues)
    if total == 0:
        return rates_total
    if prev_calculated == 0:
        cindex = 0
    ArraySetAsSeries(cot_values, False)
    ArraySetAsSeries(limit_values, False)
    ArraySetAsSeries(time, False)
    limit = prev_calculated
    if total != prev_total:
        limit = 0
        cindex = 0
        prev_total = total
    for i in range(limit, rates_total):
        if ctimes[cindex] > time[i]:
            cot_values[i] = EMPTY_VALUE
            continue
        while (cindex + 1) < total and time[i] >= ctimes[cindex + 1]:
            cindex += 1
        if cindex < DiffLag:
            cindex = DiffLag
        prev_value = cvalues[cindex - DiffLag]
        value = 0.0
        value = cvalues[cindex] - prev_value
        if not Mirror:
            cot_values[i] = value
        else:
            cot_values[i] = value * -1
        sign = (1 if (cot_values[i] >= 0) else -1)
        if MathAbs(cot_values[i]) > critv:
            limit_values[i] = critv * sign
        else:
            limit_values[i] = cot_values[i]
    return rates_total - 1

# ---- global variables initialised from expressions
ReportInfo = _alloc(CftcReportInfo)
ReportInfo.__init__()
CftcSet = _alloc(CotBaseSettings)
CftcSet.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MetaCOT2TFFMovementIndex(_MQL5Indicator):
    name = 'MetaCOT2 TFF Movement Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Source': _Choice({0: 'Futures Only', 1: 'Futures And Options'}, default=0),  # Source of Report
        'Group': _Choice({0: 'Open Interest', 1: 'Netto Dealers', 2: 'Netto Institutional', 3: 'Netto Leverage', 4: 'Netto Reportable', 5: 'Netto Nonreportable'}, default=0),  # Group of Traders
        'TffPeriod': 52,  # Period
        'DiffLag': 6,  # Movement Period
        'MovType': _Choice({0: 'COT Index', 1: 'Willco Index'}, default=0),  # Movement Type
        'critv': 40,  # Critical Value
        'ReleaseDay': _Choice({0: 'Release by Tuesday', 1: 'Release by Friday'}, default=1),  # Release Day
        'DateType': _Choice({0: 'Contracts of Traders', 1: 'Number of Traders'}, default=0),  # Data Type
        'AutoDetectReport': True,  # Auto Detect Report Name
        'Mirror': False,  # Mirror Mode
    }

