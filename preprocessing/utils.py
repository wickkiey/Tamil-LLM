import re


# ============================================================================
# FORMATTING CONVERSION FUNCTIONS
# ============================================================================

def convert_formatting(text):
    """
    Convert MediaWiki bold/italic markup to Markdown.
    
    MediaWiki uses apostrophes for formatting:
    - ''''' (5) → bold+italic → ***text***
    - ''' (3) → bold → **text**
    - '' (2) → italic → *text*
    """
    text = re.sub(r"'''''(.*?)'''''", r'***\1***', text)  # bold+italic
    text = re.sub(r"'''(.*?)'''", r'**\1**', text)        # bold
    text = re.sub(r"''(.*?)''", r'*\1*', text)            # italic
    return text


# ============================================================================
# HTML & TEMPLATE REMOVAL FUNCTIONS
# ============================================================================

def remove_html_comments_and_tags(text):
    """Remove HTML comments, <ref> tags, <nowiki> sections, and convert <br> to newlines."""
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    # Remove reference tags
    text = re.sub(r'<ref[^>]*?>.*?</ref>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<ref[^>]*/>', '', text, flags=re.IGNORECASE)
    
    # Remove nowiki sections
    text = re.sub(r'<nowiki>.*?</nowiki>', '', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Replace <br> with newline
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # remove <gallery></gallery>
    text = re.sub(r'<gallery[^>]*?>.*?</gallery>', '', text, flags=re.DOTALL|re.IGNORECASE) 
    
    return text


def remove_templates(text):
    """Remove MediaWiki templates {{...}}, handling deeply nested cases."""
    result = []
    i = 0
    
    while i < len(text):
        # Check if we're at the start of a template
        if i < len(text) - 1 and text[i:i+2] == '{{':
            # Find the matching closing braces
            brace_count = 0
            j = i
            
            while j < len(text):
                if j < len(text) - 1 and text[j:j+2] == '{{':
                    brace_count += 1
                    j += 2
                elif j < len(text) - 1 and text[j:j+2] == '}}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Found matching closing braces, skip this entire template
                        i = j + 2  # Skip past the closing }}
                        break
                    j += 2
                else:
                    j += 1
            
            # If we didn't find a matching close, this is a malformed template
            # Skip until we find content that looks like it's outside the template
            # Look for: blank line, section header (==), or bold title (''')
            if brace_count != 0:
                search_pos = i + 2
                while search_pos < len(text):
                    newline_pos = text.find('\n', search_pos)
                    if newline_pos == -1:
                        # No more newlines, skip to end
                        i = len(text)
                        break
                    
                    # Check what comes after this newline
                    next_line_start = newline_pos + 1
                    if next_line_start >= len(text):
                        i = len(text)
                        break
                    
                    # Look ahead at the next line
                    next_line_end = text.find('\n', next_line_start)
                    if next_line_end == -1:
                        next_line_end = len(text)
                    next_line = text[next_line_start:next_line_end].strip()
                    
                    # Check if we've found template end markers
                    if (not next_line or  # Blank line
                        next_line.startswith('==') or  # Section header
                        next_line.startswith("'''")):  # Bold title (article start)
                        i = next_line_start
                        break
                    
                    search_pos = newline_pos + 1
                else:
                    i = len(text)
                continue  # Don't append anything, just move to next iteration
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result)


def remove_categories(text):
    """Remove category tags from text."""
    text = re.sub(r'\[\[Category:[^\]]+\]\]', '', text)
    text = re.sub(r'\[\[பகுப்பு:.*?\]\]', '', text)
    text = re.sub(r'பகுப்பு:.*$', '', text, flags=re.MULTILINE)

    return text


def remove_images_and_files(text):
    """
    Remove MediaWiki image/file syntax with all parameters.
    Handles syntax like: [[File:name.jpg|thumb|300px|right|caption]]
    """
    def remove_images(text):
        # Match [[File: or [[Image: etc. in English and Tamil
        pattern = r'\[\[:?(?:File|Image|படிமம்|கோப்பு):[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]\]'
        return re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Apply multiple times to handle nested cases
    for _ in range(3):
        new_text = remove_images(text)
        if new_text == text:
            break
        text = new_text
    
    # Remove leftover image parameter fragments
    text = re.sub(r'\b(?:thumb|thumbnail|frame|frameless|border|left|right|center|none|\d+px)\b\|?', '', text)
    
    # Clean up leftover brackets and parentheses
    text = re.sub(r'^\s*\)\s*\]\]', '', text, flags=re.MULTILINE)
    text = re.sub(r'\(\s*\)', '', text)
    
    return text


