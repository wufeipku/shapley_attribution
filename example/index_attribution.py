# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: index_attribution.py
# @AUthor: Fei Wu
# @Time: 3月, 13, 2024


import pandas as pd
from attribution.shapley_attribution_formula import ShapleyAttributionModelFormula


def func(dau, avg_vv, live_load, cont_load, ad_load, live_ctrcvr, cont_ctrcvr,
         live_aov, cont_aov, ecpm, live_retain_rate, cont_retain_rate,
         live_take_rate, cont_take_rate):
    """
    define target function
    内容电商
    revenue = dau * 人均日均vv * 电商load * (ctr * cvr) * aov * retain_rate * take_rate
    广告
    revenue = dau * 人均日均vv * ad_load * ecpm
    货架电商
    revenue = dau * (ctr * cvr) * order_count * aov * retain_rate * take_rate

    load:流量分配
    ctr*cvr：流量转化率
    aov：客单价
    retain_rate：收货率、成单率
    take_rate:抽成比例
    ecpm：千次广告收费
    """
    return dau * avg_vv * live_load * live_ctrcvr * live_aov * live_retain_rate * live_take_rate \
           + dau * avg_vv * cont_load * cont_ctrcvr * cont_aov * cont_retain_rate * cont_take_rate \
           + dau * avg_vv * ad_load * ecpm / 1000


l1 = [6e8, 440, 0.07, 0.03, 0.1, 0.002, 0.0009, 100, 80, 25, 0.7, 0.8, 0.11, 0.09]
l2 = [6.2e8, 430, 0.08, 0.03, 0.09, 0.0023, 0.0009, 95, 80, 28, 0.68, 0.8, 0.1, 0.1]
model = ShapleyAttributionModelFormula(l1, l2, func)
result = model.attribute()
total_diff = func(*l2) - func(*l1)
attribute = pd.DataFrame(index=['dau', 'avg_vv', 'live_load', 'cont_load', 'ad_load', 'live_ctrcvr', 'cont_ctrcvr',
                                'live_aov', 'cont_aov', 'ecpm', 'live_retain_rate', 'cont_retain_rate',
                                'live_take_rate', 'cont_take_rate'],
                         columns=['贡献值'], data=list(result.values())
                         )
attribute['贡献度'] = attribute['贡献值'] / total_diff
attribute['因子before'] = l1
attribute['因子after'] = l2
attribute['因子变化率'] = attribute['因子after'] / attribute['因子before'] - 1
print('总变化', total_diff)
print('贡献', attribute)
print('总贡献', attribute['贡献值'].sum())
