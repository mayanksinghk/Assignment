%{
    open StackFrame
    exception Exp of string
%}

%token <int> INT
%token <bool> BOOL
%token <string> ID
%token <string> PARAMETERS
%token  EOF RP LP COMMA INT EQUAL
%start exp_parser
%type  <StackFrame.funcall>exp_parser 
%%

exp_parser:
      fcall EOF               { $1 }
    | fcall                   { $1 }
;

fcall: 
      ID LP constant COMMA constant RP           { Call($1, $3, $5) }
    | ID LP RP                                    { Cal ($1)}
;

constant:
          PARAMETERS     { S($1) }
        | INT            { I($1) }
;