"""Coin change problem dynamic programming implementations."""
from typing import Sequence


def coin_change_min(coins: Sequence[int], amount: int) -> int:
    """Compute the minimum number of coins needed to make up the given amount.

    Returns -1 if the amount cannot be made up by any combination of the coins.

    Time Complexity: O(n * amount)
    Space Complexity: O(amount)
    """
    if amount < 0:
        raise ValueError("amount cannot be negative")
    if any(c <= 0 for c in coins):
        raise ValueError("coin denominations must be strictly positive")
    if amount == 0:
        return 0

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0.0

    for coin in set(coins):
        for x in range(coin, amount + 1):
            if dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1

    return int(dp[amount]) if dp[amount] != float("inf") else -1


def coin_change_ways(coins: Sequence[int], amount: int) -> int:
    """Compute the number of distinct combinations that make up the given amount.

    Time Complexity: O(n * amount)
    Space Complexity: O(amount)
    """
    if amount < 0:
        raise ValueError("amount cannot be negative")
    if any(c <= 0 for c in coins):
        raise ValueError("coin denominations must be strictly positive")
    if amount == 0:
        return 1

    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in sorted(set(coins)):
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]

    return dp[amount]
