Como Executar o Programa de Estoque

Este documento contém instruções para rodar o programa corretamente e evitar problemas com a geração do arquivo JSON.

1. Executando o Programa pelo CMD

    Para evitar que o terminal feche automaticamente e visualizar possíveis erros, siga estas etapas:

Abra o Prompt de Comando (CMD):

    Pressione Win + R, digite cmd e aperte Enter.

Acesse a Pasta do Programa:

    Navegue até a pasta onde o script está localizado. Use o comando:

    cd "C:\Users\usuario\Desktop\Arco Tecnologia - Testes\teste de estoque Arco"

Execute o Programa:

    Rode o script com um dos comandos abaixo:

    python "teste de estoque Arco.py"

ou, caso python não funcione, tente:

    py "teste de estoque Arco.py"

2. Verificando se o JSON Foi Salvo

    O programa deve criar uma pasta chamada "vendas" e salvar o arquivo JSON dentro dela. Para verificar se a pasta foi criada, execute este comando no CMD:

    dir vendas

    Se a pasta não existir, crie-a manualmente antes de rodar o programa:

    mkdir vendas

3. Executando Como Administrador

    Se aparecer o erro PermissionError: [WinError 5] Acesso negado, o programa pode precisar de permissões para criar arquivos. Para corrigir isso:

Abra o Prompt de Comando como Administrador:

    Pesquise por "Prompt de Comando" no menu Iniciar.

Clique com o botão direito e selecione "Executar como Administrador".

Repita os passos de execução do programa (Seção 1).