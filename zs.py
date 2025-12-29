import sys
import regex

# define is the only true built in
# functions can have no args
# set s : alphanumeric + symbols (+,*,/)
# args, fun names, vars all set s
# recursion limit is ~20 (explicit recursion supported)
# no parentheses outside of syntax (not in string)
# function need not start on line
# at most one (read) call per statement (consider (define (double a) (+ a a)))
# read cant take neg numbers

# function result should be in parens if it should be evaluated and non void (as a function) (suggestion)

scope = {}

builtins = [
	'(define (define a b) global a;a=b)', # adds support for variables
	'(define (display s) print(s,end=""))',
   r'(define (newline) (display "\n"))',
	'(define (read) (_ if"_"in vars()else(_:=int(_)if(_:=input()).isdigit()else _)))',

	'(define (if x y z) (y if x else z))',
	'(define (= x y) (x == y))',

	'(define (+ x y) (x + y))',
	'(define (- x y) (x - y))',
]

defn = r'(?(DEFINE)(?P<rec>\((?:[^()]|(?&rec))*\)|"[^"]*"|[^\s()]+))'
arg_cap = r'((?&rec))'

def main():
	if len(sys.argv) < 2:
		print("expected filename")
		return

	filename = sys.argv[1]
	with open(filename, 'r') as f:
		source = f.read()

	statements = regex.findall("(\\((?:[^()]|(?R))*\\))", source)
	subs = {}

	lens = []
	for statement in builtins + statements:
		match = regex.match(r'\(define\s+\((?P<sig>[^)]+)\)\s+(?P<body>.*)\)', statement, regex.DOTALL)

		if "define" in statement and match:
			sig = match.group("sig")
			name, *args = sig.split()
			name = regex.escape(name)

			replace = match.group("body")
			
			replace = replace.replace("\\", "\\\\")
			# compress spaces but not if in quotes
			replace = regex.sub(r'("[^"]*")|\s+', lambda m: m.group(1) or " ", replace)

			for i, arg in enumerate(args):
				replace = regex.sub(fr"(?<=^|\W){arg}(?=$|\W)", fr"\\{i+2}", replace)

			pattern = fr"\({defn}{name}{fr"\s+{arg_cap}" * len(args)}\)"
			subs[pattern] = replace

		else:
			# some preprocessing
			# print("now at",len(statement),"chars")
			for i in range(20):
				for pattern, replace in subs.items():
					statement = regex.sub(pattern, replace, statement)

			# recursion limit
			for pattern, replace in subs.items():
				statement = regex.sub(pattern, "0", statement)

			# statement = "print(" + statement[9:-1] + ",end='')"
			lens.append(len(statement))
			# by passing local, we let created helper vars be ignored
			exec(statement, scope, {})

	print(lens)

if __name__ == "__main__":
	main()