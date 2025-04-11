import os
import json
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def jsonl_to_pdf(input_file, output_file):
    """
    Reads a JSONL file, uses pdf_page_numbers to map text to pages, and saves as a single PDF.

    Args:
        input_file (str): Path to the input JSONL file.
        output_file (str): Path to save the output PDF.
    """
    # Register DejaVuSans font from Pop!_OS system path
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Adjust if needed
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    except Exception as e:
        print(f"Error registering font: {e}. Check if {font_path} exists.")
        return

    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.fontName = 'DejaVuSans'
    heading_style = styles["Heading1"]
    heading_style.fontName = 'DejaVuSans'

    # Create PDF
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            try:
                # Parse JSON line
                data = json.loads(line)
                text_content = data.get("text", "")
                page_mappings = data.get("attributes", {}).get("pdf_page_numbers", [])

                # Debug: Print text length and mappings
                print(f"Line {i + 1}: Text length = {len(text_content)}, Page mappings = {len(page_mappings)}")

                # Process each page mapping
                for start, end, page_num in page_mappings:
                    # Extract text for this page
                    page_text = text_content[start:end]
                    
                    # Debug: Print page info
                    print(f"Page {page_num}: chars {start}-{end}, length = {len(page_text)}")

                    # Add page heading
                    story.append(Paragraph(f"Page {page_num}", heading_style))
                    story.append(Spacer(1, 12))

                    # Split text into paragraphs by newlines
                    paragraphs = page_text.split('\n')
                    for para in paragraphs:
                        if para.strip():
                            story.append(Paragraph(para, style))
                            story.append(Spacer(1, 12))

                    # Add page break (except for the last page)
                    if page_num < page_mappings[-1][2]:  # Last page number
                        story.append(PageBreak())

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {i + 1}: {e}")
            except Exception as e:
                print(f"Unexpected error on line {i + 1}: {e}")

    # Build PDF
    try:
        doc.build(story)
        print(f"Saved PDF to {output_file}")
    except Exception as e:
        print(f"Error building PDF: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert JSONL to single PDF with page mapping")
    parser.add_argument("input_file", help="Path to the input JSONL file")
    parser.add_argument("output_file", help="Path to save the output PDF (e.g., output.pdf)")
    args = parser.parse_args()

    jsonl_to_pdf(args.input_file, args.output_file)

if __name__ == "__main__":
    main()