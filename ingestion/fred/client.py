import requests
from ingestion.base.exceptions import APIConnectionError, APIResponseError
from ingestion.base.logger import get_logger

logger = get_logger(__name__)

FRED_BASE_URL = "https://api.stlouisfed.org/fred"

class FREDClient:
    """
    Client for the Federal Reserve Economic Data (FRED) API. Handles authentication, requests, and error handling.
    """
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.base_url = FRED_BASE_URL
        self.session = requests.Session()
        logger.info("FREDClient initialized.")
        
    def _build_params(self, series_id: str) -> dict:
        """
        Build query parameters for an observations request

        Args:
            series_id (str): FRED series identifier e.g. 'UNRATE'

        Returns:
            dict: The parsed params as a dictionary
        """
        return {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json"
        }
    
    def fetch_observations(self, series_id: str) -> dict:
        """
        Fetch all observations for a given FRED series.

        Args:
            series_id (str): The FRED series identifier e.g. 'UNRATE'

        Returns:
            dict: The parsed JSON response as a dictionary
        
        Raises:
            APIConnectionError: If the request cannot be made
            APIResponseError: If the API returns a non-200 response
        """
        url = f"{self.base_url}/series/observations"
        params = self._build_params(series_id)
        
        logger.info(f"Fetching observations for series: {series_id}")
        
        try:
            resp = self.session.get(url=url,params=params)
            
            if resp.status_code != 200:
                raise APIResponseError(
                    status_code=resp.status_code,
                    message=resp.text
                )
            
            observations = resp.json()
            count = len(observations.get("observations",[]))
            logger.info(f"Successfully fetched {count} observations for {series_id}")
            
            return observations
        except requests.exceptions.ConnectionError:
            raise APIConnectionError
        