from django import setup
from django.conf import settings


def configure_django():
    if configure_django._run:
        return

    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.humanize',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                },
            },
        ],
    )

    setup()

    configure_django._run = True


configure_django._run = False
