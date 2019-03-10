# Social Team Builder (In progress)

This is the twelfth and final project in the Treehouse Python tech degree.

Will be hosted on Heroku upon completion. 

## Description

You're going to build a site where people can sign up to find projects that need help or post their own projects for 
other people to join. 

Users should be able to create a brief profile for themselves after they sign up with an avatar, 
a bio, and pick their skills from a list. Users can post a project, too, giving it a title and description. They should 
also list the positions they need filled for that job with a brief description of what the position will be responsible 
for. Users should be able to find a project and ask to join it. If you're a project owner, you can approve or deny the 
person asking to join.

## Running Locally

To view locally, create a new virtual environment, clone the repo and install the requirements with `pip install -r 
requirements.txt`.

To create your database, run `python manage.py migrate` and then `python manage.py loaddata initial_data.json` to 
pre-populate the database.

You can then start the app with `python manage.py runserver`.
