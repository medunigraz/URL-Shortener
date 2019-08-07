from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template import loader
from guardian.shortcuts import get_objects_for_user, assign_perm

from .models import RedirectUrl, RedirectUrlForm


def redirect_view(request, srcUrl):
    redir = get_object_or_404(RedirectUrl, srcUrl=srcUrl)
    response = redirect(redir.dstUrl)
    return response


def detail_view(request, **kwargs):
    if request.method == 'GET':
        if kwargs.get('id', None):
            redir = get_object_or_404(RedirectUrl, pk=kwargs.get('id', None))
            if not request.user.has_perm('change_redirecturl', redir) or redir is None:
                messages.warning(request, 'Keine Berechtigung', extra_tags='alert alert-primary')
                return redirect('urlshortener:tableView')
            form = RedirectUrlForm(None, initial={'srcUrl': redir.srcUrl, 'dstUrl': redir.dstUrl, 'tmpId': redir.id})
            context = {
                'redirectUrl': redir,
                'form': form,
            }
            return render(request, 'urlshortener/detail.html', context)
        else:

            context = {
                'redirectUrl': None,
                'form': RedirectUrlForm(None),
            }
            return render(request, 'urlshortener/detail.html', context)
    elif request.method == 'POST':
        redir = RedirectUrl.objects.filter(srcUrl=request.POST.get("id")).first()
        if not request.user.has_perm('change_redirecturl', redir) and redir is not None:
            messages.warning(request, 'Keine Berechtigung', extra_tags='alert alert-primary')
            return redirect('urlshortener:detailView')
        form = RedirectUrlForm(request.POST, instance=redir)
        if form.is_valid():
            srcUrl = form.cleaned_data['srcUrl']
            dstUrl = form.cleaned_data['dstUrl']
            iid = form.cleaned_data.get('tmpId')
            obj, created = RedirectUrl.objects.update_or_create(id=iid,
                                                                defaults={'srcUrl': srcUrl, 'dstUrl': dstUrl,
                                                                          'user': request.user})
            assign_perm("delete_redirecturl", request.user, obj)
            assign_perm("change_redirecturl", request.user, obj)
            assign_perm("add_redirecturl", request.user, obj)
            return redirect('urlshortener:tableView')
        else:
            return render(request, 'urlshortener/detail.html', {'form': form})


def delete_view(request):
    if request.method == 'POST':
        if len(request.POST) <= 2:
            messages.warning(request, 'Bitte URLs auswählen', extra_tags='alert alert-primary')
        else:
            for i in list(request.POST.items())[1:-1]:
                if not request.user.has_perm('delete_redirecturl', RedirectUrl.objects.get(srcUrl=i[0])):
                    messages.warning(request, 'Keine Berechtigung', extra_tags='alert alert-primary')
                    return redirect('urlshortener:tableView')
            for i in list(request.POST.items())[1:-1]:
                RedirectUrl.objects.filter(srcUrl=i[0]).delete()
            messages.warning(request, 'Erfolgreich gelöscht!', extra_tags='alert alert-success')
    return redirect('urlshortener:tableView')


def table_view(request):
    if request.user.is_authenticated:
        template = loader.get_template('urlshortener/table.html')
        urllist = get_objects_for_user(request.user, perms={"view_redirecturl"}, klass=RedirectUrl, any_perm=True)
        context = {
            'urllist': urllist,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("Bitte loggen Sie sich ein !")
