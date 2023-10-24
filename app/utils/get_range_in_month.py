from pandas import date_range


def range_month(start: str, end: str):
    '''
        Return a list of months between two dates

        Parameters:
            start (str): Start date
            end (str): End date

        Returns:
            list: List of months between two dates

        Examples:
            >>> range_month('01/2021', '03/2021')
            ['01/2021', '02/2021', '03/2021']
    '''

    return date_range(start=start, end=end, freq='MS').strftime(
        "%m/%Y").tolist()
