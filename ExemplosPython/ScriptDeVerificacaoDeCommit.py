#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

# ######################################################################
# dependencias:
# - pip install "jira"
# #######################################################################

import sys, os, re
import logging
import subprocess
from jira import JIRA, JIRAError
import socket
import requests


# ######################################################################
# script versao 1.0 de validações de desenvolvimento MV
#  - limite mínimo de 15 caractéres no comentário
#  - comentário deve ter referência a um ticket do JIRA
#  - o ticket informado no comentário deve existir
#  - o ticket informado deve ter uma quantidade mínima de 1 componente
#  - o ticket informado deve estar na fase correta de desenvolvimento
# ######################################################################


# Funcao de retornar o conteudo do arquivo
def read(file_path):
    """ Read a file and return it's contents. """
    with open(file_path) as f:
        return f.read()


JIRA_SERVER = 'https://jira.mv.com.br'
CONSUMER_KEY = 'OauthKey'
#Verifica o diretorio onde esta configurado o HOOKS
HOOKS_PATH = str(subprocess.check_output("git config --global core.hooksPath", shell=True, universal_newlines=True))
#Monta o diretório de aocrdo com o diretorio padrao dos HOOKS
RSA_KEY = read(os.path.join(HOOKS_PATH.strip(),'keys/jira_git_hooks_soulmv_privatekey.pem'))

#Documentacao oficial de referencia para as validacoes dos HOOKS
DOCS_REF = 'https://docs.mv.com.br/x/cTq_Aw'

# Dados do Usuario
USER_TOKEN = ''
USER_TOKEN_SECRET = ''
# Lista com os possives status a serem validados pela regra#
ISSUE_STATUS = ['EM DESENVOLVIMENTO', 'EM ANDAMENTO', 'EM VALIDAÇÃO DO DESENVOLVIMENTO','EM EXECUÇÃO', 'IN PROGRESS']
ISSUE_TYPE_EXCEPT = ['TASK', 'TAREFA']


def main():
    # tipos de logs para uso: "CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET"
    logging.basicConfig(level=logging.INFO, format='MV..' + ": %(message)s")


    # pega a mensagem de commit realizada
    commit_message_file = open(sys.argv[1])
    #log Mensagem pedido de commit
    #logaccess('PEDIDO DE COMMIT')
    commit_message = commit_message_file.read().strip()

    # testa o comentário para ver se segue os padrões
    issue_jira = teste_comentario(commit_message)

    # para o processo caso o padrão de comentário não seja respeitado
    if issue_jira is None:
        return -1

    # loga feedback para o usuário, informando o ticket de trabalho
    logging.info("Pedido de commit referente ao ticket: %s", issue_jira)

    # para o processo caso os padrões do JIRA não seja respeitado
    if not teste_ticket(issue_jira):
        return -1

    # retorna ZERO (0) quando é sucesso (para testes deixar em -1)
    logging.info("Validacoes de desenvolvimento realizado com SUCESSO.")
    return 0


################################
def ler_variavel_local():
    try:
        global USER_TOKEN
        USER_TOKEN = str(subprocess.check_output("git config --global --get jirahooks.USERTOKEN", shell=True,
                                                 universal_newlines=False).decode("utf-8")).replace('\'', '').strip(
            '\n')

        global USER_TOKEN_SECRET

        USER_TOKEN_SECRET = str(
            subprocess.check_output("git config --global --get jirahooks.USERTOKENSECRET", shell=True,
                                    universal_newlines=False).decode("utf-8")).replace('\'', '').strip('\n')

        if (str(USER_TOKEN).strip and str(USER_TOKEN_SECRET).strip):
            return True

    except subprocess.CalledProcessError:
        logging.error("\033[1;31;40m except subprocess.CalledProcessError:")
        USER_TOKEN = ''
        USER_TOKEN_SECRET = ''
        return False


# ######################################################################
# teste do padrão do comentário
#  - limite mínimo de 15 caractéres
#  - deve ter referência ao padrão de ticket do JIRA
# ######################################################################
def teste_comentario(commit_message):
    required_regex = "[A-Z]{2,}-\\d+"
    required_length = 15
    issue_jira = re.search(required_regex, commit_message)

    if len(commit_message) < required_length:
        msg1='teste_comentario_required_length'
        #logaccess(msg1)
        logging.info("\033[1;31;40m Sua mensagem parece pequena, detalhe mais a sua alteracao, com mais de 15 caracteres.")
        logging.info("Referencia: %s", DOCS_REF)
        return None

    if issue_jira is None:
        msg2='teste_comentario_issue_jira'
        #logaccess(msg2)
        logging.info("\033[1;31;40m Sua mensagem do commit nao faz referencia a um ticket no JIRA no padrao: PROJETO-999999. Note que o codigo do projeto deve estar maiusculo.)")
        logging.info("Referencia: %s", "\x1b]8;;"+DOCS_REF+"\aCtrl+Click here\x1b]8;;\a")
        return None

    return issue_jira.group(0).replace('#', '', 1)


