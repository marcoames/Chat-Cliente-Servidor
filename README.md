# Aplicação de Chat Cliente-Servidor

Este projeto consiste em uma aplicação de chat cliente-servidor desenvolvida para a disciplina de Laboratório Redes de Computadores, implementada em Python, utilizando **Sockets** e **Threading**. O sistema suporta múltiplos usuários simultâneos, permitindo o envio de mensagens e arquivos entre clientes conectados.

## Tecnologias Utilizadas
- **Python**: Linguagem de programação.
- **Sockets**: Para comunicação entre cliente e servidor.
- **Threading**: Para suportar múltiplos usuários simultâneos.

## Funcionalidades Principais

### 1. Registro de Usuário
- Cada cliente pode se registrar no sistema com um apelido único.
- O servidor mantém uma lista de clientes conectados e seus apelidos.

### 2. Mensagens Diretas
- Permite o envio de mensagens privadas entre usuários registrados.
- Os usuários podem enviar mensagens diretamente para outros utilizando o apelido.

### 3. Mensagens em Broadcast
- Envio de mensagens para todos os clientes conectados.
- Ideal para notificações gerais ou conversas públicas.

### 4. Transferência de Arquivos
- Suporte para envio de arquivos de texto entre usuários.
- Os usuários podem compartilhar arquivos diretamente uns com os outros.

## Como Funciona?

### Servidor
- O servidor aceita conexões de múltiplos clientes e distribui mensagens entre eles.
- Cada cliente é tratado em uma **thread** separada, garantindo a comunicação em tempo real.

### Cliente
- Os clientes podem se registrar com um apelido único e, a partir disso, podem enviar mensagens diretas, mensagens em broadcast, ou arquivos de texto para outros usuários.

Projeto desenvolvido para a disciplina de Laboratório de Redes de Computadores. 
