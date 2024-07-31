import random
import math

def percentChance(p: float) -> bool:
    return random.random() * 100 < p


def randomDirection() -> float:
    return (random.random() - 0.5) * 2

# sum

def mulSum(nums):
    res = 1
    for num in nums:
        res *= num
    return res


def divSum(nums):
    res = 1
    for num in nums:
        res /= max(0.00001, num)
    return res


def rMulSum(nums):
    res = -1
    for num in nums:
        res *= num
    return res


def rDivSum(nums):
    res = -1
    for num in nums:
        res /= max(0.00001, num)
    return res


def sinSum(nums):
    return math.sin(sum(nums))


def tanSum(nums):
    return math.tan(sum(nums))


def cosSum(nums):
    return math.cos(sum(nums))


def powSum(nums):
    res = 2
    for num in nums:
        try:
            res = max(-math.inf, min(math.inf, res**num))
        except:
            res = 1
    return res


def median(nums):
    try:
        return sorted(nums)[round(len(nums) / 2)]
    except IndexError:
        return 0


def avg(nums):
    return sum(nums) / max(1, len(nums))


def medAvDist(nums):
    return abs(median(nums) - avg(nums))
