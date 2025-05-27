def format_as_html(row, path):
    if len(row) < 4:
        return "Yangi javob to'liq emas."

    response = f"""Sizning test natijangiz:
       
telegra.ph/{path}
"""

    return response

def format_as_html_parents(row, path):
    if len(row) < 4:
        return "Yangi javob to'liq emas."

    response = f"""Farzandingizning test natijasi: {row[21]}  telegra.ph/{path} Moliyaviy savodxonlik kursi: +998996007707"""

    return response