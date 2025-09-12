from mongoengine import Document, StringField, IntField, DateTimeField

class Review(Document):
    id = IntField(primary_key=True)
    ride_id = IntField(required=True)
    user_id = IntField(required=True)
    driver_id = IntField(required=True)
    rating = IntField(max_value=5,required=True)
    comment = StringField(max_length=200)
    created_at = DateTimeField()

    meta = {
    'collection': 'review'
    }
