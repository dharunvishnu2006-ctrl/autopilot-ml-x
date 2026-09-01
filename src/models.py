from dataclasses import dataclass
import pandas as pd
from datetime import datetime, timezone

@dataclass
class IngestResult:
    source: str                
    ok: bool                   
    frame: pd.DataFrame | None = None   
    error: str | None = None    

    def __bool__(self) -> bool:
        return self.ok             

@dataclass
class ColumnProfile:
    name: str                  
    dtype: str                   
    missing: int                
    unique: int                 


@dataclass
class DatasetProfile:
    source: str                       
    rows: int                        
    cols: int                        
    columns: list[ColumnProfile]     
    profiled_at: str = ""              

    def __post_init__(self):
        if not self.profiled_at:
            self.profiled_at = (
                datetime.now(timezone.utc).isoformat())
