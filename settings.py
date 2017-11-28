#-*- coding: utf-8 -*-
# Django settings for project project.
import os
import logging.config


#DEBUG = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


def mk_dir(list):
    for i in list:
        try: os.makedirs(i)
        except OSError: pass
        
ADMINS = (
    #('Yuriy', 'xxxxxxxxxxxx@gmail.com'),
)

MANAGERS = ADMINS
#
DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxxxxxxx_db',
        'USER': 'xxxxxxxx',
        'PASSWORD': 'xxxxxxxx',
        'HOST': 'localhost',
        'PORT': '',
    },

    'afisha': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxxxxxxx_kino',
        'USER': 'xxxxxxxx',
        'PASSWORD': 'xxxxxxxx',
        'HOST': 'localhost',
        'PORT': '',
    },

    'story': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxxxxxxx_story',
        'USER': 'xxxxxxxx',
        'PASSWORD': 'xxxxxxxx',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', ('Russian')),
    ('uk', ('Ukrainian')),
)

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), 'locale'),
)

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = '/kinoinfo.ru/upload'

MEDIA_URL = '/upload/'

STATIC_ROOT = '/kinoinfo.ru/static'

STATIC_URL = '/static/'

GEOIP_PATH = rel('user_registration/geoip/')

PATTERN_ROOT = rel('files','template')

PATTERN_URL = '/templates/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    #'/kinoinfo.ru/static/'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django_openid_consumer.middleware.OpenIDMiddleware',
    'base.middleware.SubdomainMiddleware',
)



ROOT_URLCONF = 'urls'
#ROOT_URLCONF = 'kinoinfo.urls'

TEMPLATE_DIRS = (
    rel('base','templates'),
)



TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'linkexchange_django.context_processors.linkexchange',
    #'base.context_processors.base_processor',
)



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'base',
    'api',
    'kinoinfo_folder',
    'kinoafisha',
    'slideblok',
    'dajaxice',
    'registration',
    'django_openid_consumer',
    'user_registration',
    'release_parser',
    'linkexchange_django',
    'articles',
    'tinymce',
    'movie_online',
    'feedback',
    'umrunet',
    'googlecharts',
    'kinoafisha_ua',
    'organizations',
    'vsetiinter_net',
    'film',
    'news',
    'person',
    'letsgetrhythm',
    'vladaalfimov',
    'imiagroup',
    'forums',
    'music',
    'linkanoid',
    'pmprepare'
)

API_EX_PATH = rel('api/examples')

API_STEP = 500
API_GUEST_LIMIT = 10
API_CLIENT_LIMIT = 500

API_DUMP_PATH = rel('%s/dump' % API_EX_PATH)
API_CLIENTS_PATH = rel('api/clients')

KINOBILETY_PATH = '%s/kinobilety' % API_EX_PATH

ADV_REPORTS = '%s/adv_reports' % API_EX_PATH

NOF_DUMP_PATH = '%s/nof' % API_DUMP_PATH
LOG_DUMP_PATH = '%s/log' % API_DUMP_PATH

ORGANIZATIONS_FOLDER = '/organizations'
NEWS_FOLDER = '/news'
GALLERY_FOLDER = '/gallery'

try: os.makedirs(rel('api/examples/dump'))
except OSError: pass

AVATARS = MEDIA_ROOT + '/avatars'
AVATAR_FOLDER = MEDIA_ROOT + '/profiles'
INVOICES_TMP = MEDIA_ROOT + '/invoices_pdf_tmp'
BACKGROUND_PATH = MEDIA_ROOT + '/bg'
CRON_LOG_PATH = API_EX_PATH + '/cron_log'
SUCCESS_LOG_PATH = API_EX_PATH + '/success'
POSTERS_UA_PATH = MEDIA_ROOT + '/films/posters/uk'
POSTERS_EN_PATH = MEDIA_ROOT + '/films/posters/en'
WF_PATH = MEDIA_ROOT + '/forums'
PERSONS_IMGS = MEDIA_ROOT + '/persons'
MUSIC_PLAYER = MEDIA_ROOT + '/player'
BUTTONS = MEDIA_ROOT + '/btn'
ADV = MEDIA_ROOT + '/adv'
PROFILE_BG = MEDIA_ROOT + '/profiles_bg'
TORRENT_PATH = MEDIA_ROOT + '/torrent'
BOOKING_EXCEL_PATH = MEDIA_ROOT + '/booking_excel'

ORGANIZATIONS_PATH = MEDIA_ROOT + ORGANIZATIONS_FOLDER
NEWS_PATH = MEDIA_ROOT + NEWS_FOLDER
GALLERY_PATH = MEDIA_ROOT + GALLERY_FOLDER
SEO_PATH = API_EX_PATH + '/SEO'

mk_dir([
    AVATARS, 
    AVATAR_FOLDER, 
    INVOICES_TMP, 
    BACKGROUND_PATH, 
    CRON_LOG_PATH, 
    SUCCESS_LOG_PATH, 
    POSTERS_UA_PATH, 
    POSTERS_EN_PATH, 
    ORGANIZATIONS_PATH, 
    NEWS_PATH, 
    GALLERY_PATH, 
    WF_PATH, 
    PERSONS_IMGS, 
    MUSIC_PLAYER, 
    BUTTONS,
    ADV,
    PROFILE_BG,
    SEO_PATH,
    KINOBILETY_PATH,
    ADV_REPORTS,
    TORRENT_PATH,
    BOOKING_EXCEL_PATH,
])

API_DUMPS_LIST = ( 
    'cinema', 'persons', 'city_dir', 'genre_dir', 'hall', 'hall_dir', 'film1990', 
    'metro_dir', 'sources', 'film_posters', 'film_trailers', 'film1990_1999', 
    'film2000_2009', 'film2010_2011', 'film2012', 'film2013', 'film2014', 'schedule', 
    'imovie', 'screens', 'movie_reviews', 'imdb_rate', 'country_dir', 
    'films_name', 'theater', 'releases_ua', 'screens_v2', 'schedule_v2', 
    'film_v3_1990', 
    'film_v3_1990_1999', 'film_v3_2000_2009', 'film_v3_2010_2011', 'film_v3_2012', 'film_v3_2013', 'film_v3_2014',
    'film_v4_1990', 
    'film_v4_1990_1999', 'film_v4_2000_2009', 'film_v4_2010_2011', 'film_v4_2012', 'film_v4_2013', 'film_v4_2014',
)
PARSER_DUMPS_LIST = (
    'kinometro_ru', 'film_ru', 'film_releases', 'cmc_schedules', 'cmc_kid_schedules', 'cmc_good_films',
)


CLICKATELL_USER = 'kinoinfo'
CLICKATELL_PSWD = 'xxxxxxxxxxxxxx'
CLICKATELL_API_ID = 'xxxxxxx'


# цены по форматам
PRICES = {
    0: 41, # отключение фона
    1: 42, # рекламный блок текстовый (весь сайт)
    2: 43, # фон (весь сайт)
    3: 44, # фон (страница юзера)
    4: 45, # рекламный блок (страница юзера)
    5: 46, # рекламный блок swf объект (весь сайт)
    6: 47, # рекламный блок текст (моб.версия сайта)
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'base.profile'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_tbl', #rel('cache'),
        'OPTIONS': {
            'MAX_ENTRIES': 50000
        }
    }
}


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'logfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': rel('LOGGING.TXT')
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass

