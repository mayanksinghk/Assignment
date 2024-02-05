open A1
exception Not_implemented
exception Foo of string 

                                                       
let rec cmpelement g g1 = match g1 with
                            | []-> false
                            | h::t -> (match h, g with 
                                         | (s1, t1), (s2,t2) -> if((s1 = s2)&&(t1 = t2)) then true else cmpelement g t ) 
                            
let rec cmplist g1 g2 = match g1 with 
                          | []-> true
                          | h::t -> (cmpelement h g2)&&(cmplist t g2)

 
(*Removing an entry from the table if the string type is matched*)
let rec removesame g st = match g with 
                           | []-> []
                           | h::t -> match h with 
                                         | (s, tl) -> if(s = st) then (removesame t st) else h::(removesame t st) 

(*Removing an entry from the table if the string type is matched*)
let rec removesamelist g g_list = match g_list with 
                           | []-> g
                           | h::t -> match h with 
                                         | (s, tl) -> removesamelist (removesame g s) t


(*Function for checking Var(a) type for a has the give type t or not*)
let rec checktype g s = (match g with
                         | [] -> Tunit
                         
                         | h::l -> (match h with 
                                   |(a, e1) -> let checkstring = (a = s) in
                                               if(checkstring) then e1 else checktype l s ) )



(*function that takes an input current table and an defination and gives the output table after defination*)
and tableupdate g d = match d with 
                            | Simple(s, ty, e) -> (s, ty)::g
                            | Sequence(l) -> (match l with 
                                                 | [] -> g
                                                 | h::t -> tableupdate ((removesamelist g (tableupdate g h))@(tableupdate g h)) (Sequence t) )
                            | Parallel(l) -> (match l with 
                                                 | [] -> g
                                                 | h::t -> (tableupdate (tableupdate g h) (Sequence t) ) )
                            | Local(d1, d2) -> let new_g = tableupdate g d1 in
                                               let new_gd = tableupdate new_g d2 in
                                               (removesamelist new_gd new_g)@g
                     
let rec tablechange g d gnext= match d with 
                            | Simple(s,ty, e) -> (s,ty)::[] 
                            | Sequence(l) -> (match l with 
                                                 | [] -> gnext
                                                 | h::t ->  let typeh = (tablechange g h []) in
                                                            tablechange ((removesamelist g typeh)@typeh) (Sequence t) ((removesamelist gnext typeh)@typeh) )
                            | Parallel(l) -> (match l with 
                                                 | [] -> gnext
                                                 | h::t ->  let typeh = (tablechange g h []) in
                                                            tablechange ((removesamelist g typeh)@typeh) (Parallel t) ((removesamelist gnext typeh)@typeh) )
                            | Local(d1, d2) -> let new_g = tableupdate g d1 in
                                               tablechange new_g d2 []  

let rec tableup g d = match d with
                            | Simple(s, ty, e) -> (s, ty)::g
                            | Sequence(l) -> (match l with 
                                                 | [] -> g
                                                 | h::t -> tableup (tableup g h) (Sequence t) )
                            | Parallel(l) -> g
                            | Local(d1, d2) -> let new_g = tableupdate g d1 in
                                               let new_gd = tableupdate new_g d2 in
                                               (removesamelist new_gd new_g)@g

