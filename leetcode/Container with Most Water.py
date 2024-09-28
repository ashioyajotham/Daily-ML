"""
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.
"""
# Action Plan
# 1. Initialize two pointers left and right to the start and end of the list.
# 2. Initialize the max_area to 0.
# 3. Traverse through the list until the left pointer is less than the right pointer.
# 4. Calculate the area between the two pointers.
# 5. Update the max_area if the area is greater than the max_area.
# 6. Move the pointer with the smaller height.
# 7. Return the max_area.
# Complexity Analysis
# The time complexity for this approach is O(n) where n is the length of the list.
# The space complexity is O(1).

from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_area = 0
        while left < right:
            area = min(height[left], height[right]) * (right - left)
            max_area = max(max_area, area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area