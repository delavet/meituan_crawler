from point_crawler import point_crawler


def start_crawl():
    init_lat = 39.4300
    init_lon = 115.4200
    end_lat = 41.0500
    end_lon = 117.5300
    lat = init_lat
    lon = init_lon
    cnt = 0
    i = int(input("start index i: "))
    j = int(input("start index j: "))
    lat = init_lat + 0.04 * j
    lon = init_lon + 0.04 * i
    while lat < end_lat:
        while lon < end_lon:
            print("=====INFO: cnt", cnt, "lat:", lat, ", lon:", lon, "=====")
            print("i = ", str(i), " ; j = ", str(j))
            crawler = point_crawler(lat, lon, i, j)
            try:
                crawler.crawl_point()
            except Exception as e:
                print('=====  OUT SIDE EXCEPTION =====')
                print(e)
                print('=====OUTSIDE EXCEPTION END=====')
                continue
            lon += 0.04
            i += 1
        lat += 0.04
        j += 1


if __name__ == "__main__":
    start_crawl()
    