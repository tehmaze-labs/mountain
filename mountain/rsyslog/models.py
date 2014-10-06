from mountain.db import db


SYSLOG_FACILITY = (
    'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp',
    'clock', 'authpriv', 'ftp', 'ntp', 'log-audit', 'log-alert', 'cron',
    'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6',
    'local7',
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



class SystemEvent(db.Model):
    __tablename__ = 'systemevents'
    __aliases__ = dict(
        host='fromhost',
        time='receivedat',
        date='receivedat',
    )

    id                 = db.Column(db.Integer, primary_key=True)
    customerid         = db.Column(db.BigInteger)
    receivedat         = db.Column(db.DateTime)
    devicereportedtime = db.Column(db.DateTime)
    facility           = db.Column(db.SmallInteger)
    facility.choices   = SYSLOG_FACILITY
    priority           = db.Column(db.SmallInteger)
    priority.choices   = SYSLOG_LEVEL
    fromhost           = db.Column(db.String(60))
    message            = db.Column(db.Text)
    ntseverity         = db.Column(db.Integer)
    importance         = db.Column(db.Integer)
    eventsource        = db.Column(db.String(60))
    eventuser          = db.Column(db.String(60))
    eventcategory      = db.Column(db.Integer)
    eventid            = db.Column(db.Integer)
    eventbinarydata    = db.Column(db.Text)
    maxavailable       = db.Column(db.Integer)
    currusage          = db.Column(db.Integer)
    minusage           = db.Column(db.Integer)
    maxusage           = db.Column(db.Integer)
    infounitid         = db.Column(db.Integer)
    syslogtag          = db.Column(db.String(60))
    eventlogtype       = db.Column(db.String(60))
    genericfilename    = db.Column(db.String(60))
    systemid           = db.Column(db.Integer)
    properties         = db.relationship('SystemEventProperty',
                                         backref='systemevent',
                                         lazy='dynamic')


class SystemEventProperty(db.Model):
    __tablename__ = 'systemeventsproperties'

    id                 = db.Column(db.Integer, primary_key=True)
    systemeventid = db.Column(db.Integer, db.ForeignKey('systemevents.id'))
    paramname     = db.Column(db.String(255))
    paramvalue    = db.Column(db.Text)
