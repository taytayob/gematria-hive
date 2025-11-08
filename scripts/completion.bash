# Bash completion for Gematria Hive
# Source this file or add to ~/.bash_completion.d/

_gematria_hive() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    opts="run test commit status push pull branch merge rebase"
    
    # Subcommands
    case "${prev}" in
        run)
            COMPREPLY=($(compgen -W "kanban internal-api agents ingestion pipeline" -- "${cur}"))
            return 0
            ;;
        test)
            COMPREPLY=($(compgen -W "all agents core integration api kanban" -- "${cur}"))
            return 0
            ;;
        commit)
            COMPREPLY=($(compgen -W "feat: fix: docs: refactor: test: chore:" -- "${cur}"))
            return 0
            ;;
        status)
            COMPREPLY=($(compgen -W "git system services agents" -- "${cur}"))
            return 0
            ;;
        branch)
            COMPREPLY=($(compgen -W "create list delete switch" -- "${cur}"))
            return 0
            ;;
    esac
    
    # Default completion
    if [[ ${cur} == -* ]]; then
        COMPREPLY=($(compgen -W "${opts}" -- "${cur}"))
    else
        COMPREPLY=($(compgen -W "${opts}" -- "${cur}"))
    fi
}

# Complete for gematria-hive command
complete -F _gematria_hive gematria-hive
complete -F _gematria_hive gh

# Complete for scripts
_gematria_scripts() {
    local cur
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    
    if [ -d "scripts" ]; then
        COMPREPLY=($(compgen -W "$(ls scripts/*.sh 2>/dev/null | xargs -n1 basename | sed 's/\.sh$//')" -- "${cur}"))
    fi
}

complete -F _gematria_scripts ./scripts/

