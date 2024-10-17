from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from .models import CompanyList, NewsData
from .serializers import CompanyListSerializer, NewsDataSerializer
from collections import Counter
from konlpy.tag import Hannanum
from wordcloud import WordCloud
from io import BytesIO
import base64
from django.core.cache import cache
from django.contrib.staticfiles import finders


@api_view(['GET'])
def index(request):
    companies = CompanyList.objects.all().order_by('id')  # 모든 회사 데이터를 id 기준으로 정렬
    paginator = Paginator(companies, 10)  # 페이지당 10개 항목 설정
    page_number = request.GET.get('page')  # 현재 페이지 번호를 GET 요청에서 가져옴
    page_obj = paginator.get_page(page_number)  # 현재 페이지 객체를 가져옴

    # Serializer로 데이터를 직렬화
    serializer = CompanyListSerializer(page_obj, many=True)

    # HTML 템플릿에 직렬화된 데이터를 넘김
    context = {
        'page_obj': page_obj,
        'companies': serializer.data,  # Serializer로 직렬화된 데이터
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
    }

    # HTML 템플릿으로 직렬화된 데이터를 넘겨 렌더링
    return render(request, 'search/index.html', context)

@api_view(['GET'])
def search_results(request):
    company = request.GET.get('company', '')
    results = {}
    companies = CompanyList.objects.all().order_by('id')
    
    # 페이지네이션 추가
    paginator = Paginator(companies, 10)  # 페이지당 10개 항목
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if company:
        try:
            comp = CompanyList.objects.get(name__iexact=company)
            news_data = NewsData.objects.filter(comp=comp)
            
            total = news_data.count()
            
            if total > 0:
                positive = news_data.filter(sentiment='positive').count()
                negative = news_data.filter(sentiment='negative').count()
                neutral = news_data.filter(sentiment='neutral').count()

                results = {
                    'company_name': comp.name,
                    'positive_percent': round((positive / total) * 100, 2),
                    'negative_percent': round((negative / total) * 100, 2),
                    'neutral_percent': round((neutral / total) * 100, 2),
                }
                
                # 워드클라우드 생성 (캐시 적용)
                cache_key = f'wordcloud_{comp.id}'
                wordcloud_image = cache.get(cache_key)
                if not wordcloud_image:
                    news_text = ' '.join([news.title for news in news_data])
                    wordcloud_image = generate_wordcloud(news_text)
                    cache.set(cache_key, wordcloud_image, 3600)  # 1시간 동안 캐시
                results['wordcloud'] = wordcloud_image

                # 최근 기사 10개 가져오기
                recent_news = news_data.order_by('-date')[:10]

                results['recent_news'] = recent_news

            else:
                results = {'company_name': comp.name, 'no_results': True}
        except CompanyList.DoesNotExist:
            results = {'company_name': company, 'not_found': True}

    # context 데이터 설정
    context = {
        'results': results,
        'page_obj': page_obj,
        'companies': page_obj.object_list,
    }

    # JSON 형태로 데이터를 반환 (프론트엔드 또는 템플릿에 사용)
    if request.headers.get('Accept') == 'application/json':
        return Response(context, status=status.HTTP_200_OK)

    # HTML 템플릿 렌더링
    return render(request, 'search/index.html', context)

from django.contrib.staticfiles import finders
font_path = finders.find('fonts/SB M.ttf')

@api_view(['POST'])
def generate_wordcloud_api(request):
    text = request.data.get('text', '')  # POST 요청으로 받은 텍스트

    if not text:
        return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)

    # 워드클라우드 생성 함수 호출
    img_str = generate_wordcloud(text)

    # 결과를 JSON 형태로 반환
    return Response({'wordcloud': img_str}, status=status.HTTP_200_OK)

def generate_wordcloud(text):
    hannanum = Hannanum()
    nouns = hannanum.nouns(text)
    
    words = [word for word in nouns if len(word) > 1]
    stop_words = set(['것', '등', '및', '수', '이', '그', '저', '때', '곳', '년', '월', '일'])
    words = [word for word in words if word not in stop_words]
    
    counter = Counter(words)

    wordcloud = WordCloud(
        font_path=font_path,  # 적절한 폰트 경로 지정 필요
        background_color='white',
        height=400,
        width=800,
        max_words=100,
    )

    img = wordcloud.generate_from_frequencies(dict(counter.most_common(50)))
    
    img_buffer = BytesIO()
    img.to_image().save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return img_str