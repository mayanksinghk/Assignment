{
  open A3
  exception Not_implemented
	exception Foo of string
}

(*
  Below is a dummy implementation. Please note the following
  - Tokens are defined in A3.mly
  - Return type is token and not token list
  - End of buffer is indicated by EOF token below
  - There is no trailer. The scanner function is written in the wrapper file (test_a3.ml)
*)

(* { type token =
|   INT of int          (* integer constant, positive or negative w/o leading zeros *)
|  TRUE                (* boolean constant "T" *)
|  FALSE               (* boolean constant "F" *)

|  ABS                 (* unary operator, "abs" *)
|  PLUS                (* arithmetic plus, "+" *)
|  MINUS               (* arithmetic minus, "-" *)
|  MUL                 (* arithmetic multiply, "*" *)
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


(* let removeplus t = let temp = String.length t in
					if String.get t 0 == '+'
					then int_of_string(String.sub t 1 (temp - 1))
					else
					int_of_string t *)
} *)



(*Basics like digits and char declared here*)
let digit = ['0'-'9']
let digits = digit+
let ndigit = ['1'-'9']
let sletter = ['a'-'z']
let lletter = ['A'-'Z']
let letter = sletter | lletter

(*Unary and Binary operators for integer*)
let absolute = "abs"
let plus = ("+")
let minus = ("-")
let mult = ("*")
let div = ("div")
let mod = ("mod")

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
let cif = "if"
let cthen = "then"
let celse = "else"
let cfi = "fi"

(*EOF, Whitespace, Def and all remaining decalred here*)
let whitespace = ' '


(*Regular expression for Identifier*)
let underscore = '_'
let appostro = '\''
let identifier = (lletter+)(letter |digits |underscore |appostro)*

(*Regular expression for Integer*)
let sign = '~'
let integers = ((ndigit+)(digit*) | '0')

rule read = parse
| eof                 { EOF }
| integers as i       { INT (int_of_string i)}
| boolt               { BOOL (true)}
| boolf               { BOOL (false)}

| absolute            { ABS }
| "proj"              { PROJ }
| plus                { PLUS }
| minus               { MINUS }
| mult                { TIMES }
| div                 { DIV }
| mod                 { REM }
| ','                 {COMMA}
| sign                {TILDA}

| rp                  { RP }
| lp                  { LP }

| booland             { CONJ }
| boolor              { DISJ }
| boolnot             { NOT }

| gta                 { GT }
| lta                 { LT }
| eq                  { EQ }

| cif                 { IF }
| cthen               { THEN }
| celse               { ELSE }
| cfi                 { FI }

| identifier as r     { ID r }

| whitespace          { read lexbuf}

| _                   { raise(Foo "Bad Input")}



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