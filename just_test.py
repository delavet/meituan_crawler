from point_crawler import point_crawler
from pprint import pprint


if __name__ == "__main__":
    p = point_crawler(39.1234, 117.1212)
    pprint(p.get_result_json(0))
