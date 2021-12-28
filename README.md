
# PyLisp
A Lisp interpreter written in Python loosely following John McCarthy's Recursive Functions of Symbolic Expressions and Their Computation by Machine and Common Lisp implementation.
## Functions Implemented:

 - **CAR**: Get the head of a construct 
 - **CDR**: Get the tail of a construct
 - **CONS**: Construct memory object holding two values 
 - **ATOM**: Check if an expression is atomic
 - **EQ**: check if two expressions are equal atomically
 - **LIST**: Create a chain construct that resembles a list
 - **QUOTE**: Return rest of expression
 - **ASSOC**: Associate the values of two lists as pairs
 - **Prefix Arithmatic**: +, -, *, /
 - **APPEND**: Append to a list a value
 - **PRINT**: Print a value
 - **LET**: Bind variables inside a scope and execute expression
 - **DEFUN**: Define a function
 - **SET**:  Set a variable
 - **IF**: If statement
 - **PROGN**: Do more than one statement
## What is not implemented:
 - Error management
 - Defmacro implementation
 - Package management
 - File Handling
I am planning to redo this project in the future, but as for now, this implementation does not have the previous mentioned features.
## Usage
 - To use this implementation of lisp, simply run the python script where a prompt `PyLisp>` will be waiting for input.
 - To load in a lisp file, simply write `PyLisp> load <file-dir>` when you're in the prompt.
 - You can use `test.lisp` file as an example where loading it would be as follows
 ```lisp
 PyLisp> load test.lisp
 1
2
3
4
------------------------
(1 . 2)
(3 . 4)
(4 . 5)
T
 ```
 ### Purpose of the Project:
 The idea for this project is to implement the notions learned in *CPS 710 Compilers and Interpreters* at (Previously called) *Ryerson University*. Furthermore, it is to implement a LISP interpreter following John McCarthy's original paper, and see what his logic was in each predicate he made.