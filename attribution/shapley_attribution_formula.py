# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: shapley_attribution_formula.py
# @AUthor: Fei Wu
# @Time: 3月, 01, 2024


from itertools import chain, combinations
import math
import numpy as np
import pandas as pd
from tqdm import tqdm


class ShapleyAttributionModelFormula:
    '''
    shapley attribution for pre-set formulas
    :param data_before: list data for comparent pre-time
    :param data_after: list data for comparent after-time
    '''

    def __init__(self, data_before: list(), data_after: list(), func):
        '''
        :param data_before: list data for comparent pre-time
        :param data_after: list data for comparent after-time
        '''
        assert len(data_before) == len(data_after)
        self.data_before = np.array(data_before.copy())
        self.data_after = np.array(data_after.copy())
        self.factors = set(range(len(data_before)))
        self.func = func
        # 枚举组合
        self.journeys = list(self.powerset(self.factors))

    def powerset(self, x):
        '''
        :param x: channel indexs
        :return: combination samples
        '''
        s = list(x)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def _phi(self, channel_index):
        '''
        :param channel_index: factor number
        :return: shapley values for a factor
        '''
        s_combination = [k for k in self.journeys if channel_index in k]
        score = 0
        print(f"Computing phi for factor {channel_index}...")
        for s in tqdm(s_combination):
            v_before = self.data_before.copy()
            v_after = self.data_before.copy()
            v_before[list(set(s) - set([channel_index]))] = self.data_after[list(set(s) - set([channel_index]))]
            v_after[list(s)] = self.data_after[list(s)]
            score += math.factorial(len(s) - 1) * math.factorial(len(self.factors) - len(s)) \
                     / math.factorial(len(self.factors)) * (self.func(*v_after) - self.func(*v_before))
        print(f"Attribution score for foctor {channel_index}: {score:.2f}")
        print()
        return score

    def attribute(self):
        print("Running Simplified Shapley Attribution Model...")
        print(f"Found {len(self.factors)} unique factors!")
        print("Computing combinations...")

        result = dict()
        for i in self.factors:
            result[i] = self._phi(i)
        print(f"Computing attributions...")
        print()
        return result

