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

open Parsing;;
let _ = parse_error;;
# 2 "Parser.mly"
    open StackFrame
    exception Exp of string
# 18 "Parser.ml"
let yytransl_const = [|
    0 (* EOF *);
  261 (* RP *);
  262 (* LP *);
  263 (* COMMA *);
  264 (* EQUAL *);
    0|]

let yytransl_block = [|
  257 (* INT *);
  258 (* BOOL *);
  259 (* ID *);
  260 (* PARAMETERS *);
    0|]

let yylhs = "\255\255\
\001\000\001\000\002\000\002\000\003\000\003\000\000\000"

let yylen = "\002\000\
\002\000\001\000\006\000\003\000\001\000\001\000\002\000"

let yydefred = "\000\000\
\000\000\000\000\000\000\007\000\000\000\000\000\001\000\006\000\
\005\000\004\000\000\000\000\000\000\000\003\000"

let yydgoto = "\002\000\
\004\000\005\000\011\000"

let yysindex = "\005\000\
\254\254\000\000\002\255\000\000\007\000\255\254\000\000\000\000\
\000\000\000\000\003\255\001\255\004\255\000\000"

let yyrindex = "\000\000\
\000\000\000\000\000\000\000\000\011\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000"

let yygindex = "\000\000\
\000\000\000\000\001\000"

let yytablesize = 13
let yytable = "\008\000\
\003\000\008\000\009\000\010\000\009\000\001\000\007\000\006\000\
\014\000\012\000\002\000\000\000\013\000"

let yycheck = "\001\001\
\003\001\001\001\004\001\005\001\004\001\001\000\000\000\006\001\
\005\001\007\001\000\000\255\255\012\000"

let yynames_const = "\
  EOF\000\
  RP\000\
  LP\000\
  COMMA\000\
  EQUAL\000\
  "

let yynames_block = "\
  INT\000\
  BOOL\000\
  ID\000\
  PARAMETERS\000\
  "

let yyact = [|
  (fun _ -> failwith "parser")
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'fcall) in
    Obj.repr(
# 17 "Parser.mly"
                              ( _1 )
# 89 "Parser.ml"
               : StackFrame.funcall))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'fcall) in
    Obj.repr(
# 18 "Parser.mly"
                              ( _1 )
# 96 "Parser.ml"
               : StackFrame.funcall))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 5 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 3 : 'constant) in
    let _5 = (Parsing.peek_val __caml_parser_env 1 : 'constant) in
    Obj.repr(
# 22 "Parser.mly"
                                                 ( Call(_1, _3, _5) )
# 105 "Parser.ml"
               : 'fcall))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : string) in
    Obj.repr(
# 23 "Parser.mly"
                                                  ( Cal (_1))
# 112 "Parser.ml"
               : 'fcall))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 27 "Parser.mly"
                         ( S(_1) )
# 119 "Parser.ml"
               : 'constant))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : int) in
    Obj.repr(
# 28 "Parser.mly"
                         ( I(_1) )
# 126 "Parser.ml"
               : 'constant))
(* Entry exp_parser *)
; (fun __caml_parser_env -> raise (Parsing.YYexit (Parsing.peek_val __caml_parser_env 0)))
|]
let yytables =
  { Parsing.actions=yyact;
    Parsing.transl_const=yytransl_const;
    Parsing.transl_block=yytransl_block;
    Parsing.lhs=yylhs;
    Parsing.len=yylen;
    Parsing.defred=yydefred;
    Parsing.dgoto=yydgoto;
    Parsing.sindex=yysindex;
    Parsing.rindex=yyrindex;
    Parsing.gindex=yygindex;
    Parsing.tablesize=yytablesize;
    Parsing.table=yytable;
    Parsing.check=yycheck;
    Parsing.error_function=parse_error;
    Parsing.names_const=yynames_const;
    Parsing.names_block=yynames_block }
let exp_parser (lexfun : Lexing.lexbuf -> token) (lexbuf : Lexing.lexbuf) =
   (Parsing.yyparse yytables 1 lexfun lexbuf : StackFrame.funcall)
