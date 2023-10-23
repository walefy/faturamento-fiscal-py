from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from schemas.root_get_schema import RegisterCompany, PdfRegister
from pdf_builder.pdf_builder import build_pdf

app = FastAPI()


@app.post('/', status_code=status.HTTP_200_OK)
def root(pdf_register: PdfRegister):
    file_pdf = build_pdf(
        emitter_cnpj_or_cpf='123456789',
        emitter_crc=pdf_register.crc,
        emitter_name=pdf_register.emitter_name,
        target_company_name=pdf_register.target_company_name,
        target_company_cnpj=pdf_register.target_company_cnpj,
        start_time=pdf_register.start_time,
        end_time=pdf_register.end_time,
        values=pdf_register.values
    )

    return FileResponse(
        file_pdf,
        media_type='application/pdf',
        filename='output.pdf'
    )


@app.post('/company/register')
def register_company(company: RegisterCompany):
    '''
        TODO: Register a company in the database
    '''