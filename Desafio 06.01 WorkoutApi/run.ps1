<#
.SYNOPSIS
Script de automação para Windows (VSCode) para o projeto WorkoutAPI.
- Detecta virtualenv automaticamente
- Cria migrations Alembic
- Executa migrations Alembic
- Roda Uvicorn com reload
#>

param(
    [string]$command,       # run, create-migrations, run-migrations
    [string]$d             # descrição para create-migrations
)

# Detectar virtualenv automaticamente
if (-not $env:VIRTUAL_ENV) {
    $venvPath = Join-Path $PSScriptRoot ".venv"
    if (Test-Path $venvPath) {
        Write-Host "Ativando virtualenv em $venvPath..."
        & "$venvPath\Scripts\Activate.ps1"
    } else {
        Write-Host "Virtualenv não encontrada. Execute 'python -m venv .venv' primeiro."
        exit 1
    }
} else {
    Write-Host "Virtualenv já ativa: $env:VIRTUAL_ENV"
}

switch ($command) {
    "run" {
        Write-Host "Iniciando Uvicorn..."
        uvicorn workout_api.main:app --reload
    }
    "create-migrations" {
        if (-not $d) {
            Write-Host "Você deve informar a descrição da migration com -d 'mensagem'"
            exit 1
        }
        Write-Host "Criando migration Alembic: $d"
        $env:PYTHONPATH = "$PSScriptRoot\workout_api"
        alembic revision --autogenerate -m $d
    }
    "run-migrations" {
        Write-Host "Executando migrations Alembic..."
        $env:PYTHONPATH = "$PSScriptRoot\workout_api"
        alembic upgrade head
    }
    default {
        Write-Host "Comando inválido. Use: run, create-migrations, run-migrations"
        exit 1
    }
}
