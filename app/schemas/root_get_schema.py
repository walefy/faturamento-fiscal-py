from datetime import date

from pydantic import BaseModel, Field


class RegisterCompany(BaseModel):
    company_name: str
    company_cnpj: str


class PdfRegister(BaseModel):
    target_company_name: str = Field(min_length=3, max_length=55)
    target_company_cnpj: str = Field(min_length=14, max_length=15)
    emitter_name: str = Field(min_length=3, max_length=55)
    emitter_cnpj_or_cpf: str = Field(min_length=11, max_length=14)
    crc: str = None
    start_time: date
    end_time: date
    values: list[str]
