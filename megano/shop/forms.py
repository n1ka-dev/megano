from shop.models import Comment
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': _('Review'), 'rows': 1, 'class': 'form-textarea', 'data-validate':''}),
        label='', max_length=1200)
    nickname = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': _('Name'),
                                                                                      'class': 'form-input'}),
                               error_messages={'required': _('Enter your Name or log in to leave a review')}
                               )
    email = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': _('Email'),
                                                                                   'class': 'form-input', 'data-validate':''}),
                            error_messages={'required': _('Enter your Email or log in to leave a review')}
                            )

    class Meta:
        model = Comment
        fields = ['nickname', 'text', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if email is None:
            raise ValidationError('email', _('Enter your Email or log in to leave a review'))
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if nickname is None:
            raise ValidationError('nickname', _('Enter your Name or log in to leave a review'))

        return nickname
