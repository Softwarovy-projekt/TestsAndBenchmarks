# TestsAndBenchmarks

The repo contains tests & benchmarks used to develop Cilostazol.

## How to contribute

Add C# test project to `Tests` folder. Feel free to add it as a nested directory. The build scripts find out `.csproj` files on any level.  

Add C# benchmark project to `Benchmarks` folder. Feel free to add it as a nested directory. The build scripts find out `.csproj` files on any level.  

## How to use it

Building

> Windows

```cmd
cd <root-dir-of-the-repository>
./Scripts/PowerShell/BuildTestsScript.ps1
```

> Linux 

```cmd
cd <root-dir-of-the-repository>
./Scripts/bash/BuildTestsScript.sh
```

Running

> TODO: some script which takes Cilostazol and .NET, runs all the tests/benchmarks and compares results.

> For now: Pick arbitrary .dll of test/benchmark and give it as an argument to Cilostazol (See Project Cilostazol for more info).

## More info

### Benchmarks

Downloaded from [benchmarksgame-team.pages.debian.net](https://benchmarksgame-team.pages.debian.net/benchmarksgame/).

#### Removed Benchmarks due to an unsupported API

- fannkuchredux/fannkuchredux.csharp-7.csharp
- fannkuchredux/fannkuchredux.csharp-9.csharp
- fasta/fasta.csharp
- fasta/fasta.csharp-5.csharp
- knucleotide/knucleotide.csharp
- knucleotide/knucleotide.csharp-6.csharp
- mandelbrot/mandelbrot.csharp
- mandelbrot/mandelbrot.csharp-9.csharp
- nbody/nbody.csharp-4.csharp
- nbody/nbody.csharp-6.csharp
- nbody/nbody.csharp-7.csharp
- nbody/nbody.csharp-9.csharp
- pidigits/pidigits.csharp-7.csharp
- regexredux/regexredux.csharp-5.csharp
- regexredux/regexredux.csharp-5.csharp
- revcomp/revcomp.csharp-5.csharp
- revcomp/revcomp.csharp-6.csharp
- revcomp/revcomp.csharp-7.csharp
- revcomp/revcomp.csharp-8.csharp
- spectralnorm/spectralnorm.csharp-5.csharp
- pididigits/pididigits/pididigits.csharp-4.csproj
- pididigits/pididigits/pididigits.csharp-5.csproj
- pididigits/pididigits/pididigits.csharp-6.csproj