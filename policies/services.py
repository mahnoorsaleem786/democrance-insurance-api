"""Business logic for insurance quote calculations."""

from datetime import date


class QuoteService:
    """Calculates premiums and cover amounts based on customer age."""

    @staticmethod
    def calculate_age(dob):
        """Return the customer's age in full years as of today."""

        today = date.today()

        return (
            today.year
            - dob.year
            - (
                (today.month, today.day)
                < (dob.month, dob.day)
            )
        )

    @staticmethod
    def calculate_quote(customer):
        """Return premium and cover values for the given customer."""

        age = QuoteService.calculate_age(customer.dob)

        if age < 25:
            premium = 150
            cover = 100000

        elif age <= 40:
            premium = 200
            cover = 200000

        else:
            premium = 300
            cover = 250000

        return {
            "premium": premium,
            "cover": cover,
        }
