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
#3. If yes, call the helper function to check if the word exists
#4. Return True if the word exists
#5. Return False if the word does not exist
#6. Create a helper function to check if the word exists
#7. Check if the index is out of bounds or the current value is not the letter of the word
#8. Return False if the index is out of bounds or the current value is not the letter of the word
#9. Return True if the word exists
#10. Check if the word exists in the right, left, up and down directions
#11. Return True if the word exists in the right, left, up and down directions

from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == word[0] and self.helper(board, i, j, word[1:]):
                    return True
        return False
    
    def helper(self, board, i, j, word):
        if not word:
            return True
        if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]) or board[i][j] != word[0]:
            return False
        temp = board[i][j]
        board[i][j] = '#'
        result = self.helper(board, i+1, j, word[1:]) or self.helper(board, i-1, j, word[1:]) or self.helper(board, i, j+1, word[1:]) or self.helper(board, i, j-1, word[1:])
        board[i][j] = temp
        return result