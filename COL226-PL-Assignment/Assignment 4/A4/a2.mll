{
  open A3
  exception Not_implemented
	exception Foo of string
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

(*Assignment 4*)
let letdef = "let"
let indef = "in"
let enddef = "end"
let backs = "\\"
let dot = '.'
let def = "def"
let semidef = ";"
let parallel = "||"
let localdef = "local"

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

| letdef               { LET }
| indef                { IN } 
| enddef               { END }
| backs                { BACKSLASH }
| dot                  { DOT }
| def                  { DEF }
| ';'                  { SEMICOLON }      
| parallel             { PARALLEL }
| localdef             { LOCAL }

| _                   { raise(Foo "Bad Input")}
