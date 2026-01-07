# zuspec.github.io

Web presence for Zuspec - a Python-based multi-abstraction hardware modeling language.

## Overview

This repository contains the Zuspec project website, built with Sphinx and hosted on GitHub Pages.

## Building Locally

### Prerequisites

- Python 3.8 or later
- pandoc (for PDF generation)
- LaTeX (for PDF generation)

### Setup

1. Install Python dependencies:
```bash
pip install -r docs/requirements.txt
pip install ivpm
```

2. Install project dependencies:
```bash
python3 -m ivpm update --anonymous-git
```

### Build

Build the main documentation:
```bash
make
```

This will:
1. Generate PDFs from markdown sources in `papers/`
2. Build Sphinx documentation to `docs/_build/html`
3. Copy the built documentation to `web/`
4. Create a `.nojekyll` file for GitHub Pages

The output will be in the `web/` directory.

### Building Package Documentation (Optional)

Individual packages have their own documentation in `packages/*/docs/`. To build these:

```bash
# Build all available package docs
./build-package-docs.sh

# Copy package docs to web output
make copy-package-docs
```

Note: Package documentation is optional and requires each package's dependencies to be installed.

### Clean

To clean build artifacts:
```bash
make clean          # Clean main docs only
make clean-all      # Clean main docs and all package docs
```

## Documentation Structure

The documentation is organized as follows:

- **docs/** - Main Sphinx documentation
  - **index.rst** - Main landing page
  - **overview.rst** - Project overview and motivation
  - **installation.rst** - Installation instructions
  - **papers.rst** - Academic papers and publications
  - **packages/** - Documentation for individual packages
    - **zuspec-dataclasses/** - Core language package
    - **zuspec-be-sv/** - SystemVerilog backend
    - **zuspec-be-sw/** - Software (C/C++) backend
    - **zuspec-be-hdlsim/** - HDL simulation backend
    - **zuspec-be-trace/** - Trace generation backend
    - **zuspec-be-fv/** - Formal verification backend

- **papers/** - Source materials for papers
  - **zuspec_pythonic_hw_dev/** - Main paper on Zuspec

- **packages/** - Git submodules of individual Zuspec packages
  - Each package has its own documentation in `docs/` subdirectory
  - Package docs are linked from the main site

## CI/CD

The website is automatically built and deployed to GitHub Pages when changes are pushed to the `main` branch. See `.github/workflows/ci.yaml` for the workflow configuration.

The CI builds:
- Main Sphinx documentation
- Paper PDFs
- Deploys to gh-pages branch

Individual package documentation is built separately in their own repositories.

## Contributing

Contributions are welcome! Please submit issues and pull requests on GitHub.

## License

See the LICENSE file for details.

## Links

- Website: https://zuspec.github.io/
- GitHub Organization: https://github.com/zuspec/
