"""CiscoSparkAPI init."""
import logging
from .session import Session
from .people import People
from .roles import Roles
from .rooms import Rooms
from .messages import Messages
from .teams import Teams
from .memberships import Memberships
from .team_memberships import TeamMemberships
from .organizations import Organizations
from .licenses import Licenses
from .events import Events
from .webhooks import WebHooks

log = logging.getLogger(__name__)


# noinspection PyPep8Naming
class SparkAPI:
    def __init__(self, access_token, timeout=360, debug=False):
        self.access_token = access_token
        self.timeout = timeout
        self.debug = debug
        self.session = Session(self.access_token, self.timeout)
        self.people = People(self.session)
        self.roles = Roles(self.session)
        self.rooms = Rooms(self.session)
        self.teams = Teams(self.session)
        self.messages = Messages(self.session)
        self.licenses = Licenses(self.session)
        self.events = Events(self.session)
        self.memberships = Memberships(self.session)
        self.webhooks = WebHooks(self.session)
        self.team_memberships = TeamMemberships(self.session)
        self.organizations = Organizations(self.session)
        
    @property
    def me(self):
        return self.people.me()
