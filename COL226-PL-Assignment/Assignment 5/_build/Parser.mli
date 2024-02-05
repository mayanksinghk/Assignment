type token =
  | INT of (int)
  | BOOL of (bool)
  | ID of (string)
  | MULT
  | PLUS
  | AND
  | OR
  | CMP
  | IFTE
  | LAMBDA
  | IF
  | THEN
  | ELSE
  | FI
  | EOF
  | RP
  | LP

val exp_parser :
  (Lexing.lexbuf  -> token) -> Lexing.lexbuf -> Krivine.expr
