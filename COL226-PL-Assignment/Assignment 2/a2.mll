{ type token =
   INT of int          (* integer constant, positive or negative w/o leading zeros *)
|  TRUE                (* boolean constant "T" *)
|  FALSE               (* boolean constant "F" *)

|  ABS                 (* unary operator, "abs" *)
|  PLUS                (* arithmetic plus, "+" *)
|  MINUS               (* arithmetic minus, "-" *)
|  MUL                 (* arithmetic multiply, "*" *)
|  DIV                 (* integer div, "div" *)
|  MOD                 (* remainder, "mod" *)
|  EXP                 (* exponentiation, "^" *)

|  LP                  (* left paren, "(" *)
|  RP                  (* right paren, ")" *)

|  NOT                 (* boolean NOT, "not" *)
|  AND                 (* boolean AND, "/\ " *)
|  OR                  (* boolean OR, "\/" *)

|  EQ                  (* equal to, "=" *)
|  GTA                 (* greater than, ">" *)
|  LTA                 (* less than, "<" *)
|  GEQ                 (* greater than/equal to, ">=" *)
|  LEQ                 (* less than/equal to, "<=" *)

|  IF                  (* keyword "if" *)
|  THEN                (* keyword "then" *)
|  ELSE                (* keyword "else" *)

|  ID of string        (* variable identifier, alphanumeric string with first char lowercase *)
|  DEF                 (* definition construct, "def" *)
|  DELIMITER;;         (* delimiter, ";" *)

exception Foo of string 


let removeplus t = let temp = String.length t in
					if String.get t 0 == '+'
					then int_of_string(String.sub t 1 (temp - 1))
					else
					int_of_string t

}



(*Basics like digits and char declared here*)
let digit = ['0'-'9']
let digits = digit+
let ndigit = ['1'-'9']
let sletter = ['a'-'z']
let lletter = ['A'-'Z']
let letter = sletter | lletter

(*Unary and Binary operators for integer*)
let absolute = "abs"
let plus = ("+")(" " | eof)
let minus = ("-")(" " | eof)
let mult = ("*")(" " | eof)
let div = ("div")(" " | eof)
let mod = ("mod")(" " | eof)
let exp = ("^")(" " | eof)

(*Comparator operator for integers*)
let gta = (">")
let lta = ("<")
let geq = (">=")
let leq = ("<=")
let eq = ("=")

(*Parantheses*)
let rp = ')'
let lp = '('


(*Boolean operators and symbols for true and false*)
let booltrue = 'T'
let boolfalse = 'F'
let boolnot = ("not")(" " | eof)
let booland = ("/\ ")
let boolor = "\\/"

(*keywords for conditional operator*)
let cif = "if "
let cthen = "then "
let celse = "else "

(*EOF, Whitespace, Def and all remaining decalred here*)
let cdef = "def "
let delimiter = ';'
let whitespace = ' '


(*Regular expression for Identifier*)
let identifier = (sletter+)(letter |digits)*

(*Regular expression for Integer*)
let sign = '-' | '+'
let integers = (sign?)((ndigit+)(digit*) | '0')

rule main = parse
| cdef                {DEF :: main lexbuf}  

| integers as i       { INT (removeplus i) :: main lexbuf}
| booltrue            { TRUE :: main lexbuf}
| boolfalse           { FALSE :: main lexbuf}

| absolute            { ABS :: main lexbuf}
| plus                { PLUS :: main lexbuf}
| minus               { MINUS :: main lexbuf}
| mult                { MUL :: main lexbuf}
| div                 { DIV :: main lexbuf}
| mod                 { MOD :: main lexbuf}
| exp                 { EXP :: main lexbuf}

| rp                  { RP :: main lexbuf}
| lp                  { LP :: main lexbuf}

| booland             { AND :: main lexbuf}
| boolor              { OR :: main lexbuf}
| boolnot             { NOT :: main lexbuf}

| gta                 { GTA :: main lexbuf}
| lta                 { LTA :: main lexbuf}
| geq                 { GEQ :: main lexbuf}
| leq                 { LEQ :: main lexbuf}
| eq                  { EQ :: main lexbuf}

| cif                 { IF :: main lexbuf}
| cthen               { THEN :: main lexbuf}
| celse               { ELSE :: main lexbuf}

| identifier as r     { ID r :: main lexbuf}

| delimiter           { DELIMITER :: main lexbuf }
| whitespace          { main lexbuf}
| eof                 { []}

| _                   { raise(Foo "Bad Input")}

{ let scanner s = main ( Lexing.from_string s)  }



(* assuming that we will be given only correct input format
  
   I have assumed that all my operators are space seprated and all the comparison operation 
   are assumed not to be space seprated

counterexamples:
writing scanner ";* /\\/ 52 - 9(;;;)" gives Exception: Failure "bad input".
as "or after and" makes \\ as the escape character causing problems. 
Adding a whitespace takes care of the problem.
There is no such issue with "and after or".

writing scanner "/\\"doesn't terminate the program and we have to stop it manually  (reminder for the case not possible to write the exact test code because it gives error)

writing scanner "\\//\\" doesn't terminate the program and we have to stop it manually (reminder for the case not possible to write the exact test code because it gives error)

writing scannet "/\\\/" gives bad input as a whitespace is expected after or .

writing scanner "3*4" gives bad input as I have considered all the operators must are space separated

*)