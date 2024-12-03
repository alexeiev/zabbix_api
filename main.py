#!/usr/bin/env python3

import sys
import os
import argparse

import pandas as pd
from zabbix_utils import ZabbixAPI
from dotenv import load_dotenv


load_dotenv()
# Carregar variaveis no ficheiro .env
url = os.getenv('url')
token = os.getenv('token')

"""Realizar o parse nos argumentos

"""
parser = argparse.ArgumentParser(description='Script para acesso a API do Zabbix')
parser.add_argument('-host', '--hostname',  action='store', dest='host', help='Indicar hostname para consultar o IP')
parser.add_argument('-f', '--file', action='store', dest='file_import', help='Indicar ficheiro .csv')
parser.add_argument('-t', '--title', default='name', action='store', dest='title_name', help='Titulo da coluna no ficheiro .csv (default = name)')
parser.add_argument('-e', '--export', default='export.csv',  action='store', dest='file_export', help='Indicar nome do ficheiro .csv para export (default = export.csv)')

args = parser.parse_args()

file_import = args.file_import
file_export = args.file_export
title_name = args.title_name
host = args.host


'''
Configurando o acesso a API
'''
try:
  api = ZabbixAPI(url=url, validate_certs=False)
  api.login(token=token)
except :
  print("Error ao acessar api")
  sys.exit(1)
# validar acesso a API
try:
  api.check_auth()
except:
  print("Erro na autenticação. Favor, validar o TOKEN")
  sys.exit(1)

def get_host_id(name):
  """Função que recebe um hostname responde o ID do host
    Args:
        name (str): Nome do host
  """
  id_host = api.host.get(filter={'host': name.lower()}, output=['hostid'])
  if not id_host:
    id_host = False
  else:
    id_host = id_host[0]['hostid'] 

  return id_host

def get_ip(id):
  """Função que recebe um ID responde o ip address do host
    Args:
        id (str): ID do host
  """
  ip_addr = api.hostinterface.get(filter={'hostid' : id}, output=['ip'])

  if not ip_addr:
    ip_addr = False
  else:
    ip_addr = ip_addr[0]['ip']
  
  return ip_addr

def csv_file(file):
  """Função para receber Files csv
  Args:
      file (str): ficheiro csv para tratar    
  """
  if not file or file.endswith('.csv') != True:
    print("Ficheiro CSV não encontrado.")
    sys.exit(1)
  
  dados = pd.read_csv(file, sep=',')
  if title_name in list(dados.columns):
    pass
  else:
    print(f"O Titulo passado não existe no ficheiro. Segue a lista: {list(dados.columns)}")
    sys.exit(1)
  df = pd.DataFrame(columns=['nome','ip_address'])

  for host in dados[title_name]:
    #coletar IP 
    hostname = host.lower()
    ip_addr = get_ip(get_host_id(host))
  
    # Adicionando valores ao final do ficheiro
    df.loc[len(df)] = [ hostname, ip_addr ]

  if os.path.exists(file_export):
    file_name = input('Já existe um ficheiro com este nome.\nIndique novo nome: ')
    if os.path.exists(file_name):
      print("Já existe um ficheiro com este nome. O programa será abortado!!!")
      sys.exit(1)
  else:
    df.to_csv(file_export, sep=',', index=False, encoding='utf-8')
  
  df.to_csv(file_name, sep=',', index=False, encoding='utf-8')


def main():
  """
  Chamada individual recebe hostname -> ip_address
  """

  if file_import:
    csv_file(file_import)
  elif host:
    print(f"Hostname: {host} - Ip Address: {get_ip(get_host_id(host))}")
  else:
    print(f"Não escolheu uma opção válida\n")
    parser.print_help()
  

if __name__ == "__main__":
  main()