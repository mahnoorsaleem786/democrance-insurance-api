"""Business logic for insurance quote calculations."""

from datetime import date
from typing import Any

from customers.models import Customer


class QuoteService:
    """Calculate insurance premiums and cover amounts."""

    @staticmethod
    def calculate_age(dob: date) -> int:
        """Return the customer's age in completed years."""

        today = date.today()

        return (
            today.year
            - dob.year
            - ((today.month, today.day) < (dob.month, dob.day))
        )

    @staticmethod
    def calculate_quote(customer: Customer) -> dict[str, Any]:
        """Return the calculated premium and cover for a customer."""

        age = QuoteService.calculate_age(customer.dob)

        if age < 25:
            return {
                "premium": 150,
                "cover": 100000,
            }

        if age <= 40:
            return {
                "premium": 200,
                "cover": 200000,
            }

        return {
            "premium": 300,
            "cover": 250000,
        }