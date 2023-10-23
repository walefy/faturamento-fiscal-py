from weasyprint import HTML
from os import path
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from babel.numbers import format_currency
from decimal import Decimal
from io import BytesIO

path_to_html_src = path.join(path.dirname(__file__), '..', 'html_src')
path_to_html = path.join(path_to_html_src, 'index.html')

html = ''
css = ''


def signature(
    html: BeautifulSoup,
    company_name: str,
    company_cnpj: str,
    is_company: bool = False,
    crc: str = None
):
    signature_div = html.find('div', {'id': 'signature'})

    company_name_p = html.new_tag('p')
    company_name_p.string = company_name

    company_cnpj_p = html.new_tag('p')

    if is_company:
        company_cnpj_p.string = f'CNPJ: {company_cnpj}'
    else:
        company_cnpj_p.string = f'CPF: {company_cnpj}'

        crc_p = html.new_tag('p')
        crc_p.string = f'CRC RJ: {crc}'

    signature_div.append(company_name_p)
    signature_div.append(company_cnpj_p)

    if crc_p:
        signature_div.append(crc_p)


def range_month(start: str, end: str):
    return pd.date_range(start=start, end=end, freq='MS').strftime(
        "%m/%Y").tolist()


def sumValuesList(list: list[str]):
    newValues = []

    for string in list:
        if isinstance(string, str):
            string = string.replace('R$', '')
            string = string.replace('.', '')
            string = string.replace(' ', '')
            string = string.replace(',', '.')

            numberFloat = Decimal(string)
            newValues.append(numberFloat)
        elif isinstance(string, float):
            newValues.append(Decimal(str(string)))
        elif isinstance(string, int):
            newValues.append(Decimal(str(string)))
        else:
            raise Exception('Type not supported')

    result_string = sum(newValues)

    result_string = format_currency(result_string, 'BRL', locale='pt_BR')

    return result_string


def build_pdf(
    target_company_name: str,
    target_company_cnpj: str,
    emitter_name: str,
    emitter_cnpj_or_cpf: str,
    start_time: date,
    end_time: date,
    values: list[str],
    emitter_crc: str = None,
) -> BytesIO:
    buffer = BytesIO()

    with open(path_to_html, 'r') as html_file:
        html = html_file.read()

        soup = BeautifulSoup(html, 'html.parser')
        content_div = soup.find('div', {'id': 'content'})
        description_div = soup.find('div', {'id': 'description'})

        company_name_p = soup.new_tag('p')
        company_name_p.string = target_company_name

        company_cnpj_p = soup.new_tag('p')
        company_cnpj_p.string = f'CNPJ: {target_company_cnpj}'

        description_div.append(company_name_p)
        description_div.append(company_cnpj_p)

        table = soup.new_tag('table')

        month_input = range_month(start_time, end_time)

        for index, month in enumerate(month_input):
            tr = soup.new_tag('tr')

            month_td = soup.new_tag('td')
            month_td.string = month

            value_td = soup.new_tag('td')
            value_td.string = format_currency(
                values[index],
                'BRL',
                locale='pt_BR'
            )

            tr.append(month_td)
            tr.append(value_td)
            table.append(tr)

        tr_total = soup.new_tag('tr')
        td_total = soup.new_tag('td')
        td_total_bold = soup.new_tag('b')
        td_total_bold.string = 'Total'

        td_total_value = soup.new_tag('td')
        td_total_value['style'] = 'font-weight: bold;'
        td_total_value.string = sumValuesList(values)

        td_total.append(td_total_bold)
        tr_total.append(td_total)
        tr_total.append(td_total_value)
        table.append(tr_total)

        content_div.append(table)

        signature(soup, emitter_name, emitter_cnpj_or_cpf, crc=emitter_crc)

        html = str(soup)

    htmlBuilder = HTML(string=html, base_url=path_to_html_src)

    htmlBuilder.write_pdf(buffer)
    return buffer
