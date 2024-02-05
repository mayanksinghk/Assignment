# directory "_build";;
# load "StackFrame.cmo";;
# load "Parser.cmo";;
# load "Lexer.cmo";;
open StackFrame;;
open Lexer;;
open Parser;;

(* let frame1 = Frame("main", Tup("a", 1)::Tup("b", 2)::[Tup("c", 3)], []);;
let frame2 = Frame("P", Tup("a", 1)::Tup("b", 2)::Tup("x", 11)::Tup("y", 12)::[Tup("z", 13)], ["main"]);;
let sf = frame1::[frame2];; *)

let rec pframes sframe = match sframe with 
                          | [] -> print_string ""
                          | Frame(name, llist, slink, locallist)::t -> (print_string name); (print_string ", ") ; (pframes t)

let exp_parser s = Parser.exp_parser Lexer.read (Lexing.from_string s) ;;


(* Interpreter for the assignment 6 *)
let rec demo  sframe =  let () = print_string "---------------------------\n \n" in
                        let () = print_string "1) call an stack \n" in
                        let () = print_string "2) set the value of the variable \n" in
                        let () = print_string "3) Return \n" in
                        let () = print_string "4) Show static link \n" in
                        let () = print_string "5) Show the variables value (Default value is 0) \n" in
                        let () = print_string "6) call stack \n" in
                        let () = print_string "7) Procedures that can be called \n" in
                        let i = read_int () in
                        if(i = 1)then (* calling another function *)
                          let () = print_string "Enter the command eg. P(3,4) \n" in
                          let callee = read_line() in
                          let pcallee = exp_parser callee in
                          (match sframe with 
                              | [] -> (match pcallee with 
                                        | Cal (n) -> if("main" = n) then demo (add sframe n 0 0) else raise(Foo "Can call only main procedure 1")
                                        | _ -> raise(Foo "Can call only main procedure") )
                              | Frame(name, llist, slink, locallist)::t -> let slinkframes = getFrames slink sframe in 
                                                                let varlist = getvariables slinkframes in
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
                                | Frame(name, llist, slink, locallist)::t ->   let () = print_string "Enter the name of the variable \n" in
                                                                    let n = read_line () in
                                                                    let () = print_string "Enter an integer value \n" in
                                                                    let value = read_int () in
                                                                    let ans = change n llist value in
                                                                    demo (Frame(name, ans, slink, locallist)::t) )
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
                                    | Frame(name, llist, slink, locallist)::t -> sprint_list slink ; print_string "\n"; demo sframe)
                              else
                                if( i = 5) then (* show the variables value *)
                                  (match sframe with
                                    | [] -> raise (Foo "Error no frame present")
                                    | Frame(name, llist, slink, locallist)::t -> (*let slinkframes = getFrames slink sframe in
                                                                      let varlist = getvariables slinkframes in *)
                                                                      tprint_list llist ; print_string "\n"; demo sframe)
                                else
                                  if(i = 7 )then
                                    (match sframe with 
                                      | [] -> raise (Foo "Error no frame present")
                                      | Frame(name, llist, slink, locallist)::t -> ((s; (print_string "\n")print_list (retcallfun name)); (print_string "\n");(demo sframe) ) )
                                  else
                                    if( i = 6)then
                                       ((pframes sframe); (print_string "\n"); (demo sframe))
                                    else
                                      raise (Foo "Bad input")


let start = demo [];;