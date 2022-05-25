def parse_log(file="homework6/access.log"):
    with open(file, "r") as file:
        requests_count = {}
        top_urls = {}
        requests_4xx = []
        requests_5xx = {}
        count = 0

        for line in file:
            count += 1
            request_type = line.split('"')[1].split()[0]
            url = line.split('"')[1].split()[1]
            url_no_params = line.split('"')[1].split()[1].split('?')[0].split('%')[0]
            status_code = line.split('"')[2].split()[0]
            ip = line.split('"')[0].split()[0]
            bytes_sent = line.split('"')[2].split()[1]

            if len(request_type) > 10:
                request_type = f"BAD_REQUEST_LINE_{count}"
                requests_count[request_type] = 1
            elif request_type not in requests_count:
                requests_count[request_type] = 1
            else:
                requests_count[request_type] += 1

            if url_no_params not in top_urls:
                top_urls[url_no_params] = 1
            else:
                top_urls[url_no_params] += 1

            if status_code.startswith("4"):
                requests_4xx.append(tuple((url_no_params, status_code, bytes_sent, ip)))

            if status_code.startswith("5"):
                if ip not in requests_5xx:
                    requests_5xx[ip] = 1
                else:
                    requests_5xx[ip] += 1

        top_urls_sorted = sorted(top_urls.items(), key=lambda x: x[1], reverse=True)

        requests_4xx_sorted = sorted(requests_4xx, key=lambda x: x[2], reverse=True)

        requests_5xx_sorted = sorted(requests_5xx.items(), key=lambda x: x[1], reverse=True)

        return count, requests_count, top_urls_sorted, requests_4xx_sorted, requests_5xx_sorted
