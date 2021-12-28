(defun printall (list a) (if (eq (cdr a) nil) (print (car a)) (progn (print (car a)) (printall (cdr a)))))
(printall (list 1 2 3 4))
(print ------------------------)
(printall (list (cons 1 2) (cons 3 4) (cons 4 5)))