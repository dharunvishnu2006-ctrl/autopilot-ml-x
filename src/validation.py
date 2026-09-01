from pydantic import BaseModel, field_validator


class DatasetSchema(BaseModel):
    source: str                  
    row_count: int                 
    required_columns: list[str]    
    present_columns: list[str]     

    @field_validator("row_count")
    @classmethod
    def row_count_must_be_positive(cls, v, info):
        if v < 0:
            raise ValueError(
                f"{info.data.get('source')}: "
                f"negative row count ({v})")
        return v

    def missing_columns(self) -> list[str]:
        return [c for c in self.required_columns
                if c not in self.present_columns]

    def is_valid(self) -> bool:
        return len(self.missing_columns()) == 0    