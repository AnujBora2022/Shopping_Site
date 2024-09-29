from django import forms
from .models import Product, Category
from .models import Order

class ProductForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, label='New Category')
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'stock', 'image','new_category']  # Add new_category

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'new_category': forms.TextInput(attrs={'class': 'form-control', 'id': 'new-category-input', 'style': 'display:none'})  # Hidden by default
        }  # Style for new category input
        

    def save(self, commit=True):
        product = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')
        category = self.cleaned_data.get('category')

        if new_category_name:
            # Create a new category if one doesn't exist
            category, created = Category.objects.get_or_create(name=new_category_name)
            product.category = category
        elif category:
            # Assign existing category if selected
            product.category = category
        else:
            # If no category was chosen or entered, set category to None
            product.category = None

        if commit:
            product.save()
        return product



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'payment_method', 'shipping_address']
