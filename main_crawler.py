from point_crawler import point_crawler


def start_crawl():
    init_lat = 39.4300
    init_lon = 115.4200
    end_lat = 41.0500
    end_lon = 117.5300
    lat = init_lat
    lon = init_lon
    cnt = 0
    while lat < end_lat:
        while lon < end_lon:
            print("=====INFO: cnt", cnt, "lat:", lat, ", lon:", lon, "=====")
            crawler = point_crawler(lat, lon)
            try:
                crawler.crawl_point()
            except Exception as e:
                print('=====  OUT SIDE EXCEPTION =====')
                print(e)
                print('=====OUTSIDE EXCEPTION END=====')
            lon += 0.03
        lat += 0.03


if __name__ == "__main__":
    start_crawl()
    