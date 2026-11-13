# 🎟️ EventoPass API

API REST para inscrição em eventos (palestras, workshops, meetups). Permite cadastrar participantes e eventos, filtrar eventos por cidade e gerenciar inscrições com controle de vagas e validação de regras de negócio. Construída com FastAPI, SQLAlchemy e PostgreSQL.

---

## ⚙️ Funcionalidades

- Cadastro, listagem, busca e remoção de participantes (com email único)
- Cadastro, listagem, busca e remoção de eventos
- Filtro de eventos por cidade
- Inscrição de participantes em eventos, com controle de vagas
- Cancelamento de inscrições (a vaga é liberada automaticamente)
- Consulta de um evento com suas inscrições
- Consulta de um participante com suas inscrições
- Documentação interativa automática via Swagger

---

## 📐 Regras de negócio

Ao criar uma inscrição, a API valida, nesta ordem:

| Regra | Status |
|---|:---:|
| O participante precisa existir | `404` |
| O evento precisa existir | `404` |
| O evento precisa ter vaga disponível | `400` |
| O participante não pode se inscrever duas vezes no mesmo evento | `400` |

Além disso:
- Não é possível cadastrar dois participantes com o mesmo email (`400`)
- As vagas disponíveis são calculadas em tempo real a partir das inscrições existentes; ao cancelar uma inscrição, a vaga volta a ficar disponível
- Ao remover um participante ou um evento, as inscrições relacionadas são removidas junto (cascade)

---

## 🗂️ Entidades

- **Participante:** id, nome, email
- **Evento:** id, titulo, cidade, data, vagas
- **Inscricao:** id, participante_id (FK), evento_id (FK)

```
Participante ──1:N── Inscricao ──N:1── Evento
```

A **Inscricao** é a entidade associativa que liga participantes e eventos.

---

## 🔌 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/participantes/` | Cadastra um participante |
| GET | `/participantes/` | Lista os participantes |
| GET | `/participantes/{id}` | Busca um participante |
| DELETE | `/participantes/{id}` | Remove um participante e suas inscrições |
| POST | `/eventos/` | Cadastra um evento |
| GET | `/eventos/` | Lista os eventos |
| GET | `/eventos/?cidade=São Paulo` | Filtra eventos por cidade |
| GET | `/eventos/{id}` | Busca um evento |
| DELETE | `/eventos/{id}` | Remove um evento e suas inscrições |
| POST | `/inscricoes/` | Inscreve um participante em um evento |
| GET | `/inscricoes/` | Lista as inscrições |
| DELETE | `/inscricoes/{id}` | Cancela uma inscrição |
| GET | `/eventos/{id}/inscricoes` | Retorna o evento com suas inscrições |
| GET | `/participantes/{id}/inscricoes` | Retorna o participante com suas inscrições |

---

## 🛠️ Tecnologias

- Python
- FastAPI
- SQLAlchemy (ORM)
- Pydantic
- PostgreSQL
- Uvicorn

---

## 🚀 Como executar

Pré-requisitos: Python 3 e PostgreSQL instalados.

**1. Clone o repositório:**
```bash
git clone https://github.com/guiamorim0/eventopass.git
cd eventopass
```

**2. Instale as dependências:**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv
```

**3. Crie o banco no PostgreSQL:**
```sql
CREATE DATABASE eventopass;
```

**4. Crie um arquivo `.env` na raiz:**
```
DATABASE_URL=postgresql://usuario:senha@localhost/eventopass
```

**5. Suba a API:**
```bash
uvicorn main:app --reload
```

**6. Acesse a documentação:**
```
http://localhost:8000/docs
```

---

## 📂 Estrutura

```
eventopass/
├── database.py   # Conexão com o banco
├── models.py     # Modelos SQLAlchemy (Participante, Evento, Inscricao)
├── schemas.py    # Schemas Pydantic
├── main.py       # Endpoints
├── .env          # Variáveis de ambiente (não versionado)
└── .gitignore
```

---

## 🧠 Conceitos aplicados

- Arquitetura em camadas (conexão, models, schemas, rotas)
- Entidade associativa com duas chaves estrangeiras
- Relacionamentos 1:N com cascade delete nos dois lados
- Filtro dinâmico por query parameter opcional
- Controle de vagas calculado a partir dos relacionamentos, sem campo redundante
- Validação de duplicidade com consulta de múltiplas condições
- Diferenciação entre `404` (recurso inexistente) e `400` (operação inválida)
- Carregamento otimizado de dados relacionados com `joinedload`

---

## 🏛️ Decisões de arquitetura

- **Vagas calculadas, não armazenadas:** em vez de manter um campo de "vagas restantes" que precisaria ser atualizado a cada inscrição e cancelamento, a API conta as inscrições existentes no momento da validação. Isso evita inconsistência entre o contador e os dados reais.
- **Inscrição como entidade própria:** a ligação entre participante e evento é uma tabela com identificador próprio, permitindo listar, consultar e cancelar inscrições individualmente.

---

## 👤 Autor

**Guilherme Zanchetti Amorim** — Estudante de Engenharia de Software (FIAP)

- GitHub: [github.com/guiamorim0](https://github.com/guiamorim0)