
type sign = Neg | NonNeg
type bigint = Bigint of sign*int list



(*Functions to print  bigint number*)
(*function for printing the int list*)
let rec print_list l = match l with 
     [] -> ""
    |hd::tl -> string_of_int(hd)^print_list tl;;

(*Function to print the value of the bigint*)
let print_n b = match b with 
    Bigint(x,y) -> if(x = Neg) then "Neg "
                   else "NonNeg ";;

let print_num b = match b with 
        Bigint(x, y)->  let show = print_n b in
                        let showlist  = print_list y in 
                        show^showlist;;


(*For printing boolean value on the screen*)
let print_bool b = match b with 
             true -> print_endline("true")
            | _ -> print_endline("false");;



(*function to convert int to int list*)
let rec int_to_list a acc = let temp = a/10 in 
                        let re = a mod 10 in
                       if(temp = 0) then re::acc else int_to_list temp (re::acc);;
                       
(* function to convert int to bigint*)
let rec mk_big a = if( a >= 0) then Bigint(NonNeg,(int_to_list a [])) 
                   else Bigint(Neg,(int_to_list (-1*a) []));;






(*helping functions for other functions*)

(*Calculating the length of the list*)
let rec len_list l = match l with 
         [] -> 0
        |h::t -> 1+len_list(t);;

(*removing extra 0 in the begining of the list*)
let rec remove_zero l1 = match l1 with 
                        []->[0]
                        |h::t -> if(h = 0) then (remove_zero(t)) 
                                 else (h::t);;


(*Reversing the list*)
let rec rev l acc = match l with
                []->acc
               |h::t -> rev t (h::acc);;

let rev_list l = rev l [];;



(*making the length of the input equal*)
let rec equal_len l1 l2 = if(len_list(l1)> len_list(l2)) then (equal_len (l1) (0::l2))
                          else if (len_list(l1)<len_list(l2)) then (equal_len (0::l1) (l2))
                          else (l1, l2);;

(*Concatinating 2 list l1 and l2 to give [l1;l2] *)
let concat l1 l2 =let nw_l1 = remove_zero l1 in  
                  let nl1 = rev_list nw_l1 in  
                  let rec concatinate newl1 l2 = match newl1 with
                                               [] -> l2
                                              |[0] -> l2 
                                              |h::t -> concatinate t (h::l2)
                  in
                  concatinate nl1 l2;;

(*Extracting x values from the tuple*)
let extract_x a = match a with (x ,y) -> x;; 

(*Extracting y values from the tuple*)
let extract_y a = match a with (x,y) -> y;;

(*Defining an error for any exception *)
exception Error of string ;;






(*Comparison operations for list*)

(*comparing list of equal sizes*)
let rec check l1 l2 = match l1,l2 with 
                |[], [] -> 0
                |h1::t1, h2::t2 -> if(h1>h2) then 1
                                   else if(h2>h1) then -1
                                    else check t1 t2;;

(*comparing the list for greater, equality, and less than the given list*)
let cmplist l1 l2 = 
        if(len_list(l1) > len_list(l2)) then 1
        else if(len_list(l2) > len_list(l1)) then -1
           else     check l1 l2;;

(*returns 1 if the list are equal else returns -1*)
let eql l1 l2 = if((cmplist l1 l2) = 0) then 1
                else -1;;

(*returns 1 if l1 > l2 else returns -1*)
let gtl l1 l2 = if((cmplist l1 l2) = 1) then 1
                else -1;;

(*returns 1 if l1 < l2 else returns -1*)
let ltl l1 l2 = if((cmplist l1 l2) = -1) then 1 
                else -1;;

(*returns 1 if l1 >= l2 else it returns -1*)
let geql l1 l2 = if((cmplist l1 l2) > (-1)) then 1
                 else -1;;

(*returns -1 if l1 <= l2 else it returns -1*)
let leql l1 l2 = if((cmplist l1 l2) < 1) then 1
                 else -1;;






(*Arithmetic Operations for the list*)

(*Code for Addition*)

(*Addition of list*)
let sum a b = let new_a = rev_list a in
              let new_b = rev_list b in 
              let rec isum a b c = match a, b with 
               |[],[] -> if c = 0 then [] else [c]
               |[], x | x, [] -> isum [0] x c
               |ah::at, bh::bt -> let s = ah+bh+c in
                               (s mod 10) :: isum at bt (s/10)
               in
              let revans =  isum new_a new_b 0 in
              rev_list revans;;    

(*Addition code Ends here *)




(* Subtraction Code Start*)

(*Subtraction of a single integer b form a *)
let int_sub a b c = let ans = a-b-c in  
                    if(a >= b+c) then (ans, 0)
                    else (ans+10, 1);;    

