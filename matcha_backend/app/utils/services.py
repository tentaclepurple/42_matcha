import requests


def get_location_by_ip(ip_address):
    """Get location using IP address"""
    print("IP Address en getlocation: ", ip_address)
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}')
        data = response.json()
        print("Data: ", data)
        if data['status'] == 'success':
            return {
                "type": "Point",
                "coordinates": [float(data['lon']), float(data['lat'])]
            }
    except Exception:
        return {
            "type": "Point",
            "coordinates": [0.0, 0.0]
        }
    

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except:
        # Backup service
        try:
            response = requests.get('https://api64.ipify.org?format=json')
            return response.json()['ip']
        except:
            return None
        

def get_client_ip(request):
    """Get real IP address from request headers"""
    if request.headers.get('X-Forwarded-For'):
        # Si viene de un proxy
        return request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        # Header común para IP real
        return request.headers.get('X-Real-IP')
    else:
        # Último recurso
        return request.remote_addr