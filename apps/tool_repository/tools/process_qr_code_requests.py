from qr_code_utils import generate_qrcode_for_url
from typing import Dict
from io import BytesIO


def processs_generate_link_qr_code(qr_form: Dict[str, str]) -> BytesIO:
    """
    Processes a request to generate a QR code for a link.

    This function takes a dictionary `qr_form` containing a single key "url", representing the link for which the QR code needs
    to be generated. This then calls the `generate_qrcode_for_url()` function to generate the QR code for the given URL and
    returns a BytesIO object containing the QR code.

    Args:
        qr_form: A dictionary containing the URL for which the QR code needs to be generated.

    Returns:
        A BytesIO object containing the generated QR code.
    """
    
    return generate_qrcode_for_url(qr_form["url"])
