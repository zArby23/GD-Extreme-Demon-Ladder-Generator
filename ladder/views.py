from datetime import timedelta

from django.conf import settings
from django.db import DatabaseError, connection, transaction
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gd_extreme_demon_ladder_generator.api.aredl_client import AREDLClientError
from ladder.models import LadderGeneration
from ladder.serializers import (
    LadderGenerationSerializer,
    LadderHistorySerializer,
    LadderRequestSerializer,
)
from ladder.services import generate_ladder


def _ensure_session(request) -> str:
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _history_queryset(request):
    return LadderGeneration.objects.filter(
        session_key=_ensure_session(request)
    )


def _positive_query_int(request, name: str, default: int) -> int:
    raw_value = request.query_params.get(name)
    if raw_value is None:
        return default
    try:
        return max(int(raw_value), 1)
    except ValueError:
        return default


@ensure_csrf_cookie
def csrf_token(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"detail": "CSRF cookie is ready."})


def health_check(request: HttpRequest) -> JsonResponse:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "unhealthy"}, status=503)
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_protect, name="dispatch")
class LadderListCreateView(APIView):
    def get(self, request):
        generations = _history_queryset(request)
        page_size = min(_positive_query_int(request, "page_size", 20), 50)
        page = _positive_query_int(request, "page", 1)
        start = (page - 1) * page_size
        end = start + page_size
        total = generations.count()
        page_items = list(generations[start:end])
        payload = {
            "results": LadderGenerationSerializer(page_items, many=True).data,
            "count": total,
            "next": page + 1 if end < total else None,
            "previous": page - 1 if page > 1 and start < total else None,
        }
        return Response(LadderHistorySerializer(payload).data)

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
        _trim_history(generation.session_key)
        return Response(
            LadderGenerationSerializer(generation).data,
            status=status.HTTP_201_CREATED,
        )


class LadderHistoryView(APIView):
    def get(self, request):
        return LadderListCreateView().get(request)


def _trim_history(session_key: str) -> None:
    queryset = LadderGeneration.objects.filter(session_key=session_key)
    retention_days = settings.HISTORY_RETENTION_DAYS
    if retention_days > 0:
        cutoff = timezone.now() - timedelta(days=retention_days)
        queryset.filter(created_at__lt=cutoff).delete()

    max_records = max(settings.HISTORY_MAX_PER_SESSION, 1)
    stale_ids = queryset.values_list("id", flat=True)[max_records:]
    LadderGeneration.objects.filter(id__in=stale_ids).delete()
