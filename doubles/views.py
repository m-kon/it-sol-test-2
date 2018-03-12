"""doubles/views.py"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from . import models
#from .serializers import CompanySerializer
import data_for_hook, hook

@api_view(['GET'])
def get_bitrix_doubles(req):
    """получить из bitrix список компаний"""
    
    is_there_next = True
    start = 0
    b = hook.Bitrix24Hook(data_for_hook.domain, data_for_hook.hook_code)
    result = []

    while is_there_next:
        response = b.call_method('crm.company.list', {'select': ['ID', 'TITLE', 'DATE_CREATE'], 'start': start})
        result = result + response['result']
        if not 'next' in response:
            is_there_next = False
        else:
            start = int(response['next'])

    doubles = search_doubles(result)

    return Response(doubles)

def search_doubles(data):
    title_list = [v['TITLE'] for v in data]
    count_dict = {title: title_list.count(title) for title in set(title_list)}
    double_list = [k for k, v in count_dict.items() if v > 1]
    double_list.sort()
    result_list = []
    for title in double_list:
        result_list.extend([v for v in data if v['TITLE'] == title])
    return result_list
