"""planetcycles — converted from MQL5: MQL5 Indicators/Astro Indicators/planetcycles.mq5

Copyright: J.S. 2012; Link: http://www.eselstreckdich.de; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Imports DLL/library functions: swedll32.dll (not available).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'J.S. 2012', 'link': 'http://www.eselstreckdich.de', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'PlanetCycle'}, 'levels': [], 'description': [], 'name': 'planetcycles', 'source': 'MQL5 Indicators/Astro Indicators/planetcycles.mq5', 'folder': 'Astro Indicators', 'inputs': [{'mql': 'Geocentric', 'py': 'Geocentric', 'param': 'Geocentric', 'type': 'bool', 'default': True, 'label': 'geocentric view', 'sinput': False}, {'mql': 'fastPlanet', 'py': 'fastPlanet', 'param': 'fastPlanet', 'type': 'int', 'default': 1, 'label': 'planet fast', 'sinput': False}, {'mql': 'slowPlanet', 'py': 'slowPlanet', 'param': 'slowPlanet', 'type': 'int', 'default': 0, 'label': 'planet slow', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': ['swedll32.dll'], 'libraries': []}

# enum BODY
Sun = 0
Moon = 1
Mercury = 2
Venus = 3
Mars = 4
Jupiter = 5
Saturn = 6
Uranus = 7
Neptune = 8
Pluto = 9
Mean_Node = 10
True_Node = 11
Mean_Apog = 12
Oscu_Apog = 13
Earth = 14
Chiron = 15
Pholus = 16
Ceres = 17
Pallas = 18
Juno = 19
Vesta = 20
_enum('BODY', {0: 'Sun', 1: 'Moon', 2: 'Mercury', 3: 'Venus', 4: 'Mars', 5: 'Jupiter', 6: 'Saturn', 7: 'Uranus', 8: 'Neptune', 9: 'Pluto', 10: 'Mean_Node', 11: 'True_Node', 12: 'Mean_Apog', 13: 'Oscu_Apog', 14: 'Earth', 15: 'Chiron', 16: 'Pholus', 17: 'Ceres', 18: 'Pallas', 19: 'Juno', 20: 'Vesta'})

# ---- inputs and global variables
Geocentric = _input('Geocentric', True)  # geocentric view
fastPlanet = _input('fastPlanet', Moon)  # planet fast
slowPlanet = _input('slowPlanet', Sun)  # planet slow
CycleBuffer = Arr(0, 0.0)
flag = 0

def swe_version(*args):
    raise NotImplementedError('DLL/library function swe_version from swedll32.dll')

def swe_julday(*args):
    raise NotImplementedError('DLL/library function swe_julday from swedll32.dll')

def swe_calc(*args):
    raise NotImplementedError('DLL/library function swe_calc from swedll32.dll')

def swe_calc_ut(*args):
    raise NotImplementedError('DLL/library function swe_calc_ut from swedll32.dll')

def swe_set_topo(*args):
    raise NotImplementedError('DLL/library function swe_set_topo from swedll32.dll')

def swe_get_planet_name(*args):
    raise NotImplementedError('DLL/library function swe_get_planet_name from swedll32.dll')

def swe_utc_time_zone(*args):
    raise NotImplementedError('DLL/library function swe_utc_time_zone from swedll32.dll')

def swe_utc_to_jd(*args):
    raise NotImplementedError('DLL/library function swe_utc_to_jd from swedll32.dll')

def swe_close(*args):
    raise NotImplementedError('DLL/library function swe_close from swedll32.dll')

def calculate_1(dt, ipl, data, iflag=0):
    rv = 0
    julday = 0.0
    ds = MqlDateTime()
    TimeToStruct(dt, ds)
    julday = swe_julday(ds.year, ds.mon, ds.day, ds.hour + (((ds.min * 60) + ds.sec) / 3600.0), 1)
    iflag |= 4 | 256
    rv = swe_calc_ut(julday, ipl, iflag, data, _s_calculate_err)
    if rv < 0:
        Print('SWISSEPH.calulate Error "' + CharArrayToString(_s_calculate_err) + '"')
        return False
    return rv == iflag

def calculate_2(year, month, day, hour, minute, timezone, ipl, data, iflag=0):
    y = Box(0)
    mon = Box(0)
    d = Box(0)
    h = Box(0)
    min_ = Box(0)
    rv = 0
    sec = Box(0.0)
    dret = Arr(2, 0.0, dyn=False)
    swe_utc_time_zone(year, month, day, hour, minute, 0.0, timezone, y, mon, d, h, min_, sec)
    swe_utc_to_jd(y.v, mon.v, d.v, h.v, min_.v, sec.v, 1, dret, _s_calculate_err_)
    iflag |= 4 | 256
    rv = swe_calc_ut(dret[0], ipl, iflag, data, _s_calculate_err_)
    if rv < 0:
        Print('SWISSEPH.calulate Error "' + CharArrayToString(_s_calculate_err_) + '"')
        return False
    return rv == iflag

def OnInit():
    global flag
    SetIndexBuffer(0, CycleBuffer, INDICATOR_DATA)
    flag = 0
    if not Geocentric:
        flag = 8
    return 0

def OnDeinit(reason):
    swe_close()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    a = Arr(6, 0.0, dyn=False)
    b = Arr(6, 0.0, dyn=False)
    for i in range(prev_calculated, rates_total):
        calculate_1(time[i], fastPlanet, a, flag)
        calculate_1(time[i], slowPlanet, b, flag)
        if (Geocentric and ((slowPlanet == 0 or slowPlanet == 2) or slowPlanet == 3)) and ((fastPlanet == 0 or fastPlanet == 2) or fastPlanet == 3):
            CycleBuffer[i] = a[0] - b[0]
            while CycleBuffer[i] > 180:
                CycleBuffer[i] -= 180
            while CycleBuffer[i] < -180:
                CycleBuffer[i] += 180
            if i > 0 and (CycleBuffer[i] - CycleBuffer[i - 1]) < -100:
                CycleBuffer[i] += 180
            if i > 0 and (CycleBuffer[i] - CycleBuffer[i - 1]) > 100:
                CycleBuffer[i] -= 180
        else:
            CycleBuffer[i] = a[0] - b[0]
            if CycleBuffer[i] > 360:
                CycleBuffer[i] -= 360
            if CycleBuffer[i] < -360:
                CycleBuffer[i] += 360
            if CycleBuffer[i] > 180:
                CycleBuffer[i] = 360 - CycleBuffer[i]
            if CycleBuffer[i] < -180:
                CycleBuffer[i] = 360 + CycleBuffer[i]
            CycleBuffer[i] = MathAbs(CycleBuffer[i])
    return rates_total

# ---- static local variables
_s_calculate_err = Arr(256, 0, dyn=False)
_s_calculate_err_ = Arr(256, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Planetcycles(_MQL5Indicator):
    name = 'planetcycles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Geocentric': True,  # geocentric view
        'fastPlanet': _Choice({0: 'Sun', 1: 'Moon', 2: 'Mercury', 3: 'Venus', 4: 'Mars', 5: 'Jupiter', 6: 'Saturn', 7: 'Uranus', 8: 'Neptune', 9: 'Pluto', 10: 'Mean_Node', 11: 'True_Node', 12: 'Mean_Apog', 13: 'Oscu_Apog', 14: 'Earth', 15: 'Chiron', 16: 'Pholus', 17: 'Ceres', 18: 'Pallas', 19: 'Juno', 20: 'Vesta'}, default=1),  # planet fast
        'slowPlanet': _Choice({0: 'Sun', 1: 'Moon', 2: 'Mercury', 3: 'Venus', 4: 'Mars', 5: 'Jupiter', 6: 'Saturn', 7: 'Uranus', 8: 'Neptune', 9: 'Pluto', 10: 'Mean_Node', 11: 'True_Node', 12: 'Mean_Apog', 13: 'Oscu_Apog', 14: 'Earth', 15: 'Chiron', 16: 'Pholus', 17: 'Ceres', 18: 'Pallas', 19: 'Juno', 20: 'Vesta'}, default=0),  # planet slow
    }

