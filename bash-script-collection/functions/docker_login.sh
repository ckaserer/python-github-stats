#!/bin/bash

# source execute.sh

function docker_login () { 
  local docker_user=${1}
  local docker_pass=${2}

  execute "echo \"${docker_pass}\" | docker login -u \"${docker_user}\" --password-stdin" "Docker Login (hidden)"
}
# readonly definition of a function throws an error if another function 
# with the same name is defined a second time
readonly -f docker_login
[ "$?" -eq "0" ] || return $?
