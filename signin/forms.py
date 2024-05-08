from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML
from crispy_forms.bootstrap import FormActions
from .models import Post, Link
from django.forms import DateTimeInput


class DateInput(forms.DateTimeInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


class TweetForm(forms.Form):

    tweet_content = forms.CharField(label="tweet_content", max_length=250)

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.layout = Layout("tweet_content", Submit("submit", "Post Tweet"))


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "post_text",
            "post_media",
            "twitter",
            "facebook",
            "instagram",
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["post_media"].required = False
        self.fields["post_text"].required = False
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "post_text",
            "post_media",
            HTML("<h6>Social Media*</h6>"),
            Field(
                "twitter",
                "facebook",
                "instagram",
                css_class="form-check-input",
                wrapper_class="form-check form-switch",
            ),
            Submit("post_now", "Post Now", css_class="btn-primary"),
        )


class SchedulePostForm(forms.ModelForm):
    post_schedule_date = forms.DateField(widget=DateInput())
    post_schedule_time = forms.TimeField(widget=TimeInput())

    class Meta:
        model = Post
        fields = [
            "post_text",
            "post_media",
            "twitter",
            "facebook",
            "instagram",
            "post_schedule_date",
            "post_schedule_time",
        ]
        widget = {
            "post_schedule_time": DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SchedulePostForm, self).__init__(*args, **kwargs)
        self.fields["post_media"].required = False
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field("post_text"),
            Field("post_media"),
            HTML("<h6>Social Media*</h6>"),
            Field(
                "twitter",
                "facebook",
                "instagram",
                css_class="form-check-input",
                wrapper_class="form-check form-switch",
            ),
            Field("post_schedule_date", css_class="datetimepicker"),
            Field("post_schedule_time", css_class="datetimepicker"),
            Submit("post_schedule", "Post Schedule", css_class="btn-primary"),
        )


class RepositoryForm(forms.Form):
    repository_name = forms.CharField(
        label="Repository name", max_length=100, required=False
    )
    repository_code = forms.CharField(
        label="Repository code", max_length=100, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "repository_name",
            "repository_code",
            Submit("create", "Create", css_class="btn btn-primary"),
            Submit("clone", "clone", css_class="btn btn-success"),
            Submit("push", "Push", css_class="btn btn-warning"),
        )
