from django.forms import ModelForm
from db.models import AssignmentFile
class UploadForm(ModelForm):
    class Meta:
        model = AssignmentFile