from app.ingestion.parsers import pdf_parser, docx_parser, pptx_parser, excel_parser

PARSER_FUNCTIONS = {
    "pdf": pdf_parser.parse_pdf,
    "docx": docx_parser.parse_docx,
    "pptx": pptx_parser.parse_pptx,
    "xlsx": excel_parser.parse_xlsx,
}

def get_parser(ext: str):
    return PARSER_FUNCTIONS[ext]