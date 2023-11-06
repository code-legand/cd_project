%{
    #include "y.tab.h"
    extern char * var;
    extern int num;
    extern FILE * yyin;
%}
%%
"int" {return INT;}
"main" {return MAIN;}
"(" {return OPENPARAN;}
")" {return CLOSEPARAN;}
"begin" {return BEGINS;}
"end" {return ENDS;}
"while" {return WHILE;}
"return" {return RETURN;}
">" {return GREATER;}
"=" {return EQUAL;}
"+" {return PLUS;}
"/" {return DIVIDE;}
";" {return SEMICOL;}
[ \t]+ {return SP;}
"\n" {return NL;}
[a-zA-Z_][a-zA-Z0-9_]* {var = yytext; return ID;}
[0-9]+ {num = atoi(yytext); return NUM;}
. {return yytext[0];}
%%
int yywrap(){
    return 1;
}