def remove_html_attributes(text):
    """Remove HTML/CSS attributes from tables (colspan, rowspan, style, etc.)."""
    text = re.sub(r'\s*(?:colspan|rowspan|style|class|align|valign|bgcolor|width|height)\s*=\s*"[^"]*"', '', text, flags=re.IGNORECASE)
    text = re.sub(r"\s*(?:colspan|rowspan|style|class|align|valign|bgcolor|width|height)\s*=\s*'[^']*'", '', text, flags=re.IGNORECASE)
    return text


def remove_metadata_sections(text):
    """
    Remove Wikipedia metadata sections like 'See also', 'References', 'External links', etc.
    These sections typically appear at the end of articles.
    """
    metadata_sections = [
        r'==\s*(?:இவற்றையும் பார்க்க|இவற்றையும் பார்க்கவும்|See also|மேலும் காண்க)\s*==.*',
        r'==\s*(?:மேற்கோள்கள்|References|குறிப்புகள்|சான்றுகள்)\s*==.*',
        r'==\s*(?:வெளி இணைப்புகள்|External links|புற இணைப்புகள்)\s*==.*',
        r'==\s*(?:நூற்பட்டியல்|Bibliography|நூல்கள்)\s*==.*',
        r'==\s*(?:மேலும் படிக்க|Further reading)\s*==.*',
    ]
    
    for pattern in metadata_sections:
        text = re.sub(pattern, '', text, flags=re.DOTALL|re.MULTILINE|re.IGNORECASE)
    
    return text


# ============================================================================
# LINK CONVERSION FUNCTIONS
# ============================================================================

def convert_external_links(text):
    """Convert external links [http://url label] → label (or drop if no label)."""
    def ext_link_repl(m):
        return m.group(2) if m.group(2) else ''
    
    text = re.sub(
        r'\[(?:https?://|ftp://)([^\s\]]+)(?:\s+([^\]]+))?\]', 
        ext_link_repl, text
    )
    return text


def convert_internal_links(text):
    """Convert internal links [[Page|Label]] → Label or [[Page]] → Page."""
    def int_link_repl(m):
        page = m.group(1)
        label = m.group(2)
        
        # Skip namespace links like File: or Category:
        if ':' in page:
            prefix = page.lower().split(':', 1)[0]
            if prefix in ('file', 'image', 'category', 'help', 'wikipedia', 'படிமம்', 'கோப்பு'):
                return ''
        
        return label if label else page
    
    text = re.sub(
        r'\[\[([^|\]]+)(?:\|([^]]+))?\]\]', 
        int_link_repl, text
    )
    return text


# ============================================================================
# TEXT CLEANUP FUNCTIONS
# ============================================================================

def normalize_whitespace(text):
    """Normalize whitespace in text."""
    # Max 2 consecutive newlines
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    # Normalize spaces and tabs
    text = re.sub(r'[ \t]+', ' ', text)
    return text


# ============================================================================
# LINE PROCESSING FUNCTIONS
# ============================================================================

def should_skip_line(line):
    """Check if a line should be skipped (empty punctuation)."""
    return line and line in (']]', ')', ') ]]', '|', '||')


def process_heading(line):
    """
    Process MediaWiki heading (== Heading ==) into Markdown (## Heading).
    Returns tuple: (is_heading, markdown_line or None)
    """
    m = re.match(r'^(=+)\s*(.*?)\s*(=+)$', line)
    if not m or len(m.group(1)) != len(m.group(3)):
        return False, None
    
    level = min(len(m.group(1)), 6)
    heading_text = m.group(2).strip()
    
    # Apply formatting to heading text
    heading_text = convert_formatting(heading_text)
    
    # Skip metadata section headings
    skip_headings = [
        'இவற்றையும் பார்க்க', 'இவற்றையும் பார்க்கவும்', 'See also', 'மேலும் காண்க',
        'மேற்கோள்கள்', 'References', 'குறிப்புகள்', 'சான்றுகள்',
        'வெளி இணைப்புகள்', 'External links', 'புற இணைப்புகள்',
        'நூற்பட்டியல்', 'Bibliography', 'நூல்கள்',
        'மேலும் படிக்க', 'Further reading', 'பின்வருவனவற்றையும் பார்க்கவும்', 'உசாத்துணை'
    ]
    
    if heading_text in skip_headings:
        return True, None
    
    return True, '#' * level + ' ' + heading_text


