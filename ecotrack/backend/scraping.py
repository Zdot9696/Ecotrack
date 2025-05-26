import requests
from bs4 import BeautifulSoup

def obtener_consejos_habitos():
    url = "https://www.healthline.com/nutrition/27-health-and-nutrition-tips"
    response = requests.get(url)
    response.raise_for_status()  # lanzar excepción si falla

    soup = BeautifulSoup(response.text, 'html.parser')

    consejos = []
    # Los consejos están en elementos h2
    for header in soup.find_all('h2'):
        tip = header.get_text(strip=True)  # solo el texto del título
        consejos.append({"tip": tip})

    return {"consejos": consejos}
