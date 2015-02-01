# coding=utf-8
import httplib

from wtforms import validators
from models.producer import Producer
from forms.base_form import BaseForm
from forms import widgets as flotimo_widgets
from wtforms_appengine.ndb import model_form

sys


ProducerForm = model_form(
    Producer,
    BaseForm,
    only=('name', 'price_group'),
    field_args={
        'name': {
            'label': u'Nazwa',
            'validators': [validators.Required()]
        },
        'price_group': {
            'label': u'Klasa',
            'coerce': int,
            'widget': flotimo_widgets.ChoicesSelect(
                choices=Producer._PRICE_GROUP.items()),
        }
    })