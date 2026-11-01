"""Enum.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


def TFMigrate(tf):
    _sw1 = tf
    if _sw1 == 0:
        return PERIOD_CURRENT
    elif _sw1 == 1:
        return PERIOD_M1
    elif _sw1 == 5:
        return PERIOD_M5
    elif _sw1 == 15:
        return PERIOD_M15
    elif _sw1 == 30:
        return PERIOD_M30
    elif _sw1 == 60:
        return PERIOD_H1
    elif _sw1 == 240:
        return PERIOD_H4
    elif _sw1 == 1440:
        return PERIOD_D1
    elif _sw1 == 10080:
        return PERIOD_W1
    elif _sw1 == 43200:
        return PERIOD_MN1
    elif _sw1 == 2:
        return PERIOD_M2
    elif _sw1 == 3:
        return PERIOD_M3
    elif _sw1 == 4:
        return PERIOD_M4
    elif _sw1 == 6:
        return PERIOD_M6
    elif _sw1 == 10:
        return PERIOD_M10
    elif _sw1 == 12:
        return PERIOD_M12
    elif _sw1 == 16385:
        return PERIOD_H1
    elif _sw1 == 16386:
        return PERIOD_H2
    elif _sw1 == 16387:
        return PERIOD_H3
    elif _sw1 == 16388:
        return PERIOD_H4
    elif _sw1 == 16390:
        return PERIOD_H6
    elif _sw1 == 16392:
        return PERIOD_H8
    elif _sw1 == 16396:
        return PERIOD_H12
    elif _sw1 == 16408:
        return PERIOD_D1
    elif _sw1 == 32769:
        return PERIOD_W1
    elif _sw1 == 49153:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

__all__ = ['TFMigrate']
