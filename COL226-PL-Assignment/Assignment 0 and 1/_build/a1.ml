open A0

exception Error of string;;


type  exptree =     N of int | Plus of exptree * exptree 
                             | Minus of exptree * exptree 
                             | Mult of exptree * exptree 
                             | Div of exptree * exptree 
                             | Rem of exptree * exptree 
                             | Nega of  exptree 
                             | Abs of  exptree ;;

type opcode = CONST of bigint | PLUS | TIMES | MINUS | DIV | REM | ABS | UNARYMINUS ;;


(*This function calculates the value of the expression tree*)
let rec eval t = match t with 
          |N(a)-> a
          |Plus(t1, t2) -> (eval t1)+(eval t2)
          |Minus(t1, t2) -> (eval t1)-(eval t2)
          |Mult(t1, t2) -> (eval t1)*(eval t2)
          |Div(t1, t2) -> (eval t1)/(eval t2)
          |Rem(t1, t2) -> (eval t1) mod (eval t2)
          |Nega(t1) -> (-1)*(eval t1)
          |Abs(t1) -> let temp = eval t1 in
                      if(temp >0) then temp
                      else -1*temp;;


(*This function gives the postfix expression for corresponding exptree*)
let rec compile t  = match t with 
             N(a) -> CONST(mk_big a)::[]
            |Plus(t1, t2) -> (compile t1) @ (compile t2)@ [PLUS]
            |Minus(t1, t2) -> (compile t1) @ (compile t2)@ [MINUS]
            |Mult(t1, t2) -> (compile t1) @ (compile t2)@ [TIMES]
            |Div(t1, t2) -> (compile t1) @ (compile t2)@ [DIV]
            |Rem(t1, t2) -> (compile t1) @ (compile t2)@ [REM]
            |Nega(t1) -> (compile t1) @ [UNARYMINUS]
            |Abs(t1) -> (compile t1) @ [ABS];;


(*This function calculates the value of the given exptree*)
let rec stackmc st op = match op, st with 
                |[], x::y -> x
                |[], _ -> raise(Error "There is some error stack is empty")

                | CONST(a)::tl, _ -> stackmc (a::st) tl

                |PLUS::tl, x1::x2::t -> stackmc ((add x1 x2)::t) tl
                |PLUS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                |MINUS::tl, x1::x2::t -> stackmc (( sub x1 x2)::t) tl
                |MINUS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |TIMES::tl, x1::x2::t -> stackmc ((mult x1 x2)::t) tl
                |TIMES::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |DIV::tl, x1::x2::t -> stackmc ((div x2 x1)::t) tl
                |DIV::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |REM::tl, x1::x2::t ->stackmc ((rem x2 x1)::t) tl
                |REM::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |UNARYMINUS::tl, x1::t -> stackmc ((minus x1)::t) tl
                |UNARYMINUS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")6
                
                |ABS::tl, x1::t -> stackmc ((abs x1)::t) tl
                |ABS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched");;
