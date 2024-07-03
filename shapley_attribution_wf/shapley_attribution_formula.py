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
    """
    给定指标公式后计算因子的shapley value
    """

    def __init__(self, data_before: list, data_after: list, func):
        """
        :param data_before: 前一时间段的因子取值列表
        :param data_after: 后一时间段的因子取值列表
        :param func: 指标表达式
        """
        assert len(data_before) == len(data_after)
        self.data_before = np.array(data_before.copy())
        self.data_after = np.array(data_after.copy())
        # 因子编号
        self.factors = list(range(len(data_before)))
        self.func = func
        # 枚举因子组合
        self.combinations = list(self.powerset(self.factors))

    def powerset(self, factors: list):
        """
        枚举组合samples
        :param factors: 所有因子编号
        :return: 组合samples
        """
        assert type(factors) == list
        return chain.from_iterable(combinations(factors, r) for r in range(len(factors) + 1))

    def _phi(self, factor_index):
        """
        单因子shapley value计算
        :param factor_index: 因子编号
        :return: 单因子shapley value
        """
        # 获取包含给定因子的组合samples
        s_combination = [k for k in self.combinations if factor_index in k]
        score = 0
        print(f"Computing phi for factor {factor_index}...")
        for s in tqdm(s_combination):
            v_before = self.data_before.copy()
            v_after = self.data_before.copy()
            v_before[list(set(s) - set([factor_index]))] = self.data_after[list(set(s) - set([factor_index]))]
            v_after[list(s)] = self.data_after[list(s)]
            # shapley value计算原始公式
            score += math.factorial(len(s) - 1) * math.factorial(len(self.factors) - len(s)) \
                / math.factorial(len(self.factors)) * (self.func(*v_after) - self.func(*v_before))
        print(f"Attribution score for foctor {factor_index}: {score:.2f}")
        print()
        return score

    def attribute(self):
        """
        :return:所有因子shapley value计算
        """
        print("Running Simplified Shapley Attribution Model...")
        print(f"Found {len(self.factors)} unique factors!")
        print("Computing combinations...")

        result = dict()
        for i in self.factors:
            result[i] = self._phi(i)
        print(f"Computing attributions...")
        print()
        return result

