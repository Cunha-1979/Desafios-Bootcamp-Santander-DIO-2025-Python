param(
    [string]$command,
    [string]$d
)

switch ($command) {
    "run" {
        uvicorn workout_api.main:app --reload
    }
    "create-migrations" {
        $env:PYTHONPATH="$PWD"
        alembic revision --autogenerate -m $d
    }
    "run-migrations" {
        $env:PYTHONPATH="$PWD"
        alembic upgrade head
    }
    default {
        Write-Host "Comando inválido: $command"
    }
}