# ######################################################################
# teste de validade do ticket
#  - existência do ticket
#  - quantidade mínima de 1 componente
#  - fase correta de desenvolvimento
# ######################################################################
def teste_ticket(issue_jira):
    erro = 0
    if (ler_variavel_local()):
        try:
            # ler variaveis#
            # logging.debug("USER_TOKEN: %s", str(USER_TOKEN))
            # logging.debug("USER_TOKEN_SECRET: %s", str(USER_TOKEN_SECRET).strip('\n'))

            oauth_dict = {
                'access_token': str(USER_TOKEN),
                'access_token_secret': str(USER_TOKEN_SECRET),
                'consumer_key': CONSUMER_KEY,
                'key_cert': RSA_KEY
            }
            #print(oauth_dict)
            # logging.debug("oauth_dict: '%s'", JIRA(oauth=oauth_dict, options={'server': JIRA_SERVER}))
            # SSSlogging.error("JIRA_SERVER: '%s'", JIRA_SERVER)
            # logging.debug("USER_TOKEN: %s", USER_TOKEN)
            jira = JIRA(oauth=oauth_dict, options={'server': JIRA_SERVER})
            # print(jira.user)

            # Teste de conexao, listar os projetos#
            # for project in jira.projects():
            # print(project.key)

            # logging.error("issue_jira: '%s'", issue_jira)
            issue = jira.issue(issue_jira)
            # logging.error("issue: '%s'", issue)
            # print(issue.fields.components)
            if str(issue.fields.issuetype).upper() not in ISSUE_TYPE_EXCEPT and len(issue.fields.components) < 1:
                msg3 = 'teste_ticket_components'
                #logaccess(msg3)
                logging.info("\033[1;31;40mVoce deve informar pelo menos 1 componente para o ticket: %s", issue_jira)
                logging.info("Referencia: %s", DOCS_REF)
                return False

            # if (str(issue.fields.status).upper() != ISSUE_STATUS_EM_DESENVOLVIMENTO.upper()) and (str(issue.fields.status).upper() != ISSUE_STATUS_EM_ANDAMENTO.upper())  :
            if (str(issue.fields.status).upper() not in ISSUE_STATUS):
                msg4 = 'teste_ticketstatus_status'
                #logaccess(msg4)
                logging.info(
                    "\033[1;31;40mO ticket '%s' encontra-se na fase '%s' e para realizar alteracoes deveria estar na fase '%s'.",
                    issue.key, issue.fields.status, str(ISSUE_STATUS))
                logging.info("Referencia: %s", DOCS_REF)
                return False


        except KeyboardInterrupt:
            logging.info("...interrupcao por comando do teclado")
            return False

        except JIRAError as e:

            erro = e.status_code

            if erro == 401:
                logging.info("ATENCAO: Login no JIRA falhou, verifique o usuário e senha.")
                return False

            elif erro == 404:
                logging.info("ATENCAO: O ticket informado nao foi encontrado no respositorio do JIRA: %s", issue_jira)
                return False

            else:
                logging.error("recuperacao das informacaos JIRA: '%s'", e.args)
                return False

        except Exception as e:
            logging.error("recuperacao das informacaos JIRA: '%s'", e.args)
            return False

        finally:
            if erro != 401:
                jira.close()
    else:
        logging.error("ERROR: Erro ao carregar os tokens")
    return True


# ######################################################################
# pega o ticket de uma branch de hotfix
# ######################################################################
def git_get_ticket_branch_hotfix():
    try:

        proc = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True)
        resposta = str(proc.stdout)
        resposta = resposta.replace('b', '', 1)
        resposta = resposta.replace('\'', '', 2)
        resposta = resposta.replace('\\n', '', 1)
        resposta = resposta.replace('hotfix/', '', 1)
        resposta = resposta.rstrip('\n')

        # issue_jira = git_get_curr_branchname()
        return resposta

    except KeyboardInterrupt:
        logging.info("...interrupcao por comando do teclado")
        return None

    except Exception as e:
        logging.erro("Execucao do comando: '%s'", e.args)
        return None

def logaccess(msg):
    try:
        print(socket.gethostname())
        print(socket.gethostbyname(socket.gethostname()))

        url = 'http://192.168.1.41:5000/AddHost?msg='+str(msg)+'&hostname='+str(socket.gethostname())
        print(url)

        response = requests.get(url)
    except Exception:
        print('')


# ######################################################################
# python script entry point. Dispatches main()
# - última linha do código de execução
# #######################################################################
if __name__ == "__main__":
     exit(main())