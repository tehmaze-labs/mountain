from functools import partial

from whoosh.qparser import default
from whoosh.query import compound, ranges, terms
from whoosh.query.wrappers import Not
from whoosh.qparser import plugins

from sqlalchemy.sql import and_, or_, not_, sqltypes
from sqlalchemy.sql.expression import bindparam


class ParserError(ValueError):
    pass


def get_field(model, field):
    try:
        return getattr(model, field)
    except AttributeError:
        return getattr(
            model,
            getattr(model, '__aliases__', {}).get(field, field)
        )


def to_sqlalchemy(model, query):
    if isinstance(query, compound.And):
        subqueries = map(
            partial(to_sqlalchemy, model),
            query.subqueries
        )
        return and_(*subqueries)

    elif isinstance(query, compound.Or):
        subqueries = map(
            partial(to_sqlalchemy, model),
            query.subqueries
        )
        return or_(*subqueries)

    elif isinstance(query, ranges.TermRange):
        lower = query.start
        upper = query.end
        field = get_field(model, query.fieldname)
        if lower is None:
            return field <= upper
        elif upper is None:
            return field >= lower
        else:
            return and_(field >= lower, field <= upper)

    elif isinstance(query, terms.Term):
        field = get_field(model, query.fieldname)
        if isinstance(field.property.columns[0].type, (
                sqltypes.Integer,
                sqltypes.BigInteger,
                sqltypes.SmallInteger,
                sqltypes.INT,
                sqltypes.BIGINT,
                sqltypes.SMALLINT,
            )):
            try:
                return int(query.text) == field
            except ValueError:
                if hasattr(field, 'choices') and query.text in field.choices:
                    return field.choices.index(query.text) == field
                else:
                    raise ParserError(
                        'Field {} must be an integer'.format(query.fieldname)
                    )

        else:
            return field.op('~')(query.text)

    elif isinstance(query, terms.Prefix):
        field = get_field(model, query.fieldname)
        return field.startswith(query.text[:-1])

    elif isinstance(query, terms.Wildcard):
        field = get_field(model, query.fieldname)
        text = query.text.replace('*', '%').replace('?', '_')
        return field.like(text)

    elif isinstance(query, Not):
        return not_(to_sqlalchemy(model, query.query))

    else:
        print 'dno?'
        print '\t', query
        print '\t', type(query)


class QueryParser(default.QueryParser):
    def __init__(self, model, default_field):
        self.model = model
        self.default_field = default_field
        super(QueryParser, self).__init__(self.default_field, None)

        # We don't want these
        self.remove_plugin_class(plugins.BoostPlugin)
        self.remove_plugin_class(plugins.PhrasePlugin)

    def parse(self, text, normalize=True, debug=False):
        parsed = super(QueryParser, self).parse(
            text, normalize=normalize, debug=debug,
        )

        try:
            return to_sqlalchemy(self.model, parsed)
        except AttributeError as error:
            if "'SystemEvent' has no attribute" in error.message:
                field = error.message.split("'")[3]
                raise ParserError("Invalid field '{}'".format(field))
