# Jupyter Kernel for Bosque Language

A Jupyter kernel implementation for the [Bosque programming language](https://github.com/BosqueLanguage).

## Features

- Execute Bosque code in Jupyter notebooks
- Syntax highlighting for Bosque code
- Error reporting and diagnostics
- Automatic kernel installation

## Requirements

- Python 3.7+
- JupyterLab 4.x
- Bosque compiler

## Installation

Install via pip:

```bash
pip install jupyterlab-bosque-kernel
```

The Bosque kernel will be automatically installed during package installation.

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/brakmic/jupyterlab-bosque-kernel.git
cd jupyterlab-bosque-kernel
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Project Structure

    jupyterlab-bosque-kernel/
    ├── bosque_kernel/
    │   ├── kernelspec/     # Jupyter kernel specification
    │   ├── wrapper.py      # Bosque execution wrapper
    │   └── lexer.py        # Syntax highlighting
    ├── setup.py            # Package configuration
    └── README.md

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](./LICENSE)
