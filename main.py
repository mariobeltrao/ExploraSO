"""OS Explorer: serviços do SO por meio de APIs de alto nível do Python."""

import os
from pathlib import Path
import platform
import subprocess
import sys


BASE = Path(__file__).resolve().parent
DATA = BASE / "data"


def caminho_seguro(nome):
    """Recusa links que desviem os arquivos demonstrativos para fora de data."""
    if DATA.is_symlink() or DATA.resolve() != BASE / "data":
        raise ValueError("A pasta data deve ser uma pasta real dentro do projeto.")
    DATA.mkdir(exist_ok=True)
    caminho = DATA / nome
    if caminho.is_symlink() or caminho.resolve().parent != DATA.resolve():
        raise ValueError("O destino deve permanecer diretamente dentro de data.")
    return caminho


def explicar(categoria, operacao, api, servico):
    print(f"\nCategoria: {categoria}")
    print(f"Operação: {operacao}")
    print(f"API/Função utilizada: {api}")
    print(f"Serviço do SO: {servico}")


def criar_arquivo():
    arquivo = caminho_seguro("exemplo.txt")
    try:
        # O modo x cria sem sobrescrever um arquivo que já existe.
        with arquivo.open("x", encoding="utf-8"):
            pass
        print("Arquivo criado com sucesso: data/exemplo.txt")
    except FileExistsError:
        print("data/exemplo.txt já existe; seu conteúdo foi preservado.")
    explicar("Arquivos", "Criação de arquivo", "Path.open('x')",
             "Gerenciamento do sistema de arquivos")


def escrever_ler_arquivo():
    arquivo = caminho_seguro("leitura_escrita.txt")
    # Aplicação -> Python/runtime -> mecanismos do SO -> kernel/recurso.
    # open, write e read são abstrações de alto nível, não necessariamente
    # chamadas de sistema específicas. with fecha o recurso mesmo com erros.
    with arquivo.open("w", encoding="utf-8") as recurso:
        recurso.write("Olá! O OS Explorer utiliza serviços do Sistema Operacional.\n")
    with arquivo.open("r", encoding="utf-8") as recurso:
        conteudo = recurso.read()
    print("Conteúdo escrito, arquivo fechado e reaberto: data/leitura_escrita.txt")
    print(conteudo, end="")
    explicar("Arquivos", "Escrita e leitura", "Path.open(), write(), read()",
             "Gerenciamento de arquivos e entrada/saída")


def criar_listar_diretorio():
    diretorio = caminho_seguro("teste")
    try:
        diretorio.mkdir()
        print("Diretório criado: data/teste/")
    except FileExistsError:
        if not diretorio.is_dir():
            raise ValueError("data/teste existe, mas não é um diretório.")
        print("Diretório data/teste/ já existe; pode ser reutilizado.")
    print("Conteúdo de data/:")
    for item in sorted(DATA.iterdir(), key=lambda p: p.name.lower()):
        print(f"  {item.name}")
    print("Conteúdo de data/teste/:")
    itens = sorted(diretorio.iterdir(), key=lambda p: p.name.lower())
    for item in itens:
        print(f"  {item.name}")
    if not itens:
        print("  (diretório vazio)")
    explicar("Diretórios", "Criação e listagem", "Path.mkdir(), Path.iterdir()",
             "Gerenciamento do sistema de arquivos/diretórios")


def mostrar_sistema():
    print(f"Sistema operacional: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Arquitetura da máquina: {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    explicar("Sistema", "Consulta ao ambiente",
             "platform.system(), release(), machine(), python_version()",
             "Disponibilização de informações do sistema e do ambiente")


def mostrar_pid():
    # PID (Process Identifier) é o identificador associado pelo SO ao processo.
    # os.getpid() é a interface de alto nível usada para consultar esse dado.
    print(f"PID do processo atual: {os.getpid()}")
    explicar("Processos", "Consulta do PID", "os.getpid()",
             "Gerenciamento de processos")


def criar_processo_filho():
    filho = BASE / "filho.py"
    if not filho.is_file():
        raise FileNotFoundError("filho.py não foi encontrado na pasta do projeto.")
    print(f"PID do processo pai: {os.getpid()}", flush=True)
    print("Criando processo filho...", flush=True)
    # O SO gerencia criação, execução, identificação e finalização de processos.
    # subprocess é uma API de alto nível; wait sincroniza pai e filho.
    with subprocess.Popen([sys.executable, "-u", str(filho)]) as processo:
        print(f"PID do processo filho: {processo.pid}", flush=True)
        try:
            codigo = processo.wait()
        except KeyboardInterrupt:
            # Interrompe somente o filho criado por esta aplicação.
            if processo.poll() is None:
                processo.terminate()
            processo.wait()
            raise
    print(f"Processo filho finalizado. Código de saída: {codigo}")
    if codigo != 0:
        raise RuntimeError(f"O processo filho terminou com erro (código {codigo}).")
    explicar("Processos", "Criação e espera pelo filho",
             "subprocess.Popen(), sys.executable, Popen.pid, Popen.wait()",
             "Gerenciamento do ciclo de vida e sincronização de processos")


def demonstracao_completa():
    etapas = [
        ("SISTEMA DE ARQUIVOS", [criar_listar_diretorio, criar_arquivo,
                                  escrever_ler_arquivo]),
        ("INFORMAÇÕES DO SISTEMA", [mostrar_sistema]),
        ("PROCESSOS", [mostrar_pid, criar_processo_filho]),
    ]
    for numero, (titulo, operacoes) in enumerate(etapas, start=1):
        print(f"\n{'-' * 54}\nDEMONSTRAÇÃO {numero} — {titulo}\n{'-' * 54}")
        for operacao in operacoes:
            operacao()
    print("\nDemonstração completa concluída.")


def menu():
    opcoes = {
        "1": ("Criar arquivo", criar_arquivo),
        "2": ("Escrever e ler arquivo", escrever_ler_arquivo),
        "3": ("Criar e listar diretório", criar_listar_diretorio),
        "4": ("Mostrar informações do sistema", mostrar_sistema),
        "5": ("Mostrar PID do processo atual", mostrar_pid),
        "6": ("Criar processo filho", criar_processo_filho),
        "7": ("Demonstração completa", demonstracao_completa),
    }
    while True:
        print(f"\n{'=' * 54}\n                    OS EXPLORER")
        print(f"       Serviços do Sistema Operacional\n{'=' * 54}")
        for chave, (titulo, _) in opcoes.items():
            print(f"[{chave}] {titulo}")
        print("[0] Sair")
        try:
            escolha = input("Escolha uma opção: ").strip()
            if escolha == "0":
                print("OS Explorer encerrado.")
                return
            if escolha not in opcoes:
                print("Entrada inválida. Digite um número de 0 a 7.")
                continue
            opcoes[escolha][1]()
        except FileNotFoundError as erro:
            print(f"Arquivo ou diretório não encontrado: {erro}")
        except PermissionError as erro:
            print(f"Sem permissão para executar a operação: {erro}")
        except (OSError, ValueError, RuntimeError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nOS Explorer encerrado.")
            return


if __name__ == "__main__":
    menu()
