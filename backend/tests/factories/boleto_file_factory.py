import factory
from src.models import BoletoFile


class BoletoFileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BoletoFile

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('file_name', extension='csv')
    checksum = factory.Faker('md5')
    size = factory.Faker('random_int', min=10000, max=10000000)
    uploaded_at = factory.Faker('past_datetime')
