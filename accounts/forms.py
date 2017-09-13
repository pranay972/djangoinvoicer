from django import forms
from .models import Product, ProductGroup, Tax, Bills
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db import models


class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    #__metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""

        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""

        if value == "":
            return None

        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return super(JSONField, self).get_db_prep_save(value)


#create forms here

class LoginForm(forms.Form):
	user = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

class ProductAddForm(forms.ModelForm):

	class Meta:
		model = Product
		fields = ['name', 'alias']

	name = forms.CharField(max_length=100, label = "Name")
	alias = forms.CharField(max_length=100, label = "Alias")
	#price = forms.FloatField(label = "Price")
	#inventory = forms.IntegerField(required=False, label = "Inventory")

class ProductGroupAddForm(forms.ModelForm):

	class Meta:
		model = ProductGroup
		fields = ['name', 'alias', 'products']

	name = forms.CharField(max_length=100)
	alias = forms.CharField(max_length=100)
	products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())


	def save (self, commit=True):

		instance = forms.ModelForm.save(self, False)

		old_save_m2m = self.save_m2m
		def save_m2m():
			old_save_m2m()

			instance.produts_set.clear()
			for product in self.cleaned_data['products']:
				instance.products.add(product)


		if commit:
			instance.save()
			self.save_m2m()

		return instance

class BillGenForm(forms.ModelForm):
	class Meta:
		model = Bills
		fields = ['invoice_date', 'to', 'collection']

	names_gst_and_quantities = JSONField()

class TaxForm(forms.ModelForm):
	class Meta:
		model = Tax
		fields = ['tax', ]

''' 

class Bills (models.Model):
	invoice_date = models.DateField(default=timezone.now())
	due_date = models.DateField(default=timezone.now())
	to = models.CharField(max_length=100)

class BilledProducts (models.Model):
	name = models.CharField(max_length=100)
	quantity = models.IntegerField(default=0)
	price = models.FloatField()
	bill = models.ForeignKey(Bills)

	def __str__ (self):
		return self.name

'''

