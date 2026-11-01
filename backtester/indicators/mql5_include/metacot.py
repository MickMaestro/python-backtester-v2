"""MetaCOT 2 CFTC ToolBox — ports of ``MetaCOT/ToolBox.mqh``,
``MetaCOT/Version.mqh`` / ``VersionFull.mqh`` (enums in :mod:`.metacot_enums`).

What the include does: the six *raw data* functions —
``GetCftcReportInfo``, ``GetCotAbsoluteValues``, ``GetCotLargestValues``,
``GetDCotAbsoluteValues``, ``GetTffAbsoluteValues``,
``GetCitAbsoluteValues`` — are ``#import``\\ ed from the commercial
"MetaCOT 2 CFTC ToolBox" Market product, which downloads the CFTC
Commitments-of-Traders reports. Everything else (netto positions, COT index,
Willco index, changes, the per-indicator dispatcher) is ordinary code in the
include, and is ported line by line here.

The data source is pluggable. Give :func:`set_data_source` an object with
the six methods (same arguments as the MQL5 functions, returning
``(ok, times, values)`` — times as MQL5 ``datetime`` ints, oldest first —
and ``(ok, CftcReportInfo)`` for the report info), e.g. one that reads CSV
files downloaded from cftc.gov. Without one the raw functions return
``False`` with empty arrays, which is what the indicators see in MT5 when
the library is missing, and they draw nothing.

Faithfully reproduced source bugs:

- ``GetDCotWillcoValues`` and ``GetTffWillcoValues`` compute the
  netto/open-interest ratio and then pass the **netto** values to
  ``GetIndexValues`` (the COT and CIT versions pass the ratio).
- ``CFTC_IND_LCOT_WILLCO`` returns the LCOT *index* (there is no LCOT Willco).
- ``EnumLCotToString`` has no label for ``LCOT_GROSS_SHORT_8`` or
  ``LCOT_NET_SHORT_8`` (returns ``""``).
"""

from __future__ import annotations

from dataclasses import dataclass

from .metacot_enums import *  # noqa: F401,F403 — the include exposes them all
from . import metacot_enums as E
from .mql_runtime import EMPTY_VALUE

VERSION = "2.12"
MC_LABEL = "MetaCOT " + VERSION


def Version() -> float:
    return float(VERSION)


@dataclass
class CotBaseSettings:
    report_name: str = "# BRITISH POUND STERLING - CONCATENATE"
    source: int = E.FUTURES_AND_OPTIONS
    subgroup: int = E.COT_SUBGROUP_ALL
    date_type: int = E.COT_DATA_FUTURES
    release_day: int = E.COT_RELEASE_FRIDAY


@dataclass
class CftcReportInfo:
    reverse: bool = False
    report_name: str = ""
    short_name: str = ""


@dataclass
class CftcIndParams:
    ind_type: int = 0
    group_traders: int = 0
    name_group_traders: str = ""
    period: int = 0
    mov_period: int = 0
    mov_type: int = 0


# ------------------------------------------------------------ data source

_SOURCE = None


def set_data_source(source) -> None:
    """Install the object that answers the six raw-data calls (see module doc)."""
    global _SOURCE
    _SOURCE = source


def _raw(name, *args):
    fn = getattr(_SOURCE, name, None) if _SOURCE is not None else None
    if fn is None:
        return False, [], []
    ok, times, values = fn(*args)
    return bool(ok), list(times), list(values)


def GetCftcReportInfo(symbol, report_type):
    fn = getattr(_SOURCE, "GetCftcReportInfo", None) if _SOURCE is not None else None
    if fn is None:
        return False, CftcReportInfo()
    return fn(symbol, report_type)


def GetCotAbsoluteValues(settings, group):
    return _raw("GetCotAbsoluteValues", settings, group)


def GetCotLargestValues(settings, group):
    return _raw("GetCotLargestValues", settings, group)


def GetDCotAbsoluteValues(settings, group):
    return _raw("GetDCotAbsoluteValues", settings, group)


