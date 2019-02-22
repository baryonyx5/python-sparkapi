"""Spark Message Class."""

from .spark_class import SparkDataClass, SparkAPI


class Message(SparkDataClass):
    def __init__(self, data, whitelist=(), blacklist=()):
        self.id = data.pop('id')
        self.roomId = data.pop('roomId')
        self.roomType = data.pop('roomType', '')
        self.personId = data.pop('personId', '')
        self.personEmail = data.pop('personEmail', '')
        self.toPersonId = data.pop('toPersonId', '')
        self.toPersonEmail = data.pop('toPersonEmail', '')
        self.text = data.pop('text', '') if 'text' not in blacklist else ''
        self.files = data.pop('files', []) if 'files' not in blacklist else ''
        self.mentionedPeople = self.decode_list(data.pop('mentionedPeople', []))
        self.created = self.set_datetime(data.pop('created'))
        super().__init__(data, whitelist, blacklist)

    def __str__(self):
        return 'Spark Message ({})'.format(self.id)


# noinspection PyShadowingBuiltins
class Messages(SparkAPI):

    DataClass = Message

    def get_by_room(self, roomId, mentionedPeople=None,
                    before=None, beforeMessage=None, max=None,
                    blacklist=(), whitelist=()):

        return self.list(roomId=roomId,
                         mentionedPeople=mentionedPeople,
                         before=before,
                         beforeMessage=beforeMessage,
                         max=max,
                         blacklist=blacklist,
                         whitelist=whitelist)

    def get_message(self, id, blacklist=(), whitelist=()):
        return self.get_by_id(id, blacklist, whitelist)

    def send_to_room(self, roomId, text, files=None, markdown=False):

        payload = {'roomId': roomId}
        if markdown:
            payload['markdown'] = text
        else:
            payload['text'] = text
        if files:
            payload['files'] = files

        data = self.session.post(self.url, payload=payload)
        return self.DataClass(data.json())

    def send_to_person(self, text, toPersonId=None, toPersonEmail=None,
                       files=None, markdown=False):
        payload = {}
        if markdown:
            payload['markdown'] = text
        else:
            payload['text'] = text
        if files:
            payload['files'] = files

        payload.update(self._id_or_email([('toPersonId', toPersonId),
                                          ('toPersonEmail', toPersonEmail)]))

        data = self.session.post(self.url, payload=payload)
        return self.DataClass(data.json())
