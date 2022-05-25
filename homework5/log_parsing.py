import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--json", action="store_true")
args = vars(parser.parse_args())


class LogParser:
    def parse_log(self, file="access.log"):
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
                    request_type = f"UNKNOWN_REQUEST_IN_LINE_{count}"
                    requests_count[request_type] = 1
                elif request_type not in requests_count:
                    requests_count[request_type] = 1
                else:
                    requests_count[request_type] += 1

                if url_no_params not in top_urls:
                    top_urls[url_no_params] = 1
                else:
                    top_urls[url_no_params] += 1

                if status_code.startswith("4") or status_code.startswith(" 4"):
                    requests_4xx.append(tuple((url, status_code, bytes_sent, ip)))

                if status_code.startswith("5"):
                    if ip not in requests_5xx:
                        requests_5xx[ip] = 1
                    else:
                        requests_5xx[ip] += 1

            top_urls_sorted = sorted(top_urls.items(), key=lambda x: x[1], reverse=True)

            requests_4xx_sorted = sorted(requests_4xx, key=lambda x: x[2], reverse=True)

            requests_5xx_sorted = sorted(requests_5xx.items(), key=lambda x: x[1], reverse=True)

            return count, requests_count, top_urls_sorted, requests_4xx_sorted, requests_5xx_sorted

    def write_parsed_log(self, file="access.log"):
        count, requests_count, top_urls_sorted, requests_4xx_sorted, requests_5xx_sorted = self.parse_log(file=file)
        if not args["json"]:
            with open("parsed_log.log", "w") as file:
                file.write(f"Getting total number of requests.\nThere are {count} requests in log file.\n")
                file.write(f"\nGetting number of requests for each type of request.\n")
                for request in requests_count:
                    file.write(f"{request}: {requests_count[request]}\n")
                file.write(f"\nGetting top 10 most popular requests.\n")
                for i in range(0, 10):
                    file.write(f"URL: {top_urls_sorted[i][0]} - REQUESTS: {top_urls_sorted[i][1]}\n")
                file.write(f"\nGetting 5 biggest requests with 4xx error.\n")
                for i in range(0, 5):
                    file.write(f"URL: {requests_4xx_sorted[i][0]} - STATUS CODE: {requests_4xx_sorted[i][1]} - BYTES SENT: "
                               f"{requests_4xx_sorted[i][2]} - IP: {requests_4xx_sorted[i][3]}\n")
                file.write(f"\nGetting 5 users by number of requests that ended with a 5xx error.\n")
                for i in range(0, 5):
                    file.write(f"IP: {requests_5xx_sorted[i][0]} - REQUESTS AMOUNT: {requests_5xx_sorted[i][1]}\n")
        else:
            top_10_urls = {}
            for i in range(0, 10):
                url = top_urls_sorted[i][0]
                request_num = top_urls_sorted[i][1]
                top_10_urls[i + 1] = {"url": url, "count": request_num}

            top_5_biggest_with_4 = {}
            top_5_biggest_with_5 = {}
            for i in range(0, 5):
                url = requests_4xx_sorted[i][0]
                status_code = requests_4xx_sorted[i][1]
                bytes_sent = requests_4xx_sorted[i][2]
                ip = requests_4xx_sorted[i][3]
                top_5_biggest_with_4[i + 1] = {"url": url, "statusCode": status_code, "bytesSent": bytes_sent, "ip": ip}

                ip = requests_5xx_sorted[i][0]
                amount = requests_5xx_sorted[i][1]
                top_5_biggest_with_5[i + 1] = {"ip": ip, "amount": amount}

            data = {"allRequests": count,
                    "requestsNumByType": requests_count,
                    "topUrls": top_10_urls,
                    "topUrls4Err": top_5_biggest_with_4,
                    "topUrls5Err": top_5_biggest_with_5}

            with open("json_data", "w") as file:
                json.dump(data, file)


LogParser().write_parsed_log()
