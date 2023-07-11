from io import BytesIO

from django.db.models import Sum
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import RecipeIngredient


def create_pdf(request):
    '''Create PDF cart file.'''

    # Absolute path to TrueType cyrillic font
    path = 'D:/Dev/foodgram-project-react/backend/static/data/DejaVuSerif.ttf'

    pdfmetrics.registerFont(TTFont('DejaVuSerif', path))
    buffer = BytesIO()
    doc = canvas.Canvas(buffer, pagesize=letter)
    doc.setFont('DejaVuSerif', 18)
    doc.drawCentredString(x=140, y=740, text='Список покупок')
    textobject = doc.beginText()
    textobject.setTextOrigin(40, 660)
    textobject.setFont('DejaVuSerif', 16)

    qs = RecipeIngredient.objects.filter(
        recipe_id__cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

    for ingredient in qs:
        name = ingredient['ingredient__name']
        measure = ingredient['ingredient__measurement_unit']
        amount = ingredient['amount']
        textobject.textLine(f'{name} ({measure}) — {amount}')
        textobject.moveCursor(0, 8)

    doc.drawText(textobject)
    doc.showPage()
    doc.save()

    buffer.seek(0)

    return FileResponse(
        buffer, as_attachment=True, filename='shopping_list.pdf')
