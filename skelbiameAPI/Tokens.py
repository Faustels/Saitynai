from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from Saitynai.settings import SECRET_KEY, SIMPLE_JWT
import jwt
from jwt.exceptions import ExpiredSignatureError

class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role.role

        return token


def TokenUser(token):
    if token is None:
        return None
    try:
        valid_data = jwt.decode(token, SECRET_KEY, SIMPLE_JWT["ALGORITHM"])
        user = valid_data['user_id']
        return user
    except:
        return None
    return None

def TokenCanEdit(token, requiredUser):
    if token is None:
        return False
    try:
        valid_data = jwt.decode(token, SECRET_KEY, SIMPLE_JWT["ALGORITHM"])
        role = valid_data["role"]
        if role == "admin":
            return True
        user = valid_data['user_id']
        if user == requiredUser:
            return True
    except:
        return False
    return False

def TokenIsAdmin(token):
    if token is None:
        return False
    try:
        valid_data = jwt.decode(token, SECRET_KEY, SIMPLE_JWT["ALGORITHM"])
        role = valid_data["role"]
        if role == "admin":
            return True
    except:
        return False
    return False

def ToPureToken(token):
    if token is None:
        return None
    prefix = "Bearer "
    if not token.startswith(prefix):
        return None
    return token[len(prefix):]
