
ulimit -t 60;

TIMEFORMAT=%R

for f in $(ls tests/sat/*); 
    do 
    echo $f >> sat-results-z3.txt; 
    { time z3 $f >> sat-results-z3.txt; } 2>> sat-results-z3.txt;
    printf "\n" >> sat-results-z3.txt;
    done

