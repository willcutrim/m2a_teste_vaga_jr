# Sistema Posto ABC

Projeto criado para um teste com intuito de mostrar minhas habilidades em com Python e Django.

## Requisitos

- Python 3.11+
- Django 5.0+
- Virtualenv

## Passos para Configuração e Execução do Projeto

### 1. Clonar o Repositório

Primeiro, clone o repositório para a sua máquina local usando o seguinte comando:

```bash
https://github.com/willcutrim/m2a_teste_vaga_jr
````

### 2. Criar e Ativar o Ambiente Virtual
Navegue até o diretório do projeto e crie um ambiente virtual:

```
cd nome-do-repositorio
python -m venv nome_do_ambiente
```

Ative o ambiente virtual:

* No Windows
```
nome_do_ambiente\Scripts\activate

```

* No macOS e Linux
```
source nome_do_ambiente/bin/activate

```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto listadas no arquivo `requirements.txt`:

```
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados
Execute as migrações do banco de dados para configurá-lo corretamente:

```
python manage.py makemigrations
python manage.py migrate
```

### Executar o Servidor de Desenvolvimento
Por fim, inicie o servidor de desenvolvimento do Django:

```
python manage.py runserver
```

Agora você pode acessar o projeto no seu navegador em `http://127.0.0.1:8000`.
