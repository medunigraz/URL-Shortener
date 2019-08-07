import datetime
import re
from hashlib import md5

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase


class RedirectUrl(models.Model):
    id = models.AutoField(primary_key=True, )
    tmpId = models.IntegerField(null=True, blank=True)
    srcUrl = models.CharField(max_length=400, blank=True)
    dstUrl = models.CharField(max_length=400)

    class Meta:
        default_permissions = ('add', 'change', 'delete')

    def __str__(self):
        return self.srcUrl + " ---> " + self.dstUrl


class RedirectUrlForm(ModelForm):
    class Meta:
        model = RedirectUrl
        fields = ['dstUrl', 'srcUrl', 'tmpId']
        widgets = {'srcUrl': forms.HiddenInput(),
                   'tmpId': forms.HiddenInput(),
                   'dstUrl': forms.TextInput(attrs={'class': 'form-control'})
                   }
        labels = {
            'dstUrl': 'Ziel URL',
        }

    def clean(self):
        super(RedirectUrlForm, self).clean()
        idstUrl = self.cleaned_data.get('dstUrl')
        isrcUrl = self.cleaned_data.get('srcUrl')
        if not re.match('(?:http|https)://', idstUrl):
            self.cleaned_data['dstUrl'] = 'http://{}'.format(idstUrl)
        if not isrcUrl:
            self.cleaned_data['srcUrl'] = md5((idstUrl + str(datetime.datetime.now())).encode()).hexdigest()
        return self.cleaned_data


class RedirectUrlUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(RedirectUrl, on_delete=models.CASCADE)


class RedirectUrlGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(RedirectUrl, on_delete=models.CASCADE)
