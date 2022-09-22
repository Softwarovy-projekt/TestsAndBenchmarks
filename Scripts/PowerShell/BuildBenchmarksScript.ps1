$scriptPath = $PSScriptRoot;

$benchmarksDirectory = Join-Path -Path (Get-Item $scriptPath ).parent.parent.FullName -ChildPath "Benchmarks"

$projects = Get-ChildItem -Path $benchmarksDirectory -Include *.csproj -File -Recurse -ErrorAction SilentlyContinue

foreach ($project in $projects)
{
  Write-Host $project
  dotnet build $project
}