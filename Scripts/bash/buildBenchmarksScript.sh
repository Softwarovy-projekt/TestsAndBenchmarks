#!/usr/bin/env bash

benchmarksDir="`dirname readlink -f "${BASH_SOURCE:-$0}"`/../../Benchmarks"

projects=$(find $benchmarksDir -name '*.csproj')

for project in $projects; do
	echo $project
	dotnet build $project
done
