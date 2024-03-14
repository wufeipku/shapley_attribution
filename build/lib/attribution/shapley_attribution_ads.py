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
    simplyfied shapley shapley_attribution_wf method for ads.
    R(S) is used to replace original shapley formular.
    """
    def __init__(self, journeys):
        self.channels = set(chain(*journeys))
        self.journeys = Counter([frozenset(journey) for journey in journeys])

    def _phi(self, channel_index):
        """
        :param channel_index: channel number
        :return: shapley_attribution_wf
        """
        s_channel = [k for k in self.journeys.keys() if channel_index in k]
        score = 0
        print(f"Computing phi for channel {channel_index}...")
        for S in tqdm(s_channel):
            score += self.journeys[S] / len(S)
        print(f"Attribution score for channel {channel_index}: {score:.2f}")
        print()
        return score

    def attribute(self):
        print("Running Simplified Shapley Attribution Model...")
        print(f"Found {len(self.channels)} unique channels!")
        print("Computing journey statistics...")
        print(f"Computing attributions...")
        print()
        return {j: self._phi(j) for j in self.channels}


class OrderedShapleyAttributionModel:
    """
    ordered shapley shapley_attribution_wf method
    """
    def __init__(self, journeys: list[list]):
        """
        :param journeys: visited channels for every user
        """
        self.channels = set(chain(*journeys))
        self.p_power = list(self.powerset(self.channels))
        self.journeys = journeys
        self.N = max([len(journey) for journey in self.journeys])  # get the max number of visiting channels by one user
        self.indexed_journeys = {
            i: [(s, set(s)) for s in self.journeys if len(set(s)) == i]
            for i in range(1, len(self.channels) + 1)
        }
    def powerset(self, x):
        """
        :param x: channel indexs
        :return: combination samples
        """
        s = list(x)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def _r(self, s, channel_index, touchpoint_index):
        """
        calculate the shapley value given a set s and a fixed channel and a fixed order number
        :param s: one subset of total channels
        :param channel_index: channnel index
        :param touchpoint_index: the channel order in any channels set
        :return: shapley value given a set s and a fixed channel and a fixed order number
        """
        return sum(
            [
                1 / journey.count(channel_index)  # if one channel appears in multiple touchpoints, evenly distirbute
                if (
                    (s == journey_set)
                    and (journey[touchpoint_index - 1] == channel_index)
                )
                else 0
                for journey, journey_set in self.indexed_journeys[len(s)]
                if touchpoint_index <= len(journey)
            ]
        )

    def _phi(self, channel_index, touchpoint_index):
        """
        calculate shapley_attribution_wf for one channel and one order
        :param channel_index: the select channel number
        :param touchpoint_index: the order number of this channel
        :return:
        """
        s_all = [set(S) for S in self.p_power if channel_index in S]
        score = 0
        print(
            f"Computing phi for channel {channel_index}, touchpoint {touchpoint_index}..."
        )
        for S in tqdm(s_all):
            score += self._r(S, channel_index, touchpoint_index) / len(S)
        print(
            f"Attribution score for channel {channel_index}, touchpoint {touchpoint_index}: {score:.2f}"
        )
        print()
        return score

    def attribute(self):
        """
        calculate all channels's shapley_attribution_wf
        """
        print("Running Ordered Shapley Attribution Model...")
        print(f"Found {len(self.channels)} unique channels!")
        print(f"Found {self.N} maximum touchpoints!")
        print(f"Proceeding to shapley_attribution_wf computation...")
        print()
        return {j: [self._phi(j, i) for i in range(1, self.N + 1)] for j in self.channels}


