from os.path import dirname, realpath
import sys
import os
import math
import json

ROOT_PATH = dirname(realpath(__file__))
sys.path.append(ROOT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'wham_gql.settings'
from django.conf import settings
##############################################################################################################################################

# from spotify_wham.models import SpotifyArtist
from test_models.models import Address, Person
from parse_graphql import parse_graphql

# SpotifyArtist.objects.wham_get(pk='234234')

# address = Address.objects.create(street='Sherwood Road', city='Mount Waverley', country='Australia')
# pserson = Person.objects.create(name="Michael", nickname="mike", address=address)

# for a in Address.objects.all():
#     print a.pk


def pretty_print(o):
    print json.dumps(o, indent=4)

for p in Person.objects.all():
    print p.pk

# parse_graphql

pgql = parse_graphql("""
    Person(1) {
        name,
        nickname,
        address {
            street,
            city,
            country
        }
    }
""")

pgql_object = pgql['Person']
id = pgql_object['id']
person = Person.objects.get(pk=id)

def fetch_fields(fields, object):
    out = {}
    for field in fields:
        out[field['field_name']] = fetch_field(field, object)

    return out

def fetch_field(field, object):
    field_name = field['field_name']
    child_fields = field['child_fields']
    value = getattr(object, field_name)
    if len(child_fields) > 0:
        related_object = value
        return fetch_fields(child_fields, related_object)
    else:
        return value


def fetch_object(ast, object):
    return fetch_fields(ast['fields'], object)
    return out_fields




out = {
    id: fetch_object(pgql_object, person)
}
pretty_print(out)

#output:

#{
#    "1": {
#        "nickname": "mike",
#        "name": "Michael",
#        "address": {
#            "city": "Mount Waverley",
#            "street": "Sherwood Road",
#            "country": "Australia"
#        }
#    }
#}

# print out


# print json.dumps(pgql_object, indent=4)
