from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class TweetForm(forms.Form):
    # tweet_content = forms.CharField(label='Tweet Content',widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'What\'s happening?'}), max_length=280,required=True)
    tweet_content = forms.CharField( label='tweet_content', max_length=250)

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout('tweet_content', Submit('submit', 'Post Tweet')
        )


class PostForm(forms.Form):
    
    CHOICE=[
        ('Twiter','Twitter'),
        ('Facebook','Facebook'),
        ('Instagram','Instagram'),
        ('Linkedin','Linkedin'),
        ('Pintrest','Pinterest'),   
    ]
    
    post_text = forms.CharField(
        label="Enter tags & text for your post...",
        max_length= 100,               
    )
    
    media_post = forms.FileField(
        label="Upload Media..."
    )
    
    social_account = forms.MultipleChoiceField(choices=CHOICE, widget=forms.CheckboxSelectMultiple(attrs={'class':'inline'})
    )
    
    