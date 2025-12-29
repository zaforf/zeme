(define (fib-helper count a b)
  (if (= count 0)
      a
      (fib-helper (- count 1) b (+ a b))))


(define (fib n)
  (fib-helper n 0 1))

(display (fib 1)) (newline)
(display (fib 2)) (newline)
(display (fib 3)) (newline)
(display (fib 4)) (newline)
(display (fib 5)) (newline)
(display (fib 6))
(newline)
(display (fib 7))
(newline)
(display (fib 8))
(newline)
