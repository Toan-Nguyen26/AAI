from typing import Optional, Literal, TypedDict

# Parameter type definitions
class WeightHeightParams(TypedDict):
    gender: Optional[Literal['male', 'female']]
    years_old: int
    months_old: int
    height: Optional[float]
    weight: Optional[float]

class AnomalyParams(TypedDict):
    anomaly_category: Literal['physical', 'mental', 'others'] 