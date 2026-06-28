from django.urls import reverse

def global_spa_config(request):
    """
    SPA 화면의 프론트엔드 자바스크립트가 수신할 전역 설정을 제공합니다.
    """
    try:
        # reverse 유틸리티로 Django URL 네임스페이스의 실제 물리 주소를 역추적합니다.
        api_url = reverse('todos:api_todo-list')
    except Exception:
        api_url = '/api/todos/'
        
    return {
        'API_BASE_URL': api_url,
        'SITE_META_TITLE': 'TodoBoard Premium SPA',
    }