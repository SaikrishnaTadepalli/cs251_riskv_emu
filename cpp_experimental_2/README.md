The point of this directory is to re-write the proj but make it
function closer to typical computer architecture:

### Architecture

Caches:

- L1 Instruction Cache
- L1 Data Cache
- L2 Cache
- L3 Cache

Memory:

- Unified Memory

CPU:

- 32 General Purpose registers
- Other register (More Notes Here Later)
- CPU calls caches, which pass calls down till memory

### How it will work:

- An the emulator should be called with an ARM64 assembly file
- The emulator will first attempt to assemble the ARM64 code to binary
  - (If the assembly process fails, the emulator throws an error and quits)
- The assembled binary will be placed into main memory starting at location 0x0
- The PC will be set to read instruction 0x0, and all caches & registers will be
  empty (filled with random values) except for XZR, which will contain the value 0x0.
- The PC starts

### Progress
