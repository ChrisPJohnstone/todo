#!/usr/bin/env bash
function compare_array() {
    echo "Not Implemented"
}

function completion_todo() {
    declare -a COMMANDS=(
        "add"
        "complete"
        "count"
        "rm"
        "ls"
        "query"
        "show"
        "update"
    )
    declare -a CREATE_OPTS=(
        "--due"
    )
    
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=($(compgen -W "${COMMANDS[*]}" -- "${COMP_WORDS[1]}"))
        return
    fi

    local COMMAND="${COMP_WORDS[1]}"
    if [[ ${COMMAND} == "add" ]]; then
        # TODO: Prevent duplicates
        COMPREPLY=($(compgen -W "${CREATE_OPTS[*]}" -- "${COMP_WORDS[2]}"))
        return
    fi
    # TODO: All the other commands
}

complete -F completion_todo td
