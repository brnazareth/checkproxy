# Author - ChatGPT
# Enhanced by stackoverflow
# glued together by bnazareth@zscaler.com
# 2023032001

import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Acrescente aqui a URL que deseja validar
url = 'https://consultaauxilio.cidadania.gov.br/'

# Arquivo com a lista de proxies que serao testados
proxy_file = 'proxies.txt'

# Alguns WAF validam se o user-agent é de seres humanos. 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Ler lista de proxies do arquivo
with open(proxy_file) as f:
    proxies = f.readlines()

# Remover caracteres de quebra de linha (\n) da lista de proxies
proxies = [proxy.strip() for proxy in proxies]

# Tentar acessar a URL com cada um dos proxies
for proxy in proxies:
    try:
        # Fazer solicitação HTTP usando o proxy
        response = requests.get(url, proxies={'http': proxy, 'https': proxy}, verify=False, headers = headers)
        # Exibir código HTTP de retorno
        print(f"URL {url} - Proxy {proxy} - Status code: {response.status_code}")
        # Exibir o titulo da pagina para validar se esta no website correto ou em algum redirect bizarro
        conteudo = response.text
        print(conteudo[conteudo.find('<title>') + 7 : conteudo.find('</title>')])
    # Se ocorrer algum erro ao acessar o proxy, exibir mensagem de erro
    except requests.exceptions.HTTPError as errh:
        print(f"Proxy {proxy} - Erro ao acessar")
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print(f"Proxy {proxy} - Erro ao acessar")
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print(f"Proxy {proxy} - Erro ao acessar")
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print(f"Proxy {proxy} - Erro ao acessar")
        print ("Oops: Something Else Went Wrong:",err)
