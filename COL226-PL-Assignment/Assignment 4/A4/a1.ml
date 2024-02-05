open A0

exception Error of string;;

(* abstract syntax *)
type  exptree =  
  Var of string (* variables starting with a Capital letter, represented as alphanumeric strings with underscores (_) and apostrophes (') *)
  | N of int      (* Integer constant *)
  | B of bool     (* Boolean constant *)
  (* unary operators on integers *)
  | Abs of exptree                   (* abs *)
  | Negative of exptree              (* unary minus ~ *)
  (* unary operators on booleans *)
  | Not of exptree
  (* binary operators on integers *)
  | Add of exptree * exptree         (* Addition + *)
  | Sub of exptree * exptree         (* Subtraction - *)
  | Mult of exptree * exptree        (* Multiplication * *)
  | Div of exptree * exptree         (* div *)
  | Rem of exptree * exptree         (* mod *)
  (* binary operators on booleans *)
  | Conjunction of exptree * exptree (* conjunction /\ *)
  | Disjunction of exptree * exptree (* binary operators on booleans \/ *)
  (* comparison operations on integers *)
  | Equals of exptree * exptree      (* = *)
  | GreaterTE of exptree * exptree   (* >= *)
  | LessTE of exptree * exptree      (* <= *)
  | GreaterT of exptree * exptree    (* > *)
  | LessT of exptree * exptree       (* < *)
  (* expressions using parenthesis *)
  | InParen of exptree               (* ( ) *)
  (* a conditional expression *)
  | IfThenElse of exptree * exptree * exptree (* if then else fi  *)
  (* creating n-tuples (n >= 0) *)
  | Tuple of int * (exptree list)
  (* projecting the i-th component of an expression (which evaluates to an n-tuple, and 1 <= i <= n) *)
  | Project of (int*int) * exptree   (* Proj((i,n), e)  0 < i <= n *)
  | Let of definition * exptree
  | FunctionAbstraction of string * exptree
  | FunctionCall of exptree * exptree
(* definition *)
and definition =
    Simple of string * exptree
  | Sequence of (definition list)
  | Parallel of (definition list)
  | Local of definition * definition


(* opcodes of the stack machine (in the same sequence as above) *)
type opcode = VAR of string | NCONST of bigint | BCONST of bool | ABS | UNARYMINUS | NOT
  | PLUS | MINUS | MULT | DIV | REM | CONJ | DISJ | EQS | GTE | LTE | GT | LT
  | PAREN | IFTE | TUPLE of int | PROJ of int*int | LET | FABS | FCALL
  | SIMPLEDEF | SEQCOMPOSE | PARCOMPOSE | LOCALDEF

(* The possible types of expressions in the language of expressions *)
type exptype = Tint | Tunit | Tbool | Ttuple of (exptype list) | Tfunc of (exptype * exptype)

(* The type of value returned by the definitional interpreter. *)
type value = NumVal of int | BoolVal of bool | TupVal of int * (value list)

(* The language should contain the following types of expressions:  integers and booleans *)
type answer = Num of bigint | Bool of bool | Tup of int * (answer list)

let rec revlistg l st = match l with 
                        | []-> st
                        | h::t -> revlistg t (h::st)



(*Function to check if the given input have same type or not if same type(bigint or bool) then it returns 1 else throws an exception*)
let checktype a b = match a, b with
                    |Num(a1), Num(b1) -> 1
                    |Bool(a1), Bool(b1) -> 2
                    |_, _ -> raise(Error "Type not matched")


let checkbigint a b = match a, b with
                      |Num(a1), Num(b1) -> 1
                      |_, _ -> raise(Error "Both must be of type bigint")

let checkbool a b = match a, b with
                    |Bool(a1), Bool(b1) -> 1
                    |_, _ -> raise(Error "Both must be of type bool")

(*Function for bool operations*)
let conjuction a b = match a, b with
                    |Bool(a1), Bool(b1) -> Bool(a1 && b1)
                    |_, _ -> raise(Error "Both must be of type bool")

let disjuction a b = match a, b with
                    |Bool(a1), Bool(b1) -> Bool(a1 || b1)
                    |_, _ -> raise(Error "Both must be of type bool")                    

(*This function calculates the value of the expression tree*)
let rec eval t rho = match t with
          |Var(st)-> (rho st) (* variables starting with a Capital letter, represented as alphanumeric strings with underscores (_) and apostrophes (') *)
          |N(a)-> NumVal(a)  (* Integer constant *)
          |B(b)-> BoolVal(b)         (* Boolean constant *)

          (*Calculating the answer for bigint here*)
          |Add(t1, t2) -> ( let e1 = eval t1 rho in
                           let e2 = eval t2 rho in 
                           match e1, e2 with
                           | NumVal(a), NumVal(b)-> NumVal(a + b)
                           | _, _  -> raise(Error "Type not matched"))
                           
          |Sub(t1, t2) -> (let e1 = eval t1 rho in
                            let e2 = eval t2 rho in 
                            match e1, e2 with
                           | NumVal(a), NumVal(b)-> NumVal(a - b)
                           | _, _  -> raise(Error "Type not matched") )

          |Mult(t1, t2) -> (let e1 = eval t1 rho in
                           let e2 = eval t2 rho in                            
                           match e1, e2 with
                           | NumVal(a), NumVal(b)-> NumVal(a*b)
                           | _, _  -> raise(Error "Type not matched") )

          |Div(t1, t2) -> (let e1 = eval t1 rho in
                          let e2 = eval t2 rho in                            
                          match e1, e2 with
                          | NumVal(a), NumVal(b)-> NumVal(a/b)
                          | _, _  -> raise(Error "Type not matched"))

          |Rem(t1, t2) -> (let e1 = eval t1 rho in
                          let e2 = eval t2 rho in                            
                          match e1, e2 with
                           | NumVal(a), NumVal(b)-> NumVal( a mod b)
                           | _, _  -> raise(Error "Type not matched"))

          |Negative(t1) -> (let e1 = eval t1 rho in
                           match e1 with
                           |NumVal(a) -> NumVal( (-1)*a)
                           |_ -> raise(Error "Type must be bigint"))

          |Abs(t1) -> (let temp = eval t1 rho in
                      match temp with 
                      |NumVal(a)-> NumVal(Pervasives.abs a)
                      |_ -> raise(Error "Type must be bigint"))

          (* binary operators on booleans *)
          |Conjunction(t1, t2)-> (let e1 = eval t1 rho in
                                let e2 = eval t2 rho in
                                (match e1, e2 with
                                | BoolVal(a), BoolVal(b)-> BoolVal(a && b)
                                | _, _ -> raise(Error "Type mismatch") ))
                                

          |Disjunction(t1, t2)-> (let e1 = eval t1 rho in 
                                 let e2 = eval t2 rho in 
                                 (match e1, e2 with
                                | BoolVal(a), BoolVal(b)-> BoolVal(a || b)
                                | _, _ -> raise(Error "Type mismatch") ))

          |Not(t)->(let e = eval t rho in
                   (match e with 
                   |BoolVal(a) -> if(a = true)then BoolVal(false)
                            else BoolVal(true)
                   |_ ->raise(Error "type must be of bool type")
                   ))


          (* comparison operations on integers *)                 
          |Equals(t1, t2)-> (let e1 = eval t1 rho in     (* = *)
                            let e2 = eval t2 rho in
                            match e1, e2 with
                           | NumVal(a), NumVal(b)-> BoolVal(a=b)
                           | _, _  -> raise(Error "Type not matched"))
                            
          |GreaterTE(t1, t2)-> (let e1 = eval t1 rho in  (* >= *)
                               let e2 = eval t2 rho in
                               match e1, e2 with
                              | NumVal(a), NumVal(b)-> BoolVal(a >=b)
                              | _, _  -> raise(Error "Type not matched"))
                               
          |LessTE(t1, t2)-> (let e1 = eval t1 rho in     (* <= *)
                            let e2 = eval t2 rho in
                            match e1, e2 with
                            | NumVal(a), NumVal(b)-> BoolVal( a<=b )
                            | _, _  -> raise(Error "Type not matched"))

          |GreaterT(t1, t2)-> (let e1 = eval t1 rho in   (* > *)
                              let e2 = eval t2 rho in
                              match e1, e2 with
                             | NumVal(a), NumVal(b)-> BoolVal( a>b )
                             | _, _  -> raise(Error "Type not matched"))

          |LessT(t1, t2)-> (let e1 = eval t1 rho in      (* < *)
                           let e2 = eval t2 rho in
                           match e1, e2 with
                           | NumVal(a), NumVal(b)-> BoolVal(a<b)
                           | _, _  -> raise(Error "Type not matched"))

          (* a conditional expression *)
          |IfThenElse(t1, t2, t3)-> (let e1 = eval t1 rho in (* if then else fi  *)
                                    let e2 = eval t2 rho in 
                                    let e3 = eval t3 rho in 
                                   ( match e1 with
                                    |BoolVal(c) -> (match e2, e3 with
                                                   |BoolVal(a), BoolVal(b) -> if(c = true)then e2
                                                                  else e3
                                                   |NumVal(a), NumVal(b) -> if(c = true)then e2
                                                                  else e3
                                                   | TupVal(a,a1), TupVal(b,b1) -> if(c = true)then e2
                                                                  else e3
                                                   | _, _ -> raise(Error "Output must be of same type") )
                                    | _ -> raise(Error "Condition must be of type bool") ))
                                    

          (* expressions using parenthesis *)
          |InParen(t)-> eval t rho                              (* ( ) *)

          (* creating n-tuples (n >= 0) *)
          |Tuple(a, t)-> (let rec cal t1 = (match  t1 with
                         | [] -> []
                         | h::tl -> (eval h rho)::(cal tl) ) in

                         TupVal(a, (cal t))
                         )

          (* projecting the i-th component of an expression (which evaluates to an n-tuple, and 1 <= i <= n) *)
          |Project((i, n), t)-> (let elist = (eval t rho )in
                                let rec get_nth list1 count = (match list1, count with
                                                 | [], _ -> raise (Error "get_nth")
                                                 | _, nn when (nn <= 0) -> raise (Error "get_nth")
                                                 | (x::_), 1 -> x
                                                 | (x::xs), nn -> (get_nth xs (nn - 1)))  in
                                (match elist with 
                                 TupVal(a, alist) when (a = n) -> (get_nth alist i) 
                                 | _ -> raise(Error "not correct format"))
                                 )

(*This function gives the postfix expression for corresponding exptree*)
let rec compile t  = match t with 
            |Var(st) -> VAR(st)::[]
            |N(a) -> NCONST(mk_big a)::[]
            |B(b) -> BCONST(b)::[]

            
            (*Binary Operation for integers and bool*)
            |Add(t1, t2) -> (compile t2) @ (compile t1)@ [PLUS]
            |Sub(t1, t2) -> (compile t2) @ (compile t1)@ [MINUS]
            |Mult(t1, t2) -> (compile t2) @ (compile t1)@ [MULT]
            |Div(t1, t2) -> (compile t2) @ (compile t1)@ [DIV]
            |Rem(t1, t2) -> (compile t2) @ (compile t1)@ [REM]

            |Conjunction(t1, t2) -> (compile t2) @ (compile t1)@ [CONJ]
            |Disjunction(t1, t2) -> (compile t2) @ (compile t1)@ [DISJ] 


            (*Unary Operation for integers and bool*)
            |Negative(t1) -> (compile t1) @ [UNARYMINUS]
            |Abs(t1) -> (compile t1) @ [ABS]

            |Not(t1) -> (compile t1)@ [NOT]


            (*comparison Operation for integers*)
            |Equals(t1, t2) -> (compile t2) @ (compile t1)@ [EQS]
            |GreaterTE(t1, t2) -> (compile t2) @ (compile t1)@ [GTE]
            |LessTE(t1, t2) -> (compile t2) @ (compile t1)@ [LTE]
            |GreaterT(t1, t2)-> (compile t2) @ (compile t1)@ [GT]
            |LessT(t1, t2) -> (compile t2) @ (compile t1)@ [LT]


            (*Expression using paraenthesis*)
            |InParen(t) -> (compile t)@ [PAREN]


            (* a conditional expression*)
            |IfThenElse(t1, t2, t3) -> (compile t3) @ (compile t2) @ (compile t1) @ [IFTE]

            
            (* creating n tuples *)
            |Tuple(a, l) ->(let rec revlist l st = (match l with 
                                                    | []-> st
                                                    | h::t -> revlist t (h::st)) in
                      
                             let rec comlist ls aa = (match ls with 
                                              |[] -> [TUPLE (aa)]
                                              | h::tl -> (comlist tl a) @ (revlist (compile(h) ) [] ) ) in

                            revlist (comlist l a) [] 
            )

            (*projecting the i-th component of an expression (which evaluates to an n-tuple, and 1 <= i <= n) *)
            |Project((a1, a2), t) ->((compile t) @ [PROJ(a1,a2)])


(*This function calculates the value of the given exptree*)
let rec stackmc st rho op = match op, st with 
                |[], x::y -> x
                |[], _ -> raise(Error "There is some error stack is empty")


                |NCONST(a)::tl, _ -> stackmc (Num(a)::st) rho tl
                |BCONST(b)::tl, _ -> stackmc (Bool(b)::st) rho tl
                |VAR(s)::tl, _ -> stackmc ((rho s)::st) rho tl

                (*Arithmetic Operation calculated here*)
                |PLUS::tl, x1::x2::t -> (match x1, x2 with
                                         | Num(a), Num(b) -> stackmc (Num(add a b)::t) rho tl
                                         | _, _ -> raise(Error "Type Error")  )                                      
                |PLUS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                |MINUS::tl, x1::x2::t -> ( match x1, x2 with
                                         | Num(a), Num(b) -> stackmc (Num(sub a b)::t) rho tl
                                         | _, _ -> raise(Error "Type Error"))
                |MINUS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |MULT::tl, x1::x2::t -> ( match x1, x2 with
                                         | Num(a), Num(b) -> stackmc (Num(mult a b)::t) rho tl
                                         | _, _ -> raise(Error "Type Error"))
                |MULT::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |DIV::tl, x1::x2::t -> ( match x1, x2 with
                                         | Num(a), Num(b) -> stackmc (Num(div a b)::t) rho tl
                                         | _, _ -> raise(Error "Type Error"))
                |DIV::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |REM::tl, x1::x2::t -> ( match x1, x2 with
                                         | Num(a), Num(b) -> stackmc(Num(rem a b)::t) rho tl
                                         | _, _ -> raise(Error "Type Error"))
                |REM::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")
                
                |UNARYMINUS::tl, x1::t -> (match x1 with
                                          |Num(a)-> stackmc (Num(minus a)::t) rho tl
                                          |_ -> raise(Error "Expected type bigint") )
                |UNARYMINUS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")6
                
                |ABS::tl, x1::t -> (match x1 with
                                          |Num(a)-> stackmc (Num(abs a)::t) rho tl
                                          |_ -> raise(Error "Expected type bigint") )
                |ABS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")


                (*Boolean Operation calculated here*)
                |NOT::tl, x1::t -> (match x1 with 
                                    |Bool(x1) -> if(x1 = true) then stackmc (Bool(false)::t) rho tl else stackmc (Bool(true)::t) rho tl
                                    |_ -> raise(Error "Expected Bool type") )
                |NOT::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                |CONJ::tl, x1::x2::t -> (stackmc ((conjuction x1 x2)::t) rho tl)
                |CONJ::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                |DISJ::tl, x1::x2::t -> stackmc ((disjuction x1 x2)::t) rho tl
                |DISJ::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                (*Comparison operations on integers*)
                |EQS::tl, x1::x2::t -> (match x1, x2 with
                                        |Num(a), Num(b) -> stackmc ((Bool(eq a b))::t) rho tl
                                        |_, _ -> raise(Error "Type Error") )
                |EQS::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                |GTE::tl, x1::x2::t -> (match x1, x2 with
                                        |Num(a), Num(b) -> stackmc ((Bool(geq a b))::t) rho tl
                                        |_, _ -> raise(Error "Type Error") )
                |GTE::tl, _-> raise(Error "Stack is empty and operand cann't be fetched")

                |LTE::tl, x1::x2::t -> (match x1, x2 with
                                        |Num(a), Num(b) -> stackmc ((Bool(leq a b))::t) rho tl
                                        |_, _ -> raise(Error "Type Error") )
                |LTE::tl, _-> raise(Error "Stack is empty and operand cann't be fetched")

                |GT::tl, x1::x2::t ->  (match x1, x2 with
                                        |Num(a), Num(b) -> stackmc ((Bool(gt a b))::t) rho tl
                                        |_, _ -> raise(Error "Type Error") )
                |GT::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                |LT::tl, x1::x2::t ->  (match x1, x2 with
                                        |Num(a), Num(b) -> stackmc ((Bool(lt a b))::t) rho tl
                                        |_, _ -> raise(Error "Type Error") )
                |LT::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                (*Parentheses and other operations*)
                |PAREN::tl, x1::t -> stackmc (x1::t) rho tl
                |PAREN::tl, _ ->raise(Error "Stack is empty and operand cann't be fetched")

                (*Tuple*)
                |TUPLE(a)::tl, t ->  (let rec makelist t count = (match t, count with
                                                                 |[], c when(c>0)->raise(Error "Answer stack not of enought length")
                                                                 |_, c when(c=0 )-> []
                                                                 |h::t1, c -> h::makelist t1 (c-1) ) in
                                                                 
                                                                 let rec revlist l st = (match l with 
                                                                                        | []-> st
                                                                                        | h::t -> revlist t (h::st)) in

                                    stackmc (Tup(a,revlist (makelist t a) [])::t) rho tl )
                |TUPLE(a)::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                (*Projection*)
                |PROJ(i, n)::tl, h::t ->let rec get_nth list1 count = (match list1, count with
                                                 | [], _ -> raise (Error "get_nth")
                                                 | _, nn when (nn <= 0) -> raise (Error "get_nth")
                                                 | (x::_), 1 -> x
                                                 | (x::xs), nn -> (get_nth xs (nn - 1)))  in

                                          let geti h1 n1 i1 = (match h1 with
                                                                 | Tup(a, b) when (a = n1) -> (get_nth ( revlistg b []) i1)
                                                                 | _ -> print_int(n1);raise(Error "Tuple of appropriate length not found") ) in
                                          
                                          (geti h (n) i) 
                |PROJ(i, n)::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")

                (* If then Else*)
                |IFTE::tl, x1::x2::x3::t -> (match x1 with 
                                   |Bool(a) -> if(a = true)then ( stackmc (x2::t) rho tl ) 
                                               else ( stackmc (x3::t) rho tl )
                                   |_ -> raise(Error "Condition not of bool type") )
                |IFTE::tl, _ -> raise(Error "Stack is empty and operand cann't be fetched")



                
                            