from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints Hellow World"

    def handle(self, *args, **kwargs):
        # we write the logic
        self.stdout.write("hello world") #to write message on the terminal