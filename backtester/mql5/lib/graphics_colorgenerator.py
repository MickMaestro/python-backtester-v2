"""ColorGenerator.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CColorGenerator(MqlObject):
    _q_fields = ('m_index', 'm_generate', 'm_current_palette')
    s_default_palette = None
    def __init__(self):
        self.m_index = 0
        self.m_generate = False
        self.m_current_palette = Arr(20, 0, dyn=False)
        self.m_index = 0
        self.m_generate = False
        ArrayCopy(self.m_current_palette, CColorGenerator.s_default_palette)
    def _q_dtor(self):
        pass
    def Next(self):
        if self.m_index == 20:
            self.m_index = 0
            if not self.m_generate:
                self.m_generate = True
        if self.m_generate:
            self.m_current_palette[self.m_index] = ((self.m_current_palette[self.m_index] ^ self.m_current_palette[0]) if (self.m_index == 19) else (self.m_current_palette[self.m_index] ^ self.m_current_palette[self.m_index + 1]))
        return self.m_current_palette[_incattr(self, 'm_index', 1, True)]
    def Reset(self):
        self.m_index = 0
        self.m_generate = False
        ArrayCopy(self.m_current_palette, CColorGenerator.s_default_palette)
CColorGenerator.s_default_palette = Arr.of([0x3366CC, 0xDC3912, 0xFF9900, 0x109618, 0x990099, 0x3B3EAC, 0x0099C6, 0xDD4477, 0x66AA00, 0xB82E2E, 0x316395, 0x994499, 0x22AA99, 0xAAAA11, 0x6633CC, 0xE67300, 0x8B0707, 0x329262, 0x5574A6, 0x3B3EAC], fill=0, dyn=False, size=20)

__all__ = ['CColorGenerator']
