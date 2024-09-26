"""
Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

Example 1:


Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true
Example 2:


Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
Output: true
Example 3:


Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: false
 

Constraints:

m == board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board and word consists of only lowercase and uppercase English letters.
"""

#Action Plan
#1. Iterate through the board
#2. Check if the current value is the first letter of the word
#3. If yes, call the helper function
#4. In the helper function, check if the word is empty
#5. If yes, return True
#6. Check if the row and column are out of bounds
#7. If yes, return False
#8. Check if the current value is not the first letter of the word
#9. If yes, return False
#10. Mark the current value as visited
#11. Check the adjacent cells
#12. If any of the adjacent cells return True, return True
#13. Unmark the current value
#14. Return False

from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        def helper(i, j, word):
            if not word:
                return True
            if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]) or board[i][j] != word[0]:
                return False
            temp = board[i][j]
            board[i][j] = ''
            result = helper(i+1, j, word[1:]) or helper(i-1, j, word[1:]) or helper(i, j+1, word[1:]) or helper(i, j-1, word[1:])
            board[i][j] = temp
            return result
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == word[0]:
                    if helper(i, j, word):
                        return True
        return False