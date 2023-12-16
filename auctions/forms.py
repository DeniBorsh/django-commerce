from django.forms import ModelForm, Textarea, forms
from .models import Listing, Bid

class ListingForm(ModelForm):
    class Meta: 
        model = Listing
        fields = {
            'title',
            'description',
            'price',
            'image',
            'category',
        }
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3}),
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = {
            'bid'
        }
        