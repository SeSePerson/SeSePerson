#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import seseperson

seseperson.init()
app = seseperson.asgi()

if __name__ == "__main__":
    seseperson.run()
