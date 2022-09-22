import socket, sys, pickle
import pygame
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, K_ESCAPE
from pygame.locals import (
    K_RIGHT,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    QUIT,
)

# classes
class Cliente():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg = 'request'
    reply = {} #sera preenchido com a resposta do servidor

    # estabelece conexão
    def __init__(self):
        try:
            self.s.connect((socket.gethostname(), 8080))

        except Exception as erro:
            print(str(erro))
            sys.exit(1)

    # envia msg para ser trabalhada no servidor
    def send_request(self):
        try:
            self.s.send(self.msg.encode('utf-8'))
            dados_em_bytes = self.s.recv(100000)
            resposta = pickle.loads(dados_em_bytes)
            #print(resposta)
            self.reply = resposta

        except Exception as erro:
            print(str(erro))
            sys.exit(1)
        

    # decodica resposta do servidor - em bytes 
    def get_reply(self, dados_em_bytes):
        resposta = pickle.loads(dados_em_bytes)
        # print(resposta)

class Interface():
    nome = 'TP9 - PB - João Victor ADS'
    altura = 800
    largura = 600
    tamanho_tela = (altura, largura)
    rodando = True
    count = 60
    # 1 = CPU // 2 = Memoria // 3- Redes
    tela = 1
    detalhe = ''
    detalhe_proc = 0

class Cores():
    amarelo = (255, 255, 0)
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    vermelho = (255, 0, 0)
    azul = (0, 0, 255)

#metodos
def escrever_texto(texto, tamanho_fonte, cor, pos_x, pos_y):
    pygame.font.init()
    font = pygame.font.Font(None, tamanho_fonte)
    texto = font.render(texto, True, cor)
    tela.blit(texto, (pos_x, pos_y))

def desenhar_menu(cliente):
    tela.fill(Cores().preto)
    pygame.draw.rect(tela, Cores().branco, (5, 5, 790, 37), 1)
    pygame.draw.rect(tela, Cores().branco, (267, 5, 528, 37), 1)
    pygame.draw.rect(tela, Cores().branco, (503, 5, 292, 37), 1)
    # rodape
    pygame.draw.rect(tela, Cores().branco, (5, 560, 790, 37), 1)
    escrever_texto('TP9 João Victor de Oliveira', 30, Cores().branco, 10, 568)
    #escrever_texto('Enviar relatorio', 30, Cores().vermelho, 590, 568)
    if program.tela == 1:
        escrever_texto('CPU', 32, Cores().vermelho, 100, 10)
        interface_cpu(cliente.reply['CPU'])
    else:
        escrever_texto('CPU', 32, Cores().branco, 100, 10)

    if program.tela == 2 and program.detalhe == '':
        escrever_texto('Memoria', 32, Cores().vermelho, 335, 10)
        interface_memoria(cliente.reply['MEMORIA'])
    else:
        escrever_texto('Memoria', 32, Cores().branco, 335, 10)
    if program.tela == 2 and program.detalhe == 'lista':
        escrever_texto('Memoria', 32, Cores().vermelho, 335, 10)
        interface_listar_processos(cliente.reply['PROCESSOS'])
    if program.tela == 2 and program.detalhe == 'detalhe_proc':
        escrever_texto('Memoria', 32, Cores().vermelho, 335, 10)
        interface_detalhe_proc(cliente.reply['PROCESSOS']['proc_by_mem'][program.detalhe_proc]['detalhe_pid'])
        # print(cliente.reply['PROCESSOS']['proc_by_mem'][program.detalhe_proc]['detalhe_pid'])

    if program.tela == 3:
        escrever_texto('Redes', 32, Cores().vermelho, 600, 10)
        interface_redes(cliente.reply['REDES'])
    else:
        escrever_texto('Redes', 32, Cores().branco, 600, 10)
    pygame.display.update()

