from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.serializers import (
        CharField,
        EmailField,
        HyperlinkedIdentityField,
        ModelSerializer,
        SerializerMethodField,
        ValidationError,
        )

from rest_framework_jwt.settings import api_settings
#from rest_framework.authtoken.models import Token


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserCreateSerializer(ModelSerializer):

    # Por padrão, o django aceita o campo 'email' com o valor vazio,
    # atribuir o objeto 'EmailField' a variável 'email', sobrescrever o campo
    # faz com que não seja aceito o campo vazio
    email = EmailField(label='Emdereço de email')

    email2 = EmailField(label='Confirme o email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]

        # Faz com que a senha não incluida no JSON retornado para exibição
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    # Por padrão, o django valida somente o 'username' para evitar duplicidade
    def validate(self, data):
    #     email = data['email']
    #     user_qs = User.objects.filter(email=email)
    #     if user_qs.exists():
    #         raise ValidationError("Esse endereço de email já está registrado.")
     return data

    # Duas funções para retornar o aviso de erro nos dois campos de email

    def validate_email(self, value):
        data = self.get_initial()
        email1 = value
        email2 = data.get("email2")

        if email1 != email2:
            raise ValidationError("Os endereços de email precisam ser iguais.")

        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError("Esse endereço de email já está registrado.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value

        if email2 != email1:
            raise ValidationError("Os endereços de email precisam ser iguais.")

        return value

    # Sobrescreve o método 'create' para implementar a validação da
    # senha, do contrário, a senha o usuário não será criptografada e o
    # django não aceitara como uma senha válida, o usuário ainda será
    # criado, mas não será possível fazer o login na conta.
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        user_obj = User(
                username = username,
                email = email,
                )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data


class UserLoginSerializer(ModelSerializer):

    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'token',
            'username',
            'password',
        ]

        # Faz com que a senha não incluida no JSON retornado para exibição
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, data):
        user_obj = None
        username_or_email = data.get('username', None)
        password = data['password']
        if not username_or_email:
            raise ValidationError('É necessário inserir um nome de usuário ou endereço de email.')

        user = User.objects.filter(
                Q(email=username_or_email) |
                Q(username=username_or_email)
                ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')

        # Também poderia ser dessa forma:
        # username = User.objects.filter(username_icontains=username_or_email)
        # email = User.objects.filter(email_icontains=username_or_email)
        # user = (username | email).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('Esse usuário/email não é válido.')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Usuário/email ou senha inválidos.')

            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            data['token'] = token
            data['username'] = user_obj.username

        return data
