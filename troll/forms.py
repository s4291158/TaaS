from django import forms

from .models import *


class LikeForm(forms.Form):
    def __init__(self, sessionkey, idea_id=None, *args, **kwargs):
        super(LikeForm, self).__init__(*args, **kwargs)
        self.session = Session.objects.get_or_create(key=sessionkey)[0]
        try:
            self.idea = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
            self.idea = None

        self.fields['idea_id'] = forms.IntegerField(
            widget=forms.NumberInput(
                attrs={'type': 'hidden'}
            )
        )

    def save(self):
        self.session.save()

        if self.idea:
            like, is_new = Like.objects.get_or_create(idea=self.idea, session=self.session)

            if not is_new and like.liked:
                like.liked = False
                like.save()
                self.idea.likes -= 1
            else:
                like.liked = True
                like.save()
                self.idea.likes += 1

            self.idea.save()


class IdeaForm(forms.Form):
    def __init__(self, sessionkey, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.session = Session.objects.get_or_create(key=sessionkey)[0]

        self.fields['idea_name'] = forms.CharField(
            max_length=40,
            label='Troll name here',
            error_messages={
                'required': 'Every troll has a name, come on'
            },
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Make it good"
                }
            )
        )

        self.fields['idea_description'] = forms.CharField(
            label='Ok how does it work',
            error_messages={
                'required': "you're trolling me right?"
            },
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '10',
                    'placeholder': "Don't disappoint me"
                }
            )
        )

        self.fields['email'] = forms.EmailField(
            label='Notify me if my idea gets implemented',
            required=False,
            widget=forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "If we do decide to implement it, you'd be glad to have filled it"
                }
            )
        )

    def clean(self):
        cleaned_data = super(IdeaForm, self).clean()

        ideas_with_same_name = Idea.objects.filter(name=cleaned_data['idea_name'])
        if len(ideas_with_same_name):
            self.add_error('idea_name', 'Try a different name perhaps')

        ideas_by_same_user = Idea.objects.filter(session=self.session)
        if len(ideas_by_same_user) > 20:
            raise forms.ValidationError("Slow down turbo, how many trolls do you have?")

        return cleaned_data

    def save(self):
        idea = Idea()
        idea.name = self.cleaned_data['idea_name']
        idea.description = self.cleaned_data['idea_description']
        idea.email = self.cleaned_data['email']
        idea.session = self.session
        idea.save()
