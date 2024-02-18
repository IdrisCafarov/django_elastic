
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm


from account.models import *
from blog.models import *


# get custom user
User = get_user_model()



class LoginForm(forms.Form):
    email= forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={
        "id":"usernameInput",
        "type":"email",
        "class":"w-full mt-1 group-data-[theme-color=violet]:bg-violet-400/40 group-data-[theme-color=sky]:bg-sky-400/40 group-data-[theme-color=red]:bg-red-400/40 group-data-[theme-color=green]:bg-green-400/40 group-data-[theme-color=pink]:bg-pink-400/40 group-data-[theme-color=blue]:bg-blue-400/40 py-2.5 rounded border-transparent placeholder:text-sm placeholder:text-gray-50 text-white",
        "placeholder":"Email"
        }
    ))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={
        "id":"passwordInput",
        "type":"password",
        "class":"w-full mt-1 group-data-[theme-color=violet]:bg-violet-400/40 group-data-[theme-color=sky]:bg-sky-400/40 group-data-[theme-color=red]:bg-red-400/40 group-data-[theme-color=green]:bg-green-400/40 group-data-[theme-color=pink]:bg-pink-400/40 group-data-[theme-color=blue]:bg-blue-400/40 py-2.5 rounded border-transparent placeholder:text-sm placeholder:text-gray-50 text-white",
        "placeholder":"Password"
        }
    ))

    def clean(self):
        email=self.cleaned_data.get("email")
        password=self.cleaned_data.get("password")
        if email and password:
            user=authenticate(email=email,password=password)
            if not user:
                raise forms.ValidationError("Email or Password Incorrect !")
            # if not user or user.is_superuser==False:
            #     raise forms.ValidationError("Email or Password Incorrect !")




        return super(LoginForm, self).clean()



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""






class JSONFileUploadForm(forms.Form):
    # json_file = forms.FileField()

    json_file= forms.FileField(max_length=100,widget=forms.FileInput(attrs={
        "type":"file",
        "name":"file",

        }
    ))



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""





class UpdateDataForm(forms.ModelForm):
    name = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Name"
        }
    ))
    phone = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Phone Number"
        }
    ))
    email = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'email',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Email"
        }
    ))
    image_url = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Image Url"
        }
    ))
    url = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Url"
        }
    ))
    address = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Address"
        }
    ))
    country = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Country"
        }
    ))
    province = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Province"
        }
    ))
    city = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"City"
        }
    ))

    research_areas = forms.CharField(widget=forms.Textarea(attrs={
        # 'type':'text',
        'id':'meta-description-input',
        'class':'form-control',
        'placeholder':"Research Areas",
        "rows":"3"
        }
    ))
    
    introduction = forms.CharField(widget=forms.Textarea(attrs={
        # 'type':'text',
        'id':'meta-description-input',
        'class':'form-control',
        'placeholder':"Introduction",
        "rows":"3"
        }
    ))
    achievements = forms.CharField(widget=forms.Textarea(attrs={
        # 'type':'text',
        'id':'meta-description-input',
        'class':'form-control',
        'placeholder':"Achievements",
        "rows":"3"
        }
    ))
    title = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"City"
        }))
    university = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"University"
        }
    ))
    department = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'text',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"Department"
        }
    ))
    university_world_ranking = forms.CharField(max_length=1000,widget=forms.TextInput(attrs={
        'type':'number',
        'id':'meta-keywords-input',
        'class':'form-control',
        'placeholder':"University World Ranking"
        }
    ))
    public = forms.BooleanField(
        widget=forms.Select(choices=[(True, 'Public'),(False, 'Hidden')], attrs={
            'class': 'form-select',
            'id': 'choices-publish-status-input',
        }),
        
    )
        
    

    

    class Meta:
        model = Professor
        fields = ('name','phone','email','image_url','url','address','country','province','city','research_areas','introduction','title','university','department','university_world_ranking','public','achievements')




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""