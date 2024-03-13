# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: setup.py
# @AUthor: Fei Wu
# @Time: 3月, 13, 2024


import setuptools


with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="shapley_attribution_wf",
  version="0.0.1",
  author="wufeipku",
  author_email="wufei.pku@163.com",
  description="package for calulating attrbution with shapley method",
  long_description_content_type="text/markdown",
  url="https://github.com/wufeipku/shapley_attribution.git",
  packages=setuptools.find_packages(),
  install_requires=['tqdm>=4.66.2', 'numpy>=1.26.4', 'frechetdist>=0.6', 'scikit_learn>=0.23.2'],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
