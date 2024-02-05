%{
    open A1
	exception Foo of string  

    let getf a = match a with
                |(a1, a2) -> a1

    
    let gets a = match a with
                |(a1, a2) -> a2
%}

/*
- Tokens (token name and rules) are modified wrt to A2. Please make necessary changes in A3
- LP and RP are left and right parenthesis
- Write grammar rules to recognize
  - >= <= from GT EQ LT tokens
  - if then else fi
*/
/* Tokens are defined below.  */
%token <int> INT
%token <bool> BOOL
%token <string> ID
%token ABS TILDA NOT PLUS MINUS TIMES DIV REM CONJ DISJ EQ GT LT LP RP IF THEN ELSE FI COMMA PROJ EOF
%start main
%type <A1.exptree> main /* Return type */
%%
/*
DESIGN a grammar for a simple expression language, taking care to enforce precedence rules (e.g., BODMAS)
The language should contain the following types of expressions:  integers and booleans.
*/

main:
      bool_disjunction EOF             { $1 }          /* $n on the rhs returns the value for nth symbol in the grammar on lhs */
    | EOF                              { raise(Foo "Your tree is empty") }
;

bool_disjunction:
      bool_disjunction DISJ bool_conjunction { Disjunction($1, $3)}
    | bool_conjunction                       { $1 }
;

bool_conjunction:
      bool_conjunction CONJ bool_not     { Conjunction($1, $3) }
    | bool_not                           { $1 }
;

bool_not:
       NOT bool_not                       { Not($2)}
     | cmp_expression                     { $1 }
;

cmp_expression:
      cmp_expression LT EQ as_expression { LessTE($1, $4)}
    | cmp_expression GT EQ as_expression { GreaterTE($1, $4)}
    | cmp_expression EQ as_expression    { Equals($1, $3)}
    | cmp_expression LT as_expression    { LessT($1, $3)}
    | cmp_expression GT as_expression    { GreaterT($1, $3)}
    | as_expression                      { $1 }
;    

as_expression:
      as_expression MINUS r_expression { Sub($1,$3) }
    | as_expression PLUS r_expression  {Add($1,$3) }
    | r_expression                     { $1 }
;

/* add_expression:
    LP sub_expression RP                 { PAREN($1,$3) }
    |add_expression PLUS rem_expression  { PLUS($1,$3) }
    |rem_expression                     { $1 }
; */

r_expression:
      r_expression REM abs_expression    { Rem($1,$3) }
    | r_expression TIMES abs_expression  { Mult($1,$3) }
    | r_expression DIV abs_expression    { Div($1,$3) }
    | abs_expression                     { $1 }
;

/* mult_expression:
     LP sub_expression RP                 { PAREN($1,$3) }
     |mult_expression TIMES div_expression { MULT($1,$3) } 
     |div_expression                      { $1 }
;

div_expression:
    LP sub_expression RP                 { PAREN($1,$3) }   
    |div_expression DIV abs_expression   { DIV($1,$3) }
    |ABS abs_expression                  { ABS($1) }
    |TILDA neg_expression                { UNARYMINUS($1) }
; */

abs_expression:
      ABS abs_expression                  { Abs($2) }
    | TILDA abs_expression                { Negative($2) }
    | ifthen_expression                   { $1 }
;

/* neg_expression:
      TILDA neg_expression               { Negative($2) }
    | ifthen_expression                  { $1 }
; */

ifthen_expression:
      IF bool_disjunction THEN bool_disjunction ELSE bool_disjunction FI { IfThenElse($2,$4,$6)}
    | proj_expression                                                    { $1 }
;

proj_expression:
      PROJ LP INT COMMA INT RP bool_disjunction { Project(($3, $5),$7)}
    | tuple_expression                                                    { $1 }

tuple_expression: 
       LP expression RP                      { Tuple(getf($2),gets($2)) }
     | paren_expression                      { $1 }    
;       

expression:
       bool_disjunction COMMA expression     { let (x, y) = $3 in (x+1, $1::y) }
     | bool_disjunction                      { (1, [$1]) }
;

paren_expression:
       LP bool_disjunction RP             { InParen($2) }
     | LP RP                              { Tuple(0,[]) }
     | constant                           { $1 } 
;

constant:
    ID                                   { Var($1) }
    |INT                                 { N($1) }
    |BOOL                                { B($1) }
;
/*
DESIGN a grammar for a simple expression language, taking care to enforce precedence rules (e.g., BODMAS)
The language should contain the following types of expressions:  integers and booleans.
*/