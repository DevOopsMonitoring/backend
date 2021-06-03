from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from src.api.schemas import CompanySchema
from src.models import Company
from src.extensions import db
from src.commons.pagination import paginate


class CompanyResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, company_id):
        schema = CompanySchema()
        company = Company.query.get_or_404(company_id)
        return {"company": schema.dump(company)}

    def put(self, company_id):
        schema = CompanySchema(partial=True)
        company = Company.query.get_or_404(company_id)
        company = schema.load(request.json, instance=company)

        db.session.commit()

        return {"msg": "Company updated", "company": schema.dump(company)}

    def delete(self, company_id):
        company = Company.query.get_or_404(company_id)
        db.session.delete(company)
        db.session.commit()

        return {"msg": "Company deleted"}


class CompanyList(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        schema = CompanySchema(many=True, exclude=('phone', ))
        query = Company.query
        for key, item in request.args.items():
            query = query.filter(getattr(Company, key).like(item))
        return paginate(query, schema)

    def post(self):
        schema = CompanySchema()
        company = schema.load(request.json)

        db.session.add(company)
        db.session.commit()

        return {"msg": "Company created", "company": schema.dump(company)}, 201
