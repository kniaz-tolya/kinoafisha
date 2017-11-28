﻿#-*- coding: utf-8 -*-
import os
import datetime
import operator

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.db.models import Q

from bs4 import BeautifulSoup

from base.models import User, Accounts, DjangoSite, Background
from api.models import *
from api.func import *
from user_registration.func import only_superuser, org_peoples
from articles.views import pagination as pagi

@only_superuser
@never_cache
def api_panel(request):
    '''
    Админ панель API
    '''
    return render_to_response('api/api_panel.html', context_instance=RequestContext(request)) 


def pagination(request, content, rows):
    paginator = Paginator(content, rows)
    page = 1
    if 'btn' in request.POST: 
        if request.POST['btn'].encode('utf-8') == 'Вперед':
            page = request.POST['next']
        elif request.POST['btn'].encode('utf-8') == 'Назад':
            page = request.POST['prev']
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    return p



@only_superuser
@never_cache
def edit_api_description(request):
    from api.forms import ApiDescriptionForm
    fileName = getApiDescrFileName(request)
    if request.POST:
        form = ApiDescriptionForm(request.POST)
        if form.is_valid():
            content = request.POST['text'].encode('utf-8')
            f = open(fileName,'w')
            f.write(content)
    else:
        f = open(fileName,'r')
        content = f.read()
    form = ApiDescriptionForm(initial={'text': content},)
    f.close()
    return render_to_response('api/edit_descr.html', {'form': form}, context_instance=RequestContext(request))




@only_superuser
@never_cache
def api_users_2(request):

    groups = {
        '1': {'id': '1', 'name': 'Суперюзеры', 'filter': {'user__is_superuser': True}}, 
        '2': {'id': '2', 'name': 'API клиенты', 'filter': {'user__groups': 1}}, 
        '3': {'id': '3', 'name': 'Aвторизованные', 'filter': 'exclude'},
        '4': {'id': '4', 'name': 'Остальные', 'filter': 'other'},
        '5': {'id': '5', 'name': 'Результат поиска', 'filter': {}},
    }
    
    group = None
    search = None
    date_now, date_past = (None, None)

    if request.POST:
        if 'search_btn' in request.POST:
            search = request.POST.get('user_search').strip()
            if 'date_btn' in request.POST:
                group = '4'
                date_now = request.POST.get('date_to', '').split('-')
                date_past = request.POST.get('date_from', '').split('-')
                if date_now and date_past:
                    date_now = datetime.datetime(int(date_now[2]), int(date_now[1]), int(date_now[0]), 23, 59, 59)
                    date_past = datetime.date(int(date_past[2]), int(date_past[1]), int(date_past[0]))
                else:
                    date_now, date_past = (None, None)
        else:
            group = request.POST.get('user_group')


    if not group and not search:
        search = request.session.get('filter_api_users_2__search')
        
    if search:
        group = '5'
    else:
        del groups['5']


    groups_list = groups.values()
    
    if not group:
        group = request.session.get('filter_api_users_2__group', groups_list[0]['id'])
        if not search and group == '5':
            group = groups_list[0]['id']
    
    
    filter = groups.get(group)

    filter = filter['filter']

    if search:
        users = Profile.objects.select_related('user').only('user', 'id').filter(Q(accounts__login__icontains = search) | Q(accounts__nickname__icontains = search) | Q(accounts__email__icontains = search) | Q(accounts__fullname__icontains = search) | Q(person__name__name__icontains = search, person__name__status=1, person__name__language__id=1)).distinct('user__id').order_by('user__id')[:100]
    else:
        if filter == 'exclude':
            users = Profile.objects.select_related('user').exclude(accounts=None).distinct('user__id').order_by('user__id')
        elif filter == 'other':
            if not date_past:
                date_now = datetime.datetime.now()
                date_past = date_now - datetime.timedelta(days=2)
            
            users = Profile.objects.select_related('user').filter(accounts=None, user__is_superuser=False, user__date_joined__gte=date_past, user__date_joined__lte=date_now).distinct('user__id').order_by('user__id')
        else:
            users = Profile.objects.select_related('user').filter(**filter).distinct('user__id').order_by('user__id')


    page = request.GET.get('page')
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1
        
    p, page = pagi(page, users, 15)
    

    peoples = set([i for i in p.object_list])

    groups = {}
    for i in list(Group.objects.filter(name='API', user__profile__in=peoples).values_list('user', flat=True)):
        groups[i] = True

    users_x = []
    for i in org_peoples(peoples):
        i['api_client'] = groups.get(i['id'], False)
        users_x.append(i)

    request.session['filter_api_users_2__group'] = group
    request.session['filter_api_users_2__search'] = search
    
    mlist_count = len(request.session.get('users_merge_list', []))
    
    tmplt = 'music/admin_users.html' if request.subdomain else 'api/user_controls_2.html'
    
    return render_to_response(tmplt, {'groups': groups_list, 'group': group, 'p': p, 'page': page, 'search': search, 'users_x': users_x, 'date_now': date_now, 'date_past': date_past, 'mlist_count': mlist_count}, context_instance=RequestContext(request))