def GetTffAbsoluteValues(settings, group):
    return _raw("GetTffAbsoluteValues", settings, group)


def GetCitAbsoluteValues(settings, group):
    return _raw("GetCitAbsoluteValues", settings, group)


# ------------------------------------------------------------ maths


def GetIndexValues(period: int, src_values):
    """Stochastic-style 0…100 position of each value in its ``period``
    window; EMPTY_VALUE before the first full window. → ``(ok, values)``"""
    total = len(src_values)
    ind_values = [EMPTY_VALUE] * total
    for i in range(period - 1, total):
        window = src_values[i - period + 1: i + 1]
        imax = max(range(len(window)), key=lambda k: (window[k], -k))   # first maximum
        imin = min(range(len(window)), key=lambda k: (window[k], k))    # first minimum
        mx = window[imax]
        mn = window[imin]
        curr = src_values[i]
        ind_values[i] = ((curr - mn) / (mx - mn)) * 100.0 if mx - mn != 0.0 else 100.0
    return len(ind_values) > 0, ind_values


def GetRatioValues(netto_values, oi_values):
    ratio = [0.0] * len(oi_values)
    for i in range(len(ratio)):
        ratio[i] = netto_values[i] / oi_values[i] if oi_values[i] != 0.0 else 1.0
    return len(ratio) > 0, ratio


def GetDiffValues(src_values, diff_type=E.DIFF_ABS, diff_lag: int = 1):
    diff = [EMPTY_VALUE] * len(src_values)
    for i in range(diff_lag, len(src_values)):
        delta = src_values[i] - src_values[i - diff_lag]
        if diff_type == E.DIFF_PERCENT and src_values[i - diff_lag] != 0.0:
            delta = delta / src_values[i - diff_lag] * 100.0
        diff[i] = delta
    return len(diff) > 0, diff


# ------------------------------------------------------- netto mappings

_COT_NETTO = {
    E.COT_NETTO_NCOMM: (E.COT_GROUP_NONCOMM_LONG, E.COT_GROUP_NONCOMM_SHORT),
    E.COT_NETTO_OPERATORS: (E.COT_GROUP_OPERATORS_LONG, E.COT_GROUP_OPERATORS_SHORT),
    E.COT_NETTO_NONREPORTABLE: (E.COT_GROUP_NONREP_LONG, E.COT_GROUP_NONREP_SHORT),
}
_DCOT_NETTO = {
    E.DCOT_NETTO_DEALERS: (E.DCOT_GROUP_DEALERS_LONG, E.DCOT_GROUP_DEALERS_SHORT),
    E.DCOT_NETTO_MANAGED: (E.DCOT_GROUP_MANAGED_LONG, E.DCOT_GROUP_MANAGED_SHORT),
    E.DCOT_NETTO_NONREP: (E.DCOT_GROUP_NONREP_LONG, E.DCOT_GROUP_NONREP_SHORT),
    E.DCOT_NETTO_PRODUCER: (E.DCOT_GROUP_PRODUCER_LONG, E.DCOT_GROUP_PRODUCER_SHORT),
    E.DCOT_NETTO_TOTAL: (E.DCOT_GROUP_TOTAL_LONG, E.DCOT_GROUP_TOTAL_SHORT),
    E.DCOT_NETTO_REPORTABLE: (E.DCOT_GROUP_REPORTABLE_LONG, E.DCOT_GROUP_REPORTABLE_SHORT),
}
_TFF_NETTO = {
    E.TFF_NETTO_DEALERS: (E.TFF_GROUP_DEALERS_LONG, E.TFF_GROUP_DEALERS_SHORT),
    E.TFF_NETTO_INSTITUTIONAL: (E.TFF_GROUP_INSTITUTIONAL_LONG, E.TFF_GROUP_INSTITUTIONAL_SHORT),
    E.TFF_NETTO_LEVERAGE: (E.TFF_GROUP_LEVERAGE_LONG, E.TFF_GROUP_LEVERAGE_SHORT),
    E.TFF_NETTO_REPORTABLE: (E.TFF_GROUP_OTHER_REP_LONG, E.TFF_GROUP_OTHER_REP_SHORT),
    E.TFF_NETTO_NONREPORT: (E.TFF_GROUP_NONREP_LONG, E.TFF_GROUP_NONREP_SHORT),
}
_CIT_NETTO = {
    E.CIT_NETTO_NONCOMM: (E.CIT_GROUP_NONCOMM_LONG, E.CIT_GROUP_NONCOMM_SHORT),
    E.CIT_NETTO_NONREP: (E.CIT_GROUP_NONREP_LONG, E.CIT_GROUP_NONREP_SHORT),
    E.CIT_NETTO_ALL: (E.CIT_GROUP_ALL_LONG, E.CIT_GROUP_ALL_SHORT),
    E.CIT_NETTO_OPERATORS: (E.CIT_GROUP_OPERATORS_LONG, E.CIT_GROUP_OPERATORS_SHORT),
    E.CIT_NETTO_REPORTABLE: (E.CIT_GROUP_REP_LONG, E.CIT_GROUP_REP_SHORT),
}
_LCOT_NETTO = {
    E.LCOT_NETTO_4: (E.LCOT_GROSS_LONG_4, E.LCOT_GROSS_SHORT_4),
    E.LCOT_NETTO_8: (E.LCOT_GROSS_LONG_8, E.LCOT_GROSS_SHORT_8),
    E.LCOT_NETTO_NET_4: (E.LCOT_NET_LONG_4, E.LCOT_NET_SHORT_4),
    E.LCOT_NETTO_NET_8: (E.LCOT_NET_LONG_8, E.LCOT_NET_SHORT_8),
}