(*subtraction for the list assuming that if l1 - l2 then l1 > l2 and lenght(l1)=length(l2) *)
let rec isub a b carry = match a, b with 
             [], [] -> []
             |h1::y1, h2::y2 -> let x = extract_x (int_sub h1 h2 carry) in
                                let y = extract_y (int_sub h1 h2 carry) in  
                                (x::isub y1 y2 y);; 

(*subtracting the given list*)                                   
let sub_list a b = let new_a = extract_x(equal_len a b)in 
                   let new_b = extract_y(equal_len a b)in
                   let x = rev_list new_a in
                   let y = rev_list new_b in 
                   if( (gtl a b ) =  1) then  
                     let z1 = isub x y 0 in 
                     let z = rev_list z1 in
                     remove_zero z
                   else let z1 = isub y x 0 in
                     let z = rev_list z1 in
                     remove_zero z ;; 

(*subtraction Ends here*)


(* Code for Multiplication Starts*)

(*multiplying single number by a list*)
let rec mult l a c = match l with 
                []->[c]
              | h::t -> let res = (a*h + c) in 
                        let carry = ( res/10) in
                        let num = (res mod 10) in
                        (num) ::(mult  t a carry);;

(*multiplying two list l1 and l2 in reverse state both the list*)
let rec mult_list l1 l2 = match l1 with 
                   [] -> []
                 | h::t -> let res = mult l2 h 0 in 
                           let temp = mult_list t l2 in
                           sum res (0::temp);;
                           
(*multiplying 2 list  l1 and l2*)
let multl l1 l2 = let new_l1 = rev_list l1 in
                  let new_l2 = rev_list l2 in
                  let res = mult_list new_l1 new_l2 in
                  let revres = rev_list res in 
                  remove_zero revres;;

(*Multiplication Ends here*)


(* Code for Division Start*)

(*checking how many digit two take from the dividend always len(l1) > len(l2) *)
let rec num_div l1 l2 accu = match l1 with 
                 [] -> (rev_list accu, [])
                |h::t -> if( (geql (rev_list accu) l2) = 1 ) then ( rev_list accu, l1 ) 
                else 
                  let newacc = h::accu in 
                  num_div t l2 newacc;;

(*Checking the quoitent acc=0 also l2>=l1 *)
let rec qut l1 l2 acc = let temp = (sub_list l2 l1) in
                        let newacc = acc+1 in
                       if( (gtl l2 l1 ) = 1 )then (qut l1 temp (newacc)) 
                       else if((geql l2 l1) = 1) then newacc
                       else acc;;
                  
(*dividing two number stored in the list l1/l2 this function returns the quoitent as well as the remainder*)
let rec div_l l1 l2 ac = match l1, l2 with 
                  (_, [])-> raise(Error "cannot divide by [] empty list")
                 |(_, [0]) -> raise(Error "cannot divide by 0")
                 |([],_) -> ((rev_list ac),[0])
                 |(0::t, _) -> div_l t l2 (0::ac)
                 |(_, _) -> let (res_qu, remaning_l1) = num_div l1 l2 [] in                                  (*getting the numbers from the dividend that can be used for dividing*)
                            let single_quo = qut l2 res_qu 0 in                               (*Getting the single digit value of the quoitent*)
                            let store_result = multl (single_quo::[]) l2 in                   (*Multiplying the divisor with the number obtained above to get the number which has to be subtracted*)
                            let modify_l1 = sub_list res_qu store_result in
                            let new_l1 = concat modify_l1 remaning_l1 in
                            if((geql l2 l1) = 1)then ((rev_list (ac)),new_l1)
                            else div_l new_l1 l2 (single_quo::ac);;
                            

let div_list l1 l2 = let new_l1 = remove_zero l1 in
                     let new_l2 = remove_zero l2 in
                     let ans = div_l new_l1 new_l2 [] in
                     match ans with
                      ([], y) -> ([0], y)
                     |(x, []) -> (x, [0])
                     |(x,y) -> (x,y);;

(*Division Ends here*)                     


(*Comparison operation defined for bigint*)

(* checking equality of the bigint*)
let eq b1 b2 = match b1 with 
              Bigint(x,y) -> match b2 with 
                            Bigint(u,v) -> if( u=x ) then 
                                               if((cmplist y v) = 0) then true else false
                                           else  if( y = [] && v = [] )then true
                                                 else false;;


(*checking if b1 < b2 for bigint *)
let lt b1 b2 = match b1 with 
              Bigint(x1, y1) -> match b2 with 
                                Bigint(x2, y2) -> if(x1 = x2) then 
                                                     if(x1 = NonNeg) then 
                                                        if((ltl y1 y2) = 1) then true else false
                                                     else
                                                        if((gtl y1 y2) = 1) then true else true                                                        
                                                  else if(y1 = [] && y2 = []) then false 
                                                  else if(x1 = Neg ) then true 
                                                  else false;;

