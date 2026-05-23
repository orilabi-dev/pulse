#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

set -e
set -u
set -o pipefail

colors_dir="$SCRIPT_DIR/colors.sh"

source $colors_dir

info "Validating JSON files"

if [[ ! -f ".env" ]]; then
    error "No environment file present. Run setup.sh and try again."
fi

source .env

data_raw_dir="$DATA_DIR/raw"
empty_files=0
non_empty_files=0
valid_json_files=0
invalid_json_files=0

file_count=$(find $data_raw_dir -type f | wc -l | xargs)

for file in "$data_raw_dir"/*.json; do
    [[ -f "$file" ]] || continue

    if [[ ! -s "$file" ]]; then
        ((empty_files++))
        warning "$file is empty, please review"
    else
        ((non_empty_files++))
        if python3 -m json.tool "$file" &> /dev/null; then
            ((valid_json_files++))
            success "$file - valid JSON"
        else
            ((invalid_json_files++))
            warning "$file - invalid JSON"
        fi
    fi
done

info "Validation complete — $file_count files found: $valid_json_files valid, $empty_files empty, $invalid_json_files invalid."