#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2018 Ulric Yang <yangrui@posbao.net>
#
#  This program is free software: you can redistribute it and-or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation: either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY: without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program: if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                    O* = *O
#                ____*'---'*____
#              .   ' **| |** '.
#               * **||| : |||** *
#             * _||||| -:- |||||- *
#               | | *** - *** | |
#             | *_| ''*---*'' | |
#              * .-*__ '-' ___*-. *
#           ___'. .' *--.--* '. . __
#        ."" '< '.___*_<|>_*___.' >'"".
#       | | : '- *'.:'* _ *':.'* - ' : | |
#         * * '-. *_ __* *__ _* .-' * *
# ======'-.____'-.___*_____*___.-'____.-'======
#                    '=---='
# .............................................

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# PURPOSE:
#
#
# USAGE:
#
#
# CAUTION:
#
#
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LIBRARY
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

import copy
import datetime
import logging
import os
import random
import sys
import time

try:
    from beeprint import pp as ppt
except Exception as e:
    try:
        from prettyprinter import cpprint as ppt
    except Exception as e:
        from pprint import pprint as ppt


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# CONSTANT
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOGGER
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logfilename = os.path.splitext(__file__)[0] + str(
    "".join([str(t).zfill(2) for t in datetime.datetime.now().timetuple()[0:6]])
)
logger = logging.getLogger(logfilename + ".log")
fhandler = logging.FileHandler(logfilename + ".log")
shandler = logging.StreamHandler()
fmt = " - ".join(
    ["%(asctime)s", "%(pathname)s:%(module)s:%(funcName)s", "%(lineno)s", "%(message)s"]
)
formatter = logging.Formatter(fmt)
fhandler.setFormatter(formatter)
shandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.addHandler(shandler)
logger.setLevel(logging.FATAL)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONST
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def howlong(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        logger.info("time consumed:{}".format(end - start))
        print("{} : {}".format(func.__name__, end - start))
        return r

    return wrapper


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LOGIC
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ================================================================
# PURPOSE：
# ================================================================
class MySort(object):
    """docstring for MySort."""

    def __init__(self, num):
        super(MySort, self).__init__()

        tmp = set()
        while True:
            tmp.add(random.randint(1000, 9999))
            if len(tmp) >= num:
                break

        self.numbers = list(tmp)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def insertSort(self):
        targets = copy.deepcopy(self.numbers)
        n = 0

        logger.warning("\n\n\ninsert sort,\tinitial:{}".format(targets))
        for i in range(len(targets)):
            for j in range(i):
                n += 1
                if targets[i] < targets[j]:
                    targets.insert(j, targets.pop(i))
                    logger.info(
                        "round {}, insert {} to {}, {}".format(
                            str(n).zfill(3), str(i).zfill(2), str(j).zfill(2), targets
                        )
                    )
                    break

        return targets

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def shellSort(self):
        targets = copy.deepcopy(self.numbers)
        n = 0

        logger.warning("\n\n\nshell sort,\tinitial:{}".format(targets))
        gap = len(targets)
        while gap > 1:
            gap = gap // 2
            logger.info("gap={}".format(gap))
            for i in range(gap, len(targets)):
                for j in range(i % gap, i, gap):
                    n += 1
                    if targets[i] < targets[j]:
                        targets[i], targets[j] = targets[j], targets[i]
                        logger.info(
                            "round {}, exchange {}<->{}, {}".format(
                                str(n).zfill(3), str(i).zfill(2), str(j).zfill(2), targets,
                            )
                        )

        return targets

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def selectSort(self):
        targets = copy.deepcopy(self.numbers)
        n = 0

        logger.warning("\n\n\nselect sort,\tinitial:{}".format(targets))
        for i in range(len(targets)):
            x = i
            for j in range(i + 1, len(targets)):
                n += 1
                if targets[x] > targets[j]:
                    x = j
            targets[i], targets[x] = targets[x], targets[i]
            logger.info(
                "round {}, exchange {}<->{}, {}".format(
                    str(n).zfill(3), str(i).zfill(2), str(x).zfill(2), targets
                )
            )

        return targets

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def heapSort(self):
        def heap_adjust(parent):
            child = 2 * parent + 1
            while child < len(heap):
                if child + 1 < len(heap):
                    if heap[child + 1] > heap[child]:
                        child += 1
                if heap[parent] >= heap[child]:
                    break
                logger.info("heap before:{}".format(heap))
                heap[parent], heap[child] = heap[child], heap[parent]
                logger.info("heap after:{}".format(heap))
                logger.info("parent={}, child={}".format(parent, child))
                parent, child = child, 2 * child + 1

        n = 0
        heap, targets = copy.deepcopy(self.numbers), list()
        logger.warning("\n\n\nheap sort,\tinitial:{}".format(heap))
        for i in range(len(heap) // 2, -1, -1):
            logger.info("\nheap_adjust:{}".format(i))
            heap_adjust(i)

        while len(heap):
            heap[0], heap[-1] = heap[-1], heap[0]
            targets.insert(0, heap.pop())
            logger.info("\nround {}, heap:{}, targets:{}".format(str(n).zfill(3), heap, targets))
            n += 1
            logger.info("heap_adjust_always:{}".format(0))
            heap_adjust(0)

        return targets

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def bubbleSort(self):
        targets = copy.deepcopy(self.numbers)
        n = 0

        logger.warning("\n\n\nbubble sort,\t\tinitial:{}".format(targets))
        for i in range(len(targets) - 1):
            for j in range(len(targets) - 1 - i):
                n += 1
                if targets[j] > targets[j + 1]:
                    targets[j], targets[j + 1] = targets[j + 1], targets[j]
                    logger.info(
                        "round {}, exchange {}<->{}, {}".format(
                            str(n).zfill(3), str(j + 1).zfill(2), str(j).zfill(2), targets,
                        )
                    )

        return targets

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def quickSort(self, targets):
        def quick_sort(elements):
            if elements == list():
                return elements
            else:
                partition = elements[0]
                lpart = [l for l in elements[1:] if l < partition]
                rpart = [r for r in elements[1:] if r >= partition]
                elements_l = quick_sort(lpart)
                elements_r = quick_sort(rpart)
                logger.info(
                    "\ntargets={}\npartition={}\nlpart={}\nrpart={}\nres={}".format(
                        elements, partition, lpart, rpart, elements_l + [partition] + elements_r,
                    )
                )
                return elements_l + [partition] + elements_r

        targets = copy.deepcopy(self.numbers)
        logger.warning("\n\n\nquick sort,\t\tinitial:{}".format(targets))
        return quick_sort(targets)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def mergeSort(self):
        def merge(lpart, rpart):
            logger.info("lpart={}\nrpart={}".format(lpart, rpart))
            m = list()
            while len(lpart) and len(rpart):
                if lpart[0] <= rpart[0]:
                    m.append(lpart.pop(0))
                else:
                    m.append(rpart.pop(0))
            if len(lpart):
                m.extend(lpart)
            if len(rpart):
                m.extend(rpart)
            logger.info("m={}\n".format(m))
            return m

        def recursive(part):
            if len(part) == 1:
                return part
            mid = len(part) // 2
            logger.info("part={}\n".format(part))
            return merge(recursive(part[:mid]), recursive(part[mid:]))

        targets = copy.deepcopy(self.numbers)
        logger.warning("\n\n\nmerge sort,\t\tinitial:{}".format(targets))
        res = recursive(targets)
        logger.info("res={}".format(res))
        return res

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def bucketSort(self):
        targets = copy.deepcopy(self.numbers)
        logger.warning("\n\n\nbucket sort,\t\tinitial:{}".format(targets))
        n = 0

        bucket, digit = [[]], 0
        while len(bucket[0]) != len(targets):
            bucket = [list() for i in range(10)]
            for i in range(len(targets)):
                num = (targets[i] // 10 ** digit) % 10
                bucket[num].append(targets[i])
                logger.info("round {}, num={}, bucket={}".format(str(n).zfill(2), num, bucket))
                n += 1
            targets.clear()
            for i in range(len(bucket)):
                targets += bucket[i]
            digit += 1

        return targets


# ================================================================
# PURPOSE：
# ================================================================
class AnotherSort(object):
    """docstring for AnotherSort."""

    def __init__(self, num):
        super(AnotherSort, self).__init__()

        tmp = set()
        while True:
            tmp.add(random.randint(10, 99))
            if len(tmp) >= num:
                break

        self.numbers = list(tmp)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    @howlong
    def mergeSort(self):
        def adjust_heap(elements, i, hsize):
            parent = i
            lchild = 2 * i + 1
            rchild = lchild + 1
            if i < hsize / 2:
                if lchild < hsize and elements[lchild] > elements[parent]:
                    parent = lchild
                if rchild < hsize and elements[rchild] > elements[parent]:
                    parent = rchild
                if parent != i:
                    elements[parent], elements[i] = elements[i], elements[parent]
                    adjust_heap(elements, parent, hsize)

        def build_heap(elements, hsize):
            for i in range(hsize // 2, -1, -1):
                adjust_heap(elements, i, hsize)

        targets = copy.deepcopy(self.numbers)
        logger.warning("\n\n\nmerge sort,\t\tinitial:{}".format(targets))
        build_heap(targets, len(targets))
        for j in range(0, len(targets))[::-1]:
            targets[0], targets[j] = targets[j], targets[0]
            adjust_heap(targets, 0, j)

        print(targets)
        return targets


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def batch():
    obj = MySort(128)

    obj.insertSort()
    obj.shellSort()

    obj.bubbleSort()
    obj.quickSort(obj.numbers)

    obj.selectSort()
    obj.heapSort()

    obj.mergeSort()

    obj.bucketSort()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def batch_another():
    obj = AnotherSort(8)
    obj.mergeSort()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    # batch_another()
    batch()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
