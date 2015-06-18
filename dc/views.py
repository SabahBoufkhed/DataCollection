from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.core.urlresolvers import reverse

from django.views import generic
from django.views.generic.edit import *

from django.utils.html import format_html
from .models import *
from .forms import *

import pprint
import json


def group_statements(request):
    if request.method == "GET":
        h = get_object_or_404(ModuleHeading, module_name='group')
        s = DistilledStatement.objects.all()

        r = {
            'heading': format_html(h.heading_content),
            'statements': s
        }
        return render(request, 'dc/group.html', r)

    elif request.method == "POST":
        d = json.loads(request.body.decode("utf-8"))

        current_user = get_object_or_404(Participant, pk=request.session['user_id'])
        group_number = 0

        pprint.pprint(d)
        for group in d:
            pprint.pprint(group)
            for statement in group:
                s = get_object_or_404(DistilledStatement, pk=statement['id'])
                grouping = StatementSorting(participant=current_user, order=group_number, statement=s)
                grouping.save()
            group_number += 1
        return HttpResponseRedirect(reverse('dc:rate_statements'))


def rate_statements(request):
    if request.method == "GET":
        h = get_object_or_404(ModuleHeading, module_name='rate')
        s = DistilledStatement.objects.all()

        r = {
            'heading': format_html(h.heading_content),
            'statements': s
        }

        pprint.pprint(r)
        return render(request, 'dc/rate.html', r)

    elif request.method == "POST":
        current_user = get_object_or_404(Participant, pk=request.session['user_id'])

        pprint.pprint(request.POST)
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                continue

            rating = request.POST[key]

            s = get_object_or_404(DistilledStatement, pk=key)

            rating = StatementRating(participant=current_user, statement=s, rating=rating)
            rating.save()

        return HttpResponseRedirect(reverse('dc:thanks'))


class SignInFormView(generic.UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'dc/sign_in.html'
    success_url = '/brainstorm/'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Participant, pk=self.request.session['user_id'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(SignInFormView, self).get_context_data(**kwargs)

        context['name'] = str(self.object)
        return context

    def form_valid(self, form):
        pprint.pprint(form)
        new_participant = form.save()

        #self.request.session['logged_in_as'] = new_participant.id
        return HttpResponseRedirect(self.success_url)


def logout(request):
    if 'logged_in_as' in request.session:
        del request.session['logged_in_as']
        return HttpResponse("logged out")
    else:
        return HttpResponse("wasn't logged in")


def welcome(request, user_id=None):
    if request.method == "GET":
        h = get_object_or_404(ModuleHeading, module_name='home')
        r = {
            'heading': format_html(h.heading_content)
        }

        if user_id:
            p = get_object_or_404(Participant, pk=user_id)

            request.session['user_id'] = user_id
            r['name'] = str(p)

        return render(request, 'dc/welcome.html', r)


    elif request.method == "POST":
        if 'user_id' in request.session:
            p = get_object_or_404(Participant, pk=request.session['user_id'])

            password = request.POST['password']
            if str(password) == p.password:
                print("pass matches")
            else:
                print("pass doesnt match")
            return HttpResponseRedirect(reverse('dc:sign_in'))
        else:
            return HttpResponse('you are not a user') #TODO:
#
# def sign_in(request):
#     if 'user_id' not in request.session:
#         return HttpResponse('you are not a user')
#
#     p = get_object_or_404(Participant, pk=request.session['user_id'])
#     if request.method == "GET":
#         pass
#     return render(request, 'dc/log_in.html', {'name': str(p)})
#
#     # if 'logged_in_as' in request.session:
#     #     user_id = request.session['logged_in_as']
#     #     p = get_object_or_404(Participant, pk=user_id)
#     #
#     #     return render(request, 'dc/log_in.html', {'name': str(p)})
#     # else:
#     #     return render(request, 'dc/sign_in.html')


def brainstorm(request):
    if request.method == "GET":
        h = get_object_or_404(ModuleHeading, module_name='brainstorm')
        r = {
            'heading': format_html(h.heading_content)
        }

        return render(request, 'dc/brainstorm.html', r)

    elif request.method == "POST":
        #TODO: how to guard against user not being there?
        current_user = get_object_or_404(Participant, pk=request.session['user_id'])

        statements = request.POST.getlist('statement')
        for s in statements:
            db_s = ParticipantStatement(text=s, author=current_user)
            db_s.save()

        print("Saved num=" + str(len(statements)))
        return HttpResponseRedirect(reverse('dc:thanks'))


def thanks(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        p = get_object_or_404(Participant, pk=user_id)

        return render(request, 'dc/thanks.html', {"name": str(p)})