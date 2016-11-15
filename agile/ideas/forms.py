from django import forms

# Comment Ideas Form
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment','idea_id')
		widgets = {'idea_id': forms.HiddenInput()}
