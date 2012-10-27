#!/bin/zsh
#######################
## rysnc a list of dirs to somewhere, maybe even here
#  sends dirs to target or target to dirs
##
# use rsync files-from files to specify dirs
# they are transferred with data to destination[s]
#  
# Should take much context as a given. Just be lost if out of depth

# program passes itself around with it's transfers.
# this causes every use on all machines to be 
# remembered  globally.
## 
# purpose is to bind data and a something to manipulate it
# sync_dir is where sync rules all. "~/.sync" by default
# push/pull is determined by the target. If a pull then use 
# file_list from source

source ./ask.sh
help="
    sync_dirs.sh  <command> {file_list} <rsync args> source target
        commands:
            list: lists filters and file lists
            dry: dry run
            run: do it
"

function list_sync() {
    typeset -U ftypes
    for x in $files[*]; do
        ftypes+=($x)
    done
    for x in $ftypes; do 
        print $x ":"
        for key in ${(k)files}; do
            if [[ $files[$key] == $x ]]; then
                print "\t$key"
            fi
        done
    done
}

function run() {
    from="${list}.${files[$list]}"
    opts=("-rv"  "--files-from=$from" "--filter=merge $filter")
    rsync $opts[@] --dry-run  $*
    print -n "Ok to run? "
    read ok
    if [[ $ok == (y|Y)* ]]; then
        rsync $opts[@] $*
    fi
    # all additional arguments to the program are passed to rsync
}

function edit_list() {
    blah=$($EDITOR ${list}.${files[$list]})
    # catching output makes wait on editor proc
    #
    print_files
}

function print_files() {
    print_list $( cat ${list}.${files[$list]});
}

typeset -A files
for file in *; do
    if [[ -d $file ]]; then
        print "don't put dirs here"
    fi
    files[$file:r]=$file:e
done
typeset -a cmd_list
typeset cmd 
cmd_list=('list' 'run' 'edit' 'print' 'help')
filter="global.filter"

cmd=$1
if [[ ! (($1 =~ '[/.]') || ( -z $1 )) ]]; then
    shift
else
    cmd="NULL"
fi
ask "What command should we run?" $cmd cmd $cmd_list 

list=$1
if [[ ! (($1 =~ '[./]') || ( -z $1 )) ]]; then
   shift
else
    list="NULL"
fi
ask "Which file list, my liege?" $list list ${(k)files[(R)sync]}

case $cmd in
    'list') list_sync; exit;;
    'run')  run $*;;
    'edit') edit_list;;
    'print') print_files;;
    'help') print $help;;
esac

