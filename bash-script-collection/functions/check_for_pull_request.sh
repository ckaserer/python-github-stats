#!/bin/bash

function check_for_pull_request () {
  local is_pull_request=${1:-false}
  
  if ${is_pull_request}; then
    echo "Skipping - pull requests can not utilize encrypted variables."
    echo "For further information see: https://docs.travis-ci.com/user/pull-requests/#pull-requests-and-security-restrictions"
    exit 0
  fi
}
# readonly definition of a function throws an error if another function 
# with the same name is defined a second time
readonly -f check_for_pull_request
[ "$?" -eq "0" ] || return $?
