import sys, regex, uuid

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

# need to fix arg handling of symbols
# define to a lambda is TODO

literal = lambda x: (lambda r: '"' + r[1:-1] + '"' if r.startswith("'") else r)(repr(x))
clean = lambda s: regex.sub(r'("[^"]*")|\s+', lambda m: m.group(1) or " ", s.replace("\\", "\\\\"))

scope, subs, read = {}, {}, []

builtins = """
(define (* x y) (x * y)) (define (+ x y) (x + y)) (define (- x y) (x - y))
(define (= x y) (x == y)) (define (< x y) (x < y))
(define (if x y z) (if x y z)) (define (read) (read))
(define (define a b) a=b)
(define (display s) print(s,end="")) (define (newline) (display "\\n"))
"""

process = {
    "if":   lambda m, x: m.group(3 if eval(m.group(2), scope) else 4),
    # with the addition of partial evaluation, read isnt evaluated all at once, so logic moves here
    "read": lambda m, x: literal(read[0]) if read else (read.append(int(r) if (r:=input()).lstrip('-').isdigit() else r) or literal(read[0]))
}

defn, arg_cap = r'(?(DEFINE)(?P<rec>\((?:[^()]|(?&rec))*\)|"[^"]*"|[^\s()]+))', r'\s+((?&rec))'

lambda_def = fr"{defn}\(\s*lambda\s+\((?P<params>[^)]*)\)\s+(?P<body>(?&rec))\s*\)"
lambda_pattern = fr"\({lambda_def}(?:\s*(?P<arg>(?&rec)))+\s*\)"

def alpha_convert(code):
    def converter(m):
        params = m.group("params").split()
        body = alpha_convert(m.group("body"))

        renaming = {p: f"{p.split('_')[0]}_{uuid.uuid4().hex[:4]}" for p in params}
        for old, new in renaming.items():
            body = regex.sub(fr"(?<=^|\W){old}(?=$|\W)", new, body)
        return f"(lambda ({' '.join(renaming.values())}) {body})"
    return regex.sub(lambda_def, converter, code)

def lambda_processor(m):
    body = clean(m.group("body"))
    params, args = m.group("params").split(), m.captures("arg")
    for param, arg in zip(params, args):
        body = regex.sub(fr"(?<=^|\W){param}(?=$|\W)", arg, body)
    return alpha_convert(body)

subs[lambda_pattern] = lambda_processor

def main():
    if len(sys.argv) < 2: return print("expected filename")
    
    source = alpha_convert(builtins + "\n" + open(sys.argv[1]).read())
    statements = regex.findall(r"(\((?:[^()]|(?R))*\))", source)

    for statement in statements:
        if match := regex.match(r'\(\s*define\s+\((?P<sig>[^)]+)\)\s+(?P<body>.*)\s*\)', statement, regex.DOTALL):
            name, *params = match.group("sig").split()
            body = clean(match.group("body"))

            for i, p in enumerate(params):
                body = regex.sub(fr"(?<=^|\W){p}(?=$|\W)", fr"\\{i+2}", body)

            pattern = fr"{defn}\(\s*{regex.escape(name)}{arg_cap * len(params)}\s*\)"

            def processor(match, n=name, t=body):
                expanded = match.expand(t)
                try: return process.get(n, lambda m, x: literal(eval(x, scope)))(match, expanded)
                except (NameError, SyntaxError): return expanded
            
            subs[pattern] = processor

        else:
            prev = None
            while statement != prev:
                prev = statement
                for pattern, func in subs.items():
                    statement = regex.sub(pattern, func, statement)
            exec(statement, scope)
            read.clear()

if __name__ == "__main__": main()