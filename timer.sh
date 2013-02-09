#!/bin/bash

A="45 30 45"
B="60 60"


for x in $(echo $A $A $B $A $A);
do
    # echo $(( $x * 60 )) "::" $x
    mplayer $HOME/.timebox/bell > /dev/null 2>&1
    sleep $(( $x * 60 ))
done

