# pulse

A data engineering project that ingests economic indicators from public APIs, transforms them into structured datasets, and serves a live dashboard.

## Data Sources
- [FRED](https://fred.stlouisfed.org/) - Federal Reserve Economic Data

## Setup
1. Clone the repo
2. Run `./scripts/setup.sh`
3. Fill in your API keys in `.env`
4. Run `./scripts/fetch.sh` to ingest data

## Project Structure
- `ingestion/` - Python ingestion scripts
- `transformation/` - dbt models
- `orchestration/` - Airflow DAGs
- `infrastructure/` - Terraform configs
- `scripts/` - shell utilities
- `tests/` - all test types