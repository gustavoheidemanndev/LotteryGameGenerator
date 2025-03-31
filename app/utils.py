
import io
from reportlab.pdfgen import canvas


def generate_pdf(list):
    buffer = io.BytesIO()
    total_combinations = len(list)
    p = canvas.Canvas(buffer)
    max_lines_por_pagina = 38
    titlePosition = 800
    p.drawString(100, titlePosition, str(total_combinations))
    initialPosition = 750
    y = initialPosition
    linhas_na_pagina = 0
    for item in list:
        p.drawString(100, y, str(item))
        y -= 20
        linhas_na_pagina += 1
        if linhas_na_pagina == max_lines_por_pagina:
            p.showPage()
            y = initialPosition
            linhas_na_pagina = 0

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer