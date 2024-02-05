type token =
  | INT of (int)
  | BOOL of (bool)
  | ID of (string)
  | PARAMETERS of (string)
  | EOF
  | RP
  | LP
  | COMMA
  | EQUAL

val exp_parser :
  (Lexing.lexbuf  -> token) -> Lexing.lexbuf -> StackFrame.funcall
