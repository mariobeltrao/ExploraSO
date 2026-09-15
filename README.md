# OS Explorer

Explorador de Serviços do Sistema Operacional — aplicação acadêmica de terminal,
em Python 3, sem dependências externas.

## Objetivo

Demonstrar seis operações em quatro categorias de serviços do SO: **Arquivos,
Diretórios, Sistema e Processos**. O código prioriza leitura e apresentação em aula.

## Conceito

```text
Aplicação → API / Biblioteca / Runtime → Serviço do SO → Kernel → Recurso
```

Esse fluxo é um modelo conceitual. A aplicação utiliza interfaces Python;
o runtime e as bibliotecas recorrem aos mecanismos disponíveis no sistema.
Funções como `open()`, `read()`, `write()`, `os.getpid()` e `subprocess.Popen()`
**não devem ser confundidas automaticamente com System Calls específicas**.
O caminho interno varia conforme o SO e a implementação do Python, e nem toda
consulta exige uma nova entrada no kernel: informações podem vir do runtime
ou de dados em cache. A versão do Python, por exemplo, descreve o runtime.

Arquivos e diretórios são separados em categorias didáticas da atividade,
embora ambos façam parte do gerenciamento do sistema de arquivos.

## Categorias implementadas

| Categoria | Operação | API/Função | Serviço do SO |
|-----------|----------|------------|---------------|
| Arquivos | Criar arquivo | `Path.open('x')` | Gerenciamento do sistema de arquivos |
| Arquivos | Escrever e ler | `Path.open()`, `write()`, `read()` | Arquivos e entrada/saída |
| Diretórios | Criar e listar | `Path.mkdir()`, `Path.iterdir()` | Gerenciamento de diretórios |
| Sistema | Consultar ambiente | `platform.system()`, `release()`, `machine()`, `python_version()` | Informações do sistema e do runtime |
| Processos | Consultar PID | `os.getpid()` | Identificação de processos |
| Processos | Criar filho e aguardar | `subprocess.Popen()`, `Popen.pid`, `Popen.wait()` | Ciclo de vida e sincronização de processos |

## Funcionalidades

- **1 — Criar arquivo:** cria `data/exemplo.txt` sem sobrescrever se já existir.
- **2 — Escrever e ler:** grava uma frase em `data/leitura_escrita.txt`, fecha,
  reabre e exibe o conteúdo. A cada execução, substitui o conteúdo desse arquivo demonstrativo.
- **3 — Diretórios:** cria `data/teste/`, lista `data/` e o diretório criado.
  Um diretório vazio é identificado; executar novamente reutiliza a pasta.
- **4 — Sistema:** exibe SO, release, arquitetura da máquina e versão do Python.
  Não consulta nome de usuário, nome da máquina nem outros identificadores pessoais.
- **5 — PID:** mostra o identificador do próprio processo.
- **6 — Processo filho:** mostra os PIDs do pai e filho, executa `filho.py`
  durante dois segundos e aguarda seu término, exibindo o código de saída.
- **7 — Demonstração completa:** executa as seis operações em três etapas visuais.
- **0 — Sair:** encerra o menu. EOF e Ctrl+C também encerram a aplicação.

Cada operação exibe categoria, API utilizada e serviço envolvido.

## Estrutura do projeto

```text
ExploraSO/
├── main.py
├── filho.py
├── README.md
├── .gitignore
└── data/
    ├── .gitkeep
    ├── exemplo.txt           # gerado pela opção 1
    ├── leitura_escrita.txt   # gerado pela opção 2
    └── teste/               # gerado pela opção 3
```

Os resultados em `data/` são ignorados pelo Git. Não é necessário instalar pacotes.

## Como executar

Abra o terminal na pasta do projeto. É necessário ter Python 3 instalado.

Windows:

```powershell
python main.py
```

Ou:

```powershell
py main.py
```

Linux/macOS:

```sh
python3 main.py
```

Os caminhos são calculados a partir de `main.py`, portanto também é possível
executar o programa por seu caminho completo a partir de outro diretório.

