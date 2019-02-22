"""Manage Spark Web hooks."""

from .spark_class import SparkDataClass, SparkAPI
from .messages import Message
from .memberships import Membership


class Hook(SparkDataClass):
    """
    Represent a Cisco Spark Web hook.
    """
    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.name = data.pop('name', '')
        self.resource = data.pop('resource', '')
        self.event = data.pop('event', '')
        self.targetUrl = data.pop('targetUrl', '')
        self.filter = data.pop('filt', '')
        self.orgId = data.pop('orgId', '')
        self.createdBy = data.pop('createdBy', '')
        self.appId = data.pop('appId', '')
        self.status = data.pop('status', '')
        self.secret = data.pop('secret', '')
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)

    def __str__(self):
        return 'Spark WebHook ({})'.format(self.id)


class HookEvent(Hook):
    """Represent a Cisco Spark Web hook event."""
    def __init__(self, data, whitelist=(), blacklist=()):
        self.ownedBy = data.pop('ownedBy')
        self.actorId = data.pop('actorId', '')
        super().__init__(data, whitelist, blacklist)
        self.data = self.get_data_obj(data.get('data'))

    def get_data_obj(self, data_dict):
        if not data_dict:
            return None
        if self.resource == 'messages':
            return Message(data_dict)
        elif self.resource == 'memberships':
            return Membership(data_dict)
        else:
            return None

    def msg_sent_by_bot(self):
        if self.resource == 'messages':
            return self.data.personId == self.createdBy
        return False

    def membership_create_for_bot(self):
        if self.resource == 'memberships' and self.event == 'created':
            return self.data.personId == self.createdBy

    def __str__(self):
        return 'Spark WebHook Event ({})'.format(self.id)


class WebHooks(SparkAPI):
    """Manipulate Cisco Spark Web hooks."""
    DataClass = Hook

    def get_by_name(self, name, max=None):
        """Return list of Hook objects corresponding to the name provided."""
        hooks = self.list(max=max)
        filtered_hooks = [h for h in hooks if h.name == name]
        return filtered_hooks

    def get_by_url(self, url, max=None):
        """Return list of Hook objects corresponding to the url provided."""
        hooks = self.list(max=max)
        filtered_hooks = [h for h in hooks if h.targetUrl == url]
        return filtered_hooks

    def create(self, name, url, resource, event, filt=None, secret=None):
        """Create Spark web hook."""
        payload = {'name': name,
                   'targetUrl': url,
                   'resource': resource,
                   'event': event,
                   'filter': filt,
                   'secret': secret}

        data = self.session.post(self.url, payload=payload)
        return self.DataClass(data.json())

    def update(self, id, name=None, url=None, secret=None):
        """
        Update existing web hook.
        Both name and targetUrl are required. For convenience,
        if one is not provided, it will be set to the existing value
        """
        existing = self.get_by_id(id)
        if not name:
            name = existing.name
        if not url:
            url = existing.targetUrl
        if secret is None:
            secret = existing.secret

        payload = {'name': name, 'targetUrl': url, 'secret': secret}
        data = self.session.put(self.url, id=id, payload=payload)
        return self.DataClass(data.json())

    def event(self, data):
        try:
            return HookEvent(data)
        except Exception as e:
            print(f"HookEvent Error: {e}")
            print(data)
            return None

    def update_or_create(self, name, url, secret, resource='all', event='all', filt=None):
        existing = self.get_by_name(name)
        if existing:
            return self.update(existing[0].id, name, url, secret)
        else:
            return self.create(name, url, resource, event, filt, secret)
