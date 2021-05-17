from django import forms
from django.forms import ModelForm
from .models import Review, Professor_to_Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course')
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['course'].initial = course
        self.fields['professor'].queryset = Professor_to_Course.get_queryset_professors_by_course(course)

    class Meta:
        model = Review
        fields = ['course', 'user', 'rate', 'content', 'course_load', 'professor']
        CHOICES = [['', '---'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']]
        widgets = {
            'course': forms.HiddenInput(),
            'rate': forms.Select(choices=CHOICES),
            'course_load': forms.Select(choices=CHOICES),
        }


# This class uses the built in django UserCreationForm and adds an email field
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        # There are 2 password fields to confirm the password (pw1 and pw2 are built-in function names)
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class FilterAndSortForm(forms.Form):
    initial = {'sort_by': 'id'}
    filter_choices = [('rate_over', 'rating over 3.5'), ('load_below', 'course load under 3.5'),
                      ('mand', 'mandatory'), ('elect', 'elective'), ('has_preqs', 'has prerequisites'),
                      ('no_preqs', 'no prerequisites'), ('rater_num', 'at least 5 raters')]
    sort_choices = [('id', 'identifier'), ('name', 'name'), ('rating', 'course rating'),
                    ('load', 'course load'), ('num_reviews', 'number of reviews'), ('num_raters', 'number of raters')]
    filter_by = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=filter_choices,
        required=False
        )
    sort_by = forms.ChoiceField(
        choices=sort_choices)
    widgets = {
        'filter_by': filter_by,
        'sort_by': sort_by
        }
