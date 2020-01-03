#!/bin/bash

function cmp_regex () {
    local str=${1}
    local pat=${2}
    
    if [[ ${str} =~ ${pat} ]]; then
        return `true`
    else
        return `false`
    fi
}
# readonly definition of a function throws an error if another function 
# with the same name is defined a second time
readonly -f cmp_regex
[ "$?" -eq "0" ] || return $?
