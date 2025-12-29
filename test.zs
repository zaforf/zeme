(define (add x y) (x + y))
(define (mul x y) (x * y))
(define (left x y) x)
(define (right x y) y)

(display ((left add mul) 2 3))
(display "\n")
