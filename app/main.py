from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pdf_builder.pdf_builder import build_pdf
from schemas.root_get_schema import PdfRegister, RegisterCompany

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/', status_code=status.HTTP_200_OK)
def root(pdf_register: PdfRegister):
    file_pdf_buffer = build_pdf(pdf_register)

    file_pdf_buffer.seek(0)

    return StreamingResponse(
        content=file_pdf_buffer,
        media_type='application/pdf',
    )


@app.post('/company/register')
def register_company(company: RegisterCompany):
    '''
        TODO: Register a company in the database
    '''
