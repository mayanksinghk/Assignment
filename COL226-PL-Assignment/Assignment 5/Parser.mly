%{
    open Krivine
    exception Exp of string
%}


%token <int> INT
%token <bool> BOOL
%token <string> ID
%token MULT PLUS AND OR CMP IFTE LAMBDA IF THEN ELSE FI EOF RP LP
%start exp_parser
%type <Krivine.expr> exp_parser 
%%

exp_parser:
    fcall EOF                                        { $1 }
  | fcall                                            { $1 }
;
fcall:
    fabs LP fcall RP                      { App($1,$3) }
  | fabs                                  { $1 }
  | LP fcall RP                           { $2 }
;

fabs:
    LAMBDA ID fabs                        { Lambda(V($2),$3) }
  | or_exp                                { $1 }
;

or_exp:
    or_exp OR and_exp                     { Or($1,$3) }
  | and_exp                               { $1 }
;
and_exp:
    and_exp AND add_exp                   { And($1,$3) }
  | add_exp                               { $1 }
;
add_exp:
    add_exp PLUS mult_exp                 { Plus($1,$3) }
  | mult_exp                              { $1 }
;
mult_exp:
    mult_exp MULT ifte_expression         { Mult($1,$3) }
  | ifte_expression                       { $1 }
;
ifte_expression:
    IF exp_parser THEN exp_parser ELSE exp_parser FI           { If_Then_Else($2,$4,$6) }
  | cmp_expression                                             { $1 }
;
cmp_expression:
    CMP constant                                               { Cmp($2) }
  | constant                                                   { $1 }
;
constant:
    ID                                              { V($1) }
  | INT                                             { Integer($1) }
  | BOOL                                            { Bool($1) }
;
