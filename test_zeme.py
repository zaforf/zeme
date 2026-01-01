import unittest
import subprocess
import sys
import os

class TestZeme(unittest.TestCase):
	def run_z(self, code, input_str=""):
		filename = "temp_test.zm"
		with open(filename, "w") as f:
			f.write(code)

		try:
			result = subprocess.run(
				[sys.executable, "zeme.py", filename],
				input=input_str,
				capture_output=True,
				text=True,
				timeout=3
			)
			return result.stdout.strip()
		finally:
			if os.path.exists(filename):
				os.remove(filename)

	def test_display_read(self):
		self.assertEqual(self.run_z("(display 4)"), "4")
		self.assertEqual(self.run_z('(display "test!")'), "test!")
		self.assertEqual(self.run_z('(display (+ (read) " world"))', input_str="hello"), "hello world")
		self.assertEqual(self.run_z('(display (+ (read) 5))', input_str="4"), "9")

		self.assertEqual(self.run_z('(define (space) (display "h   i")) (space)'), "h   i")
		# need multi-read test

	def test_basic_math_logic(self):
		self.assertEqual(self.run_z("(display (+ 999 5))"), "1004")
		self.assertEqual(self.run_z("(display (- 1 5))"), "-4")
		self.assertEqual(self.run_z("(display (* 3 4))"), "12")

		self.assertEqual(self.run_z("(display (if (< 2 5) 2 5))"), "2")
		self.assertEqual(self.run_z("(display (if (= 5 5) 1 0))"), "1")

	def test_basic_lambda(self):
		self.assertEqual(self.run_z("(display ((lambda (x) x) 42))"), "42") # identity
		self.assertEqual(self.run_z("(display (((lambda (x) (lambda (y) (+ x y))) 4) 5))"), "9")

	def test_variable_shadowing(self):
		code = "(display ((lambda (x) (+ x ((lambda (x) x) 10))) 5))"
		self.assertEqual(self.run_z(code), "15")

	def test_recursion_factorial(self):
		code = """
		(define (fact n) (if (= n 0) 1 (* n (fact (- n 1)))))
		(display (fact (read)))
		"""
		self.assertEqual(self.run_z(code, input_str="7"), "5040")
		self.assertEqual(self.run_z(code, input_str="4"), "24")
		self.assertEqual(self.run_z(code, input_str="0"), "1")

	def test_fibonacci(self):
		code = """
		(define (fib-helper count a b)
		  (if (= count 0)
			  a
			  (fib-helper (- count 1) b (+ a b))))


		(define (fib n)
		  (fib-helper n 0 1))

		(display (fib 3)) (newline)
		(display (fib 4)) (newline)
		(display (fib 5)) (newline)
		(display (fib 100))
		"""
		expected = "2\n3\n5\n354224848179261915075"
		self.assertEqual(self.run_z(code), expected)

	def test_u_combinator(self):
		code = """
		(display
		  ((lambda (n)
		     ((lambda (fact) (fact fact n))
		      (lambda (ft k)
		        (if (= k 1)
		            1
		            (* k (ft ft (- k 1)))))))
		   50)
		)
		"""
		expected = "30414093201713378043612608166064768844377641568960512000000000000"
		self.assertEqual(self.run_z(code), expected)

if __name__ == '__main__':
	unittest.main()