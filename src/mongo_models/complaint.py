from mongoengine import Document, StringField, IntField, DateTimeField

class complaint(Document):
    id = IntField(primary_key=True)
    user_id = IntField(required=True)
    driver_id = IntField(required=True)
    reasons = StringField(max_length=256)
    created_at = DateTimeField()

    meta = {
    'collection': 'complaint'
    }

