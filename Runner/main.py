import argparse
import glob
import os
import signal
import subprocess
import threading
import time
import psutil

from subprocess import Popen

from Record import Record

parser = argparse.ArgumentParser(description="CILOSTAZOL Benchmark Runner")
parser.add_argument("--cilostazol", help="Path to the CILOSTAZOL launcher",
                    default="../../CILOSTAZOL-100mg/launcher/target/launcher.jar")
parser.add_argument("--cilostazolLanguage", help="Path to the CILOSTAZOL language",
                    default="../../CILOSTAZOL-100mg/language/target/cil-language.jar")
parser.add_argument("--dotnet", help="Path to the .NET runtime", default="dotnet")
parser.add_argument("--dotnetLibrary", help="Path to the .NET library",
                    default="/usr/local/share/dotnet/shared/Microsoft.NETCore.App/7.0.3/")
parser.add_argument("--benchmarks", help="Path to the benchmarks", default="../Benchmarks")


def clean(benchmarks_path):
    print("Cleaning executables...")
    executables = glob.glob("bin/*")
    for executable in executables:
        os.remove(executable)


def build_executables(benchmarks_path):
    print("Building executables...")
    project_files = glob.glob(benchmarks_path + "/**/*.csproj", recursive=True)
    for project_file in project_files:
        subprocess.call([args.dotnet, "build", "-c=Release", "-o=bin", project_file], stdout=subprocess.DEVNULL)
    executables = glob.glob("bin/*.dll")

    assert len(executables) == len(project_files), "Number of executables does not match number of projects"
    return executables


def run_cilostazol_benchmark(executable, num_iterations=3):
    print("Running CILOSTAZOL benchmark: " + executable)
    results = []
    for i in range(num_iterations):
        results.append(
            run_command("[CILOSTAZOL] " + executable, ["java", "-Dtruffle.class.path.append=" + args.cilostazolLanguage,
                                                      "-jar", args.cilostazol,
                                                      "--cil.libraryPath=" + args.dotnetLibrary,
                                                      executable]))

    summarize(results)


def run_dotnet_benchmark(executable, num_iterations=3):
    print("Running .NET benchmark: " + executable)
    results = []
    for i in range(num_iterations):
        results.append(run_command("[DOTNET] " + executable, [args.dotnet, executable]))

    summarize(results)


def summarize(results):
    if len(results) == 0:
        return

    avg_elapsed = sum([result.elapsed for result in results]) / len(results)
    avg_mem = sum([result.maxMem for result in results]) / len(results)
    mid_cpu = results[len(results) // 2].cpuLoad
    max_mem = max([result.maxMem for result in results])
    print("Benchmark " + results[0].name + ":")
    print("\tAverage elapsed time [s]: " + str(avg_elapsed))
    print("\tAverage memory usage [kB]: " + str(avg_mem))
    print("\tCPU usage mid-run [%]: " + mid_cpu)
    print("\tMax memory usage [kB]: " + str(max_mem))
    print("\n")


def run_command(name, command, maxtime=300, delay=0.1):
    # Sample thread will be destroyed when the forked process _exits
    class Sample(threading.Thread):

        def __init__(self, program):
            threading.Thread.__init__(self)
            self.daemon = True
            self.timedout = False
            self.p = program
            self.maxMem = 0
            self.childpids = None
            self.start()

        def run(self):
            try:
                remaining = maxtime
                while remaining > 0:
                    mem = psutil.Process(self.p).memory_info().rss
                    time.sleep(delay)
                    remaining -= delay
                    # race condition - will child processes have been created yet?
                    self.maxMem = max((mem + self.childmem()) / 8 / 1024, self.maxMem)
                else:
                    self.timedout = True
                    os.kill(self.p, signal.SIGKILL)
            except Exception:
                pass

        def childmem(self):
            try:
                if self.childpids == None:
                    self.childpids = set()
                    for pid in psutil.pids():
                        if pid == self.p:
                            self.childpids.add(pid)
                mem = 0
                for pid in self.childpids:
                    mem += psutil.Process(pid).memory_info().rss
                return mem
            except Exception:
                return 0

    try:
        m = Record(name)

        # gtop cpu is since machine boot, so we need a before measurement
        cpus0 = psutil.cpu_times(percpu=True)
        start = time.time()

        # spawn the program in a separate process
        p = Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # start a thread to sample the program's resident memory use
        t = Sample(program=p.pid)

        # wait for program exit status and resource usage
        rusage = os.wait3(0)

        # gtop cpu is since machine boot, so we need an after measurement
        elapsed = time.time() - start
        cpus1 = psutil.cpu_times(percpu=True)

        if t.timedout:
            m.setTimedout()
        elif rusage[1] == os.EX_OK:
            m.setOkay()
        else:
            m.setError()

        m.userSysTime = rusage[2][0] + rusage[2][1]
        m.maxMem = t.maxMem

        load = map(
            lambda t0, t1:
            int(round(
                100.0 * (1.0 - float(t1.idle - t0.idle) / (
                        t1.user + t1.system + t1.idle + t1.nice - t0.user - t0.system - t0.idle - t0.nice))
            ))
            , cpus0, cpus1)

        # load.sort(reverse=1) # maybe more obvious unsorted
        m.cpuLoad = ("% ".join([str(i) for i in load])) + "%"

        m.elapsed = elapsed

    except KeyboardInterrupt:
        os.kill(p.pid, signal.SIGKILL)

    except Exception as e:
        print("Error: %s" % e)
        m.setError()

    finally:
        return m


def main(args):
    clean(args.benchmarks)
    executables = build_executables(args.benchmarks)
    for executable in executables:
        run_dotnet_benchmark(executable)
        run_cilostazol_benchmark(executable)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