def interface_cpu(dic):
    escrever_texto('MODELO: ' + dic['modelo'], 26, Cores().branco, 25, 50)
    escrever_texto('USO DA CPU: ', 26, Cores().branco, 550, 50)

    pygame.draw.rect(tela, Cores().azul, (550, 92, 225, 75))
    coeficiente = float(dic['cpu_percem']) * 2.25
    pygame.draw.rect(tela, Cores().vermelho, (550, 92, coeficiente, 75))
    escrever_texto(str(dic['cpu_percem']) + '%', 26, Cores().branco, 645, 122)


    pos_y = 50 + 32 + 10
    escrever_texto('NUCLEOS: ' + dic['qt_nucleos'], 26, Cores().branco, 25, pos_y)
    pos_y += + 32 + 10
    escrever_texto('THREADS: ' + dic['qt_threads'], 26, Cores().branco, 25, pos_y)

    pos_x = 25
    for i in range (0, len(dic['threads_percem'])):
        pygame.draw.rect(tela, Cores().azul, (pos_x, 302, 50, 240))
        pygame.draw.rect(tela, Cores().vermelho, (pos_x, 302, 50, dic['threads_percem'][i] * 2.4))
        pos_x = pos_x + 65
    
    pos_x = 32
    for i in range (0, len(dic['threads_percem'])):
        escrever_texto(str(dic['threads_percem'][i]) + "%", 24, Cores().branco, pos_x, 402)
        pos_x = pos_x + 65



    pos_y += + 32 + 10
    escrever_texto('FREQUENCIA: ' + dic['hertz'], 26, Cores().branco, 25, pos_y)
    pos_y += + 32 + 10
    escrever_texto('ARCH: ' + dic['arch'], 26, Cores().branco, 25, pos_y)
    pos_y += + 32 + 10
    escrever_texto('USO DAS THREADS: ', 26, Cores().branco, 25, pos_y)
    pos_y += + 32 + 10

