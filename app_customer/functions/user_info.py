import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ipgeolocation(ip):
    ipgeolocation_api ="4ab56753269e476ab21057e409ac1b19"
    endpoint = f"https://api.ipgeolocation.io/ipgeo?apiKey={ipgeolocation_api}&ip={ip}"
    res = requests.get(endpoint)
    if res.status_code == requests.codes.ok:
        data = res.json()
        try:
            return data['district']+','+data['city']+','+data['country_name']
        except:
            return 'unknown'
    return 'unknown'

def get_device(user_agent):
    if user_agent.is_mobile:
        return 'mobile'
    elif user_agent.is_tablet:
        return 'tablet'
    elif user_agent.is_touch_capable:
        return 'touch_capable'
    elif user_agent.is_pc:
        return 'pc'
    elif user_agent.is_bot:
        return 'bot'
    else:
        'unknown'