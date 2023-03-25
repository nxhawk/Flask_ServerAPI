from mongoengine import*
import datetime
# from models.users import User


class Post(Document):
    meta = {'collection': 'post'}
    post_name = StringField(required=True, unique=False, max_length=150)
    link_image = StringField(
        default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPXCOw4Iwzfo6Kd2vsz95hCPNF1OMuDohbgargaCciDA&s")
    description = StringField(required=True, unique=False)
    active = BooleanField(required=True, default=True, unique=False)
    # admin = ReferenceField(User, require=True)
    created_time = DateTimeField(
        default=datetime.datetime.utcnow, unique=False)
    updated_time = DateTimeField(
        default=datetime.datetime.utcnow, unique=False)

    def save(self, *args, **kwargs):
        if not self.created_time:
            self.created_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()
        return super(Post, self).save(*args, **kwargs)
