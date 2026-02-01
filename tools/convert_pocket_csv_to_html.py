import csv
import html # Using html module for escaping special characters in titles

def generate_html_header():
    """Generates the header for the Netscape Bookmark file."""
    return """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Pocket Bookmarks</TITLE>
<H1>Pocket Bookmarks</H1>
<DL><p>
"""

def generate_html_footer():
    """Generates the footer for the Netscape Bookmark file."""
    return """</DL><p>
"""

def generate_folder_start(name):
    """Generates the opening tag for a bookmark folder."""
    # Escape folder name to prevent issues with special characters
    escaped_name = html.escape(name)
    return f"""<DT><H3>{escaped_name}</H3>
<DL><p>
"""

def generate_folder_end():
    """Generates the closing tag for a bookmark folder."""
    return """</DL><p>
"""

def generate_bookmark_item(title, url):
    """Generates the HTML tag for a single bookmark item."""
    # Escape title and URL to prevent issues with special characters
    escaped_title = html.escape(title)
    escaped_url = html.escape(url)
    # Use a placeholder for the ADD_DATE attribute, as the CSV time_added is a Unix timestamp
    # Chrome can handle bookmarks without ADD_DATE, or it can be added later if needed.
    # For simplicity and direct CSV conversion as requested, we omit it.
    return f"""<DT><A HREF="{escaped_url}">{escaped_title}</A>
"""

def convert_csv_to_html(csv_filepath, html_filepath):
    """
    Reads Pocket CSV export, categorizes bookmarks by status, and generates
    a Netscape Bookmark HTML file.
    """
    # Initialize storage for bookmarks based on status
    bookmarks_by_status = {
        'unread': [],
        'archive': []
    }

    # Read and process the CSV file
    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as infile:
            # Use DictReader to easily access columns by name
            reader = csv.DictReader(infile)

            # Iterate through each row (bookmark) in the CSV
            for row in reader:
                title = row.get('title', 'No Title') # Get title, default to 'No Title' if missing
                url = row.get('url')
                status = row.get('status')

                # Ensure URL and status are present before processing
                if url and status:
                    if status == 'unread':
                        bookmarks_by_status['unread'].append({'title': title, 'url': url})
                    elif status == 'archive':
                        bookmarks_by_status['archive'].append({'title': title, 'url': url})
                    # Ignore other statuses as per plan

    except FileNotFoundError:
        print(f"Error: Input CSV file not found at {csv_filepath}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Generate the HTML content
    html_content = generate_html_header()

    # Add 'unread' folder and bookmarks if any
    if bookmarks_by_status['unread']:
        html_content += generate_folder_start("pocket/unread")
        for bookmark in bookmarks_by_status['unread']:
            html_content += generate_bookmark_item(bookmark['title'], bookmark['url'])
        html_content += generate_folder_end()

    # Add 'read' folder and bookmarks if any
    if bookmarks_by_status['archive']:
        html_content += generate_folder_start("pocket/read")
        for bookmark in bookmarks_by_status['archive']:
            html_content += generate_bookmark_item(bookmark['title'], bookmark['url'])
        html_content += generate_folder_end()

    html_content += generate_html_footer()

    # Write the HTML content to the output file
    try:
        with open(html_filepath, mode='w', encoding='utf-8') as outfile:
            outfile.write(html_content)
        print(f"Successfully converted {csv_filepath} to {html_filepath}")
    except Exception as e:
        print(f"Error writing HTML file: {e}")

# Define the input and output file paths
input_csv_filepath = r'C:\Users\johna\OneDrive\Articles\pocket eol export\part_000000.csv'
output_html_filepath = r'C:\Users\johna\OneDrive\Articles\pocket eol export\bookmarks.html'

# Run the conversion
if __name__ == "__main__":
    convert_csv_to_html(input_csv_filepath, output_html_filepath)
