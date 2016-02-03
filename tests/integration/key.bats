#!/usr/bin/env bats

setup() {
    rm ~/.serverauditor.storage || true
    touch key
}

teardown() {
    rm key
}

@test "key help by arg" {
    run serverauditor key --help
    [ "$status" -eq 0 ]
}

@test "key help command" {
    run serverauditor help key
    [ "$status" -eq 0 ]
}

@test "Add general key" {
    run serverauditor key -L test -i key
    [ "$status" -eq 0 ]
    ! [ -z $(cat ~/.serverauditor.storage) ]
}

@test "Add many keys" {
    run serverauditor key -L test_1 -i key
    run serverauditor key -L test_2 -i key
    run serverauditor key -L test_3 -i key
    [ "$status" -eq 0 ]
    ! [ -z $(cat ~/.serverauditor.storage) ]
}

@test "Update key" {
    key=$(serverauditor key -L test -i key)
    run serverauditor key -i key $key
    [ "$status" -eq 0 ]
    ! [ -z $(cat ~/.serverauditor.storage) ]
}

@test "Update many keys" {
    key1=$(serverauditor key -L test_1 -i key)
    key2=$(serverauditor key -L test_2 -i key)
    key3=$(serverauditor key -L test_3 -i key)
    run serverauditor key -i key $key1 $key2 $key3
    [ "$status" -eq 0 ]
    ! [ -z $(cat ~/.serverauditor.storage) ]
}

@test "Delete key" {
    key=$(serverauditor key -L test_1 -i key)
    run serverauditor key --delete $key
    [ "$status" -eq 0 ]
    ! [ -z $(cat ~/.serverauditor.storage) ]
}

@test "Delete many keys" {
    key1=$(serverauditor key -L test_1 -i key)
    key2=$(serverauditor key -L test_2 -i key)
    key3=$(serverauditor key -L test_3 -i key)
    run serverauditor key --delete $key1 $key2 $key3
    [ "$status" -eq 0 ]
    ! [ -z $(cat ~/.serverauditor.storage) ]
}