from drf_spectacular.extensions import OpenApiAuthenticationExtension

from authentication.adapters.django.jwt_authentication import JWTAuthentication


# For Swagger UI
class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = JWTAuthentication
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer <token>'",
        }
