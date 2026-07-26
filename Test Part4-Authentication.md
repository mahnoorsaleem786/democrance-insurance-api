# Part 4 –  Discuss how you would implement authentication for users/customers, and would these be the same or different?

## Authentication Strategy

For this coding assessment, JWT (JSON Web Token) authentication is used to secure protected API endpoints. JWT provides a stateless authentication mechanism, making it suitable for REST APIs and scalable distributed systems.

The application exposes public endpoints for customer onboarding, while all policy-related operations require a valid JWT access token.

---

## Users vs Customers

Although both users and customers authenticate using the same JWT mechanism, they represent different actors in the system and therefore should have different authorization rules.

### Customers
Customers are external users of the insurance platform.

They should be able to:
- Register and log in.
- Create insurance quotes.
- Accept their own quotes.
- View only their own policies.
- Update their own profile.

Customers should **not** have access to the Django Admin interface or other customers' data.

### Internal Users (Staff/Admin)

Internal users represent Democrance employees such as administrators, operations staff, or underwriters.

They should be able to:
- Access Django Admin.
- View all customers.
- View and manage all policies.
- Search across all customers and policies.
- Perform administrative tasks.

---

## Authentication Implementation

The current implementation uses:

- Django Authentication System
- Django REST Framework
- SimpleJWT

Protected endpoints require a valid JWT access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

Customer creation is intentionally left public to simulate a customer onboarding process.

Policy creation, policy activation, policy history, and search endpoints require authentication.

---

## Recommended Production Design

For a production system, I would associate every customer with Django's built-in `User` model using a `OneToOneField`.

Example:

```python
class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
```

This approach separates authentication information from business data while leveraging Django's secure authentication framework.

---

## Authorization

Authentication verifies **who the user is**, while authorization determines **what the user is allowed to do**.

Role-based permissions should be implemented to distinguish between customers and internal users.

Examples:

- Customers can only access their own policies.
- Staff users can access all policies.
- Only staff users can access Django Admin.

Object-level permission checks should ensure that customers cannot retrieve or modify another customer's data.

---

## Security Considerations

The current solution follows several security best practices:

- JWT authentication for protected APIs.
- Django ORM to prevent SQL injection.
- Serializer validation for all incoming requests.
- Environment variables for secrets and database credentials.
- Database transactions to maintain consistency during write operations.
- Proper HTTP status codes and error handling.

---

## Future Enhancements

For a production-ready insurance platform, I would additionally implement:

- Role-Based Access Control (RBAC).
- Email verification during registration.
- Password reset functionality.
- Multi-Factor Authentication (MFA) for staff users.
- Token rotation and revocation.
- API rate limiting.
- Audit logging for authentication and policy changes.

---

## Conclusion

Both customers and internal users can use the same JWT authentication mechanism, but they should not share the same authorization model.

Authentication should remain centralized using Django's authentication framework, while permissions should be separated using roles and object-level access control. This approach provides a secure, scalable, and maintainable authentication architecture suitable for enterprise insurance applications.