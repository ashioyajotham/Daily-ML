"""
You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Example 1:

Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6
Example 2:

Input: lists = []
Output: []
Example 3:

Input: lists = [[]]
Output: []
 

Constraints:

k == lists.length
0 <= k <= 104
0 <= lists[i].length <= 500
-104 <= lists[i][j] <= 104
lists[i] is sorted in ascending order.
The sum of lists[i].length will not exceed 104.
"""
#Action Plan
#1. Create a list to store the values of the linked lists
#2. Iterate through the linked lists
#3. Append the values of the linked lists to the list
#4. Sort the list

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import List

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        result = []
        for l in lists:
            while l:
                result.append(l.val)
                l = l.next
        result.sort()
        head = ListNode()
        current = head
        for i in result:
            current.next = ListNode(i)
            current = current.next
        return head.next
    
#Time complexity is O(nlogn) where n is the total number of nodes in the linked lists
#Space complexity is O(n) where n is the total number of nodes in the linked lists