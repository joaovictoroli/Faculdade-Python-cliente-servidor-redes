import socket, os, pickle
import psutil
import cpuinfo
import netifaces
import time
import multiprocessing
import nmap


class Servidor():
    running = True
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = socket.gethostname()  
    porta = 8080


    def __init__(self):
        self.socket_servidor.bind((self.host, self.porta))
        self.socket_servidor.listen()

class CPU:
    info_processador = cpuinfo.get_cpu_info()
    modelo = info_processador['brand_raw']
    hertz = str(info_processador['hz_advertised_friendly'])
    qt_threads = str(info_processador['count'])
    qt_nucleos = str(info_processador['l2_cache_associativity'])
    arch = str(info_processador['arch'])
    cpu_percem = str(psutil.cpu_percent(interval=0))
    threads_percem = psutil.cpu_percent(percpu=True)

class Memoria:
    disco = psutil.disk_usage('/')
    disco_total = disco.total
    disco_usada = disco.used
    disco_percem = disco.percent
    
    memoria = psutil.virtual_memory()
    memoria_total = memoria.total
    memoria_disponivel = memoria.available
    memoria_percem = memoria.percent

class Processos:
    dict_proc_bymem = []
    pid_detalhe_proc = ''

    def __init__(self):
        list_proc = []
        for proc in psutil.process_iter():
            try:
                info = proc.as_dict(attrs=['pid', 'name', 'username'])
                info['vms'] = proc.memory_info().vms / (1024 * 1024)
                list_proc.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        list_proc = sorted(list_proc, key=lambda info: info['vms'], reverse=True)


        for i in range(len(list_proc[:10])):
            process = psutil.Process(list_proc[:10][i]['pid'])
            #process.cpu_percent(interval=None)
            list_proc[:10][i]['detalhe_pid'] = {
                'nome': process.name(),
                'tempo_exec': time.ctime(process.create_time()),
                'tempo_usuario': str(round(process.cpu_times().user, 2)),
                'tempo_sistema': str(round(process.cpu_times().system, 2)),
                'cpu_uso': str(round(process.cpu_percent(interval=0.1)/multiprocessing.cpu_count(), 2)),
                'mem_uso': str(round(process.memory_percent(), 2)),
                'executavel': process.exe()
                }

            try:
                str(round(os.stat(process.exe()).st_size/1000))
                str(round(os.stat(process.exe()).st_atime))
                str(round(os.stat(process.exe()).st_mtime))
                status = True
            except:
                status = False
            if status:
                list_proc[:10][i]['detalhe_pid']['tamanho_exec'] = str(round(os.stat(process.exe()).st_size / 1000))
                list_proc[:10][i]['detalhe_pid']['tempo_criacao'] = str(time.ctime(os.stat(process.exe()).st_atime))
                list_proc[:10][i]['detalhe_pid']['tempo_modificacao'] = str(time.ctime(os.stat(process.exe()).st_mtime))
    
        self.dict_proc_bymem = list_proc[:10]

class Redes:
    ip = str(psutil.net_if_addrs()['Ethernet'][1].address)
    mascara = str(psutil.net_if_addrs()['Ethernet'][1].netmask)
    gateway =  str(netifaces.gateways()['default'][netifaces.AF_INET][0])
    info_bytes = psutil.net_io_counters()
    dados_env = str(round(info_bytes[0]/1024/1024, 2))
    dados_rec = str(round(info_bytes[1]/1024/1024, 2))
    dado_port_tcp = []

    def scan(self):
        print('Iniciando port scan.')
        nm = nmap.PortScanner()
        resposta = nm.scan(self.gateway + '-')
        print('Scan realizado.')
        for ip in resposta['scan']:
            #print(resposta['scan'][key]['addresses']['ipv4'])
            try:
                portas = resposta['scan'][ip]['tcp']
                list_port = []
                list_states = []
                for key in portas:
                    list_port.append(str(key))
                    list_states.append(portas[key]['state'])
                
                self.dado_port_tcp.append({'ipv4': resposta['scan'][ip]['addresses']['ipv4'], 
                'ports': list_port, 'states': list_states})
            except Exception as erro:
                print('Erro: ', str(erro)) #resposta['scan'])
            # erro no resposta['scan'][ip]['tcp']?

def main():
    server = Servidor()
    Redes().scan()
    #print(Redes().dado_port_tcp)
    print("Servidor de nome", server.host, "esperando conexão na porta", server.porta)
    while server.running:
        # Aceita alguma conexão
        (socket_cliente,addr) = server.socket_servidor.accept()
        print("Conectado a:", str(addr))
        msg = socket_cliente.recv(1024)
        nome = msg.decode('utf-8')
        # reply do request
        if nome == 'request':
            # dado_para_cliente = 'reply'

            # CPU
            dado_para_cliente = {'CPU': {'modelo': CPU().modelo, 'hertz': CPU().hertz, 
            'qt_threads': CPU().qt_threads, 'qt_nucleos': CPU().qt_nucleos, 'arch': CPU().arch,
            'cpu_percem': CPU().cpu_percem, 'threads_percem': CPU().threads_percem
            },
            # MEMORIA - disco + mem
            'MEMORIA': {'disco_total': Memoria().disco.total, 'disco_usado': Memoria().disco.used, 
            'disco_percem': Memoria().disco.percent, 'memoria_total': Memoria().memoria_total,
            'memoria_disponivel':  Memoria().memoria_disponivel,
            'memoria_percem':  Memoria().memoria_percem
            },
            # REDE
            'REDES': {'ip': Redes().ip, 'mascara': Redes().mascara, 'gateway': Redes().gateway,
            'dados_env': Redes().dados_env, 'dados_rec': Redes().dados_rec,
            'info': Redes().dado_port_tcp[:5]
            },
            # PROCESSOS
            'PROCESSOS': {'proc_by_mem': Processos().dict_proc_bymem
            }}
        else:
            dado_para_cliente = 'error'

        # converte a msg - dic > bytes
        bytes = pickle.dumps(dado_para_cliente)
        socket_cliente.send(bytes)
        print('Resposta enviada:', str(addr))

        socket_cliente.close()
        print('Fechando conexão:', str(addr))


if __name__ == '__main__':
    main()