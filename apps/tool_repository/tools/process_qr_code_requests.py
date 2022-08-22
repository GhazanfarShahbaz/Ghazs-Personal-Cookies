from qr_code_utils import generate_qrcode_for_url
from typing import Dict
from io import BytesIO 

def processs_generate_link_qr_code(qr_form: Dict[str, str]) -> BytesIO:
    return generate_qrcode_for_url(qr_form["url"])