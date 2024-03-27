from datetime import timedelta

from factory import Factory, Faker, SubFactory
from services.models import Subscription, Tariff, Transaction, UserTariff
from users.models import User


class UserFactory(Factory):
    class Meta:
        model = User

    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    father_name = Faker('first_name_male')
    phone_number = Faker('phone_number')


class SubscriptionFactory(Factory):
    class Meta:
        model = Subscription

    name = Faker('name')
    description = Faker('text')
    usage_policy = Faker('text')


class TariffFactory(Factory):
    class Meta:
        model = Tariff

    name = Faker('name')
    subscription = SubFactory(SubscriptionFactory)
    description = Faker('text')
    duration = timedelta(days=0)
    price = Faker('pydecimal', left_digits=10, right_digits=2)
    test_period = Faker('time_delta')
    test_price = Faker('pydecimal', left_digits=10, right_digits=2)
    cashback = Faker('pydecimal', left_digits=10, right_digits=2)
    cashback_conditions = Faker('text')


class UserTariffFactory(Factory):
    class Meta:
        model = UserTariff

    user = SubFactory(UserFactory)
    tariff = SubFactory(TariffFactory)
    start_date = Faker('date')
    end_date = Faker('date')
    is_direct = Faker('boolean')
    auto_renewal = Faker('boolean')


class TransactionFactory(Factory):
    class Meta:
        model = Transaction

    user_tariff = SubFactory(UserTariffFactory)
    date = Faker('date')
    amount = Faker('pydecimal', left_digits=10, right_digits=2)
    payment_status = Faker('random_element', elements=[0, 1, 2])
