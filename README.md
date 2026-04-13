# zeme

A code-golfed, Scheme-subset interpreter that abuses find and replace. Function definitions get compiled into regex patterns, and expressions are rewritten until Python can evaluate them. Some highlights:

- Beta reduction is essentially find and replace, which is what inspired this janky project
- Lambdas use alpha conversion (variable renaming) to avoid variable capture, another functional programming concept
- Partial evaluation: `if` conditions are evaluated during expansion when possible. This allows unlimited recursion; before it, there was a hard cap on the number of expansions and thus recursion depth.

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