def interface_memoria(dic):
    escrever_texto('DISCO: ', 26, Cores().branco, 25, 50)
    pos_y = 50 + 32 + 10
    escrever_texto('TOTAL: ' + str(round(dic['disco_total']/ 10**9, 2)) + ' GB', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('USADA: ' + str(round(dic['disco_usado']/ 10**9, 2)) + ' GB', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10

    # grafico disco
    pygame.draw.rect(tela, Cores().azul, (240, 92, 250, 50))
    pygame.draw.rect(tela, Cores().vermelho, (240, 92, dic['disco_percem'] * 2.5, 50))
    escrever_texto(str(dic['disco_percem']) + '%', 24, Cores().branco, 360, 111)

    # grafico memoria
    pygame.draw.rect(tela, Cores().azul, (240, 216, 250, 50))
    pygame.draw.rect(tela, Cores().vermelho, (240, 216, dic['memoria_percem'] * 2.5, 50))
    escrever_texto(str(dic['memoria_percem']) + '%', 24, Cores().branco, 360, 235)

    pos_y = 174
    escrever_texto('MEMORIA: ', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('TOTAL: ' + str(round(dic['memoria_total']/ 10**9, 2)) + ' GB', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('DISPONIVEL: ' + str(round(dic['memoria_disponivel']/ 10**9, 2)) + ' GB', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('Processos com maior uso de memoria', 26, Cores().branco, 25, pos_y)
    escrever_texto('aqui', 26, Cores().azul, 350, pos_y)

def interface_listar_processos(dic):
    escrever_texto('Lista de processos com maior uso de memoria', 26, Cores().branco, 25, 50)
    pos_y = 50 + 32 + 10
    escrever_texto('NOME ', 26, Cores().branco, 25, pos_y)
    escrever_texto('MAQUINA ', 26, Cores().branco, 250, pos_y)
    escrever_texto('PID ', 26, Cores().branco, 450, pos_y)
    escrever_texto('VMS ', 26, Cores().branco, 650, pos_y)

    #
    dinamic_x = 25
    dinamic_y = 127
    for i in range(0, len(dic['proc_by_mem'])):
        nome = dic['proc_by_mem'][i]['name']
        maquina = dic['proc_by_mem'][i]['username']
        pid = dic['proc_by_mem'][i]['pid']
        vms = dic['proc_by_mem'][i]['vms']
        escrever_texto(nome, 18, Cores().branco, dinamic_x, dinamic_y)
        dinamic_x = dinamic_x + 200
        escrever_texto(maquina, 18, Cores().branco, dinamic_x, dinamic_y)
        dinamic_x = dinamic_x + 210
        escrever_texto(str(pid), 18, Cores().branco, dinamic_x, dinamic_y)
        dinamic_x = dinamic_x + 200
        escrever_texto(str(vms), 18, Cores().branco, dinamic_x, dinamic_y)
        dinamic_x = 25
        dinamic_y = dinamic_y + 40

def interface_detalhe_proc(dic):
    escrever_texto('nome: ' + dic['nome'], 26, Cores().branco, 25, 50)
    pos_y = 50 + 32 + 10
    escrever_texto('tempo de execução: ' + dic['tempo_exec'], 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('tempo de usuario: ' + dic['tempo_usuario'] + ' s', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('tempo de sistema: ' + dic['tempo_sistema'] + ' s', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('percentual de uso do cpu: ' + dic['cpu_uso'] + "%", 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('percentual de memoria ram: ' + dic['mem_uso'] + "%", 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('executavel: ' + dic['executavel'], 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    if dic['tamanho_exec']:
        escrever_texto("tamanho do executavel: " + dic['tamanho_exec'] + " KB ", 26, Cores().branco, 25, pos_y)
        pos_y += 32 + 10
        escrever_texto("tempo de criacao: " + dic['tempo_criacao'], 26, Cores().branco, 25, pos_y)
        pos_y += 32 + 10
        escrever_texto("tempo de modificacao: " + dic['tempo_modificacao'], 26, Cores().branco, 25, pos_y)

def interface_redes(dic):
    escrever_texto('IP: ' + dic['ip'], 26, Cores().branco, 25, 50)
    pos_y = 50 + 32 + 10
    escrever_texto('GATEWAY: ' + dic['gateway'], 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('MASCARA: ' + dic['mascara'], 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('DADOS ENVIADOS: ' + dic['dados_env'] + ' Megas', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('DADOS RECEBIDOS: ' + dic['dados_rec'] + ' Megas', 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('DADOS PORT SCANNER DA SUB REDE:' , 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    escrever_texto('IP   |  PORTA/ESTADO ' , 26, Cores().branco, 25, pos_y)
    pos_y += 32 + 10
    #print(pos_y) = 344
    dinamic_x = 25
    dinamic_y = 344
    #print(dic['info'])
    for element in range(0, len(dic['info'])):
        escrever_texto(dic['info'][element]['ipv4'], 26, Cores().branco, dinamic_x, dinamic_y)
        for port_state in range(len(dic['info'][element]['ports'])):
            dinamic_y += 17 + 5
            escrever_texto(dic['info'][element]['ports'][port_state] + ': ' + dic['info'][element]['states'][port_state], 17, Cores().branco, dinamic_x, dinamic_y)

        dinamic_x += 150
        dinamic_y = 344
    # + dic['info'][0]['ipv4']


def mudar_tela(direcao):
    program.detalhe = ''
    if direcao == 'direita':
        if program.tela == 3:
            program.tela = 1
        else:
            program.tela += 1
    elif direcao == 'esquerda':
        if program.tela == 1:
            program.tela = 3
        else:
            program.tela -= 1  
    
# main
program = Interface()
pygame.init()
pygame.display.set_caption(program.nome)
tela = pygame.display.set_mode(program.tamanho_tela)
def main():
    print('Conectando-se ao servidor...')
    client = Cliente()
    client.send_request()
    print('Conexão realizada com sucesso.')
    desenhar_menu(client)

    while program.rodando:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                mudar_tela('direita')
                desenhar_menu(client)

            elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
                mudar_tela('esquerda')
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 350 and \
                    pygame.mouse.get_pos()[0] < 380 and pygame.mouse.get_pos()[1] > 300 and pygame.mouse.get_pos()[
                1] < 350 and program.tela == 2:
                program.detalhe = 'lista'
                desenhar_menu(client)
            
            # detalhe proc

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 127 and pygame.mouse.get_pos()[
                1] < 147 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 0
                desenhar_menu(client)


            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 147 and pygame.mouse.get_pos()[
                1] < 187 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 1
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 187 and pygame.mouse.get_pos()[
                1] < 227 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 2
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 227 and pygame.mouse.get_pos()[
                1] < 267 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 3
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 267 and pygame.mouse.get_pos()[
                1] < 307 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 4
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 307 and pygame.mouse.get_pos()[
                1] < 347 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 5
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 347 and pygame.mouse.get_pos()[
                1] < 387 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 6
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 387 and pygame.mouse.get_pos()[
                1] < 427 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 7
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 427 and pygame.mouse.get_pos()[
                1] < 467 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 8
                desenhar_menu(client)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] > 0 and \
                    pygame.mouse.get_pos()[0] < 600 and pygame.mouse.get_pos()[1] > 467 and pygame.mouse.get_pos()[
                1] < 507 and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = 'detalhe_proc'
                program.detalhe_proc = 9
                desenhar_menu(client)

            # volta da tela de memoria > lista > detalhe
            elif event.type == KEYDOWN and event.key == K_ESCAPE and program.tela == 2 and program.detalhe == 'lista':
                program.detalhe = ''
                desenhar_menu(client)

            elif event.type == KEYDOWN and event.key == K_ESCAPE and program.tela == 2 and program.detalhe == 'detalhe_proc':
                program.detalhe = 'lista'
                desenhar_menu(client)


if __name__ == '__main__':
    main()


# Fecha conexão com o servidor
#s.close()