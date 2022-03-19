from flask import render_template 
from datetime import date
import io
from xhtml2pdf import pisa 

SOURCE_HTML = "transcript_template.html"

class DocumentHelper() : 
   def __init__(self,app) :
      pass
   def get_document() : 
      pass
   
   def generate_document(self,tc_data) :
    buffer = io.BytesIO()  
    template = render_template(SOURCE_HTML,score_list = tc_data['score_list'],student=tc_data['student_identity'],date=date.today())
    pisa_status = pisa.CreatePDF(
            template,                # the HTML to convert
            dest=buffer)
    buffer.seek(0)
    return buffer,pisa_status.err
