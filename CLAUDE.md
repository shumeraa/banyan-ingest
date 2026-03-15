# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Instructions for Claude Code

**ALWAYS use the existing Python environment** when running commands. The project has a `.venv` virtual environment that should be used for all Python operations.

**NEVER install packages without explicit permission**. Always check if packages are already available in the existing environment before attempting to install anything.

**MUST ASK FOR PERMISSION** before installing any packages, dependencies, or making any changes to the system. This includes pip install, apt-get, yum, or any other package management commands. Always request explicit user approval before proceeding with installations.

**Preferred command format**:
```bash
source .venv/bin/activate && python3 command_here
```

## Project Overview

**banyan-extract** is a Python module that prepares documents for use in GenAI and LLM applications. It utilizes state-of-the-art tools like `marker` and NVIDIA's `nemotron-parse` models to extract and process content from various document formats.

## Code Architecture

The project follows a modular architecture with clear separation of concerns:

### Core Components

1. **Processors** (`src/banyan_extract/processor/`):
   - Abstract base class `Processor` defines the interface
   - Concrete implementations: `NemoparseProcessor`, `MarkerProcessor`, `PapermageProcessor`, `PptxProcessor`
   - Handle document processing logic and integration with external tools

2. **Output Handlers** (`src/banyan_extract/output/`):
   - Abstract base class `ModelOutput` defines output interface
   - Concrete implementations: `NemoparseOutput`, `MarkerOutput`, `PapermageOutput`, `PptxOutput`
   - Handle saving extracted content in various formats (Markdown, JSON, images, CSV)

3. **Converters** (`src/banyan_extract/converter/`):
   - Utility functions for format conversion
   - `pdf_to_image.py`: Convert PDF pages to images
   - `latex_table_to_csv.py`: Convert LaTeX tables to CSV format

4. **CLI** (`src/banyan_extract/cli.py`):
   - Command-line interface using argparse
   - Main entry point for the application
   - Supports batch processing and configuration via environment variables

### Key Design Patterns

- **Abstract Factory**: Processor and Output classes use abstract base classes
- **Strategy Pattern**: Different processors can be swapped based on backend selection
- **Data Classes**: Used for structured data transfer between components

## Common Development Commands

### Installation

```bash
# Install from source
pip install .

# Install with marker support
pip install .[marker]

# Install with nemotron-parse support
pip install .[nemotronparse]
```

### Running the CLI

```bash
# Basic usage with nemoparse backend
banyan-extract --backend nemoparse input.pdf output_dir/

# Process directory of files
banyan-extract --backend nemoparse --is_input_dir input_dir/ output_dir/

# With checkpointing (saves files as they're processed)
banyan-extract --backend nemoparse --checkpointing input.pdf output_dir/

# With bounding box visualization
banyan-extract --backend nemoparse --draw_bboxes input.pdf output_dir/
```

### Environment Configuration

```bash
# Copy example config
cp .env.example .env

# Edit .env to set NVIDIA endpoint
NEMOPARSE_ENDPOINT="your_endpoint_url"
NEMOPARSE_MODEL="nvidia/nemotron-parse"
```

### Running Examples

```bash
# Example scripts are provided for different backends
python example_nemoparse.py
python example_marker.py
python example_pm.py
python example_pptx.py
```

## Key Files and Their Purpose

- `src/banyan_extract/processor/processor.py`: Base processor interface
- `src/banyan_extract/output/output.py`: Base output interface
- `src/banyan_extract/processor/nemoparse_processor.py`: NVIDIA nemotron-parse integration
- `src/banyan_extract/output/nemoparse_output.py`: Output handling for nemotron-parse
- `src/banyan_extract/cli.py`: Command-line interface
- `pyproject.toml`: Build configuration and dependencies

## Development Notes

1. **Dependencies**: The project requires `poppler` to be installed for PDF processing

2. **Backend Support**: Different backends require different optional dependencies:
   - `marker`: Requires `marker-pdf` and `surya-ocr`
   - `nemotronparse`: Requires `openai`

3. **Error Handling**: The code includes basic error handling for file operations and API calls

4. **Output Formats**: The tool generates multiple output files:
   - Markdown files with extracted text
   - JSON files with bounding box data
   - PNG images (extracted images and bounding box visualizations)
   - CSV files for tables

5. **Batch Processing**: Supports processing multiple files with checkpointing option
