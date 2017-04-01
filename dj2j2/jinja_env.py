from jinja2 import Environment


jinja_environment = Environment(
    extensions=[
        'jinja2.ext.with_',
        'jinja2_django_compat.ext.DjangoCompat',
    ],
)
