# Этот скрипт читает переменные из .env и передаёт их как build-arg в docker build
# Запускать из PowerShell в корне проекта

$envFile = ".env"
$buildArgs = @()

Get-Content $envFile | ForEach-Object {
    if ($_ -match "^([A-Za-z0-9_]+)=(.+)$") {
        $name = $matches[1]
        $value = $matches[2]
        $buildArgs += "--build-arg $name=$value"
    }
}

$buildArgsString = $buildArgs -join " "

$dockerfile = "dockerfile_PM"
$tag = "aster-ssh"

$cmd = "docker build -t $tag -f $dockerfile $buildArgsString ."
Write-Host "Выполняется команда: $cmd"
Invoke-Expression $cmd
