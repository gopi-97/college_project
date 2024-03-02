# # forms.py
# from django import forms
# from .models import FarmerInventory, InventoryGallery

# class CustomInventoryUpdateForm(forms.ModelForm):
#     image = forms.FileInput(attrs={'multiple': True}, required=False) 

#     class Meta:
#         model = FarmerInventory
#         fields = ['product', 'quantity', 'image', 'gallery']

#     def clean_gallery(self):
#         gallery = self.cleaned_data.get('gallery')
#         # Your validation logic here
#         return gallery