@only_superuser
@never_cache
def api_users_OLD(request):
    '''
    Управление пользователями. Назначение прав (админ, api клиент)
    '''
    current_site = DjangoSite.objects.get_current()
    if current_site.domain in ('kinoinfo.ru', 'kinoafisha.in.ua'):
        template = 'api/user_controls.html'
    elif current_site.domain == 'umru.net':
        template = 'panel/umrunet_user_controls.html'
        
    if request.method == 'POST' and 'user' in request.POST:
        name = request.POST['user']
        def get_acc(myfilter):
            try:
                acc = Accounts.objects.filter(**myfilter).filter(profile__site=current_site.id)
                if acc.count() > 0: return acc
            except Accounts.DoesNotExist: pass
            return False
        myfilters = [{'login__iexact': name}, {'nickname__iexact': name}, {'email__iexact': name}, {'fullname__iexact': name}]
        result = {'status': 'user_api', 'account': None}
        for i in myfilters:
            account = get_acc(i)
            if account:
                acc_list = {}
                for j in account:
                    try:
                        user = User.objects.get(profile__accounts=j)
                        if acc_list.get(user.id) is None:
                            acc_list[user.id] = {'user': user, 'acc': j}
                    except User.DoesNotExist: pass
                result['content'] = acc_list
                break
    else:
        result = {'status': 'user_api' }
    return render_to_response(template, {'result': result}, context_instance=RequestContext(request))


@only_superuser
@never_cache
def get_user_list(request):
    '''
    Список всех пользователей
    '''
    current_site = request.current_site
    if current_site.domain in ('kinoinfo.ru', 'kinoafisha.in.ua'):
        template = 'api/user_controls.html'
    elif current_site.domain == 'umru.net':
        template = 'panel/umrunet_user_controls.html'
        
    users = Profile.objects.select_related('user', 'person').filter(site=current_site.id).order_by('id')
    result = {'status': 'user_list'}

    page = request.GET.get('page')
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1

    p, page = pagi(page, users, 10)
    
    return render_to_response(template, {'result': result, 'p': p, 'page': page}, context_instance=RequestContext(request))


