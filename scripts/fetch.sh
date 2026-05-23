#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

set -e
set -u
set -o pipefail

# Extract the functions for logging
source "$SCRIPT_DIR/colors.sh"

if [[ ! -f ".env" ]]; then
    error "No environment file present. Run setup.sh and try again."
fi

source .env

if [[ -z "$FRED_API_KEY" ]]; then
    error "Please visit https://fred.stlouisfed.org/docs/api/api_key.html to generate your api key"
fi

data_raw_dir="$DATA_DIR/raw"

if [[ ! -d $data_raw_dir ]]; then
    info "Creating data/raw directory"
    mkdir -p $data_raw_dir
    success "Directory created"
else
    success "Directory already exists"
fi

series=("CPIAUCSL" "UNRATE" "FEDFUNDS")

for id in "${series[@]}"; do
    info "Fetching data for series: $id"
    curl -sf "https://api.stlouisfed.org/fred/series/observations?series_id=$id&api_key=$FRED_API_KEY&file_type=json" -o "$data_raw_dir/fred_$id.json"
    success "Raw data extracted successfully for $id"
done

file_count=$(find $data_raw_dir -type f | wc -l | xargs)

success "$file_count successfully added to the $data_raw_dir directory"