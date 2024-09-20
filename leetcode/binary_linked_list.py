"""
Given a binary tree root and a linked list with head as the first node. 

Return True if all the elements in the linked list starting from the head correspond to some downward path connected in the binary tree otherwise return False.

In this context downward path means a path that starts at some node and goes downwards.

Example 1:

Input: head = [4,2,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
Output: true
Explanation: Nodes in blue form a subpath in the binary Tree.  
Example 2:



Input: head = [1,4,2,6], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
Output: true
Example 3:

Input: head = [1,4,2,6,8], root = [1,4,4,null,2,2,null,1,null,6,8,null,null,null,null,1,3]
Output: false
Explanation: There is no path in the binary tree that contains all the elements of the linked list from head.
 

Constraints:

The number of nodes in the tree will be in the range [1, 2500].
The number of nodes in the list will be in the range [1, 100].
1 <= Node.val <= 100 for each node in the linked list and binary tree.
"""

# Plan:
# 1. Traverse the binary tree in a depth-first search manner.
# 2. At each node, check if the current node is the starting node of the linked list.
# 3. If the current node is the starting node, check if the linked list is a downward path starting from the current node.
# 4. If the linked list is a downward path starting from the current node, return True.
# 5. If the linked list is not a downward path starting from the current node, continue the traversal.
# 6. If no downward path is found, return False.
# 7. Repeat steps 2 to 6 for all nodes in the binary tree.

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSubPath(self, head: ListNode, root: TreeNode) -> bool:
        def is_sub_path(head, root):
            if not head:
                return True
            if not root:
                return False
            if head.val == root.val:
                return is_sub_path(head.next, root.left) or is_sub_path(head.next, root.right)
            return False

        if not root:
            return False
        if is_sub_path(head, root):
            return True
        return self.isSubPath(head, root.left) or self.isSubPath(head, root.right)
    
# Time complexity: O(n*m) where n is the number of nodes in the binary tree and m is the number of nodes in the linked list.
# Space complexity: O(h) where h is the height of the binary tree. The space complexity is O(h) due to the recursive calls in the depth-first search traversal.