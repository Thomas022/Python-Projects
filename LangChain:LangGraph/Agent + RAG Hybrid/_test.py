# test_cp1.py
tags = ['setup', 'cp1']

import nbformat, re

notebook = nbformat.read('notebook.ipynb', as_version=4)

# -------------------------
# Validate setup cells are executed
# -------------------------
setup_cells = [
    c for c in notebook.cells
    if any(t.startswith('setup') for t in c.get('metadata', {}).get('tags', []))
]

for cell in setup_cells:
    if cell.get('execution_count') is None:
        fail_tests("Make sure to run the setup cell.")

# -------------------------
# Validate cp1 cell exists and is executed
# -------------------------
cp1_cell = next(
    (c for c in notebook.cells if 'cp1' in c.get('metadata', {}).get('tags', [])), None
)

if cp1_cell is None or cp1_cell.get('execution_count') is None:
    fail_tests("Make sure to run the Checkpoint 1 cell.")

cp1_text = cp1_cell.source

# =========================================
# Test search_documents function
# =========================================

# -------------------------
# 1. Check @tool decorator for search_documents
# -------------------------
if not re.search(r'@tool\s+def\s+search_documents', cp1_text):
    fail_tests("Make sure to use the `@tool` decorator above the `search_documents` function definition.")

# -------------------------
# 2. Check search_documents function definition
# -------------------------
if not re.search(r'\bdef\s+search_documents\s*\(', cp1_text):
    fail_tests("Make sure to define a function named `search_documents`.")

# -------------------------
# 3. Check search_documents has query parameter
# -------------------------
if not re.search(r'def\s+search_documents\s*\(\s*query\s*[:]?', cp1_text):
    fail_tests("Make sure the `search_documents` function has a parameter named `query`.")

# -------------------------
# 4. Check search_documents has docstring
# -------------------------
if not re.search(r'def\s+search_documents\s*\([^)]*\)\s*(?:->.*?)?\s*:\s*"""', cp1_text, re.DOTALL):
    fail_tests("Make sure to include a docstring for the `search_documents` function using triple quotes.")

# -------------------------
# 5. Check search_documents has return statement
# -------------------------
search_documents_function = re.search(r'def\s+search_documents\s*\([^)]*\).*?(?=\n@tool|\nclass\s|\ndef\s|\Z)', cp1_text, re.DOTALL)
if search_documents_function and not re.search(r'\breturn\b', search_documents_function.group(0)):
    fail_tests("Make sure the `search_documents` function returns a value.")

# -------------------------
# 6. Check docs variable is assigned
# -------------------------
if search_documents_function and not re.search(r'\bdocs\s*=', search_documents_function.group(0)):
    fail_tests("Make sure to assign the retrieved documents to a variable named `docs`.")

# -------------------------
# 7. Check retriever.invoke() is called
# -------------------------
if search_documents_function and not re.search(r'retriever\s*\.\s*invoke\s*\(', search_documents_function.group(0)):
    fail_tests("Make sure to call the `invoke` method on `retriever`.")

# -------------------------
# 8. Check query is passed to retriever.invoke()
# -------------------------
if search_documents_function and not re.search(r'retriever\s*\.\s*invoke\s*\(\s*query\s*\)', search_documents_function.group(0)):
    fail_tests("Make sure to pass `query` when calling the `invoke` method.")

# -------------------------
# 9. Check join() method is used
# -------------------------
if search_documents_function and not re.search(r'["\'].*["\']\.join\s*\(', search_documents_function.group(0)):
    fail_tests("Make sure to use the `join` method to combine document contents.")

# -------------------------
# 10. Check docs is used in the expression
# -------------------------
if search_documents_function and not re.search(r'\bdocs\b', search_documents_function.group(0)):
    fail_tests("Make sure to use `docs` when combining document contents.")

# -------------------------
# 11. Check .page_content attribute is accessed
# -------------------------
if search_documents_function and not re.search(r'\.page_content', search_documents_function.group(0)):
    fail_tests("Make sure to access the `page_content` attribute from each document.")

# -------------------------
# All tests passed
# -------------------------
pass_tests()