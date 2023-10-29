%{
    #include<stdio.h>
    #include<stdlib.h>
    FILE * yyin;
    char * numVar, * counterVar, * var;
    int n = 0, num;

    /***** input format *****
        int main()
        begin
            int count=1;
            while(n>1)
                count=count+1;
                n=n/2;
            end while
            return count
        end
    **********/

%}
%token INT MAIN OPENPARAN CLOSEPARAN BEGINS ENDS WHILE RETURN GREATER EQUAL PLUS DIVIDE NUM ID SEMICOL NL SP
%%
program: INT SP MAIN OPENPARAN CLOSEPARAN NL BEGINS NL stmt ENDS {printf("Valid\n");}
stmt: declstmt whilestmt returnstmt;
declstmt: SP INT SP ID EQUAL NUM SEMICOL NL {counterVar = var; n = num;};
whilestmt: SP WHILE OPENPARAN ID GREATER NUM CLOSEPARAN NL whilebody SP ENDS SP WHILE NL {numVar = var;};
whilebody: SP ID EQUAL ID PLUS NUM SEMICOL NL SP ID EQUAL ID DIVIDE NUM SEMICOL NL;
returnstmt: SP RETURN SP ID NL;
%%

int yyerror(char *s) {
    printf("Invalid\n");
    exit(0);
}

int main(int argc, char * argv[]){
    if(argc != 2){
        printf("USAGE: .\\a.out <input file>\n");
        exit(0);
    }
    yyin = fopen(argv[1], "r");
    yyparse();
    return 0;
}


