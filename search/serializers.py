from rest_framework import serializers
from .models import *

class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyList
        fields = ['id', 'name']


class NewsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsData
        fields = ['SENTIMENT_CHOICES', 'id', 'comp', ' title', 'link', 'date', 'sentiment', 'confidence']
