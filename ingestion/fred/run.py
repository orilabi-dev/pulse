from dotenv import load_dotenv
import os

from ingestion.fred.client import FREDClient
from ingestion.base.exceptions import APIConnectionError

load_dotenv()
api_key = os.getenv("FRED_API_KEY")

series = ["CPIAUCSL","UNRATE","FEDFUNDS"]

def main():
    if not api_key:
        raise APIConnectionError("lease visit https://fred.stlouisfed.org/docs/api/api_key.html to generate your api key")
    
    fred_client = FREDClient(api_key=api_key)
    
    for id in series:
        data = fred_client.fetch_observations(series_id=id)
        
        count = len(data.get("observations",[]))
        
        print(f"Successfully extracted {count} rows of data for series: {id}")
        
if __name__ == "__main__":
    main()