(*function that returns the correct type of the exptree*)
let rec istype g e = match e with 
                     | Var(a) -> (checktype g a)
                     | N(a) -> Tint
                     | B(a) -> Tbool

                     | Abs(a) -> if(((istype g a)=Tint)) then Tint else Tunit
                     | Negative(a) -> if(((istype g a)=Tint)) then Tint else Tunit
                     | Not(a) -> if(((istype g a)=Tbool)) then Tbool else Tunit

                     | Add(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tint else Tunit
                     | Sub(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tint else Tunit
                     | Mult(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tint else Tunit
                     | Div(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tint else Tunit
                     | Rem(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tint else Tunit

                     | Conjunction(e1, e2) -> if(((istype g e1)=Tbool) && ((istype g e2) = Tbool)) then Tbool else Tunit
                     | Disjunction(e1, e2) -> if(((istype g e1)=Tbool) && ((istype g e2) = Tbool)) then Tbool else Tunit

                     | Equals(e1, e2)-> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tbool else Tunit
                     | GreaterTE(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tbool else Tunit
                     | LessTE(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tbool else Tunit
                     | GreaterT(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tbool else Tunit
                     | LessT(e1, e2) -> if(((istype g e1)=Tint) && ((istype g e2) = Tint)) then Tbool else Tunit

                     | InParen(a) -> (istype g a)

                     | IfThenElse(e1, e2, e3)-> let type1 = (istype g e2) in
                                                let type2 = (istype g e2) in
                                                if(type1 = type2)then type1 else Tunit
                     | Tuple(a1, e1) -> let rec listype l g = (match l with 
                                                               | [] -> []
                                                               | h::tl -> (istype g h)::(listype tl g) ) in
                                          Ttuple(listype e1 g)
                     | Project((a1, a2), e1) -> let type1 = istype g e1 in
                                                (match type1 with 
                                                      | Ttuple(l) -> ((List.nth l (a1-1)) ) 
                                                      | _ -> Tunit)
                     | FunctionCall(e1, e2) -> let type1 = (istype g e1) in
                                               (match type1 with 
                                                     | Tfunc(t1, t2)-> t2
                                                     | _ -> Tunit)
                     | FunctionAbstraction(s,ty, e1)-> let typestring = (checktype g s) in
                                                       Tfunc(typestring, (istype g e1))
                     | Let(d1, e1) -> let new_g = tableup g d1 in
                                      istype new_g e1
 
                                                    


                                               
(* hastype : ((string * exptype) list) -> exptree -> exptype -> bool *)
let rec hastype g e t = match e with 
                       | Var(a) -> if((checktype g a) = t)then true else false
                       | N(a) -> if(t = Tint)then true else false
                       | B(a) -> if(t = Tbool)then true else false

                       | Abs(a) -> hastype g a Tint
                       | Negative(a) -> hastype g a Tint
                       
                       | Not(a) -> hastype g a Tbool

                       | Add(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                        let typea2 = (hastype g a2 Tint) in
                                        (typea1&&typea2&&(t=Tint))
                       | Sub(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                        let typea2 = (hastype g a2 Tint) in
                                        (typea1&&typea2&&(t=Tint))
                       | Mult(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                         let typea2 = (hastype g a2 Tint) in
                                         (typea1&&typea2&&(t=Tint))                                        
                       | Div(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                        let typea2 = (hastype g a2 Tint) in
                                        (typea1&&typea2&&(t=Tint))
                       | Rem(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                        let typea2 = (hastype g a2 Tint) in
                                        (typea1&&typea2&&(t=Tint))

                       | Conjunction(a1, a2) -> let typea1 = (hastype g a1 Tbool) in
                                                let typea2 = (hastype g a2 Tbool) in
                                                (typea1&&typea2&&(t=Tbool))                                        
                       | Disjunction(a1, a2) -> let typea1 = (hastype g a1 Tbool) in
                                                let typea2 = (hastype g a2 Tbool) in
                                                (typea1&&typea2&&(t=Tbool))

                       | Equals(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                           let typea2 = (hastype g a2 Tint) in
                                           (typea1&&typea2&&(t=Tbool))                                                
                       | GreaterTE(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                              let typea2 = (hastype g a2 Tint) in
                                              (typea1&&typea2&&(t=Tbool))
                       | LessTE(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                           let typea2 = (hastype g a2 Tint) in
                                           (typea1&&typea2&&(t=Tbool))
                       | GreaterT(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                             let typea2 = (hastype g a2 Tint) in
                                             (typea1&&typea2&&(t=Tbool))
                       | LessT(a1, a2) -> let typea1 = (hastype g a1 Tint) in
                                          let typea2 = (hastype g a2 Tint) in
                                          (typea1&&typea2&&(t=Tbool))

                       | IfThenElse(e1, e2, e3) -> let type1 = (hastype g e1 Tbool) in
                                                   let type2 = (hastype g e2 t) in
                                                   let type3 = (hastype g e3 t) in
                                                   (type1&&type2&&type3)
                       
                       | InParen(e1) -> hastype g e1 t

                       | Tuple(a1, l) -> let typetuple = istype g e in
                                         (typetuple = t)&&(true)
            
                       | Project((a1, a2), e1) -> let type1 = istype g e1 in
                                                (match type1 with 
                                                      | Ttuple(l) -> ((List.nth l (a1-1)) = t )&& true 
                                                      | _ -> false)

                       | Let(d, e) -> (match d with 
                                         | Parallel(ls) -> let type2 = istype g e in 
                                                            (type2 = t)&&(true)
                                         | _ -> let new_g = tableupdate g d in
                                                let type1 = istype new_g e in
                                                (type1 = t)&&(true) )
                                      
                                      
                       |FunctionAbstraction(s, ty, e1) -> (match t with 
                                                             | Tfunc(t1, t2) -> if((t1 = ty) && (hastype ((s,ty)::g) e1 t2))then true else false
                                                             | _ -> false)

                       |FunctionCall(e1, e2) -> (t = (istype g e))

                                                                                  
(* yields : ((string * exptype) list) -> definition -> ((string * exptype) list) -> bool *)
let rec yields g d g_dash = let g_calculated = tablechange g d [] in
                            (cmplist g_dash g_calculated)&&((List.length g_dash) = (List.length g_calculated))


let rec yield g d g_dash = let g_calculated = tablechange g d [] in
                               g_calculated

(* 
let rec checkdef g d = match d with 
                          | Simple(s, ty, e) -> true
                          | Sequence(l) -> (match l with 
                                                | []-> true
                                                | h::t -> )
                                                 *)