def process_horizontal_rule(line):
    """
    Process horizontal rule (----) into Markdown (---).
    Returns tuple: (is_hr, markdown_line or None)
    """
    if re.match(r'^-+$', line):
        return True, '---'
    return False, None


def process_list_item(line):
    """
    Process MediaWiki list item (* or #) into Markdown.
    Returns tuple: (is_list, markdown_line or None)
    """
    m_list = re.match(r'^([*#]+)\s*(.*)', line)
    if not m_list:
        return False, None
    
    markers, content = m_list.group(1), m_list.group(2).strip()
    content = convert_formatting(content)
    
    indent = '  ' * (len(markers) - 1)
    
    if markers[0] == '*':
        return True, f"{indent}- {content}"
    else:  # markers[0] == '#'
        return True, f"{indent}1. {content}"


def process_table_block(lines, start_index):
    """
    Extract and process a complete table block starting from {|.
    Returns tuple: (end_index, markdown_lines)
    """
    table_lines = [lines[start_index].strip()]
    i = start_index + 1
    
    # Collect until end of table
    while i < len(lines) and not lines[i].strip().startswith('|}'):
        table_lines.append(lines[i].strip())
        i += 1
    
    if i < len(lines):
        table_lines.append(lines[i].strip())  # include '|}'
    
    # Convert the table block
    md_table = convert_wikitable_to_markdown(table_lines)
    return i + 1, md_table.splitlines()


def process_lines_to_markdown(lines):
    """
    Process lines of pre-cleaned wikitext into Markdown format.
    Handles headings, lists, tables, and regular text.
    """
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty punctuation lines
        if should_skip_line(line):
            i += 1
            continue
        
        # Process tables
        if line.startswith('{|'):
            i, table_lines = process_table_block(lines, i)
            result_lines.extend(table_lines)
            continue
        
        # Process headings
        is_heading, heading_line = process_heading(line)
        if is_heading:
            if heading_line:  # Only add if not skipped
                result_lines.append(heading_line)
            i += 1
            continue
        
        # Process horizontal rules
        is_hr, hr_line = process_horizontal_rule(line)
        if is_hr:
            result_lines.append(hr_line)
            i += 1
            continue
        
        # Process lists
        is_list, list_line = process_list_item(line)
        if is_list:
            result_lines.append(list_line)
            i += 1
            continue
        
        # Process regular lines
        if not line:
            result_lines.append("")
        else:
            # Apply formatting and add trailing spaces for line break
            result_lines.append(convert_formatting(line) + "  ")
        
        i += 1
    
    return result_lines


# ============================================================================
# TABLE CONVERSION FUNCTION
# ============================================================================


# ============================================================================
# TABLE CONVERSION FUNCTION
# ============================================================================

