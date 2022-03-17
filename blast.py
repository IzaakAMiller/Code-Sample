from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import no_body, swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from ..serializers import BlastResultSerializer, BlastJobSerializer

from ..models import BlastResult, BlastJob
from ..helpers.blast_mgr import BlastMgr


class BlastViewSet(ViewSet):
    queryset = BlastResult.objects.all()
    lookup_field = "sequence"
    lookup_field_regex = '^[CAGTcagt]+$'
    serializer_class = BlastResultSerializer

    @swagger_auto_schema(
        operation_description=(
                "Retrieves a Blast Result"
        ),
        tags=["BlastResults"],
        manual_parameter=["sequence"],
        responses={
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                "Failed. Not authenticated",
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                "Failed. Not Blast result not found",
            ),
            status.HTTP_200_OK: openapi.Response(
                "Successfully retrieved blast result",
                BlastResultSerializer,
            ),
        },
    )
    def retrieve(self, request, sequence):
        try:
            blast_result = BlastResult.objects.get(sequence=sequence)
            serializer = BlastResultSerializer(blast_result)

            blast_result_data = serializer.data
            return Response({"blast_result": blast_result_data})

        except:
            return Response(f"Blast result does not exist with sequence {sequence}", status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description=(
                "Retrieves a Blast Result"
        ),
        tags=["BlastResults"],
        responses={
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                "Failed. Not authenticated",
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                "Failed. Not Blast result not found",
            ),
            status.HTTP_200_OK: openapi.Response(
                "Successfully retrieved blast result",
                BlastResultSerializer,
            ),
        },
    )
    def list(self, request):
        BlastResults = BlastResult.objects.all().values_list("blast_job", flat=True)
        response = Response(
            {
                "blast_results": [sequence for sequence in BlastResults],
            }
        )
        return response

    @swagger_auto_schema(
        operation_description=(
                "Runs Blast against a dna sequence"
        ),
        tags=["Blast"],
        manual_parameter=["sequence"],
        request_body=BlastJobSerializer,
        responses={
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                "Failed. Not authenticated",
            ),
            status.HTTP_200_OK: openapi.Response(
                "Successfully retrieved Blast result",
                BlastResultSerializer,
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        # Get query from request
        query = request.data["query"]
        blast_job = BlastJob(query=query)

        result, status_code = BlastMgr().run_blast(query)
        blast_result = BlastResult(blast_job=blast_job, result_no=result['result_no'], sstart=result['sstart'],
                                   send=result['send'], sstrand=result['sstrand'], evalue=result['evalue'],
                                   pident=result['pident'], sequence=result['sequence'])

