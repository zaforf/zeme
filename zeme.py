import sys
import regex

# define is the only true built in
# functions can have no args
# set s : alphanumeric + symbols (+,*,/)
# args, fun names, vars all set s
# theoretically unlimited recursion
# no parentheses outside of syntax (not in string)
# function need not start on line
# at most one (read) call per statement (consider (define (double a) (+ a a)))
# read cant take neg numbers rn (blame python)

# number, string, (bool), function are the only types

# function result should be in parens if it should be evaluated and non void (as a function) (suggestion)

scope = {}

builtins = [
	'(define (* x y) (x * y))',
	'(define (+ x y) (x + y))',
	'(define (- x y) (x - y))',

	'(define (= x y) (x == y))',
	'(define (< x y) (x < y))',

	'(define (if x y z) (if x y z))',

	'(define (define a b) global a;a=b)', # adds support for variables
	'(define (display s) print(s,end=""))',
   r'(define (newline) (display "\n"))',
	'(define (read) (read))',
]

red = []
process = {
	"if":   lambda m, x: m.group(3 if eval(m.group(2)) else 4),
	"read": lambda m, x: repr(red[0]) if red else (red.append(int(r) if (r:=input()).isdigit() else r) or repr(red[0]))
}

defn, arg_cap = '(?(DEFINE)(?P<rec>\\((?:[^()]|(?&rec))*\\)|"[^"]*"|[^\\s()]+))', '\\s+((?&rec))'

def main():
	if len(sys.argv) < 2: return print("expected filename")
	source = open(sys.argv[1]).read()

	statements = regex.findall("(\\((?:[^()]|(?R))*\\))", source)
	subs = {}

	lens = []
	for statement in builtins + statements:
		if match := regex.match(r'\(define\s+\((?P<sig>[^)]+)\)\s+(?P<body>.*)\)', statement, regex.DOTALL):
			name, *args = match.group("sig").split()

			replace = match.group("body").replace("\\", "\\\\")
			# compress spaces but not if in quotes
			replace = regex.sub(r'("[^"]*")|\s+', lambda m: m.group(1) or " ", replace)

			for i, arg in enumerate(args):
				replace = regex.sub(fr"(?<=^|\W){arg}(?=$|\W)", fr"\\{i+2}", replace)

			name = regex.escape(name)
			pattern = fr"\({defn}{name}{arg_cap * len(args)}\)"
			# print(pattern,replace)

			def processor(match, n=name, t=replace):
				expanded = match.expand(t)
				try: return process.get(n, lambda m, x: repr(eval(x)))(match, expanded)
				except (NameError, SyntaxError): return expanded
			subs[pattern] = processor

		else:
			# some preprocessing
			changes = 1
			mxlen, cycles = 0, 0
			while changes != 0:
				changes = 0
				for pattern, replace in subs.items():
					statement, count = regex.subn(pattern, replace, statement)
					changes += count
					mxlen = max(mxlen, len(statement))
				cycles += 1
				# print(statement)

			lens.append((mxlen, cycles))
			exec(statement, scope, {})
			red.clear() # for read

	print(lens)

if __name__ == "__main__": main()