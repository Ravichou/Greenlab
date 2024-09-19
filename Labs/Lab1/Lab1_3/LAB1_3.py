""" 
LAB 1 - Longest Palindromic Substring - Level 3
In the given string s, your task is to identify and return the longest palindromic substring. 
A palindromic substring is a contiguous sequence of characters existing within the string s that reads the same forward and backward. 
If multiple palindromic substrings of the same maximum length exist, return the one that appears first.

input: A string, accessible as s
output: A string which is the longest and first palindromic substring

LAB 1.3 - Complexity optimisation

1/ Do not generate substrings. 
2/ Read from each character of the input.
3/ From each character, read left and right to assess a potential palindrome. Return size of palindrome.
4/ Even and odd palindrome sizes need to be handled. 
5/ Determine the complexity of the algorithm implemented.
6/ How much CO2 does your implementation generate ? 
"""

##### YOU CAN EDIT THE CODE BELOW #####

def findLongestPalindrome(s: str) -> str:
    longestPalindrome = s

    return longestPalindrome