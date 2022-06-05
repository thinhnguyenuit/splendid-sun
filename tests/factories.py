import factory.fuzzy
from factory.alchemy import SQLAlchemyModelFactory

from app import models
from app.extensions import db


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = db.session

    username = factory.faker.Faker("name")
    email = factory.faker.Faker("email")
    password = "testpassword"
    # posts = factory.SubFactory(PostFactory)


class BlogPostFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BlogPost
        sqlalchemy_session = db.session

    user = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText(length=20)
    content = factory.fuzzy.FuzzyText(length=100)
