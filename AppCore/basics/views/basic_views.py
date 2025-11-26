from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.db import transaction
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from AppCore.core.exceptions.exceptions import (
    BusinessRuleException, SystemErrorException, ValidationException, AuthorizationException, NotFoundException
)

from AppCore.common.texts.messages import (
    RESPONSE_TENTE_NOVAMENTE, RESPONSE_ALGO_QUE_MANDOU_ESTA_ERRADO, RESPONSE_VOCE_NAO_PODE_FAZER_ISSO,
    RESPONSE_VOCE_NAO_PODE_FAZER_ISSO, RESPONSE_ALGUM_DADO_NAO_FOI_ENCONTRADO
)


class BasicPostAPIView(GenericAPIView):
    http_method_names = ['post']
    success_message = ''
    
    def do_action_post(self, serializer, request):
        raise SystemErrorException("Este método não foi implementado.")

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data

        try:
            with transaction.atomic():
                try:
                    sid = transaction.savepoint()
                    result = self.do_action_post(serializer, request)
                except Exception as e:
                    transaction.savepoint_rollback(sid)
                    raise e
            
                transaction.savepoint_commit(sid)

            data = {'status': 'success'}
            
            if not result: result = {}
            
            if not result.get('message'):
                result['message'] = self.success_message
            
            data['message'] = result.get('message', 'Success') if result else 'Success'

            return Response(
                data, status=result.get('status_code', status.HTTP_200_OK)
            )
        except BusinessRuleException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_TENTE_NOVAMENTE}, status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_ALGO_QUE_MANDOU_ESTA_ERRADO}, status=status.HTTP_400_BAD_REQUEST
            )
        except AuthorizationException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_VOCE_NAO_PODE_FAZER_ISSO}, status=status.HTTP_403_FORBIDDEN
            )
        except NotFoundException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_ALGUM_DADO_NAO_FOI_ENCONTRADO}, status=status.HTTP_404_NOT_FOUND
            )
        except SystemErrorException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_VOCE_NAO_PODE_FAZER_ISSO}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as err:
            return Response(
                {'status': 'error', 'detail': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class BasicGetAPIView(GenericAPIView):
    http_method_names = ['get']
    success_message = ''
    
    def validate_get(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        try:
            self.validate_get(request, *args, **kwargs)

            data = {'status': 'success'}
            
            if not result: result = {}
            
            if not result.get('message'):
                result['message'] = self.success_message
            
            data['message'] = result.get('message', 'Success') if result else 'Success'

            return Response(
                data, status=result.get('status_code', status.HTTP_200_OK)
            )
        except BusinessRuleException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_TENTE_NOVAMENTE}, status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_ALGO_QUE_MANDOU_ESTA_ERRADO}, status=status.HTTP_400_BAD_REQUEST
            )
        except AuthorizationException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_VOCE_NAO_PODE_FAZER_ISSO}, status=status.HTTP_403_FORBIDDEN
            )
        except SystemErrorException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_VOCE_NAO_PODE_FAZER_ISSO}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except NotFoundException as err:
            return Response(
                {'status': 'error', 'detail': str(err) or RESPONSE_ALGUM_DADO_NAO_FOI_ENCONTRADO}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as err:
            return Response(
                {'status': 'error', 'detail': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )