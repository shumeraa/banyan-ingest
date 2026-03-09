# Banyan Extract

`banyan_extract` is a python module that prepares documents for use in GenAI and LLM applications. 

Rather than re-invent the wheel, `banyan_extract` aims to utilize state-of-the-art tools to provide this capability. 


## Installation

### From pypi (recommended)

In a python environment (`conda`, `venv`, etc.), use the following:

```
cd PATH_TO_REPO/
pip install banyan-extract
```

### From source
```
git clone https://github.com/sandialabs/banyan-ingest.git
cd banyan-ingest/
pip install .
```

### Additional Dependecies

You will need poppler installed. 


## Supported Tools and File Formats
Currently we provide support for `marker` ([link here](https://github.com/datalab-to/marker)) and NVIDIA's `nemotron-parse` models ([link here](https://build.nvidia.com/nvidia/nemotron-parse)).
To install the necessary dependencies for these tools please use `pip install .[marker]` or `pip install .[nemotronparse]` respectively.

Note: please ensure you follow the guidelines and usage licenses of the tools.

### Using Nemotron-parse

Copy the `.env.example` file change `NEMOTRON_ENDPOINT` to the endpoint of the Nemotron-parse model you want to use.

### Examples
khe `example_XXX.py` scripts contain basic scripts for processing pdf documents using different OCR tools under the hood.

## CLI Usage
Use `banyan-extract` to run the tool from the command line. Example command that reads in a pdf named `example.pdf` and puts all the extracted content in a directory named `banyan_output`:

`banyan-extract --backend nemoparse example.pdf banyan_output/`
