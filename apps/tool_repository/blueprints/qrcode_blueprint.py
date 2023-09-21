"""
file_name = qrcode_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for qrcode endpoints.
Edit Log:
07/20/2023
-   Moved qrcode endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request, send_file, current_app

from apps.tool_repository.tools.process_qr_code_requests import (
    processs_generate_link_qr_code,
)

qrcode_blueprint: Blueprint = Blueprint("qrcode", __name__)


@qrcode_blueprint.route("/generateLinkQRCode", methods=["POST"])
def generate_qr_code_for_link():
    """
    Generates a QR code for a link.

    This function generates a QR code for a provided link by
    processing a QR form included in the POST request. The
    function calls the `process_generate_link_qr_code` function to generate the
    QR code, then returns it as a JPEG image.

    Returns:
        A JPEG image object containing the generated QR code.

    Raises:
        None.
    """

    request_form = request.json

    qr_io = processs_generate_link_qr_code(request_form["qrForm"])

    current_app.logger.info(qr_io)

    return send_file(qr_io, mimetype="image/jpeg")
