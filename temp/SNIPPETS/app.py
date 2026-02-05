"""
Code Snippets Browser - Flask Application

A web interface for browsing, searching, and copying code snippets
from the centralized snippets library.
"""

from flask import Flask, render_template, jsonify, request
import os
from pathlib import Path
import re

app = Flask(__name__)

SNIPPETS_DIR = Path(__file__).parent
EXCLUDED_DIRS = {'.git', '__pycache__', 'templates', 'static', '.claude'}
EXCLUDED_FILES = {'app.py', 'CLAUDE.md', 'README.md', 'EXTRACTION_SUMMARY.md'}


def extract_docstring(content):
    """Extract the module-level docstring from code."""
    # Match triple-quoted strings at the start of the file
    match = re.match(r'^\s*["\']{{3}}(.*?)["\']{{3}}', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def parse_snippet(filepath):
    """Parse a snippet file and extract metadata."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        docstring = extract_docstring(content)

        # Extract key information from docstring
        title = ""
        description = ""
        use_cases = []
        dependencies = []

        lines = docstring.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # First non-empty line is usually the title
            if not title and not line.startswith('-'):
                title = line
                continue

            if line.startswith('Description:'):
                current_section = 'description'
                description = line.replace('Description:', '').strip()
                continue
            elif line.startswith('Use Cases:'):
                current_section = 'use_cases'
                continue
            elif line.startswith('Dependencies:'):
                current_section = 'dependencies'
                continue
            elif line.startswith('Notes:') or line.startswith('Related') or line.startswith('Source'):
                current_section = None
                continue

            if current_section == 'description' and description:
                description += ' ' + line
            elif current_section == 'use_cases' and line.startswith('-'):
                use_cases.append(line[1:].strip())
            elif current_section == 'dependencies' and line.startswith('-'):
                dependencies.append(line[1:].strip())

        return {
            'title': title or filepath.name,
            'description': description,
            'use_cases': use_cases,
            'dependencies': dependencies,
            'content': content,
            'language': 'python' if filepath.suffix == '.py' else 'javascript',
            'filename': filepath.name,
            'size': len(content)
        }
    except Exception as e:
        return None


def scan_snippets():
    """Scan the snippets directory and organize by category."""
    categories = {}

    for category_dir in SNIPPETS_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        if category_dir.name in EXCLUDED_DIRS:
            continue

        snippets = []
        for snippet_file in category_dir.iterdir():
            if snippet_file.is_file() and snippet_file.suffix in ['.py', '.js']:
                if snippet_file.name in EXCLUDED_FILES:
                    continue

                snippet_data = parse_snippet(snippet_file)
                if snippet_data:
                    snippet_data['category'] = category_dir.name
                    snippet_data['path'] = str(snippet_file.relative_to(SNIPPETS_DIR))
                    snippets.append(snippet_data)

        if snippets:
            # Convert directory name to readable category name
            category_name = category_dir.name.replace('-', ' ').replace('_', ' ').title()
            categories[category_name] = {
                'slug': category_dir.name,
                'snippets': sorted(snippets, key=lambda x: x['filename'])
            }

    return dict(sorted(categories.items()))


@app.route('/')
def index():
    """Main page displaying all snippets."""
    categories = scan_snippets()
    total_snippets = sum(len(cat['snippets']) for cat in categories.values())

    return render_template('index.html',
                         categories=categories,
                         total_snippets=total_snippets)


@app.route('/api/search')
def search():
    """Search endpoint for filtering snippets."""
    query = request.args.get('q', '').lower()

    if not query:
        return jsonify({'results': []})

    categories = scan_snippets()
    results = []

    for category_name, category_data in categories.items():
        for snippet in category_data['snippets']:
            # Search in title, description, filename, and content
            searchable = ' '.join([
                snippet['title'],
                snippet['description'],
                snippet['filename'],
                ' '.join(snippet['use_cases']),
                snippet['content']
            ]).lower()

            if query in searchable:
                snippet['category_name'] = category_name
                results.append(snippet)

    return jsonify({'results': results, 'count': len(results)})


@app.route('/api/snippet/<path:snippet_path>')
def get_snippet(snippet_path):
    """Get full content of a specific snippet."""
    filepath = SNIPPETS_DIR / snippet_path

    if not filepath.exists() or not filepath.is_file():
        return jsonify({'error': 'Snippet not found'}), 404

    snippet_data = parse_snippet(filepath)
    if snippet_data:
        return jsonify(snippet_data)
    else:
        return jsonify({'error': 'Failed to parse snippet'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)
