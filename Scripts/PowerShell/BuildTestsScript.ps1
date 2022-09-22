$scriptPath = $PSScriptRoot;

$testsDirectory = Join-Path -Path (Get-Item $scriptPath ).parent.parent.FullName -ChildPath "Tests"

$projects = Get-ChildItem -Path $testsDirectory -Include *.csproj -File -Recurse -ErrorAction SilentlyContinue

foreach ($project in $projects)
{
  Write-Host $project
  dotnet build $project
}