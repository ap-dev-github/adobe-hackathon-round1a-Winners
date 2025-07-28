## Objective

Extract structured outlines (title and headings) from PDF files using font size and position heuristics. Output the results as JSON files.

## Tools

- pdfplumber
- Python 3
- json
- os
- collections (Counter, defaultdict)

## Functions

### group_chars_to_lines(chars, y_tolerance=2)
Groups characters into lines by rounding their vertical `top` position.

### join_chars_to_line_text(chars, x_tolerance=1.5)
Sorts characters by `x0` and joins them into line text. Inserts space if `x0 - prev.x1 > x_tolerance`.

### extract_pdf_outline(pdf_path)
- Extracts first two lines from page 1 as the title.
- For each page:
  - Groups chars into lines.
  - Calculates average font size per line.
  - Records font size frequencies.
  - Stores potential headings with metadata.
- Identifies H1 and H2 font sizes based on frequency.
- Builds final heading outline with text, level (H1/H2), and page number.

### process_all_pdfs(input_dir, output_dir)
Processes all `.pdf` files in `input_dir`:
- Runs `extract_pdf_outline` on each.
- Saves output as `.json` in `output_dir`.

## Output JSON Structure

```
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Heading Text",
      "page": 1
    },
    ...
  ]
}
```
Usage
Set paths and run the script:
```
input_dir = '/app/input'
output_dir = '/app/output'
process_all_pdfs(input_dir, output_dir)
```
