#!/bin/zsh
#######################
## get param or ask about it.
#
function print_list() {
    i=1
    print "\t:-:"
    for v in $*; do
        print "\t:$i: $v"
        (( i++))
    done
    print "\t:-:"
}

function ask() {
    # takes:
    #   value
    #   message
    #   list of possible values
    if (( $# < 3 )); then 
        print "ask() needs more args, ARRRRRRG"
        exit
    fi
    msg=$1
    shift
    val=$1;
    shift
    var=$1;
    shift
    list=($*)
    asked=0
    while [[ -z $list[(r)$val] ]]; do
        asked=1
        print_list $list
        print -n $msg " "
        read val
        if [[ $val =~ "[[:digit:]]+" ]]; then
            val=$list[$val]
        fi
    done
    eval ${var}=$val
    if (( asked == 1 )); then
        print "You chose: $val"
        echo '-----------------\n'
    fi
}