def GetCotFromNetto(ngroup, lgroup=E.COT_GROUP_OI, sgroup=E.COT_GROUP_OI):
    return _COT_NETTO.get(int(ngroup), (lgroup, sgroup))


def GetDCotFromNetto(ngroup, lgroup=E.DCOT_GROUP_OI, sgroup=E.DCOT_GROUP_OI):
    return _DCOT_NETTO.get(int(ngroup), (lgroup, sgroup))


def GetTffFromNetto(ngroup, lgroup=E.TFF_GROUP_OI, sgroup=E.TFF_GROUP_OI):
    return _TFF_NETTO.get(int(ngroup), (lgroup, sgroup))


def GetCitFromNetto(ngroup, lgroup=E.CIT_GROUP_OI, sgroup=E.CIT_GROUP_OI):
    return _CIT_NETTO.get(int(ngroup), (lgroup, sgroup))


def GetLCotFromNetto(ngroup, lgroup=E.LCOT_GROSS_LONG_4, sgroup=E.LCOT_GROSS_SHORT_4):
    return _LCOT_NETTO.get(int(ngroup), (lgroup, sgroup))


def _netto(raw_fn, oi_netto, oi_group, from_netto, settings, group):
    if oi_netto is not None and group == oi_netto:
        return raw_fn(settings, oi_group)
    long_group, short_group = from_netto(group)
    _, times, long_values = raw_fn(settings, long_group)
    _, times2, short_values = raw_fn(settings, short_group)
    values = [long_values[i] - short_values[i] for i in range(len(long_values))]
    return len(values) > 0, (times2 if times2 else times), values


def GetCotNettoValues(settings, group):
    return _netto(GetCotAbsoluteValues, E.COT_NETTO_OI, E.COT_GROUP_OI, GetCotFromNetto, settings, group)


def GetDCotNettoValues(settings, group):
    return _netto(GetDCotAbsoluteValues, E.DCOT_NETTO_OI, E.DCOT_GROUP_OI, GetDCotFromNetto, settings, group)


def GetTffNettoValues(settings, group):
    return _netto(GetTffAbsoluteValues, E.TFF_NETTO_OI, E.TFF_GROUP_OI, GetTffFromNetto, settings, group)


