from django.shortcuts import render
from django.core.cache import cache
from .models import CompanyList, NewsData
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Hannanum
import base64
from io import BytesIO

def index(request):
    companies = CompanyList.objects.all().order_by('name')
    return render(request, 'search/index.html', {'companies': companies})

def search_results(request):
    company = request.GET.get('company', '')
    results = {}
    companies = CompanyList.objects.all().order_by('name')
    
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
            else:
                results = {'company_name': comp.name, 'no_results': True}
        except CompanyList.DoesNotExist:
            results = {'company_name': company, 'not_found': True}

    return render(request, 'search/index.html', {'results': results, 'companies': companies})

def generate_wordcloud(text):
    hannanum = Hannanum()
    nouns = hannanum.nouns(text)
    
    # 단어 길이 필터링 및 불용어 제거
    words = [word for word in nouns if len(word) > 1]
    stop_words = set(['것', '등', '및', '수', '이', '그', '저', '때', '곳', '년', '월', '일'])
    words = [word for word in words if word not in stop_words]
    
    counter = Counter(words)

    wordcloud = WordCloud(
        font_path='/Users/yoonjeong/Library/Fonts/Freesentation-4Regular.ttf',
        background_color='white',
        height=400,
        width=800,
        max_words=100,  # 최대 단어 수 제한
    )

    img = wordcloud.generate_from_frequencies(dict(counter.most_common(50)))
    
    img_buffer = BytesIO()
    img.to_image().save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return img_str