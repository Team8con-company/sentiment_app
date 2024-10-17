from django.core.management.base import BaseCommand
from ...models import CorData, NewsData, SentimentData
from django.utils import timezone
import random

class Command(BaseCommand):
    help = '한국어 더미 데이터 생성'

    def handle(self, *args, **kwargs):
        self.stdout.write('한국어 더미 데이터 생성 중...')

        # CorData 생성
        companies = ['삼성전자', 'LG전자', '현대자동차', 'SK하이닉스', '네이버', '카카오', '롯데그룹', '포스코', 'KT', '한화그룹']
        for company in companies:
            CorData.objects.create(cor_name=company)

        # NewsData 생성
        news_titles = [
            "{} 신제품 출시 발표",
            "{} 실적 전년 대비 상승",
            "{} 신규 공장 설립 계획",
            "{} CEO 교체 소식",
            "{} 해외 시장 진출 확대",
            "{} 신기술 개발 성공",
            "{} 대규모 투자 계획 발표",
            "{} 직원 복지 정책 개선",
            "{} 환경 보호 캠페인 시작",
            "{} 주가 사상 최고치 기록"
        ]

        for _ in range(50):  # 50개의 뉴스 아이템 생성
            cor = random.choice(CorData.objects.all())
            title = random.choice(news_titles).format(cor.cor_name)
            NewsData.objects.create(
                cor=cor,
                news_title=title,
                news_link=f"http://example.com/news/{random.randint(1000, 9999)}",
                datetime=timezone.now() - timezone.timedelta(days=random.randint(0, 30))
            )

        # SentimentData 생성
        sentiments = ['positive', 'negative', 'neutral']
        
        for news in NewsData.objects.all():
            SentimentData.objects.create(
                news=news,
                cor=news.cor,
                news_link=news.news_link,
                datetime=timezone.now() - timezone.timedelta(hours=random.randint(1, 24)),
                result=random.choice(sentiments),
                accuracy=random.uniform(0.7, 1.0)
            )

        self.stdout.write(self.style.SUCCESS('한국어 더미 데이터 생성 완료'))