def GetCitNettoValues(settings, group):
    return _netto(GetCitAbsoluteValues, E.CIT_NETTO_OI, E.CIT_GROUP_OI, GetCitFromNetto, settings, group)


def GetLCotNettoValues(settings, group):
    return _netto(GetCotLargestValues, None, None, GetLCotFromNetto, settings, group)


def _index(netto_fn, settings, period, group):
    ok, times, netto = netto_fn(settings, group)
    if not ok:
        return False, times, []
    ok, values = GetIndexValues(period, netto)
    return ok, times, values


def GetCotIndexValues(settings, period, group):
    return _index(GetCotNettoValues, settings, period, group)


def GetDCotIndexValues(settings, period, group):
    return _index(GetDCotNettoValues, settings, period, group)


def GetTffIndexValues(settings, period, group):
    return _index(GetTffNettoValues, settings, period, group)


def GetCitIndexValues(settings, period, group):
    return _index(GetCitNettoValues, settings, period, group)


def GetLCotIndexValues(settings, period, group):
    return _index(GetLCotNettoValues, settings, period, group)


def _willco(netto_fn, raw_fn, oi_group, settings, period, group, use_ratio: bool):
    ok, times, netto = netto_fn(settings, group)
    if not ok:
        return False, times, []
    ok, _, oi = raw_fn(settings, oi_group)
    if not ok:
        return False, times, []
    _, ratio = GetRatioValues(netto, oi)
    ok, values = GetIndexValues(period, ratio if use_ratio else netto)
    return ok, times, values


def GetCotWillcoValues(settings, period, group):
    return _willco(GetCotNettoValues, GetCotAbsoluteValues, E.COT_GROUP_OI, settings, period, group, True)


def GetDCotWillcoValues(settings, period, group):
    # sic: the source indexes the netto values, not the ratio
    return _willco(GetDCotNettoValues, GetDCotAbsoluteValues, E.DCOT_GROUP_OI, settings, period, group, False)


def GetTffWillcoValues(settings, period, group):
    # sic: the source indexes the netto values, not the ratio
    return _willco(GetTffNettoValues, GetTffAbsoluteValues, E.TFF_GROUP_OI, settings, period, group, False)


def GetCitWillcoValues(settings, period, group):
    return _willco(GetCitNettoValues, GetCitAbsoluteValues, E.CIT_GROUP_OI, settings, period, group, True)


# ------------------------------------------------------- dispatching


def GetCftcTotalGroupsOfInd(ind_type) -> int:
    t = int(ind_type)
    I = E
    if t in (I.CFTC_IND_COT_ABS_POS, I.CFTC_IND_COT_ABS_CHANGES):
        return I.COT_GROUP_TOTAL
    if t in (I.CFTC_IND_COT_NETTO_POS, I.CFTC_IND_COT_NETTO_CHANGES, I.CFTC_IND_COT_INDEX,
             I.CFTC_IND_COT_MOV_INDEX, I.CFTC_IND_COT_WILLCO_INDEX):
        return I.COT_NETTO_TOTAL
    if t in (I.CFTC_IND_DCOT_ABS_POS, I.CFTC_IND_DCOT_ABS_CHANGES):
        return I.DCOT_GROUP_TOTAL
    if t in (I.CFTC_IND_DCOT_NETTO_POS, I.CFTC_IND_DCOT_NETTO_CHANGES, I.CFTC_IND_DCOT_INDEX,
             I.CFTC_IND_DCOT_WILLCO, I.CFTC_IND_DCOT_MOV_INDEX):
        return I.DCOT_NETTO_GROUP_TOTAL
    if t in (I.CFTC_IND_TFF_ABS_POS, I.CFTC_IND_TFF_ABS_CHANGES):
        return I.TFF_GROUP_TOTAL
    if t in (I.CFTC_IND_TFF_NETTO_POS, I.CFTC_IND_TFF_NETTO_CHANGES, I.CFTC_IND_TFF_INDEX,
             I.CFTC_IND_TFF_MOV_INDEX, I.CFTC_IND_TFF_WILLCO):
        return I.TFF_NETTO_TOTAL
    if t in (I.CFTC_IND_CIT_ABS_POS, I.CFTC_IND_CIT_ABS_CHANGES):
        return I.CIT_GROUP_TOTAL
    if t in (I.CFTC_IND_CIT_NETTO_POS, I.CFTC_IND_CIT_NETTO_CHANGES, I.CFTC_IND_CIT_INDEX,
             I.CFTC_IND_CIT_MOV_INDEX, I.CFTC_IND_CIT_WILLCO):
        return I.CIT_NETTO_TOTAL
    if t in (I.CFTC_IND_LCOT_ABS_POS, I.CFTC_IND_LCOT_ABS_CHANGES):
        return I.LCOT_GROUP_TOTAL
    if t in (I.CFTC_IND_LCOT_NETTO_POS, I.CFTC_IND_LCOT_NETTO_CHANGES,
             I.CFTC_IND_LCOT_MOV_INDEX, I.CFTC_IND_LCOT_WILLCO):
        return I.LCOT_NETTO_TOTAL
    return 0


