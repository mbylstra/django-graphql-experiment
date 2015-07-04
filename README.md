*This was written just after there was some basic information about GraphQL available after React Conf Jan 2015, and does not reflect the offical specification released during React Europe July 2015*

python GraphQL parser and django ORM integration

a highly experimental, probably buggy and limited proof-of-concept for GraphQL parsing and integration with the Django ORM.

to try it out:

- download code
- pip install -r requirements.py
- python scratchpad.py

You should see a GraphQL response :)

The GraphQL parser uses parsimonious (https://github.com/erikrose/parsimonious) and generates a simple AST that is converted to Django ORM queries
