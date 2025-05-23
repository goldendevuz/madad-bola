def format_as_html(row):
    if len(row) < 4:
        return "Yangi javob to'liq emas."

    response = f"""Test natijangiz:
       
{row[21]} {row[22]}
"""

    return response

def format_as_html_parents(row, path):
    if len(row) < 4:
        return "Yangi javob to'liq emas."

    response = f"""Farzandingizning test natijasi: {row[21]}  https://telegra.ph/{path} Moliyaviy savodxonlik kursi: +998996007707"""

    return response