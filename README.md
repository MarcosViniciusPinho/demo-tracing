# demo-tracing

Projeto para demonstrar o uso de **tracing distribuído** em microserviços, abrangendo desde a instrumentação até a configuração. Ferramentas utilizadas: **OpenTelemetry** e **Jaeger**.

## Índice

- [Descrição](#descrição)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Execução](#execução)
- [Exemplos de Uso](#exemplos-de-uso)
- [Observações](#observações)

## Descrição

Este projeto visa demonstrar como implementar tracing distribuído em uma arquitetura de microserviços. Através da instrumentação adequada e configuração das ferramentas OpenTelemetry e Jaeger, é possível monitorar e rastrear requisições entre diferentes serviços, facilitando a identificação de gargalos e problemas de desempenho.

## Tecnologias Utilizadas

- **Python**
- **Docker**
- **Docker Compose**
- **Make**
- **OpenTelemetry**
- **Jaeger**

## Pré-requisitos

Antes de iniciar, certifique-se de que sua máquina possui os seguintes requisitos instalados:

- **Python 3.x**
- **Docker** e **Docker Compose**
- **Make**
- **Git** (para clonar o repositório)

## Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/MarcosViniciusPinho/demo-tracing
    cd demo-tracing
    ```

2. **Crie e ative o ambiente virtual do Python:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuração do Ambiente

Certifique-se de que o Docker e o Docker Compose estão corretamente instalados e configurados em sua máquina. Além disso, verifique se o `Make` está disponível para execução dos comandos necessários.

## Execução

1. **Suba todos os serviços necessários utilizando o Make:**

    ```bash
    make docker-up
    ```

2. **Inicialize a aplicação no VSCode (opcional):**

    Caso esteja utilizando o Visual Studio Code, você pode utilizar o arquivo `launch.json` para facilitar a inicialização da aplicação em modo de depuração.

## Exemplos de Uso

### Listar pessoas

Para listar todas as pessoas cadastradas, execute o seguinte comando `curl`:

```bash
curl --location 'http://localhost:8000/pessoas'
```

### Cadastrar uma pessoa
```bash
curl --location 'http://localhost:8000/pessoas' \
--header 'Content-Type: application/json' \
--data '{
    "nome": "Marcos",
    "sobrenome": "Pinho",
    "idade": 40,
    "cpf": "37287624322"
}'
```

obs: Para matar todas as dependencias de serviços utilize o Make com o seguinte comando:

    ```bash
    make docker-destroy
    ```

Para visualizar os traces basta digitar o endereço `http://localhost:8081`