@only_superuser
@never_cache
def change_background(request):
    '''
    Изменение фона (brand.jpg) и ссылки
    '''
    from api.forms import BackgroundForm
    #Выбор шаблона для сайта kinoinfo.ru или umru.net
    current_site = request.current_site
    
    template = 'api/change_bg_banner.html'

    #загрузка изображения и ссылки, на сайт рекламодателя, в БД
    if request.method == 'POST':
        subdomain = request.subdomain
        if not subdomain:
            subdomain == None
        # для локального
        if subdomain == '127':
            subdomain == None
        
        files = request.FILES
        
        image = request.FILES.get('image')
        if image:
            image_name = image.name.encode('utf-8')
            files['image'].name = image_name.decode('utf-8')
        
        form = BackgroundForm(None, request.POST, files)
        if form.is_valid():
            f = form.save(commit=False)
            f.site = current_site
            f.subdomain = subdomain
            f.save()
            return HttpResponseRedirect('%s' % request.path)
    else:  
        country_name = 'Россия' 
        if current_site.domain == 'kinoafisha.in.ua':
            country_name = 'Украина'
            
        country = Country.objects.get(name=country_name)
        
        form = BackgroundForm(country.id,
            initial={
                'country': country.id, 
            }
        )
    
    links = {}
    if current_site.domain == 'vladaalfimovdesign.com.au':
        with open('%s/vlada_main_links.xml' % settings.API_EX_PATH, 'r') as f:
            links_tmp = BeautifulSoup(f.read())
            for i in links_tmp.findAll('link'):
                links[i['id']] = i['value']
    
    extends = 'release_parser/kinoafisha_admin.html'
    block = 'info'
    if current_site.domain == 'vsetiinter.net':
        extends = 'base.html'
        block = 'content'
    elif current_site.domain in ('vladaalfimovdesign.com.au', 'imiagroup.com.au'):
        template = 'vladaalfimov/change_bg_banner.html'
    
    return render_to_response(template, {'form': form, 'extends': extends, 'bl': block, 'links': links, 'current_site': current_site.domain}, context_instance=RequestContext(request))


@only_superuser
@never_cache 
def get_user_request_list(request, rows=100):
    '''
    Вывод лога обращений к API
    '''
    request_list = APILogger.objects.all().order_by('-date')[:rows]
    result = {'status': 'request_list'}
    p = pagination(request, request_list, 250)
    return render_to_response('api/api_calls_log.html', {'result': result, 'content': request_list, 'p': p}, context_instance=RequestContext(request))


@only_superuser
@never_cache 
def get_api_request_statistic(request):
    days = 7

    now = datetime.datetime.today()
    past_days = now - datetime.timedelta(days=days)

    data = {}
    for i in APILogger.objects.filter(date__gte=past_days, date__lte=now):
        if not data.get(i.ip):
            data[i.ip] = {'ip': i.ip, 'count': 0, 'avg': 0, 'status': 0, 'sec': 0}
        data[i.ip]['count'] += 1

    data = sorted(data.values(), key=operator.itemgetter('count'), reverse=True)
    count = len(data)
    data = data[:100]

    for i in data:
        sec = float(86400) / i['count']

        avg = float(i['count']) / days
        if i['avg'] >= 86400:
            i['status'] = 1
        elif i['avg'] >= 43200:
            i['status'] = 2

        i['avg'] = '%5.1f' % avg
        i['sec'] = '%5.1f' % sec

    return render_to_response('api/api_request_statistic.html', {'data': data, 'days': days, 'count': count}, context_instance=RequestContext(request))


@only_superuser
@never_cache
def daniya_films(request):
    
    file = open('%s/daniya_films.txt' % settings.API_EX_PATH, 'r')
    ids = [int(i) for i in file.readlines()]
    file.close()
    
    films = []
    for i in ids:
        films.append({'id': int(i), 'url': 'http://www.kinoafisha.ru/?status=1&id1=%s' % i})

    if request.POST:
        add_url = request.POST.get('add_url')
        del_url = request.POST.get('del_url')
        if add_url:
            url = request.POST.get('url')
            if url:
                result = re.findall(r'id1\=\d+', url)
                if result:
                    result = result[0].split('=')[1]
                    file = open('%s/daniya_films.txt' % settings.API_EX_PATH, 'a')
                    file.write('%s\n' % result)
                    file.close()
        elif del_url:
            checker = [int(i) for i in request.POST.getlist('checker')]
            file = open('%s/daniya_films.txt' % settings.API_EX_PATH, 'w')
            for i in ids:
                if i not in checker:
                    file.write('%s\n' % i)
            file.close()
        return HttpResponseRedirect(reverse('daniya_films'))
    
    films = sorted(films, key=operator.itemgetter('id'))

    page = request.GET.get('page')
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1
    p, page = pagi(page, films, 15)

    return render_to_response('api/daniya_films.html', {'p': p, 'page': page}, context_instance=RequestContext(request))




