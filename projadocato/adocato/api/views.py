from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from adocato.services.racaservice import RacaService
from adocato.services.gatoservice import GatoService
from adocato.api.serializers import RacaSerializer, GatoSerializer


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


class GatoListCreateAPIView(APIView):
    """
    View para listar todos os gatos ou criar um novo gato.
    GET /api/gatos/ - Lista todos os gatos
    GET /api/gatos/?nome=termo - Busca gatos por nome
    GET /api/gatos/?disponivel=true - Filtra gatos disponíveis
    GET /api/gatos/?raca_id=1 - Filtra gatos por raça
    POST /api/gatos/ - Cria um novo gato
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    @swagger_auto_schema(
        operation_description="Lista todos os gatos ou busca com filtros",
        manual_parameters=[
            openapi.Parameter(
                'nome',
                openapi.IN_QUERY,
                description="Termo para buscar gatos por nome",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'disponivel',
                openapi.IN_QUERY,
                description="Filtra gatos disponíveis (true/false)",
                type=openapi.TYPE_BOOLEAN,
                required=False
            ),
            openapi.Parameter(
                'raca_id',
                openapi.IN_QUERY,
                description="Filtra gatos por ID da raça",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={200: GatoSerializer(many=True)}
    )
    def get(self, request):
        nome = request.query_params.get('nome', None)
        disponivel_param = request.query_params.get('disponivel', None)
        raca_id = request.query_params.get('raca_id', None)
        
        disponivel = None
        if disponivel_param is not None:
            disponivel = disponivel_param.lower() == 'true'
        
        if raca_id:
            gatos = GatoService.listar_gatos_por_raca(raca_id)
        else:
            gatos = GatoService.buscar_gatos(nome=nome, disponivel=disponivel)
        
        serializer = GatoSerializer(gatos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Cria um novo gato",
        request_body=GatoSerializer,
        responses={
            201: GatoSerializer(),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = GatoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                gato = GatoService.cadastrar_gato(
                    nome=serializer.validated_data['nome'],
                    sexo=serializer.validated_data['sexo'],
                    cor=serializer.validated_data['cor'],
                    data_nascimento=serializer.validated_data['data_nascimento'],
                    raca_id=serializer.validated_data['raca_id'],
                    descricao=serializer.validated_data.get('descricao', None),
                    foto=serializer.validated_data.get('foto', None)
                )
                response_serializer = GatoSerializer(gato, context={'request': request})
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.message_dict},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GatoRetrieveUpdateDestroyAPIView(APIView):
    """
    View para obter, atualizar ou excluir um gato específico.
    GET /api/gatos/{id}/ - Obtém os detalhes de um gato
    PUT /api/gatos/{id}/ - Atualiza um gato completamente
    PATCH /api/gatos/{id}/ - Atualiza um gato parcialmente
    DELETE /api/gatos/{id}/ - Exclui um gato
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    @swagger_auto_schema(
        operation_description="Obtém os detalhes de um gato específico",
        responses={
            200: GatoSerializer(),
            404: 'Gato não encontrado'
        }
    )
    def get(self, request, pk):
        gato = GatoService.obter_gato_por_id(pk)
        if not gato:
            return Response(
                {'error': 'Gato não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = GatoSerializer(gato, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Atualiza completamente um gato",
        request_body=GatoSerializer,
        responses={
            200: GatoSerializer(),
            400: 'Bad Request',
            404: 'Gato não encontrado'
        }
    )
    def put(self, request, pk):
        gato = GatoService.obter_gato_por_id(pk)
        if not gato:
            return Response(
                {'error': 'Gato não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = GatoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                gato_atualizado = GatoService.atualizar_gato(
                    gato_id=pk,
                    nome=serializer.validated_data['nome'],
                    sexo=serializer.validated_data['sexo'],
                    cor=serializer.validated_data['cor'],
                    data_nascimento=serializer.validated_data['data_nascimento'],
                    raca_id=serializer.validated_data['raca_id'],
                    descricao=serializer.validated_data.get('descricao', None),
                    foto=serializer.validated_data.get('foto', None),
                    disponivel=serializer.validated_data.get('disponivel', True)
                )
                response_serializer = GatoSerializer(gato_atualizado, context={'request': request})
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.message_dict},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um gato",
        request_body=GatoSerializer,
        responses={
            200: GatoSerializer(),
            400: 'Bad Request',
            404: 'Gato não encontrado'
        }
    )
    def patch(self, request, pk):
        gato = GatoService.obter_gato_por_id(pk)
        if not gato:
            return Response(
                {'error': 'Gato não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = GatoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                gato_atualizado = GatoService.atualizar_gato(
                    gato_id=pk,
                    nome=serializer.validated_data.get('nome', None),
                    sexo=serializer.validated_data.get('sexo', None),
                    cor=serializer.validated_data.get('cor', None),
                    data_nascimento=serializer.validated_data.get('data_nascimento', None),
                    raca_id=serializer.validated_data.get('raca_id', None),
                    descricao=serializer.validated_data.get('descricao', None),
                    foto=serializer.validated_data.get('foto', None),
                    disponivel=serializer.validated_data.get('disponivel', None)
                )
                response_serializer = GatoSerializer(gato_atualizado, context={'request': request})
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(
                    {'errors': e.message_dict},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Exclui um gato",
        responses={
            204: 'Gato excluído com sucesso',
            404: 'Gato não encontrado'
        }
    )
    def delete(self, request, pk):
        sucesso = GatoService.excluir_gato(pk)
        if not sucesso:
            return Response(
                {'error': 'Gato não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
