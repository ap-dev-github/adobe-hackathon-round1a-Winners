## Team Members
### Ayush Pandey 
### Ayush Banerjee

# PDF Outline Extractor 
A Dockerized Python tool that extracts structured outlines (H1 and H2 headings) from PDF files and saves them as JSON. This project is optimized for a minimal footprint using a multi-stage Docker build with Alpine Linux, resulting in a lean image of approximately **165 MB**.

## How It Works

The Python script `pdf_outline_extractor.py` uses the `pdfplumber` library to perform the following steps:

1. **Character Grouping**: It reads a PDF page and groups individual characters into lines based on their vertical alignment (`y` coordinate).
2. **Font Size Analysis**: It analyzes the font sizes used throughout the document to identify the most common sizes.
3. **Heading Identification**: It establishes a hierarchy of headings based on font size. The largest font size is designated as **H1**, and the next largest is treated as the threshold for **H2** headings.
4. **JSON Output**: It processes all PDFs in an `input` directory and generates a corresponding JSON file for each in the `output` directory. The JSON file contains the document's title and a structured list of all identified H1 and H2 headings with their text, level, and page number.

##  Docker Image Optimization: From Slim to Ultralight

The primary goal of the Docker configuration was to create the smallest possible image for efficient distribution and deployment. This was achieved by moving from a `python:3.9-slim` base to a `python:3.9-alpine` base with a multi-stage build.

### The Challenge: Larger Image Size

The initial `Dockerfile` used `python:3.9-slim`. While smaller than the full Debian-based Python image, `slim` still includes many system libraries and tools not required for the script to simply *run*.

### The Solution: Alpine and Multi-Stage Builds

The new `Dockerfile` leverages two key strategies for a massive size reduction:

1. **`python:3.9-alpine` Base Image**: Alpine Linux is a minimal Linux distribution built around `musl libc` and `BusyBox`. Its base image is incredibly small (around 5-6 MB) compared to Debian-based images (`slim` is often ~50 MB+).

2. **Multi-Stage Build**: This is the critical optimization.
   - **Stage 1 (`builder`)**: This stage is a temporary environment used only to install dependencies. It installs build tools like `gcc` and `musl-dev` which are required to compile some Python packages (like those used by `pdfplumber`).
   - **Stage 2 (Final Image)**: This is the final, clean image. Instead of keeping the build tools, we **only copy the installed Python packages** and our script (`pdf_outline_extractor.py`) from the `builder` stage.

The result is a final image that contains the minimal Alpine OS, the Python runtime, and our installed packages—and nothing else. The build tools, temporary files, and package manager cache are all discarded, leading to the **~165 MB** final image size.

## Usage

Follow these steps to build the Docker image and run the extractor on your PDF files.

### Prerequisites

* [Docker](https://www.docker.com/get-started) must be installed and running.


### 1. Project Setup

Clone the repository and set up the input/output directories.

```bash
git clone git@github.com:ap-dev-github/adobe-hackathon-round1a-Winners.git
```
# Create directories for input and output
```bash
mkdir input
mkdir output
```
Place all the PDF files you want to process inside the input directory.

2. Build the Docker Image
Run the following command from the root of the project directory to build the ultralight image.

```bash
docker build -t pdf-extractor:ultralight .
```
3. Run the Container
Execute the script by running the Docker container. This command mounts your local input and output folders into the container, runs the script, and then cleans up the container after it's done.

```bash
powershell
docker run --rm `
  -v "${PWD}/input:/app/input" `
  -v "${PWD}/output:/app/output" `
  --network none `
  pdf-extractor:ultralight
```
