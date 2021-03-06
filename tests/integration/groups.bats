#!/usr/bin/env bats
load test_helper

setup() {
    clean_storage || true
}


@test "groups help by arg" {
    run termius groups --help
    [ "$status" -eq 0 ]
}

@test "groups help command" {
    run termius help groups
    [ "$status" -eq 0 ]
}

@test "List groups in table format" {
    termius group -L 'test group' --port 2 --username 'use r name'
    run termius groups
    [ "$status" -eq 0 ]
    [ $(get_models_set_length 'group_set') -eq 1 ]
}

@test "List subgroups in a group in table format" {
    parent=$(termius group -L 'test group' --port 2 --username 'use r name')
    child=$(termius group -L 'test group' --parent-group $parent --port 2 --username 'use r name')
    run termius groups $parent
    [ "$status" -eq 0 ]
    [ $(get_models_set_length 'group_set') -eq 2 ]
}

@test "List subgroups in a group" {
    parent=$(termius group -L 'test group' --port 2 --username 'use r name')
    child=$(termius group -L 'test group' --parent-group $parent --port 2 --username 'use r name')
    run termius groups -f csv -c id $parent
    [ "$status" -eq 0 ]
    [ "${lines[1]}" = "$child" ]
    [ "${lines[2]}" = "" ]
    [ $(get_models_set_length 'group_set') -eq 2 ]
}

@test "List subgroups in the root group" {
    parent=$(termius group -L 'test group' --port 2 --username 'use r name')
    termius group -L 'test group' --parent-group $parent --port 2 --username 'use r name'
    termius group -L 'test group' --parent-group $parent --port 2 --username 'use r name'
    run termius groups -f csv -c id
    [ "$status" -eq 0 ]
    [ "${lines[1]}" = "$parent" ]
    [ "${lines[2]}" = "" ]
    [ $(get_models_set_length 'group_set') -eq 3 ]
}

@test "List groups recursivly in subgroup in table format" {
    grandparent=$(termius group -L 'test group' --port 2 --username 'use r name')
    parent=$(termius group -L 'test group' --parent-group $grandparent --port 2 --username 'use r name')
    termius group -L 'test group' --parent-group $parent --port 2 --username 'use r name'
    run termius groups -f csv -c id $grandparent
    [ "$status" -eq 0 ]
    [ "${lines[1]}" = "$parent" ]
    [ "${lines[2]}" = "" ]
    [ $(get_models_set_length 'group_set') -eq 3 ]
}
