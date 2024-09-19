""" 
LAB 1 - Longest Palindromic Substring - Level 1
In the given string s, your task is to identify and return the longest palindromic substring. 
A palindromic substring is a contiguous sequence of characters existing within the string s that reads the same forward and backward. 
If multiple palindromic substrings of the same maximum length exist, return the one that appears first.

input: A string, accessible as s
output: A string which is the longest and first palindromic substring

LAB 1.1 - Naive solution - Substring iteration algorithm

1/ Implement a method that given a string returns True if the string is a palindrome, False otherwise.
2/ By iterating on substrings and using the method described above, solve longest palindrome problem.
3/ Determine the complexity of the algorithm implemented.
4/ How much CO2 does your implementation generate ?

See tests.py for examples of palindroms.
"""

##### YOU CAN EDIT THE CODE BELOW #####

def findLongestPalindrome(s: str) -> str:
    def isPalindrome(s: str) -> bool:
        # Returns True if the string is a palindrome, False otherwise.
        return False

    # Iterate on all substrings with isPalindrome
    longestPalindrome = s

    return longestPalindrome