from django import forms
class TweetForm(forms.Form):
    tweet = forms.CharField(widget= forms.Textarea, label='tweet_content')


# forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class TweetForm(forms.Form):
    tweet_content = forms.CharField(label='Tweet Content',widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'What\'s happening?'}), max_length=280,required=True)

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'tweet_content',
            Submit('submit', 'Post Tweet')
        )
