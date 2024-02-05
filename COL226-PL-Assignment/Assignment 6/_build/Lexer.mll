{
  open Parser
	exception Foo of string
}

let sletter = ['a'-'z']
let lletter = ['A'-'Z']
let letter = (sletter | lletter)
let identifier = "main" | "P" | "Q" | "R" | "S" | "V" | "T" | "U" | "W"
let lett = "a" | "b" | "c" | "x" | "y" | "z" | "w" | "m" | "n" | "i" | "j" | "k" | "h" | "p" | "g"

let digit = ['0'-'9']
let digits = digit+
let ndigit = ['1'-'9']
let integers = ((ndigit+)(digit*) | '0')

rule read = parse
| eof                 { EOF }

| '('                 { LP }
| ')'                 { RP }
| identifier as r     { ID r }
| lett as rr          { PARAMETERS (String.make 1 rr )}
| ','                 { COMMA }
| "="                 { EQUAL }

| integers as i       { INT (int_of_string i)}

| ' '                 { read lexbuf}

| _                   { raise(Foo "Bad Input")}