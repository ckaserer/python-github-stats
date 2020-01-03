#!/bin/bash

echo_stderr () { 
  echo "$@" 1>&2; 
}
readonly -f echo_stderr
[ "$?" -eq "0" ] || return $?
