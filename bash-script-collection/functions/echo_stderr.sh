#!/bin/bash

function echo_stderr () { 
  echo "$@" 1>&2; 
}
# readonly definition of a function throws an error if another function 
# with the same name is defined a second time
readonly -f echo_stderr
[ "$?" -eq "0" ] || return $?
