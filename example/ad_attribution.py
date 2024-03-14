# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: ad_attribution.py
# @AUthor: Fei Wu
# @Time: 3月, 13, 2024
import json
from shapley_attribution_wf.shapley_attribution_ads import SimplifiedShapleyAttributionModel


with open("../data/sample.json", "r") as f:
    journeys = json.load(f)
# chopse one model from (SimplifiedShapleyAttributionModel, OrderedShapleyAttributionModel)
model = SimplifiedShapleyAttributionModel(journeys)
result = model.attribute()
print(result)
