from weasyprint import HTML
from os import path
from bs4 import BeautifulSoup
import pandas as pd
import locale
from decimal import Decimal

path_to_html_src = path.join(path.dirname(__file__), 'html_src')
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


def get_values(range_numbers=12):
    values = []
    values_default = ['1.000.000.000,50', '2.000.000.000,34']
    for _ in range(range_numbers):
        # index = random.randint(0, 1)
        values.append(values_default[0])
    return values


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

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    result_string = locale.currency(result_string, grouping=True)

    return result_string


with open(path_to_html, 'r') as html_file:
    html = html_file.read()

    soup = BeautifulSoup(html, 'html.parser')
    content_div = soup.find('div', {'id': 'content'})
    description_div = soup.find('div', {'id': 'description'})

    faturamento_meses = input('meses: ')
    company_name = input('company_name: ')
    company_cnpj = input('company_cnpj: ')

    company_name_p = soup.new_tag('p')
    company_name_p.string = company_name

    company_cnpj_p = soup.new_tag('p')
    company_cnpj_p.string = f'CNPJ: {company_cnpj}'

    description_div.append(company_name_p)
    description_div.append(company_cnpj_p)

    table = soup.new_tag('table')

    month_input = range_month('2020-01-01', '2021-12-01')
    values = get_values(24)
    for index, month in enumerate(month_input):
        tr = soup.new_tag('tr')

        month_td = soup.new_tag('td')
        month_td.string = month

        value_td = soup.new_tag('td')
        value_td.string = f'R$ {str(values[index])}'

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

    signature(soup, company_name, company_cnpj, crc='123456789')

    html = str(soup)

htmlBuilder = HTML(string=html, base_url=path_to_html_src)

htmlBuilder.write_pdf('./test_pdf.pdf')
