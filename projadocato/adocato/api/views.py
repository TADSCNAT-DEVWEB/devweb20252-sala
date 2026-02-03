from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from adocato.services.racaservice import RacaService
from adocato.api.serializers import RacaSerializer


class RacaListCreateAPIView(APIView):
    """
    View para listar todas as raças ou criar uma nova raça.
    GET /api/racas/ - Lista todas as raças
    GET /api/racas/?nome=termo - Busca raças por nome
    POST /api/racas/ - Cria uma nova raça
    """
    
    @swagger_auto_schema(
        operation_description="Lista todas as raças ou busca por nome",
        manual_parameters=[
            openapi.Parameter(
                'nome',
                openapi.IN_QUERY,
                description="Termo para buscar raças por nome",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={200: RacaSerializer(many=True)}
    )
    def get(self, request):
        nome = request.query_params.get('nome', None)
        if nome:
            racas = RacaService.buscar_racas(nome=nome)
        else:
            racas = RacaService.listar_racas()
        
        serializer = RacaSerializer(racas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Cria uma nova raça",
        request_body=RacaSerializer,
        responses={
            201: RacaSerializer(),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = RacaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                raca = RacaService.cadastrar_raca(
                    nome=serializer.validated_data['nome']
                )
                response_serializer = RacaSerializer(raca)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.message_dict},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RacaRetrieveUpdateDestroyAPIView(APIView):
    """
    View para obter, atualizar ou excluir uma raça específica.
    GET /api/racas/{id}/ - Obtém os detalhes de uma raça
    PUT /api/racas/{id}/ - Atualiza uma raça completamente
    PATCH /api/racas/{id}/ - Atualiza uma raça parcialmente
    DELETE /api/racas/{id}/ - Exclui uma raça
    """
    
    @swagger_auto_schema(
        operation_description="Obtém os detalhes de uma raça específica",
        responses={
            200: RacaSerializer(),
            404: 'Raça não encontrada'
        }
    )
    def get(self, request, pk):
        raca = RacaService.obter_raca_por_id(pk)
        if not raca:
            return Response(
                {'error': 'Raça não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RacaSerializer(raca)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Atualiza completamente uma raça",
        request_body=RacaSerializer,
        responses={
            200: RacaSerializer(),
            400: 'Bad Request',
            404: 'Raça não encontrada'
        }
    )
    def put(self, request, pk):
        raca = RacaService.obter_raca_por_id(pk)
        if not raca:
            return Response(
                {'error': 'Raça não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RacaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                raca_atualizada = RacaService.atualizar_raca(
                    raca_id=pk,
                    nome=serializer.validated_data['nome']
                )
                response_serializer = RacaSerializer(raca_atualizada)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.message_dict},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Atualiza parcialmente uma raça",
        request_body=RacaSerializer,
        responses={
            200: RacaSerializer(),
            400: 'Bad Request',
            404: 'Raça não encontrada'
        }
    )
    def patch(self, request, pk):
        raca = RacaService.obter_raca_por_id(pk)
        if not raca:
            return Response(
                {'error': 'Raça não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RacaSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                nome = serializer.validated_data.get('nome', None)
                raca_atualizada = RacaService.atualizar_raca(
                    raca_id=pk,
                    nome=nome
                )
                response_serializer = RacaSerializer(raca_atualizada)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.message_dict},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Exclui uma raça",
        responses={
            204: 'Raça excluída com sucesso',
            404: 'Raça não encontrada'
        }
    )
    def delete(self, request, pk):
        sucesso = RacaService.excluir_raca(pk)
        if not sucesso:
            return Response(
                {'error': 'Raça não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
