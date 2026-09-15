from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gd_extreme_demon_ladder_generator.api.aredl_client import AREDLClientError
from ladder.models import LadderGeneration
from ladder.serializers import LadderGenerationSerializer, LadderRequestSerializer
from ladder.services import generate_ladder


def _ensure_session(request) -> str:
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


class LadderListCreateView(APIView):
    def get(self, request):
        generations = LadderGeneration.objects.filter(
            session_key=_ensure_session(request)
        )
        return Response(LadderGenerationSerializer(generations, many=True).data)

    @transaction.atomic
    def post(self, request):
        serializer = LadderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result, warnings = generate_ladder(**serializer.validated_data)
        except LookupError as error:
            return Response({"detail": str(error)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except AREDLClientError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        generation = LadderGeneration.objects.create(
            session_key=_ensure_session(request),
            result=result,
            warnings=warnings,
            **serializer.validated_data,
        )
        return Response(
            LadderGenerationSerializer(generation).data,
            status=status.HTTP_201_CREATED,
        )


class LadderHistoryView(APIView):
    def get(self, request):
        generations = LadderGeneration.objects.filter(
            session_key=_ensure_session(request)
        )
        return Response(LadderGenerationSerializer(generations, many=True).data)
