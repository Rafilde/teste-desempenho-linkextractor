from locust import HttpUser, task, between

URLS_PARA_TESTAR = [
    "https://en.wikipedia.org/wiki/Portal:Contents",
    "https://en.wikipedia.org/wiki/List_of_cities_proper_by_population",
    "https://www.archive.org/",
    "https://news.ycombinator.com/",
    "https://www.reddit.com/r/all/",
    "https://stackoverflow.com/questions",
    "https://github.com/trending",
    "https://www.imdb.com/chart/top",
    "https://www.craigslist.org/about/sites",
    "https://www.bbc.com/news",
]

class LinkExtractorUser(HttpUser):

    @task
    def extrair_links_sequencialmente(self):
        """
        realizar uma sequência de 10 invocações... 
        passando uma URL diferente a cada invocação.
        """
        
        for url in URLS_PARA_TESTAR:

            try:
                self.client.get(f"/api/{url}", name="/api/[url_dinamica]")
                
                print(f"Requisitado: {url}")

            except Exception as e:
                print(f"Erro ao requisitar {url}: {e}")