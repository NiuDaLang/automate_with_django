from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import csv

# Proposed command - python manage.py importdata file_path model_name
# Sample dataset available at https://www.kaggle.com/datasets

class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file")
        parser.add_argument("model_name", type=str, help="Name of the model")

    def handle(self, *args, **kwargs):
        # logic goes here
        file_path = kwargs["file_path"]
        model_name = kwargs["model_name"].capitalize()

        model = None

        # search for the model across all installed apps
        for app_config in apps.get_app_configs():
            # print(f"App Name: {app_config.name}")
            # print(f"Verbose Name: {app_config.verbose_name}")
            # print(f"App Label: {app_config.label}")
            # print(f"App Path: {app_config.path}")
            # print("-" * 20)
            # ---- will return ---
            # App Name: dataentry
            # Verbose Name: Dataentry
            # App Label: dataentry
            # App Path: /Users/yokofutsukaichi/Documents/Udemy/Django/AutomateWithDjango/dataentry
            # --------------------

            #  try to search for the model
            try:
                model=apps.get_model(app_config.label, model_name)
                break # stop searching once the model is found

            except LookupError:
                continue #if model is not found in one app, continue with the next app

        if not model:
            raise CommandError(f"Model {model_name} was not found in any app!")

        with open(file_path, "r") as file: # !!!important!!! use [with] for properly closing the file
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row) # equiavlent to roll_no=data["roll_no"] etc...
        self.stdout.write(self.style.SUCCESS("Data inserted successfully!"))