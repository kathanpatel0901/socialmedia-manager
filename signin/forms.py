from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit,Field
from crispy_forms.bootstrap import FormActions 
from .models import Post
class TweetForm(forms.Form):

    tweet_content = forms.CharField( label='tweet_content', max_length=250)

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout('tweet_content', Submit('submit', 'Post Tweet')
        )


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['post_text', 'post_media', 'social_media']
     
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_media'].required = False
        self.fields['post_text'].required = False
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'post_text',    
            'post_media',
            Field('social_media', css_class='checkbox-inline'),
            Submit('post_now', 'Post Now', css_class='btn-primary'),
            )

class SchedulePostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['post_text', 'post_media', 'social_media','post_schedule_time']
     
    def __init__(self, *args, **kwargs):
        super(SchedulePostForm, self).__init__(*args, **kwargs)
        self.fields['post_media'].required = False
        self.helper = FormHelper()  
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('post_text'),    
            Field('post_media'),
            Field('social_media', css_class='checkbox-inline'),
            Field('post_schedule_time', placeholder="YYYY-MM-DD HH:MM:SS"),
            Submit('post_schedule', 'Post Schedule', css_class='btn-primary'),
                   
    )   
        
# class SchedulePostForm(forms.ModelForm):
    
#     class Meta:
#         model = Post
#         fields = ['post_text', 'post_media', 'social_media', 'post_schedule_time']
     
#     def __init__(self, *args, **kwargs):
#         super(SchedulePostForm, self).__init__(*args, **kwargs)
#         self.fields['post_media'].required = False
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.layout = Layout(
#             Field('post_text'),    
#             Field('post_media'),
#             Field('social_media', css_class='checkbox-inline'),
#             Field('post_schedule_time', placeholder="YYYY-MM-DD HH:MM:SS"),
#             Submit('post_schedule', 'Post Schedule', css_class='btn-primary'),
#         )