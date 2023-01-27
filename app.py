from flask import Flask
from database import connector
from model import InstitutionModel, UserModel, ProjectModel
from schemas import (
    Institution,
    Institutions,
    Users,
    UserWithProjects,
    User,
    Projects,
    InstitutionWithProjectsAndUsers,
    Project,
    ProjectWithDaysLeft,
    InstitutionCreateData,
    InstitutionUpdateData,
)
from datetime import date
from flask_pydantic import validate
from flask_restx import Api, Resource


db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)
api = Api(app)


@api.route("/institutions")
class InstitutionView(Resource):
    @validate()
    def get(self):
        db_session = db.getSession(engine)
        institutions_orm = db_session.query(InstitutionModel).all()
        institutions = Institution.from_orms(institutions_orm)
        institutions_result = Institutions(institutions=institutions)
        return institutions_result

    @validate()
    def post(self, body: InstitutionCreateData):
        db_session = db.getSession(engine)
        new_institution = InstitutionModel(**body.dict())
        db_session.add(new_institution)
        db_session.commit()
        return "New institution created!"

    @validate()
    def patch(self, institution_id, body: InstitutionUpdateData):
        db_session = db.getSession(engine)
        institution = db_session.query(InstitutionModel).get({"id": institution_id})
        institution.name = body.name
        institution.description = body.description
        institution.address = body.address
        db_session.add(institution)
        db_session.commit()
        return f"Institution with id = {institution_id} updated!"


@api.route("/institutions/<string:institution_id>")
class InstitutionByIdView(Resource):
    @validate()
    def patch(self, institution_id, body: InstitutionUpdateData):
        db_session = db.getSession(engine)
        institution = db_session.query(InstitutionModel).get({"id": institution_id})
        institution.name = body.name
        institution.description = body.description
        institution.address = body.address
        db_session.add(institution)
        db_session.commit()
        return f"Institution with id = {institution_id} updated!"

    @validate()
    def delete(self, institution_id):
        db_session = db.getSession(engine)
        institution = (
            db_session.query(InstitutionModel)
            .filter(InstitutionModel.id == institution_id)
            .first()
        )
        db_session.delete(institution)
        db_session.commit()
        return f"Institution with id {institution_id} deleted"

    @validate()
    def get(self, institution_id):
        db_session = db.getSession(engine)
        institution_orm = db_session.query(InstitutionModel).get({"id": institution_id})
        institution_result = InstitutionWithProjectsAndUsers.from_orm(institution_orm)
        return institution_result


@api.route("/institutions/with-adress-url")
class InstitutionWithAddressUrlView(Resource):
    @validate()
    def get(self):
        db_session = db.getSession(engine)
        institutions_orm = db_session.query(InstitutionModel).all()
        institutions = Institution.from_orms(institutions_orm)

        for institution in institutions:
            address = institution.address
            name = institution.name
            institution.address = f"https://www.google.com/maps/search/{address}"
            institution.name = name[0:3]

        institutions_result = Institutions(institutions=institutions)
        return institutions_result


@api.route("/users")
class UsersView(Resource):
    @validate()
    def get(self):
        db_session = db.getSession(engine)
        users_orm = db_session.query(UserModel).all()
        users = User.from_orms(users_orm)
        users_result = Users(users=users)
        return users_result


@api.route("/users/<string:user_rut>")
class UsersByIdView(Resource):
    @validate()
    def get(self, user_rut):
        db_session = db.getSession(engine)
        user_orm = db_session.query(UserModel).filter(UserModel.RUT == user_rut).first()
        user_result = UserWithProjects.from_orm(user_orm)
        return user_result


@api.route("/projects")
class ProjectsView(Resource):
    @validate()
    def get(self):
        db_session = db.getSession(engine)
        projects_orm = db_session.query(ProjectModel).all()
        projects = Project.from_orms(projects_orm)
        projects_result = Projects(projects=projects)
        return projects_result


@api.route("/projects/days-left")
class ProjectByIdView(Resource):
    @validate()
    def get(self):
        db_session = db.getSession(engine)
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


if __name__ == "__main__":
    app.secret_key = ".."
    app.run(debug=True)
