from django.db import models

class CompanyList(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'company_list'
        verbose_name = '기업 테이블'
        verbose_name_plural = '기업 테이블'

    def __str__(self):
        return self.name

class NewsData(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]

    id = models.AutoField(primary_key=True)
    comp = models.ForeignKey(CompanyList, on_delete=models.CASCADE, db_column='comp_id')
    title = models.CharField(max_length=200, null=False)
    link = models.CharField(max_length=200, null=False)
    date = models.DateTimeField(null=True, blank=True)
    sentiment = models.CharField(max_length=8, choices=SENTIMENT_CHOICES, null=False)
    confidence = models.FloatField(null=False)

    class Meta:
        db_table = 'news_data'
        verbose_name = '데이터 테이블'
        verbose_name_plural = '데이터 테이블'

    def __str__(self):
        return self.title