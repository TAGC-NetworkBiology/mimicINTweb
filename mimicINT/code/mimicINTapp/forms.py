from django import forms


GROUP_LIST = [
	('none', 'choose a template set'),
    ('group1', 'Group 1'),
    ('group2', 'Group 2'),
    ('group3', 'Group 3'),
]

IUMETHOD_LIST = [
    ('short', 'Short'),
    ('long', 'Long'),
]

#onchange='this.form.filename.value = this.value'
#formulaire de soumission de job
class MyForm(forms.Form):

	query_sequencies = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control', 'style' : 'min-width: 300px ; max-height: none;' , 'rows': '18', 'placeholder' : 'Paste here your query sequence(s)'}), required=False)
	query_fasta_file = forms.FileField(widget=forms.FileInput(attrs={'class' : 'inputfile inputfile-1', 'accept': '.fasta,.fa,.faa,.txt', 'onchange' : 'file_to_textarea()'}),label="Upload FASTA sequence",required=False)

	run_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter a short run name (optional)'}), max_length=30, required=False)
	microbe_species = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter the name of your organism'}), max_length=30, required=False)
	query_informations = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control', 'rows': '5', 'placeholder' : 'Write a short description of your run (optional)'}), required=False)
	send_mail = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter your email if you want to be warned'}), max_length=30, required=False)

	interaction_templates = forms.MultipleChoiceField(required=False, widget=forms.Select(attrs={'id' : 'interaction_templates'}), choices=GROUP_LIST)

	#disorder_threshold =  forms.MultipleChoiceField(required=False, widget=forms.CheckboxInput(attrs={'id' : 'disorder_threshold', 'class' : 'switch', 'checked': False}))
	iumethod = forms.MultipleChoiceField(widget=forms.Select(attrs={'id': 'iumethod'}), choices=IUMETHOD_LIST)
	iucut =forms.IntegerField(widget=forms.NumberInput(attrs={'id' : 'iucut', 'class' : 'custom-range', 'type':'range', 'step': '0.1',  'min': '0', 'max': '1', 'value': '0.4'}))
	minregion = forms.IntegerField(widget=forms.NumberInput(attrs={'id' : 'minregion', 'class' : 'custom-range', 'type':'range', 'step': '1',  'min': '0', 'max': '30', 'value': '10'}))
	conserved_motifs = forms.IntegerField(widget=forms.NumberInput(attrs={'id' : 'conserved_motifs', 'class' : 'custom-range', 'type':'range', 'step': '1',  'min': '2', 'max': '6', 'value': '5'}))
	domain_score_threshold =forms.IntegerField(widget=forms.NumberInput(attrs={'id' : 'domain_score_threshold', 'class' : 'custom-range', 'type':'range', 'step': '0.1',  'min': '0', 'max': '0.4', 'value': '0.3'}))
	def save(self, *args, **kwargs):
		get_text = self.query_fasta_file.read()
		self.query_sequencies = get_text
		super(MyForm, self).save(*args, **kwargs) # Call the "real" save() method.
	



#formulaire de soumission d'ID de job
class jobForm (forms.Form):
	job_id = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter job ID'}), max_length=30, required=True)
