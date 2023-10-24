from decimal import Decimal


def format_str_to_decimal(string: str) -> Decimal:
    '''
        This function receives a string and returns a Decimal number.
        The string must be in the format 'R$ 1.000,00'.
        The return is a Decimal number.

        Example:
        >>> format_str_to_decimal('R$ 1.000,00')
        Decimal('1000.00')
    '''

    string = string.replace('R$', '')
    string = string.replace('.', '')
    string = string.replace(' ', '')
    string = string.replace(',', '.')

    number = Decimal(string)

    return number
