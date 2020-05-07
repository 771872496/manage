# 引入表单类
from django import forms
# 引入 User 模型


from .models import Bill, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = "__all__"
