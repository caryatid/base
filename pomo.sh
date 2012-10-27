#!/bin/zsh

#######################
## modules

zmodload zsh/system
zmodload zsh/zselect
zmodload zsh/datetime

#######################
## countdown timer
## nice things:
##		- default timer sets
##		- run arbitray commands
##		- display
##		- pipe-able output
##		- interaction
##		- loop over timer set
## 		- set time unit

#######################
## options
time_set=(1 5)
end_command="print all over"
output="display"
help="pomo is a countdown timer
	options are:
		-h : this help
		-s : provide time sets
		-c : provide timer end command
		-d : change the display type
		-l : turn on looping of time sets"
loop=1 # off
unit="minutes"
cur_timer=1
past_time=0
quanta=.1

while getopts "hs:c:d:l" opt; do
	case $opt in 
		h) print $help ;;
		s) time_set=${OPTARG} ;;
		c) end_command=${OPTARG} ;;
		d) output=${OPTARG} ;;
		## TODO - check for valid output setting
		l) lool=0 ;; # on 
	esac
done


#######################
## event loop
# 	- consumes list of times
get_cur_span() {
	print -n  $(( $time_set[$cur_timer] * 60 ))
}
run_timer() {
	if [[ $past_time -lt $(get_cur_span) ]]; then
		start_time=$EPOCHSECONDS
		# TODO real output
	#	print -n "\r" $past_time " : " $( get_cur_span )
                output
		sleep ${quanta}
		past_time=$((past_time + EPOCHSECONDS - start_time))
        else
                print "end"
	fi
}
spin_pos=1
spin=('/' '-' '\' '|')
output() {
        print -n "\r     "  $spin[$(( (spin_pos % 4) + 1 ))] " : " $past_time " of  " $( get_cur_span )
        spin_pos=$(( spin_pos + 1 ))
}
         

handle_event() {
	print $1
}
test_fun () {
	print $1
}

run_loop() {
	while :; do
		sysread -i 0 -t 0 input
		case $? in 
			1|2|3|5) exit ;;
			0) handle_event $input ;;
			4) run_timer ;;
		esac
	done
}


run_loop

