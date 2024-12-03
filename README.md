# Projeto de acesso a API do Zabbix

Este Projeto foi criado com o intúito de validação de endereço IP primário dos hosts.

## Dependências

* pandas >=2.2.3
* zabbix-utils >=2.0.1
* Python >= 3.9


## Modo de uso

Para utilizar o script, deverá deverá clonar o projeto:
### Clone repositório
```bash
git clone https://github.com/alexeiev/zabbix_api.git
```
### Criando ambiente virtual para o Python

```bash
cd zabbix_api
python3 -m venv .venv
```

Agora vamos ativar o ambiente Virtal

```bash
source .venv/bin/activate
```

### Instalando dependências
```bash
pip3 install -r requirements.txt
```
criar ficheiro de environment

```bash
cat << EOF >> .env 
url="https://monitorizacao.local/zabbix"
token=''
EOF
```

### Execução

Vamos conhecer o HELP
```bash
[alexeiev@localhost zabbix_api]$ ./main.py 
Não escolheu uma opção válida

usage: main.py [-h] [-host HOST] [-f FILE_IMPORT] [-t TITLE_NAME] [-e FILE_EXPORT]

Script para acesso a API do Zabbix

optional arguments:
  -h, --help            show this help message and exit
  -host HOST, --hostname HOST
                        Indicar hostname para consultar o IP
  -f FILE_IMPORT, --file FILE_IMPORT
                        Indicar ficheiro .csv
  -t TITLE_NAME, --title TITLE_NAME
                        Titulo da coluna no ficheiro .csv (default = name)
  -e FILE_EXPORT, --export FILE_EXPORT
                        Indicar nome do ficheiro .csv para export (default = export.csv)
```

* Executar com apenas um host
```bash
[alexeiev@localhost zabbix_api]$ ./main.py -host srv-mysql.homelab.local
Hostname: srv-mysql.homelab.local - Ip Address: 10.0.0.114
```
* Executar com um ficheiro CSV com uma lista de hosts.

* É necessário indicar o nome da coluna onde esta os hosts. Caso não exista, deverá ser criada.

Ex.:
```text
name     | ip_address
srv-bd01 | 10.0.0.10
srv-bd02 | 10.0.0.11
srv-bd03 | 10.0.0.12
srv-bd04 | 10.0.0.13
```

```bash
./main.py --file lista2.csv --title name
```

**Ao Finalizar, desativar o ambiente virtual com o seguinte comando**
```bash
deactivate
```