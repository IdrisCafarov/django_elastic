import random
import string
# import pandas as pd
# from io import BytesIO
# from openpyxl import Workbook


from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
import xml.etree.ElementTree as ET
# from app.core.payment.epoint import KapitalPayment
from account.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse



def code_slug_generator(size=12, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_slug_shortcode(size, model_):
    new_code = code_slug_generator(size=size)
    qs_exists = model_.objects.filter(slug=new_code).exists()
    return create_slug_shortcode(size, model_) if qs_exists else new_code






# class ExcelExporter:
#     def __init__(self, queryset, field_names, filename, sheet_name):
#         self.queryset = queryset
#         self.field_names = field_names
#         self.filename = filename
#         self.sheet_name = sheet_name

#     def export(self):
#         # Convert queryset to a list of dictionaries
#         data = list(self.queryset.values(*self.field_names))

#         # Create a new Excel workbook
#         workbook = Workbook()

#         # Access the active sheet
#         sheet = workbook.active

#         # Write header row
#         for col_num, field_name in enumerate(self.field_names, 1):
#             sheet.cell(row=1, column=col_num, value=field_name)

#         # Write data rows
#         for row_num, row_data in enumerate(data, 2):
#             for col_num, field_name in enumerate(self.field_names, 1):
#                 sheet.cell(row=row_num, column=col_num, value=row_data[field_name])

#         # Create a BytesIO buffer to write the Excel file to
#         excel_buffer = BytesIO()

#         # Save the workbook to the buffer
#         workbook.save(excel_buffer)

#         # Seek to the beginning of the buffer
#         excel_buffer.seek(0)

#         # Create an HTTP response with the Excel file
#         response = HttpResponse(excel_buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = f'attachment; filename={self.filename}'

#         return response