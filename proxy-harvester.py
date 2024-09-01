import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Main function
def main():
    ua = UserAgent()  # From here we generate a random user agent
    proxy_pool = []  # Will contain proxies [ip:port]

    # we want a rotating proxy system, we need to retrieve them from the beginning and we'll achieve that by scraping the site sslproxies.org
    proxies_req = Request("https://www.us-proxy.org/")
    proxies_req.add_header("User-Agent", ua.random)
    proxies_doc = urlopen(proxies_req).read().decode("utf8")
    soup = BeautifulSoup(proxies_doc, "html.parser")
    # print(soup)
    free_proxies_table = soup.find(class_="table")

    # parse the table for proxies
    for row in free_proxies_table.tbody.find_all("tr"):
        proxy_pool.append(
            f"{row.find_all("td")[0].string}:{row.find_all("td")[1].string}"
        )

    # Print the extracted IP addresses
    print(proxy_pool)

    # Retrieve a random index proxy (we need the index to delete it if not working)
    def random_proxy():
        return random.randint(0, len(proxy_pool) - 1)

    proxy_index = random_proxy()

    proxy = proxy_pool[proxy_index]

    # test to validate free_poxy list
    for n in range(1, 100):
        # we'll make 100 requests to icanhazip.com which will return our current IP (proxied)
        print(proxy)
        req = Request("https://icanhazip.com/")
        req.set_proxy(proxy, "https")
        req.add_header("User-Agent", ua.random)

        # Every 10 requests, generate a new proxy
        if n % 10 == 0:
            proxy_index = random_proxy()
            proxy = proxy_pool[proxy_index]

        # Make the call
        try:
            my_ip = urlopen(req).read().decode("utf8")
            print("#" + str(n) + ": " + my_ip)
        except:  # If error, delete this proxy and find another one
            del proxy_pool[proxy_index]
            print("This Proxy is no good " + proxy + " so we deleted it from the pool.")
            proxy_index = random_proxy()
            proxy = proxy_pool[proxy_index]


if __name__ == "__main__":
    main()
