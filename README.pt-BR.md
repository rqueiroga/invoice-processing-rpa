# Invoice Processing RPA

[English](README.md)

Projeto de portfólio de RPA de ponta a ponta que automatiza um fluxo comum de Contas a Pagar entre dois sistemas empresariais fictícios.

Todas as empresas, credenciais, registros, sistemas e documentos deste repositório são fictícios.

![Arquitetura](docs/architecture.svg)

## O que a automação faz

1. Lê tarefas pendentes em uma fila no Excel.
2. Entra no **Portal de Fornecedores** e consulta cada nota.
3. Baixa o primeiro e o último documento de apoio.
4. Une os arquivos em um único pacote PDF.
5. Abre o **Portal Financeiro** e localiza o pedido de compra relacionado.
6. Confere se a nota já foi registrada.
7. Mapeia o tipo da nota, envia o PDF e salva o cadastro.
8. Grava o resultado no Excel após cada linha processada.

A demonstração inclui casos de sucesso e exceções de negócio, como pedido de compra inexistente e tipo de nota sem mapeamento.

## Como rodar

Agora existe apenas **um comando principal**. Não é necessário ativar `.venv`, liberar scripts do PowerShell ou executar arquivos `.bat`.

Abra um terminal dentro da pasta do projeto e execute:

```bash
py start.py
```

Na primeira execução, o próprio `start.py`:

- cria o `.venv`;
- instala as bibliotecas do projeto;
- baixa o Chromium do Playwright;
- restaura os dados da demonstração;
- inicia os dois sistemas fictícios;
- executa o RPA.

Nas próximas execuções, a etapa de instalação é ignorada e a demonstração começa diretamente.

Se `py` não estiver disponível, use:

```bash
python start.py
```

### Interface em português

```bash
py start.py --pt
```

Os sistemas também possuem um seletor **EN / PT-BR** no topo. O robô usa seletores `data-testid`, então mudar o idioma da interface não interfere no funcionamento.

### Velocidade da demonstração

O padrão é `600 ms` adicionais entre as ações para que seja possível acompanhar visualmente o fluxo.

```bash
py start.py --speed 300
py start.py --speed 900
```

Use `0` para uma execução próxima da velocidade normal.

## Credenciais da demonstração

| Sistema | Usuário | Senha |
| --- | --- | --- |
| Portal de Fornecedores | `supplier.demo` | `demo123` |
| Portal Financeiro | `finance.demo` | `demo123` |

As credenciais são públicas de propósito porque todo o ambiente é local e fictício.

## Estrutura do projeto

```text
invoice-processing-rpa/
├── start.py                # Único ponto de entrada e configuração automática
├── main.py                 # Automação RPA
├── demo_server.py          # Dois sistemas fictícios
├── run_demo.py             # Orquestra a demonstração
├── reset_demo.py           # Restaura o estado inicial
├── START_HERE.txt          # Instruções mínimas de execução
├── data/
│   └── invoice_queue.xlsx  # Fila de processamento
├── sample_documents/       # PDFs fictícios
├── docs/
│   └── architecture.svg
├── runtime/                # Dados gerados durante a execução
├── .gitignore
└── requirements.txt
```

## Cenários incluídos

- `INV-1001`: cadastro normal de nota de serviço
- `INV-1002`: cadastro normal de nota de produto
- `INV-1003`: pedido de compra inexistente
- `INV-1004`: cadastro de reembolso de despesas
- `INV-1005`: tipo de nota sem mapeamento automático

## Tecnologias

- Python
- Playwright
- OpenPyXL
- pypdf
- HTML/CSS
- servidor HTTP da biblioteca padrão do Python

## O que o projeto demonstra

O projeto não é apenas automação de cliques. Ele mostra processamento por fila, navegação entre dois sistemas, downloads, manipulação de PDFs, regras de negócio, prevenção de duplicidade, tratamento de exceções, persistência de progresso em Excel e um ambiente local reproduzível para demonstração.
