# MonteCarlo
How to run:
 - First ensure that the file `./src/django/monte_project/settings.py` contains credentials for a mysql database
 - Open a powershell in the src directory
 - Run the command `pip -r install ../requirements.txt`
 - Navigate to django directory `cd django`
 - Run the command `python manage.py makemigrations`
 - Then run `python manage.py migrate` to create the required tables
 - Once migration is complete, run the command `python manage.py runserver` to run the application
 - You should now be able to browse the site on localhost:8000