## Demonstração

Escolha **7**. O programa cria e lista o diretório, cria o arquivo, escreve e lê,
consulta o sistema, mostra o PID e inicia o filho. Espere cerca de dois segundos
até a mensagem de finalização. O menu reaparece; escolha **0** para sair.
A demonstração pode ser repetida. Se uma etapa falhar, o erro é exibido e o
controle retorna ao menu, sem anunciar conclusão da demonstração.

## Guia para apresentação

| Opção | O que foi implementado? | Qual API/função? | Qual serviço do SO? | Como demonstrar? |
|-------|------------------------|-----------------|--------------------|-----------------|
| 1 | Criação sem sobrescrita | `Path.open('x')` | Sistema de arquivos | Escolher 1; repetir para mostrar preservação do arquivo |
| 2 | Escrita, fechamento, reabertura e leitura | `Path.open()`, `write()`, `read()` com `with` | Arquivos e entrada/saída | Escolher 2 e ler a frase exibida; mostrar os dois blocos `with` |
| 3 | Criação e listagem de pastas | `Path.mkdir()`, `Path.iterdir()` | Diretórios | Escolher 3 e apontar `teste` na listagem; repetir |
| 4 | Consulta ao SO e ao runtime | Funções do módulo `platform` | Informações do ambiente | Escolher 4 e identificar SO, release, arquitetura e Python |
| 5 | Consulta ao identificador do processo atual | `os.getpid()` | Processos | Escolher 5; repetir e observar o mesmo PID nesta execução |
| 6 | Criação de outro processo e espera pelo término | `subprocess.Popen()`, `sys.executable`, `.pid`, `.wait()` | Processos e sincronização | Escolher 6; comparar os PIDs e observar a espera de dois segundos |
| 7 | Sequência automática das seis operações | Funções anteriores | As quatro categorias | Escolher 7 e acompanhar as três etapas |

**Frases para explicar:** PID significa *Process Identifier*, um identificador
atribuído pelo SO a um processo em execução. O pai usa `wait()` para aguardar
o filho. O SO gerencia o ciclo de vida dos processos; Python oferece as APIs
para solicitar esses serviços. `sys.executable` seleciona o interpretador atual,
sem depender de um comando `python` global. A ordem exata de algumas mensagens
do pai e do filho pode variar devido ao escalonamento do SO.

## Tratamento de erros e segurança

O menu informa entradas inválidas, arquivos ausentes, falta de permissão e
falhas de leitura, escrita ou criação de processos. Um filho com código de
saída diferente de zero é sinalizado como erro. Diretórios existentes podem
ser reutilizados; colisão com um arquivo é informada.

Os nomes dos arquivos são fixos e as gravações ficam em `data/`. A aplicação
recusa destinos simbólicos que redirecionem essas operações. Não altera
configurações, não pede privilégios e não executa comandos de shell.
Ctrl+C durante a espera encerra apenas o filho iniciado pela aplicação.
Esta é uma demonstração local: não constitui uma sandbox contra alterações
concorrentes maliciosas na pasta ou arquivos previamente preparados com hard links.

## Testes manuais

Roteiro para repetir a validação:

1. Executar `python main.py` e escolher 1, 2, 3, 4, 5 e 6 individualmente.
2. Conferir os arquivos gerados e o conteúdo exibido pela opção 2.
3. Na opção 6, conferir PIDs diferentes e a finalização antes do retorno ao menu.
4. Executar 7 e observar todas as etapas.
5. Repetir 1, 2, 3 e 7; não deve haver falhas por destinos já existentes.
6. Digitar `abc`, uma opção fora do intervalo e uma entrada vazia: o menu continua.
7. Escolher 0 para encerrar.

Validação realizada no Windows com Python 3.13, incluindo todas as opções,
repetições, entrada inválida e conferência dos arquivos e da espera pelo filho.
Linux/macOS não foram executados neste ambiente; o código usa APIs portáveis
da biblioteca padrão. O terminal deve suportar texto Unicode para exibir os acentos.
