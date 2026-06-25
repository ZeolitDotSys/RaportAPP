from pydantic import BaseModel, Field


class ReportRequest(BaseModel):
    weather: str = Field(default="-")
    operator: str = Field(default="")
    inspection: str = Field(default="")
    company: str = Field(default="")
    city: str = Field(default="")
    street: str = Field(default="")
    start_manhole: str = Field(default="")
    end_manhole: str = Field(default="")
    distance: float = Field(gt=0)
    level_difference: float
    filming_date: str = Field(default="")
    diameter: str = Field(default="")


class ReportResponse(BaseModel):
    image_url: str
    filename: str
    distance: float
    level_difference: float
    start_manhole: str
    end_manhole: str
