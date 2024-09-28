"""
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.
Example 1:
2 -> 4 -> 3
5 -> 6 -> 4
7 -> 0 -> 8


Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]
Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
 

Constraints:

The number of nodes in each linked list is in the range [1, 100].
0 <= Node.val <= 9
It is guaranteed that the list represents a number that does not have leading zeros.

"""
# Action Plan
# 1. Create a dummy node and a current node to keep track of the current node.
# 2. Create a carry variable to keep track of the carry.
# 3. Traverse through the linked list and add the values of the two linked lists and the carry.
# 4. Update the carry and the current node.
# 5. Return the next of the dummy node.
# 6. Time complexity is O(n) where n is the length of the linked list.
# 7. Space complexity is O(1) as we are not using any extra space.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()
        current = dummy
        carry = 0
        while l1 or l2 or carry:
            value = 0
            if l1:
                value += l1.val
                l1 = l1.next
            if l2:
                value += l2.val
                l2 = l2.next
            value += carry
            carry = value // 10
            value = value % 10
            current.next = ListNode(value)
            current = current.next
        return dummy.next
    
# Let's create a linked list
l1 = ListNode(2)
l1.next = ListNode(4)
l1.next.next = ListNode(3)

l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)

s = Solution()

result = s.addTwoNumbers(l1, l2)

# Let's test the function