(*checking if b1>b2 for bigint*)
let gt b1 b2 = match b1 with 
                Bigint(x1, y1) -> match b2 with 
                                  Bigint(x2, y2) -> if(x1 = x2 )then 
                                                      if(x1 = Neg) then 
                                                        if((ltl y1 y2) = 1) then true else false
                                                      else
                                                        if((gtl y1 y2) = 1) then true else false                                                        
                                                    else if(y1 = [] && y2 = []) then false 
                                                    else if(x1 = NonNeg ) then true
                                                    else false;;


(*Checnking if a >= b  for the given bigint a and b*)
let geq b1 b2 = if((gt b1 b2) = true) then true 
                else if((eq b1 b2) = true) then true 
                else false;;


(*Checnking if a =< b  for the given bigint a and b*)
let leq b1 b2 = if((lt b1 b2) = true) then true 
                else if((eq b1 b2) = true) then true 
                else false;;




(*Arithmetic Operation defined for the bigint *)

(*Function for adding 2 bigint*)
 let add b1 b2 = match b1, b2 with
               Bigint(Neg, y1), Bigint(Neg, y2) -> Bigint(Neg , (sum y1 y2))
              |Bigint(NonNeg, y1), Bigint(NonNeg, y2) -> Bigint(NonNeg, (sum y1 y2)) 
              |Bigint(Neg, y1), Bigint(NonNeg, y2) -> if((gtl y1 y2) = 1) then Bigint(Neg, (sub_list y1 y2)) else Bigint(NonNeg, (sub_list y2 y1))
              |Bigint(NonNeg, y1), Bigint(Neg, y2) -> if((gtl y1 y2) = 1) then Bigint(NonNeg, (sub_list y1 y2)) else Bigint(Neg, (sub_list y2 y1));;


(*Function for subtracting 2 bigint b1 - b2*)
let sub b1 b2 = match b1, b2 with 
              Bigint(Neg, y1), Bigint(Neg, y2) -> if((gtl y1 y2) = 1) then Bigint(Neg, (sub_list y1 y2))else Bigint(NonNeg, (sub_list y2 y1))
             |Bigint(NonNeg, y1), Bigint(NonNeg, y2) -> if((gtl y1 y2) = 1) then Bigint(NonNeg, (sub_list y1 y2)) else Bigint(Neg, (sub_list y2 y1))
             |Bigint(Neg, y1), Bigint(NonNeg, y2) -> Bigint(Neg, (sum y1 y2))
             |Bigint(NonNeg, y1), Bigint(Neg, y2) -> Bigint(NonNeg, (sum y1 y2));;

 
(*Function for multiplying 2 bigint*)
let mult b1 b2 = match b1, b2 with 
                 Bigint(x1, y1), Bigint(x2, y2) -> if( x1 = x2 ) then Bigint(NonNeg, (multl y1 y2) ) else Bigint(Neg, (multl y1 y2));;

(*Function for Quotient of 2 bigint b1 and b2 answer is b1/b2*)
let div b1 b2 = match b1, b2 with 
                 Bigint(NonNeg, y1), Bigint(NonNeg, y2) -> Bigint(NonNeg , extract_x(div_list y1 y2))
                |Bigint(Neg, y1), Bigint(NonNeg, y2) -> Bigint(Neg, extract_x(div_list y1 y2))
                |Bigint(NonNeg, y1), Bigint(Neg, y2) -> Bigint(Neg, extract_x(div_list y1 y2))
                |Bigint(Neg, y1), Bigint(Neg, y2) -> Bigint(NonNeg, extract_y(div_list y1 y2));;                                            

(*Function for Remainder of 2 bigint b1 and b2 answer is b1%b2*)
let rem b1 b2 = match b1, b2 with 
                 Bigint(NonNeg, y1), Bigint(NonNeg, y2) -> Bigint(NonNeg , extract_y(div_list y1 y2))
                | Bigint(Neg, y1), Bigint(NonNeg, y2) -> Bigint(Neg, extract_y(div_list y1 y2))
                |Bigint(NonNeg, y1), Bigint(Neg, y2) -> Bigint(NonNeg,  extract_y(div_list y1 y2))
                |Bigint(Neg, y1), Bigint(Neg, y2) -> Bigint(Neg,  extract_y(div_list y1 y2));;


(*Calculating the absolute value*)
let abs x = match x with 
    Bigint(x, y) -> Bigint(NonNeg,y);;


(*Unary Negation*)
let minus x = match x with 
    Bigint(x,y) -> if(x=Neg)then Bigint(NonNeg,y)
                   else Bigint(Neg, y);;
