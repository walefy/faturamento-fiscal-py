# from pydantic import BaseModel, Field, field_validator, validator
# from datetime import date, timedelta

from pydantic import BaseModel, Field
from datetime import date


class RegisterCompany(BaseModel):
    company_name: str
    company_cnpj: str


class PdfRegister(BaseModel):
    target_company_name: str = Field(min_length=3, max_length=55)
    target_company_cnpj: str
    emitter_name: str = Field(min_length=3, max_length=55)
    crc: str = None
    start_time: date
    end_time: date
    values: list[str]

    # @field_validator('start_time')
    # @classmethod
    # def start_time_is_valid(cls, value):
    #     if value > cls.end_time:
    #         raise ValueError('start_time must be less than end_time')
    #     return value

    # @field_validator('end_time')
    # @classmethod
    # def end_time_is_valid(cls, value):
    #     if value < cls.start_time:
    #         raise ValueError('end_time must be greater than start_time')
    #     return value

    # @validator('start_time', 'end_time')
    # @classmethod
    # def date_range_is_valid(cls, value):
    #     if cls.start_time and cls.end_time:
    #         twenty_four_months_in_days = 730
    #         delta = cls.end_time - cls.start_time
    #         if delta > timedelta(days=twenty_four_months_in_days):
    #             raise ValueError(
    #              'The date range must be less than 24 months')
    #     return value
