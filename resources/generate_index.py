import os
import sys

def generate_html_index(directory, output_file=None):
    """
    Generates an HTML index file listing all .slides.html and .pdf files in the directory and its subdirectories.
    
    :param directory: Path to the directory containing the files.
    :param output_file: Name of the output HTML file.
    """
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    # Start building the HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lecture Material Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            background-color: #f4f4f9;
        }
        h1 {
            color: #333;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
        }
        a {
            text-decoration: none;
            color: #007BFF;
            font-size: 18px;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Lecture Material Index</h1>
    <ul>
"""

    filepaths = []

    # Walk through the directory recursively
    for root, _, files in os.walk(directory):

        filepaths += [os.path.relpath(os.path.join(root, f), directory) for f in files]

    for filepath in sorted(filepaths):

        # Include only .html and .pdf files
        if filepath.endswith(('.slides.html', '.pdf')):
            html_content += f'        <li><a href="{filepath}" target="_blank">{filepath}</a></li>\n'

    # Close the HTML content
    html_content += """    </ul>
</body>
</html>"""

    # Default output_file
    if output_file is None:
        output_file = os.path.join(directory, "index.html")

    # Write to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML index successfully generated: {output_file}")

# Entry point
if __name__ == "__main__":

    target_directory = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_html_index(target_directory, output_file)
