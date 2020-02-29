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
import logging
import os
import random
import sys
from functools import lru_cache

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
logfilename = os.path.splitext(__file__)[0]
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
logger.setLevel(logging.INFO)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONST
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LOGIC
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ================================================================
# PURPOSE：
# ================================================================
class DynamicProgramming(object):
    """docstring for DynamicProgramming."""

    def __init__(self):
        super(DynamicProgramming, self).__init__()

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def coinChange(self):
        coins = {2, 5, 7}
        sum = 38
        howmany = [sys.maxsize for _ in range(-sum, sum + 1)]
        howmany[0] = 0
        for i in range(1, sum + 1):
            howmany[i] = min([howmany[i - coin] for coin in coins]) + 1

        for i, n in enumerate(howmany[0 : sum + 1]):
            print("{} -> {}".format(i, n))

        return howmany[sum + 1]

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def uniquePath(self):
        m, n = 6, 9
        p = [[0 for i in range(m)] for j in range(n)]

        for i in range(n):
            for j in range(m):
                if i == 0 or j == 0:
                    p[i][j] = 1
                else:
                    p[i][j] = p[i - 1][j] + p[i][j - 1]

        return p[i][j]

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def frogJump(self):
        m = [2, 3, 1, 1, 4]
        m = [3, 2, 1, 0, 4]
        m = [random.randint(0, 10) for _ in range(10)]
        ppt(m)
        jump = [True] + [False for _ in range(1, len(m))]

        for j in range(1, len(m)):
            for i in range(j):
                if jump[i] and m[i] >= j - i:
                    jump[j] = True
                    break

        ppt(jump)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def storeRobbery(self):
        N = 16
        nums = [random.randint(1, N) for _ in range(N)]
        ppt(nums)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        @lru_cache()
        def solve(idx):
            if idx < 0:
                return 0
            return max(solve(idx - 2) + nums[idx], solve(idx - 1))

        ppt(solve(len(nums) - 1))

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def dp_solve():
            if N == 0:
                return 0
            if N == 1:
                return nums[0]
            maxsums = [0 for _ in range(0, N)]
            for i in range(len(maxsums)):
                if i == 0:
                    maxsums[i] = nums[0]
                if i == 1:
                    maxsums[i] = max(nums[0], nums[1])
                maxsums[i] = max(maxsums[i - 2] + nums[i], maxsums[i - 1])
                ppt(maxsums)
            return maxsums[-1]

        ppt(dp_solve())

        # ----------------------------------------------------------------
        # METHOD:
        # PARAMETERS:
        # RESULT:
        # ----------------------------------------------------------------
        maxsumz = [-1 for _ in range(N)]

        def dp_recursive_solve(idx):
            if idx < 0:
                return 0
            if maxsumz[idx] >= 0:
                return maxsumz[idx]
            maxsumz[idx] = max(dp_recursive_solve(idx - 2) + nums[idx], dp_recursive_solve(idx - 1))
            ppt(maxsumz)
            return maxsumz[idx]

        ppt(dp_recursive_solve(N - 1))

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def fibonacci(self):
        N = 100
        fibs = [-1 for _ in range(N + 1)]

        @lru_cache()
        def fib_recursive(n):
            if n <= 1:
                return n
            if n == 2:
                return 1
            return fib_recursive(n - 1) + fib_recursive(n - 2)

        print("fib_recursive({})={}".format(N, fib_recursive(N)))

        @lru_cache()
        def fib(n):
            if n <= 1:
                return n
            if n == 2:
                return 1
            if fibs[n] > 0:
                return fibs[n]
            fibs[n] = fib(n - 1) + fib(n - 2)
            return fibs[n]

        print("fib({})={}".format(N, fib(N)))

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def backpack(self):
        weights = [1, 4, 3, 1]
        values = [15, 30, 20, 20]
        capacity = 4

        x = list()
        v = 0
        optp = [[0 for i in range(capacity + 1)] for j in range(len(weights))]

        for i in range(len(weights)):
            for j in range(capacity + 1):
                if j >= weights[i]:
                    optp[i][j] = max(optp[i - 1][j], optp[i - 1][j - weights[i]] + values[i])
                else:
                    optp[i][j] = optp[i - 1][j]

        j = capacity
        idx = list()
        for i in range(len(values) - 1, 0, -1):
            if optp[i][j] > optp[i - 1][j]:
                idx.append(i)
                j -= weights[i]

        ppt(idx)
        ppt(optp)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def LongestIncreasingSubsequence(self):
        N = 8
        lis = [random.randint(0, N) for _ in range(N)]
        d = [1 for _ in range(len(lis))]
        res = 1

        for i in range(len(lis)):
            for j in range(i):
                if lis[j] <= lis[i] and d[i] < d[j] + 1:
                    d[i] = d[j] + 1
                res = max(res, d[i])

        ppt(lis)
        ppt(d)
        ppt(res)

        return res

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def LongestCommonSubsequence(self):
        sa = [1, 3, 4, 5, 6, 7, 7, 8]
        sb = [3, 5, 7, 4, 8, 6, 7, 8, 2]

        d = [[0 for i in range(len(sb) + 1)] for j in range(len(sa) + 1)]

        for i in range(1, len(sa) + 1):
            for j in range(1, len(sb) + 1):
                if sa[i - 1] == sb[j - 2]:
                    d[i][j] = d[i - 1][j - 1] + 1
                else:
                    d[i][j] = max(d[i - 1][j], d[i][j - 1])
        ppt(d)

        return d[-1][-1]

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def MaxSumSub(self):
        N = 8
        nums = [random.randint(-N, N) for _ in range(N)]

        if max(nums) < 0:
            return max(nums)

        d = [nums[0]] + [0 - sys.maxsize for _ in range(1, len(nums))]
        for i in range(1, len(nums)):
            d[i] = max(d[i - 1] + nums[i], nums[i])

        ppt(nums)
        ppt(d)
        ppt(max(d))

        return max(d)

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def darkString(self):
        # f(n) = 3*Same(n-1) + 2*Different(n-1)
        # f(n-1) = Same(n-1) + Different(n-1)
        # Same(n) = Same(n-1) + Different(n-1) => Same(n) = f(n-1)
        @lru_cache()
        def solve_recursive(n):
            if n == 1:
                # C(3,1)=3
                return 3
            elif n == 2:
                # C(3,1)+A(3,2)=9
                return 9
            else:
                return 2 * solve_recursive(n - 1) + solve_recursive(n - 2)

        def solve_deductive(n):
            d = [0 for i in range(n + 1)]
            d[1] = 3
            d[2] = 9
            for i in range(1, len(d)):
                if i == 1:
                    d[i] = 3
                elif i == 2:
                    d[i] = 9
                else:
                    d[i] = 2 * d[i - 1] + d[i - 2]
            ppt(d)
            return d[-1]

        N = 16
        ppt(solve_recursive(N))
        ppt(solve_deductive(N))

    # ----------------------------------------------------------------
    # METHOD:
    # PARAMETERS:
    # RESULT:
    # ----------------------------------------------------------------
    def LongestPalindrome(self):
        test_string = "123454321"
        test_string = "sdfada123321"
        test_string = "a12321ababa"
        test_string = "^12421$"

        def solve1(s):
            if len(s) < 2 or s == s[::-1]:
                return s
            max_len = 1
            start = 0
            for i in range(1, len(s)):
                even = s[i - max_len : i + 1]
                odd = s[i - max_len - 1 : i + 1]
                if i - max_len - 1 >= 0 and odd == odd[::-1]:
                    start = i - max_len - 1
                    max_len += 2
                    continue
                if i - max_len >= 0 and even == even[::-1]:
                    start = i - max_len
                    max_len += 1
            return s[start : start + max_len]

        def solve_deductive(s):
            d = [[0 for _ in range(len(s) + 1)] for _ in range(len(s) + 1)]

            res = 0
            for i in range(1, len(s)):
                for j in range(len(s) - 2, 0, -1):
                    if i < j:
                        if s[i] == s[j]:
                            d[i][j] = d[i - 1][j + 1] + 2
                            if i == j - 2:
                                d[i][j] += 1
                    res = max(res, d[i][j])
            ppt(d)
            return res

        ppt(solve_deductive(test_string))


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNCTION:
# PARAMETERS:
# RESULT:
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def batch():
    obj = DynamicProgramming()
    obj.coinChange()
    obj.uniquePath()
    obj.frogJump()
    obj.storeRobbery()
    obj.fibonacci()
    obj.backpack()
    obj.LongestIncreasingSubsequence()
    obj.LongestCommonSubsequence()
    obj.MaxSumSub()
    obj.darkString()
    obj.LongestPalindrome()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MAIN
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main(args):
    batch()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
