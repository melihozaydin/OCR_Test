import json
import os
import sys

def jsonl_to_markdown(input_file, output_dir):
    """
    Reads a JSONL file, extracts the 'text' field from each line, and saves it as a Markdown file.

    Args:
        input_file (str): Path to the input JSONL file.
        output_dir (str): Directory to save the Markdown files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            try:
                # Parse the JSON line
                data = json.loads(line)
                text_content = data.get("text", "")

                # Convert to Markdown format
                markdown_content = f"# Extracted Content (Line {i + 1})\n\n{text_content}"

                # Save to a Markdown file
                output_file = os.path.join(output_dir, f"line_{i + 1}.md")
                with open(output_file, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_content)

                print(f"Extracted and saved line {i + 1} to {output_file}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {i + 1}: {e}")
            except Exception as e:
                print(f"Unexpected error on line {i + 1}: {e}")

# Example usage
# input_jsonl_file = "/path/to/test.jsonl"  # Replace with the actual path to your JSONL file
# output_directory = "/path/to/output_markdown"  # Replace with the desired output directory
# jsonl_to_markdown(input_jsonl_file, output_directory)

if __name__ == "__main__":

  if len(sys.argv) != 3:
    print("Usage: python jsonl_to_markdown.py <input_file> <output_dir>")
    sys.exit(1)

  input_file = sys.argv[1]
  output_dir = sys.argv[2]

  jsonl_to_markdown(input_file, output_dir)
