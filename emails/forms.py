from django import forms
from .models import Email
from django_ckeditor_5.widgets import CKEditor5Widget


class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["body"].required = False


    class Meta:
        model = Email
        fields = ("__all__")
        # widgets = {
        #             "body": CKEditor5Widget(
        #                 attrs={"class": "django_ckeditor_5"}, config_name="extends"
        #             )
        #           }
        body = CKEditor5Widget(
                        attrs={"class": "django_ckeditor_5"}, config_name="extends"
                  )
