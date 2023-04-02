import requests

def Gen_report(C):
    url = 'https://wttr.in/{}'.format(C)
    try:
        data = requests.get(url)
        return data.text
    except:
        return "Error Occurred"