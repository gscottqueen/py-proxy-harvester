import random, re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# Main function
def main():
    ua = UserAgent()  # From here we generate a random user agent
    proxy_pool = []  # Will contain proxies [ip:port]

    # we want a rotating proxy system, we need to retrieve them from the beginning and we'll achieve that by scraping the site sslproxies.org
    proxies_req = Request(
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&country=us&protocol=http&proxy_format=ipport&format=text&anonymity=Anonymous&timeout=20000"
    )  # this isn't going to work

    # we need to set up our own proxy server in an ephemerial pipeline
    # it should:

    # create a webserver with a random ip
    # run our jobs making requests
    # dump the information into an artifact
    # scan the artifact for mallware
    # if it begins to be blocked for crawling, it exits
    # start a new one to do it again

    proxies_req.add_header("User-Agent", ua.random)
    proxies_doc = urlopen(proxies_req).read().decode("utf8")
    soup = BeautifulSoup(proxies_doc, "html.parser")
    # print(soup)
    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b"
    proxy_pool = re.findall(pattern, str(soup))

    # Print the extracted IP addresses
    print(
        proxy_pool,
        end="\n\n",
    )

    # Retrieve a random index proxy (we need the index to delete it if not working)
    def random_proxy():
        return random.randint(0, len(proxy_pool) - 1)

    proxy_index = random_proxy()

    proxy = proxy_pool[proxy_index]

    # test to validate free_poxy list
    for n in range(1, 10):
        # we'll make requests to icanhazip.com which will return our current IP (proxied)
        print("checkig proxy #" + str(n) + ": " + proxy)
        req = Request("https://icanhazip.com/")
        req.set_proxy(proxy, "http")
        req.add_header("User-Agent", ua.random)
        print(
            "request",
            vars(req),
            end="\n\n",
        )

        # Every 10 requests, generate a new proxy
        if n % 10 == 0:
            proxy_index = random_proxy()
            proxy = proxy_pool[proxy_index]

        # Make the call
        try:
            my_ip = urlopen(req).read().decode("utf8")
            print("This is a good proxy!! #" + str(n) + ": " + my_ip)
        except Exception as e:  # If error, delete this proxy and find another one
            print(f"Error: {e}")
            print(f"Proxy: {proxy}")

            del proxy_pool[proxy_index]
            print(
                "This Proxy is no good " + proxy + " so we deleted it from the pool.",
                end="\n\n",
            )
            if len(proxy_pool) == 0:
                print("No more proxies to check...")
                return -1
            proxy_index = random_proxy()
            proxy = proxy_pool[proxy_index]


if __name__ == "__main__":
    main()
