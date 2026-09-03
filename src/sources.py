from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


class DataSource(ABC):
    SUFFIXES: tuple[str, ...] = ()

    def __init__(self, path: str | Path):
        self._path = None
        self.path = path         

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, value):
        p = Path(value)
        if p.suffix.lower() not in self.SUFFIXES:
            raise ValueError(
                f"{type(self).__name__} cannot read {p.suffix}")
        self._path = p

    @abstractmethod
    def read(self) -> pd.DataFrame:
        ...

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.path.name})"

    def __len__(self) -> int:
        return len(self.read())

    def __eq__(self, other) -> bool:
        if not isinstance(other, DataSource):
            return NotImplemented
        return self.path == other.path


class CSVSource(DataSource):
    SUFFIXES = (".csv",)

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.path)


class JSONSource(DataSource):
    SUFFIXES = (".json",)

    def read(self) -> pd.DataFrame:
        return pd.read_json(self.path)


class ExcelSource(DataSource):
    SUFFIXES = (".xlsx", ".xls")

    def read(self) -> pd.DataFrame:
        return pd.read_excel(self.path)


_REGISTRY = {
    ".csv": CSVSource,
    ".json": JSONSource,
    ".xlsx": ExcelSource,
    ".xls": ExcelSource,
}


def source_for(path: str | Path) -> DataSource:
    suffix = Path(path).suffix.lower()
    if suffix not in _REGISTRY:
        raise ValueError(
            f"Unsupported format: {suffix} ({path})")
    return _REGISTRY[suffix](path)

class ProfileStrategy(ABC):
    @abstractmethod
    def profile(self, df: pd.DataFrame) -> dict:
        ...


class QuickProfile(ProfileStrategy):
    def profile(self, df: pd.DataFrame) -> dict:
        return {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "dtypes": df.dtypes.astype(str).to_dict(),
        }


class DeepProfile(ProfileStrategy):
    def profile(self, df: pd.DataFrame) -> dict:
        return {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict(),
        }    