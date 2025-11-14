from pathlib import Path
import sys
import re
from weasyprint import HTML

def read_file_from_arg() -> str:
    """
    Reads and returns the content of a file whose path is passed
    as the first command-line argument.

    Returns:
        str: The full content of the file.
    Raises:
        SystemExit: If no file path is provided or file not found.
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"Error: File not found → {file_path}")
        sys.exit(1)

    with file_path.open("r", encoding="utf-8") as f:
        return f.read()

def split_into_stanzas(content: str) -> list[str]:
    """
    Splits song text into stanzas based on markers like ---[<SongPart>:1]---.

    Args:
        content (str): Full text of the song file.

    Returns:
        list[str]: A list of stanza strings (one per verse).
    """
    # Split using regex pattern for ---[<SongPart>:x]---
    parts = re.split(r'---\[\w+:\d+\]---', content)

    # Clean and filter out any empty strings or whitespace
    stanzas = [part.strip() for part in parts if part.strip()]

    return stanzas


def format_stanzas_to_html(stanzas: list[str]) -> str:
    """
    Wraps each stanza in a <div class="page"><p class="text">...</p></div> block,
    and adds <br> at the end of each line.

    Args:
        stanzas (list[str]): List of verse text blocks.

    Returns:
        str: Full HTML string containing all formatted stanzas.
    """
    formatted_blocks = []

    for stanza in stanzas:
        # Split by lines and strip extra whitespace
        lines = [line.strip() for line in stanza.splitlines() if line.strip()]

        # Join lines with <br> tags
        stanza_html = "<br>\n".join(lines) + "<br>"

        # Wrap stanza in div/p block
        block = f"""
  <div class="page">
    <p class="text">
      {stanza_html}
    </p>
  </div>"""
        formatted_blocks.append(block.strip())

    # Join all stanza blocks
    return "\n\n".join(formatted_blocks)

def html_head_content():
    return """
    <!DOCTYPE html>
    <html>

    <head>
      <meta charset="UTF-8">
      <title>Song Presentation</title>

      <!-- ✅ Google Fonts CDN for Hindi + Latin with bold & italic variants -->
      <link
        href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:ital,wght@0,400;0,700;1,400;1,700&display=swap"
        rel="stylesheet">

      <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        @page {
          size: 28cm 15.75cm;
          margin: 0;
        }

        html,
        body {
          width: 28cm;
          height: 15.75cm;
          font-family: 'Noto Sans Devanagari', sans-serif;
          background: #ffaa95;
        }

        .page {
          width: 28cm;
          height: 15.75cm;
          display: flex;
          justify-content: center;
          align-items: center;
          page-break-after: always;
          background-color: #ffaa95;
          overflow: hidden;
        }

        .text {
          font-size: 40px;
          text-align: center;
          color: #000;
          max-width: 100%;
          word-wrap: break-word;
          font-weight: normal;
        }

        b {
          font-weight: 700;
        }

        i {
          font-style: normal;
          transform: skew(-10deg);
          display: inline-block;
        }

        @media print {

          html,
          body {
            width: 297mm;
            height: 210mm;
          }

          .page {
            margin: 0;
            page-break-after: always;
          }
        }
      </style>
    </head>

    <body>
    """

def html_tail_content():
    return """
    </body>

    </html>
    """

def insert_into_html(html_output: str, html_file: str = "song.html") -> None:
    """
    Inserts the given HTML string into the <body>...</body> of song.html.
    Replaces any existing content inside <body>.

    Args:
        html_output (str): The HTML to insert inside <body>.
        html_file (str): Path to the HTML file (default: 'song.html').
    """
    path = Path(html_file)

    content = html_head_content() + html_output + html_tail_content()

    # Write back updated HTML
    path.write_text(content, encoding="utf-8")
    print(f"✅ Updated {html_file} with new body content.")

def html_to_pdf(html_file: str = "song.html", pdf_file: str = "song.pdf"):
    """
    Converts an HTML file to a PDF that visually matches the browser view.
    Each .page <div> becomes a new PDF page automatically (via CSS).
    """
    html_path = Path(html_file)

    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    # Load the HTML and render to PDF
    HTML(filename=str(html_path)).write_pdf(pdf_file)
    print(f"✅ PDF created: {pdf_file}")

def main():
    """
    Each Page (denoted by ---[<SongPart>:n]---) should have a max of:
        - 10 lines
        - 50 chars per line
    This is from font size 40pts on 28cm x 15.75cm paper
    """
    file_content = read_file_from_arg()
    stanzas = split_into_stanzas(file_content)
    html_content = format_stanzas_to_html(stanzas)
    insert_into_html(html_content)
    html_to_pdf()

if __name__ == "__main__":
    main()
