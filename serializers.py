from .models import BlastResult, BlastJob
from rest_framework import serializers

class BlastResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlastResult
        fields = ('sequence','result_no', 'sstart', 'send', 'sstrand', 'evalue', 'pident')


class BlastJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlastJob
        fields = (
            "query",
        )