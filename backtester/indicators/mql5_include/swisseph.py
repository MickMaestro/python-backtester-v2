"""``swisseph.mqh`` (J.S., 2012) — the Swiss Ephemeris wrapper behind the
astro indicators (Astro Indicators, planetary cycles…).

The MQL5 include ``#import``s ``swedll32.dll`` (the Swiss Ephemeris C
library). The Python equivalent is the **pyswisseph** package
(``pip install pyswisseph``; ships Windows wheels), which wraps the same C
library — so positions are identical. This module keeps the include's
constants, the ``BODY`` enum and its two ``calculate()`` helpers, and maps the
``swe_*`` imports onto pyswisseph. Without the package installed the
functions raise :class:`ImportError` with that install hint, which is the
offline analogue of MT5 failing to load the DLL.

``calculate`` returns ``(ok, data)`` — ``data`` is the 6 values
``[longitude, latitude, distance, speed_long, speed_lat, speed_dist]`` that
the MQL5 version writes into its ``double &data[]``; ``ok`` is the source's
``rv == iflag`` check (the requested flags were honoured).
"""

from __future__ import annotations

from . import terminal as T

# enum BODY
(Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto,
 Mean_Node, True_Node, Mean_Apog, Oscu_Apog, Earth,
 Chiron, Pholus, Ceres, Pallas, Juno, Vesta) = range(21)

SE_JUL_CAL = 0
SE_GREG_CAL = 1
SE_ECL_NUT = -1
SE_SUN = 0
SE_MOON = 1
SE_MERCURY = 2
SE_VENUS = 3
SE_MARS = 4
SE_JUPITER = 5
SE_SATURN = 6
SE_URANUS = 7
SE_NEPTUNE = 8
SE_PLUTO = 9
SE_MEAN_NODE = 10
SE_TRUE_NODE = 11
SE_MEAN_APOG = 12
SE_OSCU_APOG = 13
SE_EARTH = 14
SE_CHIRON = 15
SE_PHOLUS = 16
SE_CERES = 17
SE_PALLAS = 18
SE_JUNO = 19
SE_VESTA = 20
SE_INTP_APOG = 21
SE_INTP_PERG = 22
SE_NPLANETS = 23
SE_FICT_OFFSET = 40
SE_NFICT_ELEM = 15
SE_CUPIDO = 40
SE_HADES = 41
SE_ZEUS = 42
SE_KRONOS = 43
SE_APOLLON = 44
SE_ADMETOS = 45
SE_VULKANUS = 46
SE_POSEIDON = 47
SE_ISIS = 48
SE_NIBIRU = 49
SE_HARRINGTON = 50
SE_NEPTUNE_LEVERRIER = 51
SE_NEPTUNE_ADAMS = 52
SE_PLUTO_LOWELL = 53
SE_PLUTO_PICKERING = 54
SE_AST_OFFSET = 10000
SEFLG_JPLEPH = 1
SEFLG_SWIEPH = 2
SEFLG_MOSEPH = 4
SEFLG_HELCTR = 8
SEFLG_TRUEPOS = 16
SEFLG_J2000 = 32
SEFLG_NONUT = 64
SEFLG_SPEED3 = 128
SEFLG_SPEED = 256
SEFLG_NOGDEFL = 512
SEFLG_NOABERR = 1024
SEFLG_EQUATORIAL = 2048
SEFLG_XYZ = 4096
SEFLG_RADIANS = 8192
SEFLG_BARYCTR = 16384
SEFLG_TOPOCTR = (32*1024)
SEFLG_SIDEREAL = (64*1024)
SEFLG_ICRS = (128*1024)


def _swe():
    try:
        import swisseph as swe          # pyswisseph
    except ImportError as exc:          # pragma: no cover - depends on the machine
        raise ImportError("The Swiss Ephemeris functions need the pyswisseph package: "
                          "pip install pyswisseph") from exc
    return swe


def swe_version() -> str:
    return _swe().version


def swe_julday(year, month, day, hour, gregflag=SE_GREG_CAL) -> float:
    return _swe().julday(int(year), int(month), int(day), float(hour), int(gregflag))


def swe_calc(tjd_et, ipl, iflag):
    """→ ``(retflag, xx)``; ``retflag < 0`` on error, as in C."""
    swe = _swe()
    try:
        xx, ret = swe.calc(tjd_et, int(ipl), int(iflag))
        return ret, list(xx)
    except swe.Error:
        return -1, [0.0] * 6


def swe_calc_ut(tjd_ut, ipl, iflag):
    """→ ``(retflag, xx)``; ``retflag < 0`` on error, as in C."""
    swe = _swe()
    try:
        xx, ret = swe.calc_ut(tjd_ut, int(ipl), int(iflag))
        return ret, list(xx)
    except swe.Error:
        return -1, [0.0] * 6


def swe_set_topo(geolon, geolat, altitude) -> None:
    _swe().set_topo(geolon, geolat, altitude)


def swe_get_planet_name(ipl) -> str:
    return _swe().get_planet_name(int(ipl))


def swe_utc_time_zone(iyear, imonth, iday, ihour, imin, dsec, d_timezone):
    return tuple(_swe().utc_time_zone(int(iyear), int(imonth), int(iday), int(ihour),
                                      int(imin), float(dsec), float(d_timezone)))


def swe_utc_to_jd(iyear, imonth, iday, ihour, imin, dsec, gregflag=SE_GREG_CAL):
    """→ ``[jd_et, jd_ut]`` (the source's ``dret``)."""
    return list(_swe().utc_to_jd(int(iyear), int(imonth), int(iday), int(ihour), int(imin),
                                 float(dsec), int(gregflag)))


def swe_close() -> None:
    _swe().close()


def calculate(dt=None, ipl=Sun, iflag=0, *, year=None, month=None, day=None, hour=None,
              minute=None, timezone=None):
    """Both overloads of the include's ``calculate``:

    - ``calculate(dt, ipl, iflag=0)`` with an MQL5 ``datetime`` (seconds);
    - ``calculate(year=…, month=…, day=…, hour=…, minute=…, timezone=…, ipl=…)``
      for a local time with a UTC offset in hours.
    """
    iflag |= SEFLG_MOSEPH | SEFLG_SPEED
    if year is None:
        ds = T.TimeToStruct(int(dt))
        julday = swe_julday(ds.year, ds.mon, ds.day,
                            ds.hour + (ds.min * 60 + ds.sec) / 3600.0, SE_GREG_CAL)
    else:
        y, mon, d, h, mi, sec = swe_utc_time_zone(year, month, day, hour, minute, 0, timezone)
        julday = swe_utc_to_jd(y, mon, d, h, mi, sec, SE_GREG_CAL)[1]
    rv, data = swe_calc_ut(julday, ipl, iflag)
    if rv < 0:
        return False, data
    return rv == iflag, data
