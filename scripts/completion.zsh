# Zsh completion for Gematria Hive
# Add to ~/.zsh/completions/

#compdef gematria-hive gh

_gematria_hive() {
    local -a commands subcommands
    
    commands=(
        'run:Run services (kanban, internal-api, agents, ingestion, pipeline)'
        'test:Run tests (all, agents, core, integration, api, kanban)'
        'commit:Commit changes (feat:, fix:, docs:, refactor:, test:, chore:)'
        'status:Check status (git, system, services, agents)'
        'push:Push to remote'
        'pull:Pull from remote'
        'branch:Manage branches (create, list, delete, switch)'
        'merge:Merge branches'
        'rebase:Rebase branches'
    )
    
    _arguments "1: :->command" "*::arg:->args"
    
    case $state in
        command)
            _describe 'command' commands
            ;;
        args)
            case $words[1] in
                run)
                    _values 'service' 'kanban' 'internal-api' 'agents' 'ingestion' 'pipeline'
                    ;;
                test)
                    _values 'test-type' 'all' 'agents' 'core' 'integration' 'api' 'kanban'
                    ;;
                commit)
                    _values 'type' 'feat:' 'fix:' 'docs:' 'refactor:' 'test:' 'chore:'
                    ;;
                status)
                    _values 'status-type' 'git' 'system' 'services' 'agents'
                    ;;
                branch)
                    _values 'branch-action' 'create' 'list' 'delete' 'switch'
                    ;;
            esac
            ;;
    esac
}

# Complete for scripts
_gematria_scripts() {
    if [ -d "scripts" ]; then
        _files -W scripts -g '*.sh'
    fi
}

compdef _gematria_scripts ./scripts/

