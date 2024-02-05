# directory "_build";;
# load "StackFrame.cmo";;
# load "Parser.cmo";;
# load "Lexer.cmo";;
open StackFrame;;
open Lexer;;
open Parser;;

let frame1 = Frame("main", [], Tup("a", 6)::Tup("b", 2)::[Tup("c", 3)], []);;
let frame2 = Frame("P", Tup("a", 1)::[Tup("b", 22)], Tup("x", 11)::Tup("y", 12)::[Tup("z", 13)], ["main"]);;
let sf = frame2::[frame1];;

let exp_parser s = Parser.exp_parser Lexer.read (Lexing.from_string s) ;;


(* Interpreter for the assignment 6 *)
let rec demo  sframe =  let () = print_string "---------------------------\n \n" in
                        let () = print_string "1) call a stack \n" in
                        let () = print_string "2) set value of the variable \n" in
                        let () = print_string "3) Return \n" in
                        let () = print_string "4) Show static link \n" in
                        let () = print_string "5) Show variables value (Default value is 0) \n" in
                        let () = print_string "6) Show call stack\n" in
                        let () = print_string "7) what functions can be called \n" in
                        let i = read_int () in
                        if(i = 1)then (* calling another function *)
                          let () = print_string "Enter the command eg. P(3,4) \n" in
                          let callee = read_line() in
                          let pcallee = exp_parser callee in
                          (match sframe with 
                              | [] -> (match pcallee with 
                                        | Cal (n) -> if("main" = n) then demo (add sframe n 0 0) else raise(Foo "Can call only main procedure 1")
                                        | _ -> raise(Foo "Can call only main procedure") )
                              | Frame(name, plist, llist, slink)::t ->  let slinkframes = getFrames slink sframe in 
                                                                        let varlist = getvariables (revlist slinkframes) in
                                                                        (match pcallee with 
                                                                            | Call(n, S(a), S(b)) -> let a1 = get_val_from_tuple_list  a varlist in
                                                                                                    let a2 = get_val_from_tuple_list b varlist in
                                                                                                    if(checkfuncall n name) then demo (add sframe n a1 a2) 
                                                                                                    else let () = print_string "Cannot call this function from here\n" in 
                                                                                                        demo sframe
                                                                            | Call(n, S(a), I(b)) -> let a1 = get_val_from_tuple_list a varlist in
                                                                                                     if(checkfuncall n name) then demo (add sframe n a1 b) 
                                                                                                     else let () = print_string "Cannot call this function from here\n" in 
                                                                                                        demo sframe
                                                                            | Call(n, I(a), S(b)) -> let a2 = get_val_from_tuple_list b varlist in
                                                                                                     if(checkfuncall n name) then demo (add sframe n a a2) 
                                                                                                     else let () = print_string "Cannot call this function from here\n" in 
                                                                                                        demo sframe
                                                                            | Call(n, I(a), I(b)) -> if(checkfuncall n name) then demo (add sframe n a b) 
                                                                                                     else let () = print_string "Cannot call this function from here\n" in 
                                                                                                        demo sframe
                                                                            | Cal (n) ->if(checkfuncall n name) then demo (add sframe n 0 0) 
                                                                                        else let () = print_string "Cannot call this function from here\n" in 
                                                                                        demo sframe 
                                                                            | _ -> raise (Foo "Error ") )  )                       
                        else
                           if( i=2 )then  (* setting the variable of local variable  *)
                            (match sframe with 
                                | [] -> raise(Foo "Currently no frame")
                                | Frame(name, plist, llist, slink)::t ->  let () = print_string "Enter the name of the variable \n" in
                                                                          let n = read_line () in
                                                                          let () = print_string "Enter an integer value \n" in
                                                                          let value = read_int () in
                                                                          let ans = changevariable slink sframe n value in
                                                                          demo ans ) 
                          else
                            if( i = 3) then (* returning from a given function *)
                              let () = print_string "Returning the procedure \n" in
                              (match sframe with
                                | [] -> raise (Foo "Cannot return from the empty Frame")
                                | h::t -> demo t)
                            else
                              if(i = 4)then (* displaying the content of the static link *)
                                (match sframe with 
                                    | [] -> raise (Foo "currently no frame")
                                    | Frame(name, plist, llist, slink)::t -> sprint_list slink ; print_string "\n"; demo sframe)
                              else
                                if( i = 5) then  (*showing the value of all the variables *)
                                  (match sframe with
                                    | [] -> raise (Foo "Error no frame present")
                                    | Frame(name, plist, llist, slink)::t -> let slinkframes = getFrames slink sframe in
                                                                             let varlist = getvariables slinkframes in
                                                                             tprint_list varlist ; print_string "\n"; demo sframe)
                                else
                                  if(i = 6)then
                                    ((print_stack sframe); print_string "\n"; (demo sframe))
                                  else
                                    if( i = 7)then
                                      (match sframe with
                                          | [] -> raise(Foo "Empty stack head")
                                          | Frame(name, plist, llist, slink)::t -> (sprint_list (retcallfun name)); print_string "\n"; (demo sframe))
                                    else
                                      raise (Foo "Bad input")


let start = demo [];;