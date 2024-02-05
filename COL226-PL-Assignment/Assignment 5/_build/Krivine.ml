exception Exp of string

type expr = V of string | Lambda of (expr * expr) | App of (expr * expr) | Plus of (expr * expr) | Mult of (expr * expr) |And of (expr * expr) | Or of (expr * expr) 
| Bool of bool | Integer of int | Cmp of expr | If_Then_Else of (expr * expr * expr);;

type opcode = S of string | APP | PLUS | MULT | AND | OR | BOOL of bool | INT of int| CMP | COND of opcode list*opcode list | CLOS of expr*opcode list | RET;;

type env = E of string*answer
and answer = I of int | B of bool | Ansclos of string*opcode list*env list;;

type dump = D of answer list* env list* opcode list;;

type closure = Clos of (expr*table)
and table =  (expr*closure)list;;


(* returns an closure from the list of string*closure *)
  let rec search_list ls st = (match ls with 
                                  | [] -> raise(Exp "Element not found")
                                  | h::t -> (match h with 
                                                | (V(s), Clos(cls)) -> if(s = st)then Clos(cls) else search_list t st
                                                | _ -> search_list t st))
(* Returns the head of the list *)
let gethead l = match l with 
                  | [] -> raise(Exp "Empty list")
                  | h::t -> h 

(* Returns the tail of the list *)
let gettail l = match l with 
                  | [] -> raise(Exp "Empty list")
                  | h::t -> t

let rec search_env l s = match l with 
                           | [] -> raise(Exp "Element not found")
                           | h::t -> (match h with 
                                       | E(st, ans) -> if(st = s)then ans else search_env t s
                                       | _ -> raise(Exp "Type Error"))
(* Implementing krivine implementation here*)
let rec krivine cls st = match cls with
                            | Clos(Integer(i), tb) -> cls
                            | Clos(Bool(b), tb) -> cls
                            | Clos(V(s), tb) -> krivine (search_list tb s) st

                            | Clos(Plus(a1,a2), tb) -> let k1 = krivine (Clos(a1, tb)) st in 
                                                       let k2 = krivine (Clos(a2, tb)) st in
                                                       (match k1, k2 with 
                                                          | Clos(Integer(i1), tb1), Clos(Integer(i2), tb2) -> Clos(Integer(i1+i2),[])
                                                          | _ -> raise(Exp "Type Error"))
                            | Clos(Mult(a1,a2), tb) -> let k1 = krivine (Clos(a1, tb)) st in 
                                                       let k2 = krivine (Clos(a2, tb)) st in
                                                       (match k1, k2 with 
                                                          | Clos(Integer(i1), tb1), Clos(Integer(i2), tb2) -> Clos(Integer(i1*i2),[])
                                                          | _ -> raise(Exp "Type Error"))

                            | Clos(And(a1, a2), tb) -> let k1 = krivine (Clos(a1, tb)) st in 
                                                       let k2 = krivine (Clos(a2, tb)) st in
                                                       (match k1, k2 with 
                                                          | Clos(Bool(i1), tb1), Clos(Bool(i2), tb2) -> Clos(Bool(i1&&i2),[])
                                                          | _ -> raise(Exp "Type Error"))
                            | Clos(Or(a1, a2), tb) -> let k1 = krivine (Clos(a1, tb)) st in 
                                                      let k2 = krivine (Clos(a2, tb)) st in
                                                      (match k1, k2 with 
                                                          | Clos(Bool(i1), tb1), Clos(Bool(i2), tb2) -> Clos(Bool(i1||i2),[])
                                                          | _ -> raise(Exp "Type Error"))

                            | Clos(If_Then_Else(a1, a2, a3), tb) -> let k1 = krivine (Clos(a1, tb)) st in
                                                               let k2 = krivine (Clos(a2, tb)) st in
                                                               let k3 = krivine (Clos(a3, tb)) st in
                                                               (match k1 with 
                                                                  | Clos(Bool(i1), tb1) -> if(i1 = true)then k2 else k3
                                                                  | _ -> raise(Exp "Condition is not of type Bool") )

                            | Clos(Cmp(a), tb) -> let k = krivine (Clos(a, tb)) st in 
                                                  (match k with 
                                                      | Clos(Integer(i), tb) -> if(i>0)then Clos(Bool(true), []) else Clos(Bool(false), [])
                                                      | _ -> raise(Exp "Can only compare integers"))
                                                   
                            | Clos(Lambda(a1, a2), tb) -> (match a1 with 
                                                               | V(s) -> krivine (Clos(a2, (V(s),(gethead st))::tb)) (gettail st)
                                                               | _ -> raise(Exp "Not of type string"))

                            | Clos(App(a1, a2), tb) -> krivine (Clos(a1, tb)) ((Clos(a2, tb))::st)

