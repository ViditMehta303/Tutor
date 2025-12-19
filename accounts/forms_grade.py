from django import forms

class GradeSelectForm(forms.Form):
    GRADE_CHOICES = [(i, str(i)) for i in range(1, 11)]
    grade_level = forms.ChoiceField(choices=GRADE_CHOICES, label="Select your grade (1–10)")
