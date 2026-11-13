"""In-place QuickSort with 3-way Dutch National Flag partitioning."""
import random
from typing import List, TypeVar

from utils.comparable import Comparable

T = TypeVar("T", bound=Comparable)

def quick_sort(arr: List[T]) -> List[T]:
    """Sort a list using randomized 3-way quicksort in-place."""
    def _sort(low: int, high: int):
        if low >= high:
            return
        
        pivot_idx = random.randint(low, high)
        pivot = arr[pivot_idx]
        
        lt, i, gt = low, low, high
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
                
        _sort(low, lt - 1)
        _sort(gt + 1, high)

    _sort(0, len(arr) - 1)
    return arr
