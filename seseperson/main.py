#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from pathlib import Path

import nonebot

from .configs import Config

__conf_path = Path("..") / "configs.yml"
__conf = Config(__conf_path)


def init():
    nonebot.init(**__conf.get_runtime_conf())
