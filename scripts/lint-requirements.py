import sys
import os
import re
import yaml

def get_banned_words_from_rules(rules_path=".claude/rules/requirements.md"):
    """Dynamically parses the markdown rules file to extract forbidden words from Section 1."""
    banned = []
    if not os.path.exists(rules_path):
        # Fallback defaults if rules file doesn't exist
        return ["fast", "slow", "quickly", "extremely", "user-friendly", "robust"]
        
    with open(rules_path, "r") as f:
        content = f.read()
    
    # Only extract from the italicized comma-separated word lists in Section 1 bullets
    # These lines look like: - **Category**: *word1, word2, word3* (explanation)
    for match in re.finditer(r"\*\*(?:Performance|Time|Usability)\*\*:\s*\*([^*]+)\*", content):
        words_str = match.group(1)
        for word in words_str.split(","):
            cleaned = word.strip().lower()
            if cleaned:
                banned.append(cleaned)
    return list(set(banned))

def validate_yaml_frontmatter(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    parts = content.split("---")
    if len(parts) < 3:
        print(f"❌ Quality Gate Failure: Missing YAML Frontmatter in {file_path}")
        return None, "Invalid YAML format"
        
    try:
        metadata = yaml.safe_load(parts[1])
        return metadata, parts[2]
    except Exception as e:
        print(f"❌ Quality Gate Failure: Failed to parse YAML: {e}")
        return None, str(e)

def lint_requirement_file(file_path, banned_words):
    print(f"🔍 Auditing requirement file: {file_path}")
    metadata, body = validate_yaml_frontmatter(file_path)
    if not metadata:
        return False

    errors = []

    # 1. Check for EARS Grammar Keywords ("shall" is mandatory)
    if "shall" not in body.lower():
        errors.append("Mandatory EARS keyword 'shall' is missing from the requirement statement.")

    # 2. Check for Vague Words (Read dynamically from your rules!)
    for word in banned_words:
        if word in body.lower() or word in metadata.get("title", "").lower():
            errors.append(f"Found banned vague adjective: '{word}'. Replace with a quantifiable metric.")

    # 3. Dynamic Grounding Verification (Reads whatever source file is in the YAML)
    source_file = metadata.get("source")
    lines_range = str(metadata.get("lines", ""))
    evidence_quote = metadata.get("evidence_quote")

    if not source_file or not lines_range or not evidence_quote:
        errors.append("Missing source traceback metadata ('source', 'lines', or 'evidence_quote').")
    else:
        if not os.path.exists(source_file):
            errors.append(f"Cited source file does not exist: {source_file}")
        else:
            try:
                start_line, end_line = map(int, lines_range.split("-"))
                with open(source_file, "r") as f:
                    source_lines = f.readlines()
                
                # Build transcript marker index (L## -> cleaned content)
                transcript_index = {}
                for file_line in source_lines:
                    stripped = file_line.strip()
                    marker = re.match(r'^L(\d+)\s', stripped)
                    if marker:
                        line_num = int(marker.group(1))
                        cleaned = re.sub(r"^L\d+\s+(?:[A-Z]:\s*)?", "", stripped)
                        transcript_index[line_num] = cleaned
                
                # Use transcript markers if they exist in the range, else fall back to file lines
                has_markers = any(ln in transcript_index for ln in range(start_line, end_line + 1))
                
                evidence_segment = []
                if has_markers:
                    for ln in range(start_line, end_line + 1):
                        if ln in transcript_index:
                            evidence_segment.append(transcript_index[ln])
                else:
                    for idx in range(start_line - 1, min(end_line, len(source_lines))):
                        line_text = source_lines[idx].strip()
                        cleaned_line = re.sub(r"^L\d+\s+(?:[A-Z]:\s*)?", "", line_text)
                        evidence_segment.append(cleaned_line)
                
                source_paragraph = " ".join(evidence_segment).lower()
                cleaned_quote = re.sub(r"\s+", " ", evidence_quote.strip().lower())
                
                source_clean = re.sub(r"[^\w\s]", "", source_paragraph)
                quote_clean = re.sub(r"[^\w\s]", "", cleaned_quote)

                quote_sub_chunks = [c.strip() for c in quote_clean.split("dot") if c.strip()]
                
                for chunk in quote_sub_chunks:
                    if chunk not in source_clean:
                        errors.append(
                            f"Grounding Audit Failed! Cited quote does not appear in source {source_file} at lines {lines_range}.\n"
                            f"Cited quote: '{evidence_quote}'\n"
                            f"Found lines in source: '{' '.join(source_lines[start_line-1:end_line]).strip()}'"
                        )
                        break
            except Exception as e:
                errors.append(f"Grounding verification crashed: {e}")

    if errors:
        for err in errors:
            print(f"❌ Quality Gate Failure: {err}")
        print("-" * 50)
        return False
    
    print("✅ Success: Requirement passed all automated checks!")
    print("-" * 50)
    return True

if __name__ == "__main__":
    req_dir = "requirements"
    banned_words = get_banned_words_from_rules()
    print(f"⚙️ Loaded dynamic banned word list: {banned_words}")
    
    all_passed = True

    # Pass 1: Check for duplicate requirement IDs
    ids_seen = {}
    for file in sorted(os.listdir(req_dir)):
        if file.endswith(".md") and not file.startswith("_"):
            filepath = os.path.join(req_dir, file)
            metadata, _ = validate_yaml_frontmatter(filepath)
            if metadata:
                req_id = metadata.get("id", "")
                if req_id in ids_seen:
                    print(f"❌ Quality Gate Failure: Duplicate ID '{req_id}' in {filepath} and {ids_seen[req_id]}")
                    all_passed = False
                else:
                    ids_seen[req_id] = filepath

    # Pass 2: Lint each requirement file
    for file in sorted(os.listdir(req_dir)):
        if file.endswith(".md") and not file.startswith("_"):
            filepath = os.path.join(req_dir, file)
            if not lint_requirement_file(filepath, banned_words):
                all_passed = False
                
    sys.exit(0 if all_passed else 1)
