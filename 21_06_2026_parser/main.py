import json
from openpyxl import Workbook

import requests
from bs4 import BeautifulSoup


def _get_soup(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        if response.status_code != 200:
            return None
        return soup
    except Exception as e:
        print(f"Error: {e}")

def _get_headers(soup):
    headers = []
    first_row = soup.find_all('th')
    if first_row:
        headers = [header.text.strip() for header in first_row]
    return headers

def parse_data(soup):
    data = []
    currency = soup.find('table', class_='data')
    if currency is None:
        return []

    rows = currency.find_all('tr')

    for row in rows[1:]:
        tds = row.find_all('td')
        currency = {
            "digit_code": tds[0].text.strip(),
            "char_code": tds[1].text.strip(),
            "count": tds[2].text.strip(),
            "name": tds[3].text.strip(),
            "rate": tds[4].text.strip(),
        }
        data.append(currency)

    return data

def _save_json(data:list):
    with open('json.txt', 'w', encoding='utf-8') as f:
        try:
            json_string = json.dumps(data, ensure_ascii=False, indent=2)
            f.write(json_string,)
            print("JSON записан")
        except Exception as e:
            print(f"Error: {e}")

def _save_excel(data:list, headers:list):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Курсы валют"

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)

        for row, currency in enumerate(data, 2):
            ws.cell(row=row, column=1, value=currency["digit_code"])
            ws.cell(row=row, column=2, value=currency["char_code"])
            ws.cell(row=row, column=3, value=currency["count"])
            ws.cell(row=row, column=4, value=currency["name"])
            ws.cell(row=row, column=5, value=currency["rate"])

        wb.save('currency.xlsx')
        print("Excel файл успешно создан")
    except Exception as e:
        print(f"Error: {e}")



def get_currency_data(url:str) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    soup = _get_soup(url, headers)
    if soup is None:
        return None

    tabel_headers = _get_headers(soup)
    data = parse_data(soup)
    print("Как сохранить данные?")
    print("1. JSON")
    print("2. Excel")
    request = input(">>> ")
    match(request):
        case '1':
            _save_json(data)
        case '2':
            _save_excel(data,tabel_headers)
    return None


if __name__ == "__main__":
    url = "https://www.cbr.ru/currency_base/daily/"
    get_currency_data(url)