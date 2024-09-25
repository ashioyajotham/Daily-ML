"""
Given the head of a linked list, remove the nth node from the end of the list and return its head.
Example 1:
1 ----> 2 ----> 3 -----> 4 -----> 5
                |
1 ----> 2 ----- 3                 5

Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
Example 2:

Input: head = [1], n = 1
Output: []
Example 3:

Input: head = [1,2], n = 1
Output: [1]
 

Constraints:

The number of nodes in the list is sz.
1 <= sz <= 30
0 <= Node.val <= 100
1 <= n <= sz

"""

## Action Plan
#1. Create a dummy node and point it to the head of the linked list
#2. Create two pointers slow and fast and point them to the dummy node
#3. Move the fast pointer n times
#4. Move the slow and fast pointers until the fast pointer reaches the end of the linked list
#5. Remove the nth node from the end of the linked list by pointing the slow pointer to the next of the next node
#6. Return the dummy.next node

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0)
        dummy.next = head
        slow = dummy
        fast = dummy
        for i in range(n):
            fast = fast.next
        while fast.next:
            slow = slow.next
            fast = fast.next
        slow.next = slow.next.next
        return dummy.next

#Time complexity is O(n) where n is the number of nodes in the linked list
#Space complexity is O(1) as we are using only constant space
#Test the function with the examples