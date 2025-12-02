from django.db import transaction
from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from AppCore.core.exceptions.exceptions import SystemErrorException, NotFoundException
from AppCore.basics.decorators.decorators import handle_exceptions

from AppCore.common.textos.mensagens import RESPONSE_ALGUM_DADO_NAO_FOI_ENCONTRADO


class BasicPostAPIView(GenericAPIView):
    http_method_names = ['post']
    mensagem_sucesso = ''
    
    def do_action_post(self, serializer, request):
        raise SystemErrorException("Este método não foi implementado.")

    @handle_exceptions
    def post(self, request, *args, **kwargs):
        serializer_object = self.get_serializer(data=request.data)
        serializer_object.is_valid(raise_exception=True)
        serializer_data = serializer_object.validated_data

        resultado = {}

        with transaction.atomic():
            try:
                sid = transaction.savepoint()
                resultado = self.do_action_post(serializer_data, request)
            except Exception as e:
                transaction.savepoint_rollback(sid)
                raise e
        
            transaction.savepoint_commit(sid)

        data = {'status': 'success'}
        
        if not resultado: resultado = {}
        
        if not resultado.get('mensagem'):
            resultado['mensagem'] = self.mensagem_sucesso
        
        data['mensagem'] = resultado.get('mensagem', 'Sucesso')

        return Response(
            data, status=resultado.get('status_code', status.HTTP_200_OK)
        )


class BasicGetAPIView(GenericAPIView):
    http_method_names = ['get']
    mensagem_sucesso = ''
    
    def validate_get(self, request, *args, **kwargs):
        pass

    @handle_exceptions
    def get(self, request, *args, **kwargs):
        self.validate_get(request, *args, **kwargs)
        
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            
            data = {
                'status': 'success',
                'mensagem': self.mensagem_sucesso or 'Sucesso',
                'count': paginated_response.data.get('count'),
                'next': paginated_response.data.get('next'),
                'previous': paginated_response.data.get('previous'),
                'dados': paginated_response.data.get('results'),
            }
            return Response(data, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        
        data = {
            'status': 'success',
            'mensagem': self.mensagem_sucesso or 'Sucesso',
            'dados': serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)


class BasicDeleteAPIView(GenericAPIView):
    http_method_names = ['delete']
    mensagem_sucesso = ''

    def do_action_delete(self, instance, request):
        raise SystemErrorException("Este método não foi implementado.")

    @handle_exceptions
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            raise NotFoundException(RESPONSE_ALGUM_DADO_NAO_FOI_ENCONTRADO)

        with transaction.atomic():
            try:
                sid = transaction.savepoint()
                self.do_action_delete(instance, request)
            except Exception as e:
                transaction.savepoint_rollback(sid)
                raise e
        
            transaction.savepoint_commit(sid)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class BasicPutAPIView(GenericAPIView):
    http_method_names = ['put']
    mensagem_sucesso = ''

    def do_action_put(self, instance, serializer_data, request):
        raise SystemErrorException("Este método não foi implementado.")

    @handle_exceptions
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            raise NotFoundException(RESPONSE_ALGUM_DADO_NAO_FOI_ENCONTRADO)

        serializer_object = self.get_serializer(data=request.data)
        serializer_object.is_valid(raise_exception=True)
        serializer_data = serializer_object.validated_data

        resultado = {}

        with transaction.atomic():
            try:
                sid = transaction.savepoint()
                resultado = self.do_action_put(instance, serializer_data, request)
            except Exception as e:
                transaction.savepoint_rollback(sid)
                raise e
        
            transaction.savepoint_commit(sid)

        data = {'status': 'success'}
        
        if not resultado: resultado = {}
        
        if not resultado.get('mensagem'):
            resultado['mensagem'] = self.mensagem_sucesso
        
        data['mensagem'] = resultado.get('mensagem', 'Sucesso')

        return Response(
            data, status=resultado.get('status_code', status.HTTP_200_OK)
        )

class BasicRetrieveAPIView(GenericAPIView):
    http_method_names = ['get']
    mensagem_sucesso = ''
    
    def validate_retrieve(self, request, *args, **kwargs):
        pass

    @handle_exceptions
    def get(self, request, *args, **kwargs):
        self.validate_retrieve(request, *args, **kwargs)
        
        try:
            instance = self.get_object()
        except Http404:
            raise NotFoundException(RESPONSE_ALGUM_DADO_NAO_FOI_ENCONTRADO)

        serializer = self.get_serializer(instance)

        data = {'status': 'success'}
        
        resultado = {}
        
        resultado['mensagem'] = self.mensagem_sucesso
        
        data['mensagem'] = resultado.get('mensagem', 'Sucesso')
        
        data['dados'] = serializer.data

        return Response(
            data, status=resultado.get('status_code', status.HTTP_200_OK)
        )
