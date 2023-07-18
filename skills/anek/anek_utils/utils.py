import aiohttp
from bs4 import BeautifulSoup


async def get_anek():
    """Make async http request to get anek."""
    async with aiohttp.ClientSession() as session:
        url = 'https://baneks.ru/random'
        async with session.get(url) as result:
            page = await result.text()
            soup = BeautifulSoup(page, "html.parser")
            anek = soup.find('article')
            anek = str(anek)
            for i in ('<article>', '</article>', '<h2>', '</h2>', '<br>', '<br/>', '<p>', '</p>'):
                anek = anek.replace(i, '')
            anek = anek.replace('#', '№')
            return anek
