from typing import Any, Dict

from core.factories import SemesterFactory, UserFactory
from django.utils.timezone import utc
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyDecimal
from factory.helpers import post_generation
from otisweb.tests import UniqueFaker

from .models import Guess, Market


class MarketFactory(DjangoModelFactory):
	class Meta:
		model = Market

	semester = SubFactory(SemesterFactory)
	start_date = Faker('past_datetime', tzinfo=utc)
	end_date = Faker('future_datetime', tzinfo=utc)

	slug = UniqueFaker('slug')
	title = Faker('bs')
	prompt = Faker('paragraph')


class GuessFactory(DjangoModelFactory):
	class Meta:
		model = Guess

	user = SubFactory(UserFactory)
	market = SubFactory(MarketFactory)
	value = FuzzyDecimal(1, 10000)

	@post_generation
	def score(self, create: bool, extracted: Any, **kwargs: Dict[str, Any]):
		self.score = self.get_score()  # type: ignore
