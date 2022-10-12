#!/usr/bin/env bash

pathToGraal="/Library/Java/JavaVirtualMachines/graalvm-ee-java17-22.0.0.2/Contents/Home/bin/java"
pathToBacil="/Users/leskovde/repos/BACIL/launcher/target/bacil-launcher.jar"
pathToCilLibrary="/usr/local/share/dotnet/x64/shared/Microsoft.NETCore.App/6.0.4"
vmOptions="-Dtruffle.class.path.append=/Users/leskovde/repos/BACIL/language/target/language-1.0-SNAPSHOT.jar"

benchmarksDir="`dirname readlink -f "${BASH_SOURCE:-$0}"`/../../Benchmarks"
dlls=$(find $benchmarksDir -name '*.dll')

for dll in $dlls; do
	echo $dll
	cmdText="$pathToGraal $vmOptions -jar $pathToBacil \"--cil.libraryPath=$pathToCilLibrary\" $dll"
	
	echo "Executing: $cmdText"
	eval $cmdText
done
