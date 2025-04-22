#!/usr/bin/env bash
function compare_array() {
    read -ra ARRAY1 <<< $1
    read -ra ARRAY2 <<< $2
    declare -a ARRAY3=()
    for i in "${ARRAY1[@]}"; do
        if ! printf '%s\0' "${ARRAY2[@]}" | grep -Fxqz -- $i; then
            ARRAY3+=($i)
        fi
    done
    echo ${ARRAY3[@]}
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
        MISSING_OPTS=($(compare_array "${CREATE_OPTS[*]}" "${COMP_WORDS[*]}"))
        COMPREPLY=($(compgen -W "${MISSING_OPTS[*]}"))
        return
    fi
    # TODO: Above doesn't work very well for multiple options (`td add --opt1<tab>` becomes `td add --opt2<tab>`)
    # TODO: All the other commands
}

complete -F completion_todo td
