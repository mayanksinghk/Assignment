{ type token =
|   INT of int          (* integer constant, positive or negative w/o leading zeros *)
|  BOOL of bool                (* boolean constant "T" *)

|  ABS                 (* unary operator, "abs" *)
|  PLUS                (* arithmetic plus, "+" *)
|  MINUS               (* arithmetic minus, "-" *)
|  TIMES                 (* arithmetic multiply, "*" *)
|  DIV                 (* integer div, "div" *)
|  REM                 (* remainder, "mod" *)
|  TILDA                 (* unaryminus, "~" *)

|  LP                  (* left paren, "(" *)
|  RP                  (* right paren, ")" *)

|  NOT                 (* boolean NOT, "not" *)
|  CONJ                (* boolean AND, "/\ " *)
|  DISJ                (* boolean OR, "\/" *)


|  EQ                  (* equal to, "=" *)
|  GT                  (* greater than, ">" *)
|  LT                  (* less than, "<" *)


|  IF                  (* keyword "if" *)
|  THEN                (* keyword "then" *)
|  ELSE                (* keyword "else" *)
|  FI                  (* keyword "fi "*)

| COMMA                (* comma for tuples ","*)
| PROJ                 (*Projection*)
| EOF                  (*End of code*)

|  ID of string;;        (* variable identifier, alphanumeric string with first char lowercase *)

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

(*Regular expression for Integer*)
(* let sign = '~' *)
let integers = ((ndigit+)(digit*) | '0')

(*Unary and Binary operators for integer*)
let absolute = "abs"
let plus = ("+")
let minus = ("-")
let mult = ("*")
let div = ("div")
let mod = ("rem")

(*Comparator operator for integers*)
let gta = (">")
let lta = ("<")
let eq = ("=")

(*Parantheses*)
let rp = ')'
let lp = '('


(*Boolean operators and symbols for true and false*)
let boolt = 'T' 
let boolf = 'F' 
let boolnot = ("not")
let booland = ("/\\")
let boolor = "\\/"

(*keywords for conditional operator*)
let cif = "if "
let cthen = "then "
let celse = "else "
let cfi = "fi "

(*EOF, Whitespace, Def and all remaining decalred here*)
let whitespace = ' '


(*Regular expression for Identifier*)
let underscore = '_'
let appostro = '\''
let identifier = (lletter+)(letter |digits |underscore |appostro)*


rule main = parse
|eof                  { EOF::[] }
| integers as i       { INT (int_of_string i):: main lexbuf}
| boolt               { (BOOL (true)) :: main lexbuf}
| boolf               { (BOOL (false)) :: main lexbuf}

| absolute            { ABS :: main lexbuf }
| plus                { PLUS :: main lexbuf }
| minus               { MINUS :: main lexbuf }
| mult                { TIMES :: main lexbuf }
| div                 { DIV :: main lexbuf }
| mod                 { REM :: main lexbuf }

| rp                  { RP :: main lexbuf }
| lp                  { LP :: main lexbuf }

| booland             { CONJ :: main lexbuf }
| boolor              { DISJ :: main lexbuf }
| boolnot             { NOT :: main lexbuf }

| gta                 { GT :: main lexbuf }
| lta                 { LT :: main lexbuf }
| eq                  { EQ :: main lexbuf }

| cif                 { IF :: main lexbuf }
| cthen               { THEN :: main lexbuf }
| celse               { ELSE :: main lexbuf }
| cfi                 { FI :: main lexbuf }

| identifier as r     { (ID r):: main lexbuf }

| whitespace          { main lexbuf}

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