from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.core.urlresolvers import reverse

from django.views import generic
from django.views.generic.edit import *

from django.utils.html import format_html
from .models import *
from .forms import *

import json
import pprint

def welcome(request, user_id=None):
    h = get_object_or_404(ModuleHeading, module_name='home')
    r = {
        'heading': format_html(h.heading_content),
        'user': None
    }

    if request.method == "GET":
        if user_id:
            request.session['attempt_login_id'] = user_id
            p = get_object_or_404(Participant, pk=user_id)
            r['user'] = {
                'first_name': str(p.first_name),
                'id': p.id
            }
        return render(request, 'dc/welcome.html', r)

    elif request.method == "POST":
        if request.POST.get('consent_checkbox'):
            p = get_object_or_404(Participant, pk=request.session.get('attempt_login_id'))

            if not request.POST.get('password') == p.password:
                r['error_message'] = "Incorrect password."
                r['user'] = {
                    'first_name': p.first_name,
                    'id': p.id
                }

                return render(request, 'dc/welcome.html', r)

            request.session['user_id'] = str(p.id)

            if p.current_phase == 'newly_added':
                return HttpResponseRedirect(reverse('dc:sign_in'))
            elif p.current_phase in ('brainstorming_completed', 'rating_completed'):
                return HttpResponseRedirect(reverse('dc:thanks'))
            elif p.current_phase == 'grouping_enabled':
                return HttpResponseRedirect(reverse('dc:group_statements'))
        else:
            print('user didn;t consent')


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
        context['user'] = self.object
        return context

    def form_valid(self, form):
        new_participant = form.save()

        return HttpResponseRedirect(self.success_url)


def error(request):
    return render(request, 'dc/error.html')


def brainstorm(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('dc:error'))

    p = get_object_or_404(Participant, pk=request.session['user_id'])

    if request.method == "GET":
        h = get_object_or_404(ModuleHeading, module_name='brainstorm')
        r = {
            'heading': format_html(h.heading_content)
        }

        return render(request, 'dc/brainstorm.html', r)

    elif request.method == "POST":
        statements = request.POST.getlist('statement')
        for s in statements:
            if s:
                db_s = ParticipantStatement(text=s, author=p)
                db_s.save()

        p.current_phase = 'brainstorming_completed'
        p.save()

        return HttpResponseRedirect(reverse('dc:thanks'))


def group_statements(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('dc:error'))

    p = get_object_or_404(Participant, pk=request.session['user_id'])

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

        group_number = 0

        for group in d:
            for statement in group:
                group_name = statement['group_name']
                s = get_object_or_404(DistilledStatement, pk=statement['id'])

                grouping = StatementSorting(author=p, order=group_number, statement=s, group_name=group_name)
                grouping.save()
            group_number += 1
        return HttpResponseRedirect(reverse('dc:rate_statements'))


def rate_statements(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('dc:error'))

    p = get_object_or_404(Participant, pk=request.session['user_id'])
    s = DistilledStatement.objects.all()

    if request.method == "GET":
        h = get_object_or_404(ModuleHeading, module_name='rate')

        r = {
            'heading': format_html(h.heading_content),
            'statements': s
        }

        return render(request, 'dc/rate.html', r)

    elif request.method == "POST":

        my_dict = dict(request.POST.items())
        pprint.pprint(my_dict)
        #
        # if len(my_dict)-1 < s.count():


        for key, rating in my_dict.items():
            if key == 'csrfmiddlewaretoken':
                continue

            rating = request.POST[key]

            s = get_object_or_404(DistilledStatement, pk=key)

            rating = StatementRating(author=p, statement=s, rating=rating)
            rating.save()


        # for key in request.POST:
        #     print(key + " " + request.POST[key])




        p.current_phase = 'rating_completed'
        p.save()

        return HttpResponseRedirect(reverse('dc:thanks'))


def thanks(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse('dc:error'))

    user_id = request.session.get('user_id')
    print('user_id={}'.format(user_id))
    p = get_object_or_404(Participant, pk=request.session['user_id'])

    return render(request, 'dc/thanks.html', {"first_name": p.first_name})
