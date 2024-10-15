from django.db import models

# Create your models here.

class CorData(models.Model):
    cor_id = models.AutoField(primary_key=True)
    cor_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Cor_data'
        verbose_name = '기업 테이블'
        verbose_name_plural = '기업 테이블'

class NewsData(models.Model):
    news_id = models.AutoField(primary_key=True)
    cor = models.ForeignKey(CorData, on_delete=models.CASCADE)
    news_title = models.CharField(max_length=200)
    news_link = models.CharField(max_length=200)
    datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'News_data'
        verbose_name = '데이터 테이블'
        verbose_name_plural = '데이터 테이블'

class SentimentData(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]

    news = models.ForeignKey(NewsData, on_delete=models.CASCADE)
    cor = models.ForeignKey(CorData, on_delete=models.CASCADE)
    news_link = models.CharField(max_length=200)
    datetime = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=8, choices=SENTIMENT_CHOICES)
    accuracy = models.FloatField()

    class Meta:
        db_table = 'Sentiment_data'
        verbose_name = '감정분석 테이블'
        verbose_name_plural = '감정분석 테이블'