"""HashMapTemplate.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class HashMapTemplate(MqlObject):
    _q_fields = ('keys', 'values', 'count', 'emptyKey', 'emptyValue')
    def _q_ctor1(self):
        self.keys = Arr(0, None)
        self.values = Arr(0, None)
        self.count = 0
        self.emptyKey = 0
        self.emptyValue = 0
        self.count = 0
        self.emptyKey = K(None)
        self.emptyValue = V(EMPTY_VALUE)
    def _q_ctor2(self, nokey, empty):
        self.keys = Arr(0, None)
        self.values = Arr(0, None)
        self.count = 0
        self.emptyKey = 0
        self.emptyValue = 0
        self.count = 0
        self.emptyKey = K(nokey)
        self.emptyValue = V(empty)
    def __init__(self, *args):
        if 0 <= len(args) <= 0:
            self._q_ctor1(*args)
            return
        if 2 <= len(args) <= 2:
            self._q_ctor2(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        self.reset()
    def add(self, key, value):
        ArrayResize(self.keys, self.count + 1)
        ArrayResize(self.values, self.count + 1)
        _assign(self.keys[self.count], key)
        _assign(self.values[self.count], value)
        self.count += 1
    def reset(self):
        ArrayResize(self.keys, 0)
        ArrayResize(self.values, 0)
        self.count = 0
    def getIndex(self, key):
        for i in range(0, self.count):
            if self.keys[i] == key:
                return i
        return -1
    def getKey(self, index):
        if index < 0 or index >= self.count:
            Print('HashMapTemplate::getKey', ': index out of bounds = ', index)
            return None
        return self.keys[index]
    def __getitem__(self, index):
        if index < 0 or index >= self.count:
            Print('HashMapTemplate::operator[]', ': index out of bounds = ', index)
            return self.emptyValue
        return self.values[index]
    def __getitem__(self, key):
        for i in range(0, self.count):
            if self.keys[i] == key:
                return self.values[i]
        Print('HashMapTemplate::operator[]', ': no key=', key)
        return self.emptyValue
    def set(self, key, value):
        index = self.getIndex(key)
        if index != -1:
            _assign(self.values[index], value)
        else:
            self.add(key, value)
    def inc(self, key, value):
        index = self.getIndex(key)
        if index != -1:
            self.values[index] += value
        else:
            self.add(key, value)
    def remove(self, key):
        index = self.getIndex(key)
        if index != -1:
            _assign(self.keys[index], self.emptyKey)
            _assign(self.values[index], self.emptyValue)
    def purge(self):
        write = 0
        i = 0
        while i < self.count:
            while i < self.count and self.keys[i] == self.emptyKey:
                i += 1
            while i < self.count and self.keys[i] != self.emptyKey:
                if write < i:
                    _assign(self.values[write], self.values[i])
                    _assign(self.keys[write], self.keys[i])
                i += 1
                write += 1
        self.count = write
        ArrayResize(self.keys, self.count)
        ArrayResize(self.values, self.count)
    def getSize(self):
        return self.count

__all__ = ['HashMapTemplate']
