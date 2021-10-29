
import optparse
import sys
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.params import NULL
from m5.util import addToPath, fatal, warn

addToPath('../')

from ruby import Ruby

from common import Options
from common import Simulation
from common import CacheConfig
from common import CpuConfig
from common import ObjectList
from common import MemConfig
from common.FileSystemConfig import config_filesystem
from common.Caches import *
from common.cpu2000 import *

def get_processes(options):
    """Interprets provided options and returns a list of processes"""

    multiprocesses = []
    inputs = []
    outputs = []
    errouts = []
    pargs = []

    workloads = options.cmd.split(';')
    if options.options != "":
        pargs = options.options.split(';')

    np = options.num_cpus
    idx = 0

    for wrkld in workloads:
        for i in range(np):
            process = Process(pid = 100 + idx)
            process.executable = wrkld
            process.cmd = [wrkld] + pargs
            multiprocesses.append(process)
            idx += 1
    return multiprocesses, 1

parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

if '--ruby' in sys.argv:
    Ruby.define_options(parser)

(options, args) = parser.parse_args()

if args:
    print("Error: script doesn't take any positional arguments")
    sys.exit(1)

multiprocesses = []
numThreads = 1

multiprocesses, numThreads = get_processes(options)

(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)
CPUClass.numThreads = numThreads

mp0_path = multiprocesses[0].executable

np = options.num_cpus
system = System(cpu = [CPUClass(cpu_id=i) for i in range(np)],
                mem_mode = test_mem_mode,
                mem_ranges = [AddrRange(options.mem_size)],
                cache_line_size = options.cacheline_size,
                workload = SEWorkload.init_compatible(mp0_path))

# Create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = options.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock =  options.sys_clock,
                                   voltage_domain = system.voltage_domain)
print("system clock =",system.clk_domain)
# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = options.cpu_clock,
                                       voltage_domain =
                                       system.cpu_voltage_domain)

# All cpus belong to a common cpu_clk_domain, therefore running at a common
# frequency.a
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain

for i in range(np):
    system.cpu[i].workload = multiprocesses[i]
    system.cpu[i].createThreads()

Ruby.create_system(options, False, system)

assert(options.num_cpus == len(system.ruby._cpu_ports))
system.ruby.clk_domain = SrcClockDomain(clock = options.ruby_clock,
                                    voltage_domain = system.voltage_domain)
for i in range(np):
    ruby_port = system.ruby._cpu_ports[i]
    system.cpu[i].createInterruptController()
    ruby_port.connectCpuPorts(system.cpu[i])

root = Root(full_system = False, system = system)
Simulation.run(options, root, system, FutureClass)
