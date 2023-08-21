# TestsAndBenchmarks

The repo contains benchmarks used to evaluate the correctness and performance of Cilostazol during complex tasks.

## How to run the tests

Run `Runner/main.py` with the following arguments:

```
  --cilostazol <Path to the CILOSTAZOL launcher>
  --cilostazolLanguage <Path to the CILOSTAZOL language>
  --dotnet <Path to the .NET runtime> (Default: dotnet)
  --dotnetLibrary <Path to the .NET library> (E.g., Microsoft.NETCore.App/x.y.z)
  --benchmarks <Path to the benchmarks> (Default: ../Benchmarks)

```

The script will run all tests and benchmarks in the provided path, both on the .NET runtime and on Cilostazol.
After multiple runs, it will print the average execution time of each test and benchmark.

Example:

```
Benchmark [CILOSTAZOL] binarytrees-2.dll:
	Average elapsed time [s]: 209.10286704699197
	Average memory usage [kB]: 318340.1666666667
	CPU usage mid-run [%]: 30% 28% 24% 22% 91% 84% 25% 13%
	Max memory usage [kB]: 488770.5
```

## Benchmarks

Downloaded from [benchmarksgame-team.pages.debian.net](https://benchmarksgame-team.pages.debian.net/benchmarksgame/).
