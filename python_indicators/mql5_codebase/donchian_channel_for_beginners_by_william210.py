"""Donchian Channel for beginners by William210 — converted from MQL5: MQL5 Indicators/Donchian Channel for beginners by William210/Donchian Channel for beginners by William210.mq5

Donchian Channel beginner tutorial to learn
If this code malfunctions for whatever reasons, forgetting or MQL5 upgrades\\nlet me know so I can correct it, thank you\\n
May this code help you\\n
You can find all my indicator codes in CodeBase or the Marketplace, free or purchasable, by searching for William210
Copyright: Copyright 2023, GwDs; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, GwDs', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421504], 2: [32768], 3: [255]}, 'widths': {3: 1, 2: 1}, 'styles': {1: 2, 2: 0, 3: 0}, 'labels': {1: 'Donchian Middle', 2: 'Donchian upper', 3: 'Donchian Lower'}, 'levels': [], 'description': ['Donchian Channel beginner tutorial to learn', 'If this code malfunctions for whatever reasons, forgetting or MQL5 upgrades\\nlet me know so I can correct it, thank you\\n', 'May this code help you\\n', 'You can find all my indicator codes in CodeBase or the Marketplace, free or purchasable, by searching for William210'], 'name': 'Donchian Channel for beginners by William210', 'source': 'MQL5 Indicators/Donchian Channel for beginners by William210/Donchian Channel for beginners by William210.mq5', 'folder': 'Donchian Channel for beginners by William210', 'inputs': [{'mql': 'g_DonPeriod', 'py': 'g_DonPeriod', 'param': 'g_DonPeriod', 'type': 'uchar', 'default': 21, 'label': 'Period for Donchian Channel', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_DonPeriod = _input('g_DonPeriod', 21)  # Period for Donchian Channel
g_BuffDonchianMD = Arr(0, 0.0)  # Middle band
g_BuffDonchianUP = Arr(0, 0.0)  # Upper band
g_BuffDonchianDW = Arr(0, 0.0)  # lower band

def OnInit():
    Comment("My apologies, this code is no longer available and I don't know how to remove/hide it from codebase")
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianChannelForBeginnersByWilliam210(_MQL5Indicator):
    name = 'Donchian Channel for beginners by William210'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_DonPeriod': 21,  # Period for Donchian Channel
    }