def convert_wikitable_to_markdown(table_lines):
    """
    Convert a list of lines in a MediaWiki table ({| ... |}) into Markdown table syntax.
    
    Args:
        table_lines: List of strings representing a MediaWiki table
        
    Returns:
        String containing the Markdown table
    """
    headers = []
    rows = []
    caption = None

    # Check for caption (first line after "{|") that starts with "|+"
    if len(table_lines) > 1 and table_lines[1].startswith('|+'):
        caption = table_lines[1].lstrip('|+').strip()
        table_lines.pop(1)
    
    # Join all lines and then re-split properly to handle multi-line cells
    full_text = '\n'.join(table_lines)
    
    # Remove HTML attributes from table cells
    full_text = re.sub(r'\s*(?:colspan|rowspan|style|class|align|valign|bgcolor|width|height)\s*=\s*"[^"]*"\s*\|', ' | ', full_text, flags=re.IGNORECASE)
    full_text = re.sub(r'\s*(?:colspan|rowspan|style|class|align|valign|bgcolor|width|height)\s*=\s*"[^"]*"', '', full_text, flags=re.IGNORECASE)
    
    # Split by row separator |-
    table_rows = re.split(r'\n\|-+\n?', full_text)
    
    for row_text in table_rows:
        row_text = row_text.strip()
        if not row_text or row_text.startswith('{|') or row_text.startswith('|}'):
            continue
        
        # Check if this is a header row (starts with !)
        if row_text.startswith('!'):
            cells = re.split(r'!!|\n!', row_text)
            cleaned_cells = []
            for cell in cells:
                cell = cell.lstrip('!').strip()
                if '|' in cell:
                    cell = cell.split('|')[-1].strip()
                if cell:
                    cell = convert_formatting(cell)
                    cleaned_cells.append(cell)
            if not headers and cleaned_cells:
                headers = cleaned_cells
        
        # Check if this is a data row (starts with |)
        elif row_text.startswith('|'):
            cells = re.split(r'\|\||\n\|', row_text)
            cleaned_cells = []
            for cell in cells:
                cell = cell.lstrip('|').strip()
                if '|' in cell:
                    cell = cell.split('|')[-1].strip()
                if cell:
                    cell = convert_formatting(cell)
                    cleaned_cells.append(cell)
            
            # If only one cell and no headers yet, treat as caption
            if len(cleaned_cells) == 1 and not headers and not rows:
                caption = cleaned_cells[0]
            elif cleaned_cells:
                rows.append(cleaned_cells)
    
    # If no explicit header but rows exist, use first row as header
    if not headers and rows:
        headers = rows.pop(0)
    if not headers:
        return ""

    # Determine the maximum number of columns
    max_cols = max(len(headers), max((len(row) for row in rows), default=0))
    
    # Pad headers if needed
    if len(headers) < max_cols:
        headers += [''] * (max_cols - len(headers))

    # Build markdown table
    md = []
    if caption:
        md.append(f"**{caption}**\n")
    md.append("| " + " | ".join(headers) + " |")
    md.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        # Pad row if it has fewer cells than headers
        if len(row) < len(headers):
            row += [''] * (len(headers) - len(row))
        # Truncate if too many cells
        elif len(row) > len(headers):
            row = row[:len(headers)]
        md.append("| " + " | ".join(row) + " |")
    md.append("")
    return "\n".join(md)


# ============================================================================
# MAIN CONVERSION ORCHESTRATOR
# ============================================================================

def wikitext_to_markdown(wiki_text):
    """
    Convert MediaWiki wikitext (including Tamil text) into Markdown format.
    
    This is the main orchestrator function that calls all processing steps in order:
    1. Remove HTML comments, tags, and references
    2. Remove MediaWiki templates
    3. Remove categories
    4. Remove images and files
    5. Convert external links
    6. Convert internal links
    7. Remove HTML attributes
    8. Remove metadata sections
    9. Normalize whitespace
    10. Process lines (headings, lists, tables, text) into Markdown
    
    Args:
        wiki_text: String containing MediaWiki wikitext
        
    Returns:
        String containing clean Markdown text
    """
    # Step 1: Remove HTML comments, tags, and references
    text = remove_html_comments_and_tags(wiki_text)
    
    # Step 2: Remove MediaWiki templates
    text = remove_templates(text)
    
    # Step 3: Remove category tags
    text = remove_categories(text)
    
    # Step 4: Remove images and files
    text = remove_images_and_files(text)
    
    # Step 5: Convert external links to plain text
    text = convert_external_links(text)
    
    # Step 6: Convert internal wiki links to plain text
    text = convert_internal_links(text)
    
    # Step 7: Remove HTML attributes from tables
    text = remove_html_attributes(text)
    
    # Step 8: Remove metadata sections
    text = remove_metadata_sections(text)
    
    # Step 9: Normalize whitespace
    text = normalize_whitespace(text)
    
    # Step 10: Process lines into Markdown format
    lines = text.splitlines()
    result_lines = process_lines_to_markdown(lines)
    
    return "\n".join(result_lines)
