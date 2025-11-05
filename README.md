# Git Helper

O `git-helper` é um script Python que fornece uma interface de linha de comando simples para realizar operações Git comuns. Ele simplifica tarefas como clonar repositórios, verificar o status, criar commits, criar tags e enviar alterações.

## Funcionalidades

-   **Clonar Repositórios**: Clone um novo repositório a partir de uma URL.
-   **Trabalhar com Repositórios Locais**: Gerencie facilmente seus repositórios git locais.
-   **Status do Git**: Mostra o status da árvore de trabalho.
-   **Verificar Acesso Remoto**: Verifica a conexão com o repositório remoto.
-   **Criar Commits**: Adiciona e faz o commit de todas as alterações no diretório de trabalho.
-   **Criar Tags**: Crie tags anotadas.
-   **Enviar Alterações (Push)**: Envie commits e/ou tags para o repositório remoto.

## Como Usar

### Linux/macOS

1.  Execute o script:
    ```bash
    python3 git-helper.py
    ```

2.  O script apresentará um menu com opções para clonar um repositório ou trabalhar com um repositório local existente.

3.  Se você optar por trabalhar com um repositório local, o script listará todos os repositórios git encontrados no diretório base (`~/Documentos/Git` por padrão).

4.  Após selecionar um repositório, você pode escolher em uma lista de ações a serem executadas.

### Windows

Para usar o `git-helper` no Windows, você precisará ter o [Python](https://www.python.org/downloads/) e o [Git](https://git-scm.com/download/win) instalados e configurados no PATH do sistema.

1.  Abra o `cmd` ou o `PowerShell` e navegue até o diretório onde o script `git-helper.py` está localizado.

2.  Execute o script usando o comando `python`:
    ```bash
    python git-helper.py
    ```

3.  O script funcionará da mesma forma que no Linux, apresentando um menu para você interagir.

## Compatibilidade entre Plataformas

O script é escrito em Python e usa o módulo `pathlib`, que lida com operações de caminho de forma multiplataforma. Isso permite que o script seja executado em sistemas Windows e Linux sem modificação.