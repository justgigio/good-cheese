import factory
from src.models import Boleto

from tests.factories.boleto_file_factory import BoletoFileFactory


class BoletoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Boleto

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name', locale='pt_BR')
    government_id = factory.Faker('rg', locale='pt_BR')
    email = factory.Faker('email', locale='pt_BR')
    debt_amount = factory.Faker('random_int', min=5000, max=1000000)
    debt_due_date = factory.Faker('date_time_between', start_date='-3m', end_date='+20d')
    debt_id = factory.Faker('uuid4')
    processed_at = None

    boleto_file = factory.SubFactory(BoletoFileFactory)
