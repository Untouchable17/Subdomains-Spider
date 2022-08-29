import sys
import optparse

import requests
from fake_headers import Headers


def get_command_arguments():
    parser = optparse.OptionParser()
    parser.add_option(
        "-t", "--target", dest="target",
        help="set target domain name(example: google.com)"
    )
    parser.add_option(
        "-f", "--file", dest="file",
        help="set file with subdomains"
    )
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error(
            "[-] Please specify an target, use --help for more info"
        )
    elif not options.file:
        parser.error(
            "[-] Please specify an file, use --help for more info"
        )
    return options


class SpiderScanner:

    def __init__(self, target_url: str, subdomain_file: str):
        self.target_url = target_url
        self.headers = Headers(
            browser="chrome",
            os="win",
            headers=True
        )
        self.subdomain_file = subdomain_file

    def send_subdomain_request(self, sub_domain: str) -> None:
        with requests.Session() as session:
            template_url = "https://" + sub_domain.strip('\n') + "." + self.target_url
            spider_request = session.get(template_url, headers=self.headers.generate())
            if spider_request.status_code == 200:
                print(f"[200] {spider_request.url} | {template_url}")
            elif spider_request.status_code == 404:
                print(f"[404] {spider_request.url}")

    def read_data_file(self):
        with open(self.subdomain_file, "r") as file:
            for sub_domain in file:
                try:
                    self.send_subdomain_request(sub_domain)
                except Exception as ex:
                    pass


def spider_setup():
    options = get_command_arguments()
    target_host = options.target
    subdomain_file = options.file
    try:
        requests.get("https://" + target_host)
    except Exception as ex:
        print(f"Enter a valid hostname(example: google.com)")
        sys.exit()

    spider = SpiderScanner(target_host, subdomain_file)
    spider.read_data_file()


if __name__ == "__main__":
    spider_setup()
