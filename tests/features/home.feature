Feature: Home

    Scenario Outline: Vagas
        Given I load the website
        When I go to "/" page
        Then Capture vacancies city "<string>"
        Examples:
            | string                 |
            | São Paulo |

