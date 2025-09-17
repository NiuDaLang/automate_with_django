from django.apps import apps
import hashlib
import time
from django.core.management.base import CommandError
from django.db import DataError
import csv
from django.conf import settings
import datetime
import os
from django.core.mail import EmailMultiAlternatives
from emails.models import Email, Sent, EmailTracking, Subscriber
from bs4 import BeautifulSoup


def get_all_custom_models():
    default_models = ["LogEntry", "Permission", "Group", "ContentType", "Session", "User", "Upload",]

    # try to get all the apps
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models


def check_csv_errors(file_path, model_name):
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

    # compare csv header with model's field names
    # get all the field names of the model that we found
    model_fields = [field.name for field in model._meta.fields if field.name != "id"]

    try:
        with open(file_path, "r") as file: # !!!important!!! use [with] for properly closing the file
            reader = csv.DictReader(file) # csv.DictReader considers the 1st row as the header row
            csv_header = reader.fieldnames

            # compare csv header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields.")
    except Exception as e:
        raise e

    return model


# EmailMessage version
# def send_email_notification(mail_subject, body, to_email, attachment=None, html=None):
#     try:
#         from_email = settings.DEFAULT_FROM_EMAIL
#         mail = EmailMessage(mail_subject, body, from_email, to=to_email)
#         if attachment is not None:
#             mail.attach_file(attachment)
#         mail.content_subtype = "html"
#         mail.send()
#     except Exception as e:
#         raise e


# EmailMultiAlternatives version
def send_email_notification(mail_subject, text, to_email, email_id=None, attachment=None, html=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL

        for recipient_email in to_email:
            new_message = html
            # Create EmailTracking record
            if email_id: # run this code only during bulk email sending
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subscriber = subscriber,
                    unique_id = unique_id,
                )

                base_url = settings.BASE_URL
                # Generate the tracking pixel
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"

                # Search for the links in the email body
                soup = BeautifulSoup(html, "html.parser")
                urls = [a["href"] for a in soup.find_all("a", href=True)]

                # If there are links or urls in the email body, inject our click tracking url to that original link
                if urls:
                    for url in urls:
                        # make the final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")

                # Create the email content with tracking pixel image
                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message += open_tracking_img

            mail = EmailMultiAlternatives(
                    subject = mail_subject, 
                    body = text, 
                    from_email = from_email, 
                    to = [recipient_email],
                )
            if attachment is not None:
                mail.attach_file(attachment)
            if html is not None:
                mail.attach_alternative(new_message, "text/html")
            mail.send()

        # Store the total sent emails inside the Sent model
        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails() # count happens when email sending occurs
            sent.save()

    except Exception as e:
        raise e


def generate_csv_file(model_name):
    # generate the timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # define the csv file name/path
    export_dir = "exported_data"
    file_name = f"exported_{model_name}_data_{timestamp}.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path