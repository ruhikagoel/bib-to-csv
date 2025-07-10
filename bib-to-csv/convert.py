import re
import pandas as pd
import os
print("Importing necessary libraries....")

def parse_bibtex(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        bibtex_content = file.read()

    # Split entries by '@' but keep the delimiter
    entries = re.split(r'(?=@\w+)', bibtex_content)
    parsed_entries = []

    for entry in entries:
        if not entry.strip():
            continue
        # Match entry type and citation key
        header_match = re.match(r'@(\w+)\s*{\s*([^,]+),', entry, re.DOTALL)
        if not header_match:
            continue
        entry_type, citation_key = header_match.groups()

        # Find all fields (handles multiline and nested braces)
        fields = {}
        for field_match in re.finditer(r'(\w+)\s*=\s*({(?:[^{}]|{[^{}]*})*}|".*?")\s*,?', entry, re.DOTALL):
            key = field_match.group(1)
            value = field_match.group(2).strip()
            # Remove wrapping braces or quotes
            if value.startswith('{') and value.endswith('}'):
                value = value[1:-1]
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            fields[key] = value.replace('\n', ' ').strip()
        fields['entry_type'] = entry_type
        fields['citation_key'] = citation_key
        parsed_entries.append(fields)

    return pd.DataFrame(parsed_entries)

def save_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"CSV saved to: {output_path}")

if __name__ == "__main__":
    print("Starting BibTeX to CSV conversion...")

    bibs_folder = "bibs"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(bibs_folder):
        if filename.lower().endswith(".bib"):
            bibtex_file = os.path.join(bibs_folder, filename)
            output_csv = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
            print(f"Processing {bibtex_file}...")
            df = parse_bibtex(bibtex_file)
            save_to_csv(df, output_csv)

