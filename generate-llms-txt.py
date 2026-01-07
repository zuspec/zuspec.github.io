#!/usr/bin/env python3
"""
Generate llms.txt file for Zuspec based on packages.

This script analyzes the zuspec-dataclasses package and backend packages
to create a comprehensive LLM-friendly documentation file covering:
- How users should apply Zuspec (decorators, types, patterns)
- How backends should process the resulting description (IR, code generation)
"""

import os
import sys
from pathlib import Path


LLMS_TXT_CONTENT = """# Zuspec: Python-Based Multi-Abstraction Hardware Modeling Language

Zuspec is a Python-embedded DSL for modeling digital hardware from behavioral to RTL abstraction levels. It provides decorators and types for type-safe hardware modeling with support for simulation, verification, and code generation.

## Core Concepts

### 1. Components and Structure

Components are the basic building blocks, defined using `@zdc.dataclass`:

```python
import zuspec.dataclasses as zdc

@zdc.dataclass
class Counter(zdc.Component):
    clock : zdc.bit = zdc.input()
    reset : zdc.bit = zdc.input()
    count : zdc.u32 = zdc.output()
```

Base classes:
- `Component` - Structural hardware components with ports/exports/bindings
- `Bundle` - Interface/port collections with directionality (input/output)
- `Struct` - Data-only types with C-like alignment
- `PackedStruct` - Bitwise packed data structures (for registers/protocols)
- `XtorComponent[T]` - Transactor components with signal and operation interfaces

### 2. Type System

**Width-Annotated Integers** (for hardware synthesis):
- Unsigned: `u1` to `u32`, `u64`, `u128` (or `uint1_t` to `uint32_t`, etc.)
- Signed: `i8`, `i16`, `i32`, `i64`, `i128` (or `int8_t`, `int16_t`, etc.)
- Bit types: `bit`, `bit1` to `bit8`, `bit16`, `bit32`, `bit64`
- Variable width: `bitv`, `bv` (width specified with `width=` parameter)

**Structural Types**:
- `Reg[T]` - Single register with read/write methods
- `RegFile` - Collection of registers with automatic address mapping
- `RegFifo[T]` - FIFO register for buffering
- `Memory` - Memory storage with size
- `AddressSpace` - Software view of memory/registers
- `AddrHandle` - Pointer abstraction for memory access

**Communication Types**:
- `GetIF[T]` / `PutIF[T]` - Basic producer/consumer interfaces
- `Channel[T]` - Bidirectional channel with get/put endpoints
- `ReqRspIF[Treq,Trsp]` - Request-response interface
- `ReqRspChannel[Treq,Trsp]` - Request-response channel

**Synchronization Types**:
- `Lock` - Async mutex for resource synchronization
- `Pool[T]` / `ClaimPool[T]` - Resource pools with arbitration
- `Event` - Interrupt/callback event handling

**Time**:
- `Time.s()`, `Time.ms()`, `Time.us()`, `Time.ns()`, `Time.ps()`, `Time.fs()`

### 3. Field Decorators

**Signal Direction (RTL)**:
```python
clock : zdc.bit = zdc.input()
data_out : zdc.u32 = zdc.output()
data_bus : zdc.bitv = zdc.input(width=lambda s: s.DATA_WIDTH)
```

**Structural Parameters**:
```python
DATA_WIDTH : zdc.u32 = zdc.const(default=32)  # Compile-time parameter
```

**Interfaces**:
```python
# Bundle instantiation with directionality
bus : MyBus = zdc.bundle(kwargs=lambda s: dict(WIDTH=s.DATA_WIDTH))
mirrored : MyBus = zdc.mirror()  # Flipped directionality
mon : MyBus = zdc.monitor()  # Passive monitoring

# Component instantiation
counter : Counter = zdc.inst(kwargs=lambda s: dict(WIDTH=s.WIDTH))
```

**Port/Export Pattern** (for TLM communication):
```python
from typing import Protocol

class ITarget(Protocol):
    async def access(self, addr: zdc.u32, data: zdc.u32) -> zdc.u32: ...

@zdc.dataclass
class Initiator(zdc.Component):
    target : ITarget = zdc.port()  # Consumer of interface

@zdc.dataclass  
class Target(zdc.Component):
    api : ITarget = zdc.export()  # Provider of interface
    
    def __bind__(self):
        return {self.api.access: self.handle_access}
    
    async def handle_access(self, addr: zdc.u32, data: zdc.u32) -> zdc.u32:
        # Implementation
        return zdc.u32(0)
```

### 4. Process Decorators

**Behavioral Process** (async, always running):
```python
@zdc.process
async def run(self):
    while True:
        await self.wait(zdc.Time.ns(10))
        # Process logic
```

**Synchronous Process** (clocked, RTL):
```python
@zdc.sync(clock=lambda s: s.clock, reset=lambda s: s.reset)
def _counter_proc(self):
    if self.reset:
        self.count = 0  # Deferred assignment
    else:
        self.count = self.count + 1
```

**Combinational Process** (immediate, RTL):
```python
@zdc.comb
def _logic(self):
    self.out = self.a ^ self.b  # Immediate assignment
```

**Invariant**:
```python
@zdc.invariant
def _check_bounds(self):
    assert self.count < 1024
```

### 5. Synchronization Primitives

**Edge Detection**:
```python
await posedge(self.clock)  # Wait for rising edge
await negedge(self.clock)  # Wait for falling edge
await edge(self.clock)     # Wait for any edge
```

**Timing**:
```python
await self.wait(zdc.Time.ns(10))  # Wait 10 nanoseconds
```

**Locks**:
```python
async with self.lock:
    # Critical section
    pass
```

### 6. Parameterization

Structural parameters use `const` fields with lambda expressions for width computation:

```python
@zdc.dataclass
class AXI4Lite(zdc.Bundle):
    ADDR_WIDTH : zdc.u32 = zdc.const(default=32)
    DATA_WIDTH : zdc.u32 = zdc.const(default=32)
    
    awaddr : zdc.bitv = zdc.output(width=lambda s: s.ADDR_WIDTH)
    wdata : zdc.bitv = zdc.output(width=lambda s: s.DATA_WIDTH)
    wstrb : zdc.bitv = zdc.output(width=lambda s: int(s.DATA_WIDTH/8))

@zdc.dataclass
class MyComponent(zdc.Component):
    BUS_WIDTH : zdc.u32 = zdc.const(default=64)
    
    axi : AXI4Lite = zdc.bundle(
        kwargs=lambda s: dict(
            ADDR_WIDTH=32,
            DATA_WIDTH=s.BUS_WIDTH))
```

### 7. Binding

Components connect via `__bind__` method returning a dictionary mapping ports to exports:

```python
@zdc.dataclass
class Top(zdc.Component):
    prod : Producer = zdc.field()
    cons : Consumer = zdc.field()
    ch : zdc.Channel[int] = zdc.field()
    
    def __bind__(self):
        return {
            self.prod.output_port : self.ch.put,
            self.cons.input_port : self.ch.get
        }
```

### 8. Profile System

Profiles enforce validation rules for different targets:

```python
from zuspec.dataclasses import profiles

@zdc.dataclass(profile=profiles.PythonProfile)
class SoftwareModel:
    x: int  # Standard Python types OK

@zdc.dataclass(profile=profiles.RetargetableProfile)  
class HardwareModel:
    x: zdc.uint32_t  # Width-annotated types required
```

Built-in profiles:
- `PythonProfile` - Permissive, standard Python types allowed
- `RetargetableProfile` - Strict, requires width-annotated types

## How Zuspec Processes Descriptions

### 1. Data Model (IR)

Zuspec builds an intermediate representation (IR) from decorated Python classes:

```python
import zuspec.dataclasses as zdc

# User writes this:
@zdc.dataclass
class Counter(zdc.Component):
    clock : zdc.bit = zdc.input()
    count : zdc.u32 = zdc.output()

# Generate IR:
dm_factory = zdc.DataModelFactory()
dm_context = dm_factory.build(Counter)
```

The IR (`zuspec.dataclasses.ir` module) contains:

**Core IR Types**:
- `Context` - Top-level container with `type_m` dict mapping qualified names to types
- `DataType` - Base class for all types
  - `DataTypeInt` - Integer types with `bits` and `signed` attributes
  - `DataTypeStruct` - Structs with `fields` and `functions` lists
  - `DataTypeClass` - Classes (polymorphic structs)
  - `DataTypeComponent` - Components with `bind_map`, `sync_processes`, `comb_processes`
  - `DataTypeExtern` - External/blackbox components
  - `DataTypeProtocol` - Interface definitions (from Python Protocol)
  - `DataTypeRef` - Forward reference by name
  - `DataTypeGetIF`, `DataTypePutIF`, `DataTypeChannel` - TLM types

**Fields and Bindings**:
- `Field` - Component/struct field with `name`, `datatype`, `metadata`
  - `FieldKind` enum: `CONST`, `INPUT`, `OUTPUT`, `BUNDLE`, `MIRROR`, `MONITOR`, `PORT`, `EXPORT`, `INST`
  - `SignalDirection` enum: `INPUT`, `OUTPUT`, `INOUT`
- `Bind` - Connection between port and export
- `BindSet` - Collection of bindings

**Functions and Processes**:
- `Function` - Method/function with `name`, `args`, `body`, `returns`, `is_async`
  - `process_kind`: `None`, `ProcessKind.SYNC`, or `ProcessKind.COMB`
  - `sensitivity_list`: List of signals for edge detection
- `Process` - Standalone process with `name` and `body`

**Statements** (IR AST nodes):
- `StmtAssign` - Assignment statement
- `StmtAugAssign` - Augmented assignment (+=, -=, etc.)
- `StmtIf` - If/elif/else
- `StmtFor` / `StmtWhile` - Loops
- `StmtReturn` - Return statement
- `StmtExpr` - Expression statement
- `StmtWith` - Context manager (async with)
- `StmtTry` / `StmtExceptHandler` - Exception handling

**Expressions**:
- `ExprBin` - Binary operation with `BinOp` enum (Add, Sub, Mult, Div, etc.)
- `ExprUnary` - Unary operation with `UnaryOp` enum (Not, UAdd, USub, Invert)
- `ExprCompare` - Comparison with `CmpOp` enum (Eq, NotEq, Lt, Gt, LtE, GtE)
- `ExprBool` - Boolean operation with `BoolOp` enum (And, Or)
- `ExprRef` - Reference (variable, field, parameter)
  - `ExprRefSelf` - Reference to self
  - `ExprRefField` - Field access (obj.field)
  - `ExprRefParam` - Parameter reference
  - `ExprRefLocal` - Local variable
- `ExprConstant` - Literal value
- `ExprCall` - Function call with args and keywords
- `ExprAwait` - Await expression
- `ExprAttribute` / `ExprSubscript` / `ExprSlice` - Access operations

### 2. Backend Processing Workflow

Backends traverse the IR to generate code:

**Step 1: Validate IR**
```python
from zuspec.be.sw import CValidator

validator = CValidator()
errors = validator.validate(dm_context)
if errors:
    for err in errors:
        print(f"Error: {err.message}")
```

**Step 2: Generate Code**
```python
from zuspec.be.sw import CGenerator
from pathlib import Path

generator = CGenerator(output_dir=Path("./output"))
source_files = generator.generate(dm_context)
# Returns list of Path objects for generated .h and .c files
```

**Step 3: Compile (for SW backend)**
```python
from zuspec.be.sw import CCompiler

compiler = CCompiler(output_dir=Path("./output"))
result = compiler.compile(
    sources=source_files,
    output=Path("./output/executable")
)
if result.success:
    print("Compilation successful")
else:
    print(f"Error: {result.stderr}")
```

**Step 4: Run Tests (for SW backend)**
```python
from zuspec.be.sw import TestRunner

runner = TestRunner()
test_result = runner.run(Path("./output/executable"))
print(f"Exit code: {test_result.returncode}")
print(f"Output: {test_result.stdout}")
```

### 3. Backend-Specific Details

**SW Backend (C Code Generation)** (`zuspec.be.sw`):
- `CGenerator` - Main generator class
  - Converts IR to C code (headers + source + main)
  - Includes runtime library (zsp_component.h, zsp_timebase.c, etc.)
  - Handles async/await translation
- `TypeMapper` - Maps Zuspec types to C types
- `StmtGenerator` - Generates C statements from IR
- `DmAsyncMethodGenerator` - Converts async methods to C state machines
- `CCompiler` - Compiles generated C with runtime
- `TestRunner` - Executes compiled binaries

Key runtime files: `zsp_alloc.c`, `zsp_timebase.c`, `zsp_thread.c`, `zsp_component.c`, etc.

**SV Backend (SystemVerilog Generation)** (`zuspec.be.sv`):
- `SVGenerator` - Main SystemVerilog generator
  - Converts IR components to SystemVerilog modules
  - Flattens bundles to individual ports
  - Generates module declarations with proper port lists
  - Sanitizes names for SystemVerilog compatibility

Example usage:
```python
from zuspec.be.sv import SVGenerator

generator = SVGenerator(output_dir=Path("./sv_output"))
sv_files = generator.generate(dm_context)
# Returns list of .sv files
```

**HDLSim Backend** (`zuspec.be.hdlsim`):
- Interfaces with HDL simulators (Verilator, etc.)

**Trace Backend** (`zuspec.be.trace`):
- Generates execution traces (VCD, etc.)

**FV Backend** (`zuspec.be-fv`):
- Formal verification output

### 4. Visitor Pattern

Backends use visitor pattern to traverse IR:

```python
from zuspec.dataclasses.ir import Visitor, DataTypeComponent, Function

class MyBackendVisitor(Visitor):
    def visit_DataTypeComponent(self, comp: DataTypeComponent):
        # Process component
        for field in comp.fields:
            # Process each field
            pass
        for func in comp.functions:
            self.visit(func)
    
    def visit_Function(self, func: Function):
        # Process function
        for stmt in func.body:
            self.visit(stmt)
```

## Common Patterns

### Register File Example

```python
@zdc.dataclass
class MyCtrl(zdc.PackedStruct):
    enable : zdc.u1 = zdc.field()
    mode : zdc.u3 = zdc.field()
    reserved : zdc.u28 = zdc.field()

@zdc.dataclass
class MyRegs(zdc.RegFile):
    ctrl : zdc.Reg[MyCtrl] = zdc.field()  # Offset 0x00
    data : zdc.Reg[zdc.u32] = zdc.field()  # Offset 0x04
    status : zdc.Reg[zdc.u32] = zdc.field()  # Offset 0x08
```

### TLM Communication Example

```python
@zdc.dataclass
class Producer(zdc.Component):
    out : zdc.PutIF[int] = zdc.port()
    
    @zdc.process
    async def run(self):
        for i in range(10):
            await self.out.put(i)
            await self.wait(zdc.Time.ns(10))

@zdc.dataclass
class Consumer(zdc.Component):
    inp : zdc.GetIF[int] = zdc.port()
    
    @zdc.process
    async def run(self):
        while True:
            value = await self.inp.get()
            print(f"Received: {value}")

@zdc.dataclass
class Top(zdc.Component):
    prod : Producer = zdc.field()
    cons : Consumer = zdc.field()
    ch : zdc.Channel[int] = zdc.field()
    
    def __bind__(self):
        return {
            self.prod.out : self.ch.put,
            self.cons.inp : self.ch.get
        }
```

### RTL Counter Example

```python
@zdc.dataclass
class Counter(zdc.Component):
    clock : zdc.bit = zdc.input()
    reset : zdc.bit = zdc.input()
    enable : zdc.bit = zdc.input()
    count : zdc.u32 = zdc.output()
    
    @zdc.sync(clock=lambda s: s.clock, reset=lambda s: s.reset)
    def _counter_proc(self):
        if self.reset:
            self.count = 0
        elif self.enable:
            self.count = self.count + 1
```

## Key Design Principles

1. **Python-Native**: Use Python decorators, type hints, and async/await
2. **Multi-Level**: Support behavioral (PV/TLM) and structural (RTL) abstractions
3. **Type-Safe**: Static type checking via MyPy plugin
4. **Retargetable**: Generate C, SystemVerilog, formal models from single source
5. **Composable**: Components connect via ports/exports with automatic binding
6. **Parameterizable**: Structural parameters with lambda-based width expressions
7. **Profile-Based**: Different validation rules for different targets

## Installation and Usage

```bash
# Install
pip install zuspec-dataclasses

# For MyPy plugin, add to pyproject.toml:
[tool.mypy]
plugins = ["zuspec.dataclasses.mypy.plugin"]

# Generate IR and process
import zuspec.dataclasses as zdc
from zuspec.be.sw import CGenerator

@zdc.dataclass
class MyHardware(zdc.Component):
    clock : zdc.bit = zdc.input()
    data : zdc.u32 = zdc.output()

# Build IR
dm_context = zdc.DataModelFactory().build(MyHardware)

# Generate C code
generator = CGenerator(output_dir="./output")
files = generator.generate(dm_context)
```

## Project URLs

- Website: https://zuspec.github.io/
- GitHub: https://github.com/zuspec/
- Packages: zuspec-dataclasses, zuspec-be-sw, zuspec-be-sv, zuspec-be-hdlsim, zuspec-be-trace, zuspec-be-fv
"""


def main():
    """Generate llms.txt file."""
    script_dir = Path(__file__).parent
    output_file = script_dir / "llms.txt"
    
    print(f"Generating {output_file}...")
    
    # Write the content
    output_file.write_text(LLMS_TXT_CONTENT)
    
    print(f"✓ Generated {output_file}")
    print(f"  Size: {len(LLMS_TXT_CONTENT)} bytes")
    print(f"  Lines: {LLMS_TXT_CONTENT.count(chr(10))} lines")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
