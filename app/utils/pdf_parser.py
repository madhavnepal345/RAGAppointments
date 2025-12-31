from typing import Optional,Tuple
import PyPDF2
from io import BytesIO
import logging


logger = logging.getLogger(__name__)

class FileParser:
    @staticmethod
    def parse_pdf(file_content:bytes)->str:
        try:
            pdf_reader=PyPDF2.PDFReader(BytesIO(file_content))
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise ValueError("Failed to parse PDF file") from e
    
    @staticmethod
    def Parse_text(file_content:bytes)->str:
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            return file_content.decode('latin-1')
        
    @staticmethod
    def parse_file(file_content:bytes,filename:str)->Tuple[str,str]:
        if filename.lower().endswith('.pdf'):
            return FileParser.parse_pdf(file_content),'pdf'
        elif filename.lower().endswith('.txt'):
            return FileParser.Parse_text(file_content),'text'
        else:
            raise ValueError("Unsupported file type")
