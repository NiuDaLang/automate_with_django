from django.core.management.base import BaseCommand


# Proposed command = python manage.py greeting YoYo
# Proposed output = Hi {name}, Good Morning!
class Command(BaseCommand):
    help = "Greets the user" # command level help: python manage.py greeting --help

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Specifies user name") # argument level help

    def handle(self, *args, **kwargs):
        # write the logic
        name = kwargs["name"]
        greeting = f"Hi {name}, Good Morning!"
        # self.stdout.write(greeting) # normal output
        # self.stderr.write(greeting) # prints out in RED text
        # self.stdout.write(self.style.WARNING(greeting)) # prints out in YELLOW text
        self.stdout.write(self.style.SUCCESS(greeting)) # prints out in GREEN text