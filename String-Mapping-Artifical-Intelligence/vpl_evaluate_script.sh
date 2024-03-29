#/bin/bash
. vpl_environment.sh
ls
unzip *.zip > /dev/null
orig_dir=$(pwd)
first_par=${VPL_SUBFILE0%.*}
cd $first_par
ls
echo '_____________________________________________'
printf "Checking writeup.txt\n"
if python $orig_dir/writeup_checker.py ./writeup.txt; then
    printf "Proceeding for further checks\n"
else
    printf "Not proceeding for further checks\n"
    exit 0
fi
echo '_____________________________________________'

file_arr=(inputfile1.txt inputfile2.txt inputfile3.txt)
printf "Running compile.sh : \n"
chmod +x compile.sh
if timeout 30s ./compile.sh; then
    printf "\n"
    echo "____Runnning against input files____"
    chmod +x run.sh
    for input_file in ${file_arr[@]};
    do
        execution=$(timeout 0.2m ./run.sh $orig_dir/$input_file $orig_dir/output.txt 2>&1) # equivalent to 0.2 mins time limit in input files
        exit_status=$?
        if [ $exit_status -eq 124 ] #timeout occured
        then
            printf "Execution Timeout (>12 secs) while evaluating $inputfile\n\n"
            printf "Inputfile was \n"
            cat $input_file

        elif [ $exit_status -eq 0 ] #No runtime error occured (Correct or wrong answer)
        then
            printf "Executed run.sh for $input_file :\n"
            printf "$execution\n\n"
            printf "Running format checker \n"
            python3 $orig_dir/format_checker.py $orig_dir/$input_file $orig_dir/output.txt

        else #some error occured for this test case
            printf "Runtime Error: $execution\n\n"
            printf "Input file was \n"
            cat $orig_dir/$input_file
        fi
        
        echo '_____________________________________________'
    done

else
    echo "compilation failed/timed out"
fi
