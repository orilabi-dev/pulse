class PulseIngestionError(Exception):
    """Base exception for all ingestion errors."""
    pass

class APIConnectionError(PulseIngestionError):
    """Raised when a connection to an external API cannot be established."""
    pass

class APIResponseError(PulseIngestionError):
    """Raised when an API returns an unexpected or error response."""
    def __init__(self, status_code:int, message:str):
        self.status_code=status_code
        super().__init__(f"API error {status_code}: {message}")
        
class DataValidationError(PulseIngestionError):
    """Raised when ingested data fails validation checks."""
    pass