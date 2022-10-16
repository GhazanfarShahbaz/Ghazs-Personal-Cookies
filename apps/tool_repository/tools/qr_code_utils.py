import qrcode

from io import BytesIO


def get_qr_settings() -> qrcode.main.QRCode:
    qr: qrcode.main.QRCode = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    return qr


def qr_code_to_io(qr_code) -> BytesIO:
    img_io = BytesIO()
    qr_code.save(img_io, 'PNG', quality=70)
    img_io.seek(0)

    return img_io


def generate_qrcode_for_url(url: str) -> BytesIO:
    qr: qrcode.main.QRCode = get_qr_settings()

    qr.make(fit=True)
    qr.add_data(data=url)

    img = qr.make_image(back_color=(0, 0, 0), fill_color=(226, 220, 110))

    return qr_code_to_io(img)
