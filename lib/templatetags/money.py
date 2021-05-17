from django.template import Library

from lib.utils import money


register = Library()

register.filter('money', money)
