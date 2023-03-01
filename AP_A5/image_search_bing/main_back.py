import requests
from bs4 import BeautifulSoup


def get_list_of_images(query:str):
    """
    Get the image url from bing search
    :param query:
    :return:
    """
    query = query.replace(' ', '+').strip()
    url = f'https://www.bing.com/images/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.findChildren('div', {'id':'mmComponent_images_2'})[0]
    results = []
    for img in images.find_all('img'):
        results.append(img.attrs.get('src'))
    
    return results


def get_image_content(link):
    """
    Get the image content from the link
    :param link:
    :return:
    """
    if link is None:
        return None
    try:
        response = requests.get(link, timeout=5)
    except requests.exceptions.Timeout:
        print('Timeout')
    except Exception as exp:
        print('link: ', link)
        raise exp
    else:
        return response.content
