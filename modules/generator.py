from jinja2 import Template
import pdfkit
import tempfile
import os
import base64

def generate_pdf(data):
    # ================= BASE64 LOGO (FIX TOTAL) =================
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "..", "logo.jpg")
    logo_path = os.path.abspath(logo_path)

    print("LOGO EXISTS:", os.path.exists(logo_path))

    with open(logo_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    data["logo"] = f"data:image/jpeg;base64,{encoded}"

    # ================= LOAD TEMPLATE =================
    with open("templates/template.html", encoding="utf-8") as f:
        template = Template(f.read())

    html = template.render(**data)

    # ================= TEMP HTML =================
    tmp_html = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    tmp_html.write(html.encode("utf-8"))
    tmp_html.close()

    pdf_path = tmp_html.name.replace(".html", ".pdf")

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    options = {
        'enable-local-file-access': None
    }

    pdfkit.from_file(
        tmp_html.name,
        pdf_path,
        configuration=config,
        options=options
    )

    with open(pdf_path, "rb") as f:
        return f.read(), html