# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: shapley_attribution_ads.py
# @AUthor: Fei Wu
# @Time: 3月, 01, 2024


from collections import Counter
from itertools import chain, combinations
from tqdm import tqdm


class SimplifiedShapleyAttributionModel:
    """
    实现类似广告投放场景的渠道效用shapley归因计算.
    """
    def __init__(self, journeys: [list[list]]):
        """
        :param journeys: 用户访问渠道记录，每个子列表代表一个用户访问的所有渠道。
        """
        # 从用户访问记录中获取所有渠道编号
        self.channels = set(chain(*journeys))
        # 统计每种访问渠道组合数量
        self.journeys = Counter([frozenset(journey) for journey in journeys])

    def _phi(self, channel_index: int):
        """
        功能：实现单个shapley value计算
        :param channel_index: 渠道的编号
        :return: 对应渠道的shapley value
        """
        # 获取所有包含渠道channel_index的访问记录
        s_channel = [k for k in self.journeys.keys() if channel_index in k]
        # 使用简化的shapley公式计算
        score = 0
        for S in tqdm(s_channel):
            score += self.journeys[S] / len(S)
        return score

    def attribute(self):
        """
        :return: 返回所有渠道shapley value值
        """
        print("Running Simplified Shapley Attribution Model...")
        print(f"Found {len(self.channels)} unique channels!")
        print("Computing journey statistics...")
        print(f"Computing attributions...")
        print()
        return {j: self._phi(j) for j in self.channels}


class OrderedShapleyAttributionModel:
    """
    考虑有序情况的广告渠道shapley value计算
    """
    def __init__(self, journeys: list[list]):
        """
        :param journeys: 用户访问渠道记录，每个子列表代表一个用户访问的所有渠道
        """
        self.channels = set(chain(*journeys))
        # 得到所有渠道组合
        self.p_power = list(self.powerset(self.channels))
        self.journeys = journeys
        # 获取用户最多访问的渠道个数
        self.N = max([len(journey) for journey in self.journeys])
        # 对访问不同渠道个数的用户进行归类，存成字典，key代表访问不同渠道的个数，value存储对应的所有访问渠道记录的列表，每个元素对应一个用户
        self.indexed_journeys = {
            i: [(s, set(s)) for s in self.journeys if len(set(s)) == i]
            for i in range(1, len(self.channels) + 1)
        }

    def powerset(self, channel_index: int):
        """
        :param channel_index: 渠道号
        :return: 所有组合samples
        """
        s = list(channel_index)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def _r(self, channels_combination: set, channel_index: int, touchpoint_index: int):
        """
        根据给定的渠道组合、渠道号、访问次序，计算均分后的访问效用
        :param channels_combination: 一种渠道组合
        :param channel_index: 渠道号
        :param touchpoint_index: 渠道次序
        :return: 某个渠道组合、渠道号、访问次数的访问效用值
        """
        return sum(
            [
                # 同一个渠道出现在一个用户访问记录中的多个位置，采用均分方式计算
                1 / journey.count(channel_index)
                if (
                    # 找到channels_combination对应的访问记录
                    (channels_combination == journey_set)
                    # 找到渠道号对应的访问次序，即touchpoint_index
                    and (journey[touchpoint_index - 1] == channel_index)
                )
                else 0
                for journey, journey_set in self.indexed_journeys[len(channels_combination)]
                if touchpoint_index <= len(journey)
            ]
        )

    def _phi(self, channel_index: int, touchpoint_index: int):
        """
        给定渠道号、访问次序，计算shapley value
        :param channel_index: 渠道号
        :param touchpoint_index: 访问次序
        :return:shapley value
        """
        # 获取包含channel_index渠道的所有组合samples
        s_all = [set(S) for S in self.p_power if channel_index in S]
        score = 0
        print(
            f"Computing phi for channel {channel_index}, touchpoint {touchpoint_index}..."
        )
        # 计算shapley value
        for S in tqdm(s_all):
            score += self._r(S, channel_index, touchpoint_index) / len(S)
        print(
            f"Attribution score for channel {channel_index}, touchpoint {touchpoint_index}: {score:.2f}"
        )
        print()
        return score

    def attribute(self):
        """
        计算所有渠道shapley value
        """
        print("Running Ordered Shapley Attribution Model...")
        print(f"Found {len(self.channels)} unique channels!")
        print(f"Found {self.N} maximum touchpoints!")
        print(f"Proceeding to shapley_attribution_wf computation...")
        print()
        return {j: [self._phi(j, i) for i in range(1, self.N + 1)] for j in self.channels}


