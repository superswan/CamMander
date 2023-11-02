import shodan
from time import sleep

SHODAN_API_KEY = ""

api = shodan.Shodan(SHODAN_API_KEY)

vuln_models = ["dcs-1130", "dcs-2102", "dcs-2121", "dcs-3410", "dcs-5230", "dcs-5605", "tv-ip512"]
total_count = 0

vuln_ip_list = []

def dump_list_to_txt(file_path, data_list):
    with open(file_path, 'w') as file:
        for item in data_list:
            file.write("%s\n" % item)

def is_vulnerable(version):
    version_string = ''.join(filter(str.isdigit, version))[:3]
    return int(version_string[-1]) < 4

for model in vuln_models:
    query = f'dcs-lig-httpd "{model}"'
    try:
        for result in api.search_cursor(query):
            total_count += 1
            try:
                if 'ip_camera' in result and is_vulnerable(result['ip_camera']['version']):
                    ip_str = result['ip_str']
                    port = result['port']
                    full_addr = f"{ip_str}:{port}"
                    print(f"{model} {result['ip_camera']['version']} {full_addr}")
                    vuln_ip_list.append(full_addr)
            except KeyError:
                print("Error parsing results")
            except Exception as e:
                print(f"Error: {e}")

        sleep(1.337)  # Sleep to avoid rate limiting
    except shodan.APIError as e:
        print(f'Shodan API error: {e}')
    except Exception as e:
        print('Error: {}'.format(e))

print(f'{len(vuln_ip_list)}/{total_count} vulnerable')
dump_list_to_txt('vuln_ips.txt', vuln_ip_list)
