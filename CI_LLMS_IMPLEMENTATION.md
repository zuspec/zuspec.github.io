# CI and llms.txt Implementation Summary

## Overview

Updated the CI workflow to build and deploy Sphinx documentation with automatic llms.txt generation. The llms.txt file provides comprehensive LLM-friendly documentation covering both user-facing Zuspec usage and backend processing details.

## Changes Made

### 1. Created `generate-llms-txt.py`

A standalone Python script that generates the llms.txt file with comprehensive documentation:

**Content Coverage**:
- **User-Facing (How to use Zuspec)**:
  - Components and structure (Component, Bundle, Struct, PackedStruct)
  - Type system (width-annotated integers, structural types, communication types)
  - Field decorators (input/output, const, bundle/mirror/monitor, port/export, inst)
  - Process decorators (@process, @sync, @comb, @invariant)
  - Synchronization primitives (posedge, negedge, edge, locks)
  - Parameterization with const fields and lambda expressions
  - Binding mechanism via __bind__
  - Profile system (PythonProfile, RetargetableProfile)

- **Backend Processing (How to process Zuspec)**:
  - IR (Intermediate Representation) data model structure
  - Core IR types (Context, DataType hierarchy, Field, Bind, Function, Process)
  - Statement and expression AST nodes
  - Backend processing workflow (validate → generate → compile → test)
  - Backend-specific details (SW/C, SystemVerilog, HDLSim, Trace, FV)
  - Visitor pattern for IR traversal

- **Common Patterns**:
  - Register file examples
  - TLM communication examples
  - RTL counter examples

**Output**: 15KB, 521 lines of concise documentation

### 2. Updated `Makefile`

Added `generate-llms` target and integrated it into the build process:

```makefile
build-docs:
	cd docs && $(MAKE) html
	rm -rf web
	cp -r docs/_build/html web
	touch web/.nojekyll
	$(MAKE) generate-llms

generate-llms:
	@echo "Generating llms.txt..."
	python3 generate-llms-txt.py
	@mkdir -p web
	cp llms.txt web/llms.txt
	@echo "✓ llms.txt generated and copied to web/"
```

**Key Features**:
- Runs automatically as part of `make` (via build-docs target)
- Can be run standalone with `make generate-llms`
- Ensures web directory exists before copying
- Cleans llms.txt with `make clean`

### 3. Updated `.github/workflows/ci.yaml`

Modernized CI workflow with Sphinx documentation build and llms.txt generation:

**Key Changes**:
- Updated to use modern GitHub Actions (checkout@v4, setup-python@v5)
- Switched from git submodules to IVPM for package management
- Uses `uvx ivpm update -a` to fetch anonymous package dependencies
- Builds Sphinx documentation (replacing Jekyll)
- Generates llms.txt automatically
- Verifies llms.txt was created before deployment
- Deploys to GitHub Pages with clean deployment

**Workflow Steps**:
1. Checkout code (without submodules)
2. Setup Python 3.11
3. Install system dependencies (pandoc, LaTeX)
4. Install Python dependencies (uv, Sphinx requirements)
5. Fetch packages with `uvx ivpm update -a`
6. Build documentation and generate llms.txt via `make`
7. Verify llms.txt exists in web/
8. Deploy web/ to gh-pages branch

## File Locations

- **Generator Script**: `/generate-llms-txt.py`
- **Source llms.txt**: `/llms.txt` (generated, git-ignored)
- **Published llms.txt**: `https://zuspec.github.io/llms.txt` (deployed to web/)

## Testing

Verified locally:
```bash
# Clean build
make clean

# Generate llms.txt
make generate-llms
# Output: llms.txt (15KB) and web/llms.txt created

# Full build
make
# Builds papers, Sphinx docs, generates llms.txt
```

## Deployment

On push to `main` branch:
1. CI builds Sphinx documentation
2. CI generates llms.txt from package analysis
3. CI copies llms.txt to web/ root
4. CI deploys web/ to GitHub Pages
5. llms.txt available at https://zuspec.github.io/llms.txt

## Benefits

1. **Automated**: llms.txt generated automatically on every deployment
2. **Comprehensive**: Covers both user usage and backend processing
3. **Concise**: 15KB focused documentation optimized for LLMs
4. **Discoverable**: Published at standard /llms.txt URL
5. **Maintainable**: Single Python script, easy to update content
6. **Modern CI**: Uses latest GitHub Actions and best practices

## Future Enhancements

Possible improvements:
- Dynamic content extraction from actual package sources
- Version-specific llms.txt for different releases
- Additional sections for advanced topics
- Integration with package documentation builds
