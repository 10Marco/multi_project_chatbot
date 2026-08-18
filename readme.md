
# 🤖 Chatbot Multi-Projeto (WhatsApp + FastAPI)

Sistema de chatbot inteligente integrado ao WhatsApp, capaz de atender múltiplos projetos com uma única arquitetura.

---

## 🚀 Features

* 📲 Integração com WhatsApp (Baileys)
* ⚡ Backend em FastAPI
* 🔁 Retry automático de requisições
* 🧵 Estado de conversa com Redis
* 🔀 Roteamento multi-projeto por número
* 🔌 Arquitetura plugável (GLPI, e-commerce, serviços)

---

## 🧠 Arquitetura

```
WhatsApp (Baileys)
        ↓
FastAPI (Router + lógica)
        ↓
Services (integrações específicas)
        ↓
Redis (estado da conversa)
```

---

## 📦 Requisitos

* Docker
* Docker Compose

---

## ⚙️ Setup

```bash
git clone <repo>
cd chatbot
docker compose up --build
```

---

## 📱 Conectar WhatsApp

* Escaneie o QR code exibido no terminal
* Aguarde a conexão

---

## 🧪 Teste

Após conectar o WhatsApp, envie mensagens como:

* oi
* iniciar atendimento
* bom dia

---

## 🔀 Multi-Projeto

O sistema detecta automaticamente qual projeto utilizar com base no número do WhatsApp:

```env
GLPI_NUMBER=556139615186@c.us
GARAGEM_NUMBER=556195546360@c.us
LOJA_NUMBER=5561777777777@c.us
```

---

## 🧠 Fluxo

1. Usuário inicia conversa
2. Backend executa ações
3. Redis mantém o estado
4. Resposta retorna ao WhatsApp

---

## 📁 Estrutura

```
api/
services/
whatsapp-service/
docker-compose.yml
```

---

## 🔮 Atualizações futuras

* 🔐 Validação de usuário via API interna
* 📊 Métricas de atendimento por projeto
* ☁️ Deploy em cloud
