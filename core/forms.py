from django import forms
from .models import Post
from django.utils import timezone


class CreatePostForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    media = forms.FileField(label='Media (Image/Video)', required=False)
    post_type = forms.ChoiceField(choices=[('draft', 'Draft'), ('schedule', 'Schedule')], initial='draft', label='Post Type')
    schedule_datetime = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), label='Schedule Date & Time')

    def clean_schedule_datetime(self):
        schedule_datetime = self.cleaned_data['schedule_datetime']

        if schedule_datetime <= timezone.now():
            raise forms.ValidationError("Scheduled date and time must be in the future.")

        return schedule_datetime


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media', 'scheduled_datetime', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the choices for the 'status' field and exclude 'posted'
        status_choices = [(key, value) for key, value in Post.STATUS_CHOICES if key != 'posted']

        # Update the 'status' field choices
        self.fields['status'].choices = status_choices

    def clean(self):
        cleaned_data = super().clean()
        scheduled_datetime = cleaned_data.get('scheduled_datetime')

        if scheduled_datetime and scheduled_datetime <= timezone.now():
            raise forms.ValidationError("Scheduled date and time must be in the future.")