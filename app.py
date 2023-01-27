from flask import Flask, request
from database import connector
from model import InstitutionModel, UserModel, ProjectModel
from schemas import (
    Institution,
    Institutions,
    Users,
    User,
    Projects,
    Project,
    ProjectWithDaysLeft,
    InstitutionCreateData,
    InstitutionUpdateData,
)
from datetime import date
from flask_pydantic import validate

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route("/institutions", methods=["GET"])
@validate()
def fetch_institutions():
    db_session = db.getSession(engine)
    if request.method == "GET":
        institutions_orm = db_session.query(InstitutionModel).all()
        institutions = Institution.from_orms(institutions_orm)
        institutions_result = Institutions(institutions=institutions)
        return institutions_result


@app.route("/institutions", methods=["POST"])
@validate()
def create_institution(body: InstitutionCreateData):
    db_session = db.getSession(engine)
    if request.method == "POST":
        new_institution = InstitutionModel(**body.dict())
        db_session.add(new_institution)
        db_session.commit()
        return "New institution created!"
    return "Method not allowed"


@app.route("/institutions/<institution_id>", methods=["PATCH"])
@validate()
def patch_institution(institution_id, body: InstitutionUpdateData):
    db_session = db.getSession(engine)
    if request.method == "PATCH":
        institution = db_session.query(InstitutionModel).get({"id": institution_id})
        institution.name = body.name
        institution.description = body.description
        institution.address = body.address
        db_session.add(institution)
        db_session.commit()
        return f"Institution with id = {institution_id} updated!"
    return "Method not allowed"


@app.route("/institutions/<institution_id>", methods=["DELETE"])
@validate()
def delete_institution(institution_id):
    db_session = db.getSession(engine)

    if request.method == "DELETE":
        institution = (
            db_session.query(InstitutionModel)
            .filter(InstitutionModel.id == institution_id)
            .first()
        )
        db_session.delete(institution)
        db_session.commit()
        return f"Institution with id {institution_id} deleted"

    return "Method not allowed"


@app.route("/institutions/<institution_id>", methods=["GET"])
@validate()
def fetch_institution_by_id(institution_id):
    db_session = db.getSession(engine)
    if request.method == "GET":
        institution_orm = db_session.query(InstitutionModel).get({"id": institution_id})
        institution_result = Institution.from_orm(institution_orm)
        return institution_result

    return "Method not allowed"


@app.route("/institutions/with-adress-url", methods=["GET"])
@validate()
def fetch_institutions_with_adress_url():
    db_session = db.getSession(engine)
    if request.method == "GET":
        institutions_orm = db_session.query(InstitutionModel).all()
        institutions = Institution.from_orms(institutions_orm)

        for institution in institutions:
            address = institution.address
            name = institution.name
            institution.address = f"https://www.google.com/maps/search/{address}"
            institution.name = name[0:3]

        intitutions_result = Institutions(institutions=institutions)
        return intitutions_result

    return "Method not allowed"


@app.route("/users", methods=["GET"])
@validate()
def fetch_users():
    db_session = db.getSession(engine)
    if request.method == "GET":
        users_orm = db_session.query(UserModel).all()
        users = User.from_orms(users_orm)
        users_result = Users(users=users)
        return users_result

    return "Method not allowed"


@app.route("/users/<user_rut>", methods=["GET"])
@validate()
def fetch_user_by_rut(user_rut):
    db_session = db.getSession(engine)
    if request.method == "GET":
        user_orm = db_session.query(UserModel).filter(UserModel.RUT == user_rut).first()
        user_result = User.from_orm(user_orm)
        return user_result

    return "Method not allowed"


@app.route("/projects", methods=["GET"])
@validate()
def fetch_projects():
    db_session = db.getSession(engine)
    if request.method == "GET":
        projects_orm = db_session.query(ProjectModel).all()
        projects = Project.from_orms(projects_orm)
        projects_result = Projects(projects=projects)
        return projects_result

    return "Method not allowed"


@app.route("/projects/days-left", methods=["GET"])
@validate()
def fetch_projects_with_days_left():
    db_session = db.getSession(engine)
    if request.method == "GET":
        projects_orm = db_session.query(ProjectModel).all()
        projects = Project.from_orms(projects_orm)

        projects_with_days_left = []
        for project in projects:
            today = date.today()
            end_date = project.end_date
            days_left = (end_date - today).days
            projects_with_days_left.append(
                ProjectWithDaysLeft(**project.dict(), days_left=days_left)
            )

        projects_result = Projects(projects=projects_with_days_left)
        return projects_result

    return "Method not allowed"


if __name__ == "__main__":
    app.secret_key = ".."
    app.run(debug=True)