_IND_NAMES = {v: k for k, v in E.ENUM_CFTC_INDICATORS.items()}


def EnumToString_CftcInd(ind_type) -> str:
    return _IND_NAMES.get(int(ind_type), str(ind_type))


def GetCftcReportFromInd(ind_type) -> int:
    s_ind = EnumToString_CftcInd(ind_type)
    for token, report in (("_COT_", E.CFTC_COT), ("_DCOT_", E.CFTC_DCOT), ("_CIT_", E.CFTC_CIT),
                          ("_TFF_", E.CFTC_TFF), ("_LCOT_", E.CFTC_LCOT)):
        if s_ind.find(token, 8) != -1:
            return report
    return -1


def CftcIndTypeFromString(ind: str):
    """→ ``(found, ind_type)`` (the bool-returning overload)."""
    for i in range(E.CFTC_INDICATORS_TOTAL):
        if EnumToString_CftcInd(i) == ind:
            return True, i
    return False, 0


def EnumCftcToString(report) -> str:
    names = {v: k for k, v in E.ENUM_CFTC_REPORT.items()}
    parts = names.get(int(report), "").split("_")
    return parts[1] if len(parts) >= 2 else "CFTC"


def EnumCotToString(source) -> str:
    return "Futures Only" if source == E.FUTURES_ONLY else "Futures And Options"


