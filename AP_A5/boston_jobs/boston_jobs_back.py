from bs4 import BeautifulSoup
import requests

def get_search_results(title:str) -> list[tuple[str]]:
    """
    :param title: The title that you want to search for.
    :return: list of tuples. the first element is the description of job and the second one is the link of it.
    """
    # get searched page
    page = requests.get(f'https://boston.craigslist.org/search/jjj?query={title}')

    # extract results (text, link)
    soup = BeautifulSoup(page.text, 'html.parser')
    search_results_html = soup.find_all("ul", {'id': 'search-results'})[0]

    results = []
    for res in search_results_html.find_all('li'):
        link:str = res.find('a').attrs['href']
        text:str = res.find('h3', {'class':'result-heading'}).get_text()
        results.append((text.strip(), link))

    return results

def get_search_titles() -> dict[str, str]:
    """
    :return: dict of titles and their queries.
    """
    page = requests.get("https://boston.craigslist.org/search/jjj?")
    soup = BeautifulSoup(page.text, 'html.parser')
    titles = soup.find_all('select', {'id': "subcatAbb"})

    res = dict()
    for title in titles[0].find_all('option'):
        res[title.get_text()] = title.attrs['value']

    return res


def get_description(page_url:str) -> tuple[str, str]:
    """
    :param page_url: The page of the job
    :return: The job title and the description of the page.
    """
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    return (soup.find('span', {'id': 'titletextonly'}).text,
            soup.find('section', {'id': 'postingbody'}).text.lstrip('\n\nQR Code Link to This Post\n\n\n'))
