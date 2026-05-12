# zeme

A code-golfed, Scheme-subset interpreter that abuses find and replace.

- While studying functional programming, I realized beta reduction was basically just find and replace, which inspired this project.
- All functions, including those defined by the user, get compiled into regex. During evaluation, the regex is continually applied until the result can be evaluated in Python via `exec()`.
- Lambdas use alpha conversion (variable renaming) to avoid variable capture, another functional programming concept.
- Partial evaluation: the conditions of `if` expressions are evaluated during expansion when possible. This allows unlimited recursion; before, there was a hard cap on the number of expansions and thus recursion depth.

```scheme
(define (fact n)
  (if (= n 0)
      1
      (* n (fact (- n 1)))))

(display (fact (read)))
```

See `examples/` for more.

To run tests:

```
pip install -r requirements.txt
python test_zeme.py
```
