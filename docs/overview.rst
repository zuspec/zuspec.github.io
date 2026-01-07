Overview
========

The Abstraction Gap and Model Fragmentation
--------------------------------------------

The abstraction gap and model fragmentation are two key drivers of hardware
design-flow complexity. The abstraction difference between a 
natural-language design specification and the register-transfer-level (RTL) 
model that implements it is enormous, and only increasing as designs 
become larger and more complex. It's natural to prioritize the 
RTL model, since that is required to get to implementation. However, 
because RTL models are detailed and execute slowly, they don't do a good job of
meeting the needs of adjacent disciplines, such as firmware. 
This delays how early software teams obtain access to a representation of the design,
and limits the platforms on which they can work to fast hardware emulation
or prototyping environments.

Over time, new requirements have resulted in the development of new 
domain-specific languages and language-like class libraries. SystemVerilog, 
PSS, UPF, IP-XACT, SystemC, and others all provide features that address pain 
points of hardware development. Unfortunately, this has also led to a very 
fragmented ecosystem with loosely-integrated languages and methodologies and 
complex build flows.

Considering the Ecosystem
--------------------------

All of these innovations have primarily come from a hardware-design 
perspective, and focus on enabling hardware-design flows. That,
in itself, is a challenge given the relative sizes of the 
hardware- and software-engineering ecosystems. While it's 
difficult to find accurate detailed data, US Bureau of Labor 
Statistics reports a labor-market size of 76,800 for hardware 
engineers vs a labor-market size of 1,534,790 for software 
engineers (inclusive of all sub-disciplines in both cases). 

Given that the collective challenge is a combined hardware and 
software system, getting buy-in from both disciplines is critical.
It seems quite unlikely that a language created to serve the unique
requirements of the ecosystem's minority can serve the combined
needs and gain the acceptance of the majority.

Why Zuspec?
-----------

Zuspec adopts Python as its starting point, and embeds hardware semantics 
into that ecosystem. The result is a platform that is familiar to software 
engineers, offers high productivity for hardware engineering, and has the goal 
of increasing the ability to share artifacts across the disciplines.

Why Python?
~~~~~~~~~~~

Many factors are involved in selecting a language for any purpose: 
key language features, tool ecosystem, relevant libraries, as well
as the community around the language. Applying an existing language to the 
semantics of another domains raises another factor to consider: 
flexibility of the language. 

Python is a popular language overall, holding the top spot in many
rankings for several consecutive years, and being ranked highly 
for many years before that. Language popularity has a direct bearing on 
language technical features. Larger communities produce more ideas for using 
a language and, thus, a larger library ecosystem. Larger communities more-rapidly
produce and refine adjacent technologies, such as code development and package 
management tools, and new language features.

Popularity often builds upon itself, and there is evidence that 
AI is acting as a driver of Python's popularity.
Specifically, AI assistants are often reported to be more 
effective with Python than with other languages. This has the effect of 
drawing more developers to Python, which increases the available code in 
Python, which more-rapidly increases the quality of results with Python.

Multi-Abstraction Modeling
---------------------------

Zuspec provides a unified framework for modeling hardware at multiple levels 
of abstraction:

* **Transfer Function Level**: High-level behavioral models for early software 
  development and architectural exploration
* **Transaction Level**: Cycle-approximate models for performance analysis
* **Register Transfer Level**: Synthesizable hardware descriptions

This multi-abstraction approach allows teams to:

* Start software development earlier with fast executable models
* Refine designs incrementally from high-level to detailed implementations
* Maintain consistency across abstraction levels
* Reuse test content across different model abstractions

Key Features
------------

* **Python-Native**: Leverage the entire Python ecosystem including libraries, 
  tools, and IDE support
* **Multiple Backends**: Generate SystemVerilog RTL, C/C++ software models, 
  and verification frameworks
* **Dataclass-Based**: Use familiar Python dataclass syntax for hardware 
  modeling
* **Type-Safe**: Static type checking for hardware constructs
* **Extensible**: Plugin architecture for custom backends and transformations

Getting Started
---------------

To get started with Zuspec, see the :doc:`installation` guide and explore the
:doc:`packages/zuspec-dataclasses/index` documentation for the core language.

For a comprehensive overview, see the :doc:`papers` section which includes the
full academic paper on Zuspec.
