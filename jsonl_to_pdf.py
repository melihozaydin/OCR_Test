import os
import json
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def jsonl_to_pdf(input_file, output_dir):
    """
    Reads a JSONL file, extracts the 'text' field, and saves as PDF with DejaVuSans from system.

    Args:
        input_file (str): Path to the input JSONL file.
        output_dir (str): Directory to save the PDF files.
    """
    # Register DejaVuSans font from system path
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Adjust if path differs
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    except Exception as e:
        print(f"Error registering font: {e}. Check if {font_path} exists.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.fontName = 'DejaVuSans'
    heading_style = styles["Heading1"]
    heading_style.fontName = 'DejaVuSans'

    with open(input_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            try:
                # Parse the JSON line
                data = json.loads(line)
                text_content = data.get("text", "")
                
                # Debug: Print raw text from JSON
                print(f"Raw text from JSON (line {i + 1}): {repr(text_content)}")

                # No additional decoding needed; text is already Unicode
                decoded_text = text_content

                # Debug: Print text before PDF
                print(f"Text for PDF (line {i + 1}): {repr(decoded_text)}")

                # Create PDF file
                output_file = os.path.join(output_dir, f"page_{i + 1}.pdf")
                doc = SimpleDocTemplate(output_file, pagesize=letter)
                
                # Build content
                story = []
                story.append(Paragraph(f"Page {i + 1}", heading_style))
                story.append(Spacer(1, 12))
                
                # Split text into paragraphs and add to story
                paragraphs = decoded_text.split('\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para, style))
                        story.append(Spacer(1, 12))

                # Build PDF
                doc.build(story)
                print(f"Extracted and saved line {i + 1} to {output_file}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {i + 1}: {e}")
            except Exception as e:
                print(f"Unexpected error on line {i + 1}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert JSONL file to PDF pages with DejaVuSans")
    parser.add_argument("input_file", help="Path to the input JSONL file")
    parser.add_argument("output_dir", help="Directory to save the PDF files")
    args = parser.parse_args()

    jsonl_to_pdf(args.input_file, args.output_dir)

if __name__ == "__main__":
    main()
