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
%token ABS TILDA NOT PLUS MINUS TIMES DIV REM CONJ DISJ EQ GT LT LP RP IF THEN ELSE FI COMMA PROJ
LET IN END BACKSLASH DOT DEF SEMICOLON PARALLEL LOCAL EOF
%start def_parser exp_parser
%type <A1.definition> def_parser /* Returns definitions */
%type <A1.exptree> exp_parser /* Returns expression */
%%
/* The grammars written below are dummy. Please rewrite it as per the specifications. */



/* Implement the grammar rules for definitions, which may use the parser for expression  */

/* Implement the grammar rules for expressions, which may use the parser for definitions */
exp_parser:
      bool_disjunction EOF             { $1 }          /* $n on the rhs returns the value for nth symbol in the grammar on lhs */
     | EOF                              { raise(Foo "Error")}
;

bool_disjunction:
      bool_disjunction DISJ bool_conjunction { Disjunction($1, $3)}
    | LET def IN bool_disjunction END         { Let($2, $4)}
    | bool_disjunction LP bool_disjunction RP { FunctionCall($1, $3)}
    | BACKSLASH ID DOT bool_disjunction       { FunctionAbstraction($2, $4)}
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

r_expression:
      r_expression REM abs_expression    { Rem($1,$3) }
    | r_expression TIMES abs_expression  { Mult($1,$3) }
    | r_expression DIV abs_expression    { Div($1,$3) }
    | abs_expression                     { $1 }
;

abs_expression:
      ABS abs_expression                  { Abs($2) }
    | TILDA abs_expression                { Negative($2) }
    | ifthen_expression                   { $1 }
;

ifthen_expression:
      IF bool_disjunction THEN bool_disjunction ELSE bool_disjunction FI { IfThenElse($2,$4,$6)}
    | proj_expression                                                    { $1 }
;

proj_expression:
      PROJ LP INT COMMA INT RP bool_disjunction { Project(($3, $5),$7)}
    | tuple_expression                                                    { $1 }

tuple_expression: 
       LP expression RP                      { Tuple(getf($2),gets($2)) }
     | paren_expression                        { $1 }    
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

def_parser:
  def EOF { $1 }
| EOF     {raise (Foo "Error")}
;

def:
  simple_def          {$1}
| para_def            {$1}
| seq_def             {$1}
;

seq_def:
  sequence_def SEMICOLON simple_def {match $1 with 
                                      Sequence(l1) -> Sequence(l1@[$3])
                                      |_           -> Sequence($1::[$3])
                                    }
;

sequence_def:
 simple_def    {Sequence([$1])}
|para_def      {$1}
|sequence_def SEMICOLON simple_def  {let Sequence(l1) = $1 in Sequence(l1@[$3])}
;

para_def:
  parallel_def PARALLEL simple_def {match $1 with 
                                      Parallel(l1) -> Parallel(l1@[$3])
                                      |_           -> Parallel($1::[$3])
                                    }
;

parallel_def:
 simple_def    {Parallel([$1])}
|seq_def       {$1}
|parallel_def PARALLEL simple_def  {let Parallel(l1) = $1 in Parallel(l1@[$3])}
;

simple_def:
  DEF ID EQ bool_disjunction    {Simple($2, $4)}
| LOCAL def IN def END          {Local($2, $4)}
;
