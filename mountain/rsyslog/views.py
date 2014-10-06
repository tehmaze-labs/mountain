import re

from flask import Blueprint, request, render_template
import jinja2

from .models import SystemEvent
from mountain.app import app
from mountain.query.parser import QueryParser, ParserError

# Define the blueprint
mod_rsyslog = Blueprint('rsyslog', __name__)

# Syslog specifics
SYSLOG_FACILITY = (
    'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp',
    'clock', 'authpriv', 'ftp', 'ntp', 'log-audit', 'log-alert', 'cron',
    'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6',
    'local7',
)
SYSLOG_FACILITY_MAP = {facility: i for i, facility in enumerate(SYSLOG_FACILITY)}
SYSLOG_FACILITY_DEFAULT = (
    SYSLOG_FACILITY.index('kern'),
    SYSLOG_FACILITY.index('user'),
    SYSLOG_FACILITY.index('daemon'),
    SYSLOG_FACILITY.index('auth'),
    SYSLOG_FACILITY.index('syslog'),
    SYSLOG_FACILITY.index('authpriv'),
)
SYSLOG_LEVEL = (
    'emergency',        # 0       Emergency: system is unusable
    'alert',            # 1       Alert: action must be taken immediately
    'critical',         # 2       Critical: critical conditions
    'error',            # 3       Error: error conditions
    'warning',          # 4       Warning: warning conditions
    'notice',           # 5       Notice: normal but significant condition
    'informational',    # 6       Informational: informational messages
    'debug',            # 7       Debug: debug-level messages
)

# Link filters
LINK_FILTERS = (
    (   # IPv4 address
        'message:',
        re.compile(r'\b((?:\d{1,3}\.){3}\d{1,3})\b'),
    ),
    (   # Mac address
        'message:',
        re.compile(r'\b((?:[0-9a-fA-F]{2}[:-]){5}(?:[0-9a-fA-F]{2}))\b'),
    ),
    (   # Postfix queue id
        'message:',
        re.compile(r'\b([0-9A-F]{10})\b'),
    ),
    (   # user
        'message:',
        re.compile(r'user[ =](\S+)', re.I),
    ),
)


def rsyslog_link(message, query=''):
    replace = {}
    for term, match in LINK_FILTERS:
        for hit in match.findall(message):
            replace[hit] = term

    if query:
        query = '+' + query

    for hit, term in replace.items():
        message = message.replace(
            hit,
            '<a href="?_q={query}{term}\'{link}\'">{hit}</a>'.format(
                query=query,
                hit=hit,
                link=''.join(['%{:02x}'.format(ord(c)) for c in hit]),
                term=term,
            )
        )

    return jinja2.Markup(message)


app.jinja_env.filters['rsyslog_link'] = rsyslog_link


@mod_rsyslog.route('/')
def index():
    try:
        page = int(request.args.get('page', 1))
    except (KeyError, ValueError):
        page = 1

    facilities = request.args.getlist('facility')
    facilities = facilities or SYSLOG_FACILITY_DEFAULT
    try:
        facilities = map(int, facilities)
    except ValueError:
        facilities = SYSLOG_FACILITY_DEFAULT

    filters = None
    query = request.args.get('_q', '')
    query_error = None
    if query:
        scope = SYSLOG_FACILITY_MAP.copy()
        try:
            filters = QueryParser(
                SystemEvent, 'message',
            ).parse(query)
        except (ParserError, SyntaxError) as query_error:
            pass

    if filters is not None:
        print 'filters', filters
        events = SystemEvent.query.filter(filters)
    else:
        events = SystemEvent.query.filter(
            SystemEvent.facility.in_(facilities),
        )
    events = events.order_by('receivedat DESC')
    pager = events.paginate(page, 50, False)

    return render_template(
        'rsyslog/index.html',
        pager=pager,
        query=query,
        query_error=query_error,
        facility=SYSLOG_FACILITY,
        current_facilities=facilities,
    )
