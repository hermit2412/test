import unittest
from palindrome_func import is_palindrome

class TestPalindrome(unittest.TestCase):

	def test_is_palindrome(self):
		self.assertEqual(is_palindrome('rotator'),True)
		self.assertEqual(is_palindrome('kayak'),True)
		self.assertEqual(is_palindrome('hello'),False)


if __name__ == '__main__':
	unittest.main()