def GetCftcValuesByIndType(settings: CotBaseSettings, ind_params: CftcIndParams):
    """Dispatch one MetaCOT indicator type → ``(ok, times, values)``; also sets
    ``ind_params.name_group_traders`` as the source does."""
    I = E
    t = int(ind_params.ind_type)
    g = ind_params.group_traders
    p = ind_params

    def changes(src):
        ok, times, values = src
        _, diff = GetDiffValues(values, p.mov_type, p.mov_period)
        return len(diff) > 0, times, diff

    def mov(index_fn, willco_fn):
        if p.mov_type == I.MOVMENT_ON_COT_INDEX or willco_fn is None:
            _, times, src = index_fn(settings, p.period, g)
        else:
            _, times, src = willco_fn(settings, p.period, g)
        _, diff = GetDiffValues(src, I.DIFF_ABS, p.mov_period)
        return len(diff) > 0, times, diff

    groups = (
        (I.CFTC_IND_COT_ABS_POS, I.CFTC_IND_COT_ABS_CHANGES, I.CFTC_IND_COT_NETTO_POS,
         I.CFTC_IND_COT_NETTO_CHANGES, I.CFTC_IND_COT_INDEX, I.CFTC_IND_COT_MOV_INDEX,
         I.CFTC_IND_COT_WILLCO_INDEX, I.EnumCotGroupToString, I.EnumCotNetGroupToString,
         GetCotAbsoluteValues, GetCotNettoValues, GetCotIndexValues, GetCotWillcoValues),
        (I.CFTC_IND_DCOT_ABS_POS, I.CFTC_IND_DCOT_ABS_CHANGES, I.CFTC_IND_DCOT_NETTO_POS,
         I.CFTC_IND_DCOT_NETTO_CHANGES, I.CFTC_IND_DCOT_INDEX, I.CFTC_IND_DCOT_MOV_INDEX,
         I.CFTC_IND_DCOT_WILLCO, I.EnumDCotGroupToString, I.EnumDCotNettoToString,
         GetDCotAbsoluteValues, GetDCotNettoValues, GetDCotIndexValues, GetDCotWillcoValues),
        (I.CFTC_IND_TFF_ABS_POS, I.CFTC_IND_TFF_ABS_CHANGES, I.CFTC_IND_TFF_NETTO_POS,
         I.CFTC_IND_TFF_NETTO_CHANGES, I.CFTC_IND_TFF_INDEX, I.CFTC_IND_TFF_MOV_INDEX,
         I.CFTC_IND_TFF_WILLCO, I.EnumTffGroupToString, I.EnumTffNettoGroupToString,
         GetTffAbsoluteValues, GetTffNettoValues, GetTffIndexValues, GetTffWillcoValues),
        (I.CFTC_IND_CIT_ABS_POS, I.CFTC_IND_CIT_ABS_CHANGES, I.CFTC_IND_CIT_NETTO_POS,
         I.CFTC_IND_CIT_NETTO_CHANGES, I.CFTC_IND_CIT_INDEX, I.CFTC_IND_CIT_MOV_INDEX,
         I.CFTC_IND_CIT_WILLCO, I.EnumCitGroupToString, I.EnumCitNettoGroupToString,
         GetCitAbsoluteValues, GetCitNettoValues, GetCitIndexValues, GetCitWillcoValues),
    )
    for (abs_pos, abs_ch, net_pos, net_ch, idx, mov_idx, willco, abs_name, net_name,
         raw_fn, net_fn, idx_fn, willco_fn) in groups:
        if t == abs_pos:
            p.name_group_traders = abs_name(g)
            return raw_fn(settings, g)
        if t == abs_ch:
            p.name_group_traders = abs_name(g)
            return changes(raw_fn(settings, g))
        if t == net_pos:
            p.name_group_traders = net_name(g)
            return net_fn(settings, g)
        if t == net_ch:
            p.name_group_traders = net_name(g)
            return changes(net_fn(settings, g))
        if t == idx:
            p.name_group_traders = net_name(g)
            return idx_fn(settings, p.period, g)
        if t == mov_idx:
            p.name_group_traders = net_name(g)
            return mov(idx_fn, willco_fn)
        if t == willco:
            p.name_group_traders = net_name(g)
            return willco_fn(settings, p.period, g)
    if t == I.CFTC_IND_LCOT_ABS_POS:
        p.name_group_traders = I.EnumLCotToString(g)
        return GetCotLargestValues(settings, g)
    if t == I.CFTC_IND_LCOT_ABS_CHANGES:
        p.name_group_traders = I.EnumLCotToString(g)
        return changes(GetCotLargestValues(settings, g))
    if t == I.CFTC_IND_LCOT_NETTO_POS:
        p.name_group_traders = I.EnumLCotNettoToString(g)
        return GetLCotNettoValues(settings, g)
    if t == I.CFTC_IND_LCOT_NETTO_CHANGES:
        p.name_group_traders = I.EnumLCotNettoToString(g)
        return changes(GetLCotNettoValues(settings, g))
    if t == I.CFTC_IND_LCOT_MOV_INDEX:
        p.name_group_traders = I.EnumLCotNettoToString(g)
        return mov(GetLCotIndexValues, None)
    if t == I.CFTC_IND_LCOT_WILLCO:
        p.name_group_traders = I.EnumLCotNettoToString(g)
        return GetLCotIndexValues(settings, p.period, g)
    return True, [], []
