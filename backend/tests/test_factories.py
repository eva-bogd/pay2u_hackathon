import factory.fuzzy
from factory import Faker, SubFactory
from services.models import Subscription, Tariff, Transaction, UserTariff
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    father_name = Faker('first_name_male')
    phone_number = Faker('phone_number')
    username = Faker('user_name')
    password = Faker('password')


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    name = Faker('name')
    description = Faker('text')
    partner_rules = Faker('text')
    personal_data_policy = Faker('text')


class TariffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tariff

    name = Faker('name')
    subscription = SubFactory(SubscriptionFactory)
    description = Faker('text')
    period = Faker('random_element', elements=[1, 3, 6, 12])
    price = Faker('pydecimal', left_digits=5, right_digits=2)
    test_period = Faker('random_element', elements=[1, 3, 6])
    test_price = Faker('pydecimal', left_digits=5, right_digits=2)
    cashback = Faker('random_int', min=1, max=100)
    cashback_conditions = Faker('text')


class UserTariffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserTariff

    user = SubFactory(UserFactory)
    tariff = SubFactory(TariffFactory)
    start_date = Faker('date')
    end_date = Faker('date')
    is_direct = Faker('boolean')
    auto_renewal = Faker('boolean')
    promo_code = Faker('text', max_nb_chars=10)
    promo_code_period = Faker('date')


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user_tariff = SubFactory(UserTariffFactory)
    date = Faker('date')
    cashback = Faker('random_int', min=1, max=20)
    amount = Faker('pydecimal', left_digits=5, right_digits=2)
    payment_status = 1
