from src.models import Company, Server, ReadData
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

def count_sensors_on_server():
    servers = Server.query.all()
    result = []
    for server in servers:
        result.append({
            'name': server.name,
            'count': len(server.reading_rules)
        })
    return {'report': result}


def count_fail_on_server():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    for i, server in enumerate(Server.query.all()):
        tmp = 0
        for rule in server.reading_rules:
            tmp += ReadData.query.filter(ReadData.server_id==server.id, ReadData.sensor_id==rule.sensor_id, ReadData.value > rule.critical_value).count()
            print(ReadData.query.filter(ReadData.server_id==server.id, ReadData.sensor_id==rule.sensor_id, ReadData.value > rule.critical_value).all())

        text = f'Сервер "{server.name}" достиг критического значения {tmp} раз'
        pdf.cell(200, 10, txt=text, ln=i + 1, align="L")

    pdf.output("simple_demo.pdf")
    pdf.close()
    static_file = open('simple_demo.pdf', 'rb')
    return send_file(static_file, mimetype='application/pdf')


def count_sensors_on_server_print():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    servers = Server.query.all()

    for i, server in enumerate(servers):
        text = f'На сервере "{server.name}" установлено {len(server.reading_rules)} датчиков'
        pdf.cell(200, 10, txt=text, ln=i + 1, align="L")

    pdf.output("simple_demo.pdf")
    pdf.close()
    static_file = open('simple_demo.pdf', 'rb')
    return send_file(static_file, mimetype='application/pdf')


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
