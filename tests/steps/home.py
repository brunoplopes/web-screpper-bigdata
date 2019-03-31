from behave import given, when, then
from pages.home import home


@then(u'Capture vacancies city "{city}"')
def capture_vacancies(context, city):
    home.capture_vacancies(city)
