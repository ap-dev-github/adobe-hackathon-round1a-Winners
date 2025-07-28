import pdfplumber
import json
import os
from collections import defaultdict, Counter

def group_chars_to_lines(chars, y_tolerance=2):
    """Group characters into lines based on their vertical position."""
    lines = defaultdict(list)
    for c in chars:
        key = round(c['top'] / y_tolerance) * y_tolerance
        lines[key].append(c)
    return lines

def join_chars_to_line_text(chars, x_tolerance=1.5):
    """Join characters into line text based on x gaps."""
    if not chars:
        return ""
    chars = sorted(chars, key=lambda c: c['x0'])
    text = chars[0]['text']
    for prev, curr in zip(chars, chars[1:]):
        if curr['x0'] - prev['x1'] > x_tolerance:
            text += ' '
        text += curr['text']
    return text.strip()

def extract_pdf_outline(pdf_path):
    """Extract structured outline from a PDF file."""
    result = {
        "title": "",
        "outline": []
    }

    font_size_counter = Counter()
    headings = []

    with pdfplumber.open(pdf_path) as pdf:
        # Get title from first 2 lines of page 1
        first_page_lines = group_chars_to_lines(pdf.pages[0].chars)
        title_lines = []
        for i, (_, chars) in enumerate(sorted(first_page_lines.items())):
            if i >= 2:
                break
            title_lines.append(join_chars_to_line_text(chars))
        result["title"] = "\n".join(title_lines).strip()

        all_heading_candidates = []

        for page_num, page in enumerate(pdf.pages, 1):
            lines = group_chars_to_lines(page.chars)
            for top, line_chars in sorted(lines.items()):
                if not line_chars:
                    continue
                line_text = join_chars_to_line_text(line_chars)
                avg_size = round(sum(c["size"] for c in line_chars) / len(line_chars), 1)
                font_name = line_chars[0]["fontname"].lower()
                font_size_counter[avg_size] += 1

                # Save as potential heading
                all_heading_candidates.append({
                    "text": line_text,
                    "size": avg_size,
                    "font": font_name,
                    "page": page_num
                })

        # Determine H1 and H2 thresholds
        common_sizes = [size for size, _ in font_size_counter.most_common()]
        if not common_sizes:
            return result

        h1_size = max(common_sizes)
        h2_sizes = [s for s in common_sizes if s < h1_size]
        h2_threshold = max(h2_sizes) if h2_sizes else h1_size

        for item in all_heading_candidates:
            if item["size"] == h1_size:
                level = "H1"
            elif item["size"] >= h2_threshold:
                level = "H2"
            else:
                continue  # skip normal text

            headings.append({
                "level": level,
                "text": item["text"],
                "page": item["page"]
            })

    result["outline"] = headings
    return result

def process_all_pdfs(input_dir, output_dir):
    """Process all PDFs in input directory and save results to output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            output = extract_pdf_outline(pdf_path)
            
            output_filename = os.path.splitext(filename)[0] + '.json'
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w') as f:
                json.dump(output, f, indent=2)

if __name__ == "__main__":
    input_dir = '/app/input'
    output_dir = '/app/output'
    process_all_pdfs(input_dir, output_dir)