(* Making an compile opcode list*)
let rec compile e = match e with 
                        | Integer(a) -> INT(a)::[]
                        | Bool(a) -> BOOL(a)::[]
                        | V(s) -> S(s)::[]
                        | Plus(a1, a2) -> (compile a2)@(compile a1)@[PLUS]
                        | Mult(a1, a2) -> (compile a2)@(compile a1)@[MULT]
                        | And(a1, a2) -> (compile a2)@(compile a1)@[AND]
                        | Or(a1, a2) -> (compile a2)@(compile a1)@[OR]
                        | Cmp(a) -> (compile a)@[CMP]
                        | If_Then_Else(a1, a2, a3) -> (compile a1)@[COND((compile a2),(compile a3))]
                        | Lambda(a1, a2) -> [CLOS(a1, (compile a2)@[RET])]
                        | App(a1, a2) -> (compile a1)@(compile a2)@[APP];;

(* Implementing SECD machine here  s = stack   e = enviroment  c = opcode list   d = dump  *)
let rec secd s e c d = match c with
                           | [] -> gethead s
                           | INT(a)::cc -> secd (I(a)::s) e cc d
                           | BOOL(a)::cc -> secd (B(a)::s) e cc d
                           | S(st)::cc -> secd ((search_env e st)::s) e cc d

                           | COND(a1, a2)::cc -> (match s with 
                                             | B(a)::t -> if( a = true )then secd t e (a1@cc) d else secd t e (a2@cc) d  
                                             | _ -> raise(Exp "error due to type mismatch or empty stack error 1") )
                           | PLUS::cc -> (match s with 
                                             | I(a2)::I(a1)::tl -> secd (I(a2+a1)::tl) e cc d
                                             | _ -> raise(Exp "error due to type mismatch or empty stack error 2"))
                           | MULT::cc -> (match s with 
                                             | I(a2)::I(a1)::tl -> secd (I(a2*a1)::tl) e cc d
                                             | _ -> raise(Exp "error due to type mismatch or empty stack error 3"))
                           | AND::cc ->  (match s with 
                                             | B(a2)::B(a1)::tl -> secd (B(a2&&a1)::tl) e cc d
                                             | _ -> raise(Exp "error due to type mismatch or empty stack error 4"))
                           | OR::cc ->   (match s with 
                                             | B(a2)::B(a1)::tl -> secd (B(a2||a1)::tl) e cc d
                                             | _ -> raise(Exp "error due to type mismatch or empty stack error 5"))
                           | CMP::cc -> (match s with 
                                             | I(a)::tl -> if( a>0 )then secd (B(true)::tl) e cc d else secd (B(false)::tl) e cc d
                                             | _ -> raise(Exp "error due to type mismatch or empty stack error 6"))
                           | CLOS(V(st), c)::cc -> secd (Ansclos(st, c, e)::s) e cc d
                           | CLOS(_ , c)::cc -> raise(Exp "Error incorrect type")
                           | APP::cc -> (match s with 
                                             | h1::Ansclos(st, cl, en)::tl -> secd [] ((E(st, h1))::en ) cl (D(tl, e, cc)::d)
                                             | _ -> raise(Exp "Error") )
                           | RET::cc -> let rest = gethead d in
                                        (match rest with 
                                             | D(s1, e1, c1) -> secd ((gethead s)::s1) e1 c1 (gettail d) 
                                             | _ -> raise(Exp "Error"))



(* krivine that takes expt as input *)
let kriv s st = krivine (Clos(s, [])) st;;