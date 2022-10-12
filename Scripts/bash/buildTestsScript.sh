#!/usr/bin/env bash

testsDir="`dirname readlink -f "${BASH_SOURCE:-$0}"`/../../Tests"

projects=$(find $testsDir -name '*.csproj')

for project in $projects; do
	echo $project
	dotnet build $project
done
