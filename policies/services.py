from datetime import date


class QuoteService:

    @staticmethod
    def calculate_age(dob):
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