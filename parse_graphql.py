from parsimonious.grammar import Grammar
import json
grammar = Grammar("""

     root =         WS object_name WS OPEN_ROUND WS object_id WS CLOSE_ROUND WS WS object WS

     object = OPEN_CURLY WS field_list WS CLOSE_CURLY
     WS =           ~"\s*"
     OPEN_CURLY =   "{"
     CLOSE_CURLY =  "}"
     OPEN_ROUND =   "("
     CLOSE_ROUND =   ")"
     COMMA = ","
     object_name =  ~"[A-Z0-9]*"i
     object_id =    ~"[A-Z0-9]*"i
     name =         ~"[A-Z0-9]*"i
     field_name =   ~"[A-Z0-9]*"i
     field_list = field WS (COMMA WS field)*
     field = field_name WS optional_object
     optional_object = object?

""")


# print ast


#convert to a python dict

IGNORE_NAMES = ['WS', 'OPEN_CURLY', 'CLOSE_CURLY', 'COMMA', 'OPEN_ROUND', 'CLOSE_ROUND']

split_list = lambda lst: (lst[0], lst[1:])

def filter_tokens(node):
    return node.expr_name not in IGNORE_NAMES


def convert_field(ast):
    (field_name, _, optional_object) = ast

    child_fields = [] if len(optional_object.children) == 0 else (
        convert_object(optional_object.children[0])
    )

    return {
        'field_name': field_name.text,
        'child_fields': child_fields
    }

def convert_object(ast):
    print 'convert_object'
    head, rest = filter(filter_tokens, filter(filter_tokens, ast.children)[0])
    map(lambda x: filter(filter_tokens, x.children)[0], rest.children)

    fields = [head] + map(lambda x: filter(filter_tokens, x.children)[0],
                          rest.children)

    fields = [convert_field(field) for field in fields]
    return fields

def convert_root_object(ast):
    (object_name, object_id, my_object) = filter(filter_tokens, ast.children)

    return {
        object_name.text: {
            'fields': convert_object(my_object),
            'id': object_id.text
        }
    }

# output = convert_root_object(ast)
# print json.dumps(output, indent=4)

def parse_graphql(graphql):

    #eg:
    #graphql = """
    #    User (234234) {
    #        one {
    #            sub1,
    #            sub2
    #        },
    #        two,
    #        three,
    #        four
    #    }
    #"""

    ast = grammar.parse(graphql)
    return convert_root_object(ast)
