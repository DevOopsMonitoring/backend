from src.models import Company
from fpdf import FPDF
from flask import send_file


def number_employees_in_companies():
    companies = Company.query.all()
    result = []
    for company in companies:
        result.append({
            'name': company.name,
            'count': len(company.users)
        })

    return {"report":  result}

def number_employees_in_companies_print():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    companies = Company.query.all()
    for i, company in enumerate(companies):
        text = f'В компании "{company.name}" работает {len(company.users)} человек'
        pdf.cell(200, 10, txt=text, ln=i+1, align="L")

    pdf.output("simple_demo.pdf")
    pdf.close()
    static_file = open('simple_demo.pdf', 'rb')
    return send_file(static_file, mimetype='application/pdf')


def number_servers_in_companies():
    companies = Company.query.all()
    result = []
    for company in companies:
        result.append({
            'name': company.name,
            'count': sum([len(u.servers) for u in company.users])
        })

    return {"report":  result}


def number_servers_in_companies_print():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    companies = Company.query.all()
    for i, company in enumerate(companies):
        text = f'В компании "{company.name}" находится {sum([len(u.servers) for u in company.users])} серверов'
        pdf.cell(200, 10, txt=text, ln=i + 1, align="L")

    pdf.output("simple_demo.pdf")
    pdf.close()
    static_file = open('simple_demo.pdf', 'rb')
    return send_file(static_file, mimetype='application/pdf')
