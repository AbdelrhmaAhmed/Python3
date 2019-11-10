# LeetCode Problem [Easy] 

Given an array of integers arr, write a function that returns true if and only if the number of occurrences of each value in the array is unique.

# My Solution:
```python3
class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        countedItems=[]
        for item in set(arr): countedItems.append(arr.count(item))
        return True if len(countedItems) == len(set(countedItems)) else False 
```
