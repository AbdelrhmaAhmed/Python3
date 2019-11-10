# LeetCode problem [Easy] 
https://leetcode.com/problems/defanging-an-ip-address/

Given a valid (IPv4) IP address, return a defanged version of that IP address.
A defanged IP address replaces every period "." with "[.]".

My Solution: 
```python3
import re
class Solution:
    def defangIPaddr(self, address: str) -> str:
        return re.sub(r'\.','[.]', address)
```
