import duckdb
import json
from pathlib import Path
from ingestion.base.logger import get_logger

logger = get_logger(__name__)

DATA_RAW = Path("data/raw")
DB_PATH = Path("data/pulse.duckdb")

def load_fred_series(conn: duckdb.DuckDBPyConnection, series_id: str) -> int:
    """
    Load a FRED JSON file into a DuckDB table.
    Returns the number of rows inserted.

    Args:
        conn (duckdb.DuckDBPyConnection): _description_
        series (id): _description_

    Returns:
        int: _description_
    """
    file_path = DATA_RAW /f"fred_{series_id}.json"
    
    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return 0
    
    with open(file_path) as f:
        raw = json.load(f)
        
    observations = raw.get("observations",[])
    
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS fred_{series_id} (
            date DATE,
            value DOUBLE,
            series_id VARCHAR
        )             
    """)
    
    conn.execute(f"DELETE FROM fred_{series_id}")
    
    rows = [
        (obs["date"], float(obs["value"]) if obs["value"] != "." else None, series_id)
        for obs in observations
    ]
    
    conn.executemany(
        f"INSERT INTO fred_{series_id} VALUES (?, ?, ?)",
        rows
    )
    
    logger.info(f"Loaded {len(rows)} rows into fred_{series_id}")
    return len(rows)

def main():
    conn = duckdb.connect(str(DB_PATH))
    series = ["CPIAUCSL","UNRATE","FEDFUNDS"]
    
    for s in series:
        load_fred_series(conn, s)
        
    conn.close()
    logger.info(f"Database saved to {DB_PATH}")
    
if __name__ == "__main__":
    main()