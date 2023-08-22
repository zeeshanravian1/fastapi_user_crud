# FastAPI User CRUD Single Role (Beta)



## Getting started (Beta)

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/zeeshanravian1/fastapi_user_crud_single_role.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/zeeshanravian1/fastapi_user_crud_single_role/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open-source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
FastAPI User CRUD with a single role for each user.

## Description
This project is built in [FastAPI](https://fastapi.tiangolo.com/) (The most popular framework of python) using python 3.11.0.
You can also use [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations for this project.

This project contains all the routes relating to users such as:
- Register a single user with email verification.
- Super Admin can assign a single role to the user.
- Get a single user.
- Get all users with pagination.
- Update a single user.
- Partially update a single user.
- Delete a single user.
- Change user password.
- Reset the user password.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
- Python Installation:
To install project dependencies you must have python 3.11.0 installed on your system.
If python 3.11.0 is not installed you can download it from the [python website](https://www.python.org/downloads/) or you can configure your system to handle multiple python versions using [pyenv](https://realpython.com/intro-to-pyenv/).

Verify your python installation by typing this command in your terminal:
```
python --version
```

- Pipenv Installation:
After that, you need to install pipenv to handle the virtual environments, you can install it by typing this command in your terminal:
```
pip install pipenv or
pip3 install pipenv
```

Adding pipenv to path
```
echo 'export PATH="/home/<user>/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

Verify your pipenv installation:
```
pipenv
```

- Creating Virtual Environment
Go to the project directory and type the following command in the terminal.
```
pipenv sync
```

This will create a virtual environment for your project along with dependencies.

- Activate Virtual Environment
To active virtual environment type the following command in the terminal.
```
pipenv shell
```

You can verify your environment dependencies by running:
```
pip list
```

## Configure [Alembic](https://alembic.sqlalchemy.org/en/latest/) for Database Migrations.
First, create your schema in the database. It is mandatory otherwise alembic will give you an error.

- Type the following command to initialize migrations
```
alembic init migrations
```

- Edit env.py in the migrations folder to set the path for your database:
```
from core.models.database import (metadata, SQLALCHEMY_DATABASE_URL)
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
target_metadata = metadata
```

- Your first migrations
```
alembic revision --autogenerate -m "<Migration Name>"
```

- Apply Migrations
```
alembic upgrade heads
```

## Usage
- Pre Defined Roles:
Run roles_insertion.py from core/database_insertions to insert pre-defined roles

- Run FastAPI Server:
To run the FastAPI server run this command
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Access Swagger UI:
http://0.0.0.0:8000/docs

- Access Redoc UI:
http://0.0.0.0:8000/redoc

## Support
Tell people where they can go for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires an external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
