from factories.entities import InstitutionFactory, UserFactory, ProjectFactory

n_institutions = 3
n_users = 5
n_projects = 10

# Create institutions
institutions = InstitutionFactory.create_batch(n_institutions)

# Create users
users = UserFactory.create_batch(n_users)

# Create projects

for i in range(n_projects):
    user = users[i % n_users]
    institution = institutions[i % n_institutions]
    ProjectFactory.create(user_id=str(user.id), institution_id=str(institution.id))
