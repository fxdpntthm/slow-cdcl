
ulimit -t 60;

TIMEFORMAT=%R

for f in $(ls tests/unsat/*); 
    do 
    echo $f >> unsat-results-z3.txt; 
    { time z3 $f >> unsat-results-z3.txt; } 2>> unsat-results-z3.txt;
    printf "\n" >> unsat-results-z3.txt;
    done

