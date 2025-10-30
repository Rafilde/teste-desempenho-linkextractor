import pandas as pd
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns

def resultados():
    """
    Script para ler os 12 CSVs do Locust, compilar os dados 
    e gerar gráficos de análise de desempenho.
    """
    
    # --- 1. CONFIGURAÇÃO (AGORA MAIS DIDÁTICA) ---
    pasta_planilhas = 'planilhas'
    
    # Em vez de Regex, definimos uma lista de todos os testes
    # que queremos ler e quais são suas propriedades.
    testes_para_ler = [
        # Python com Cache
        {'arquivo': 'python-cache-10user.csv', 'ambiente': 'Python', 'cache': 'Com Cache', 'usuarios': 10},
        {'arquivo': 'python-cache-50user.csv', 'ambiente': 'Python', 'cache': 'Com Cache', 'usuarios': 50},
        {'arquivo': 'python-cache-100user.csv','ambiente': 'Python', 'cache': 'Com Cache', 'usuarios': 100},
        
        # Python Sem Cache
        {'arquivo': 'python-sem-cache-10user.csv', 'ambiente': 'Python', 'cache': 'Sem Cache', 'usuarios': 10},
        {'arquivo': 'python-sem-cache-50user.csv', 'ambiente': 'Python', 'cache': 'Sem Cache', 'usuarios': 50},
        {'arquivo': 'python-sem-cache-100user.csv','ambiente': 'Python', 'cache': 'Sem Cache', 'usuarios': 100},
        
        # Ruby com Cache
        {'arquivo': 'ruby-cache-10user.csv', 'ambiente': 'Ruby', 'cache': 'Com Cache', 'usuarios': 10},
        {'arquivo': 'ruby-cache-50user.csv', 'ambiente': 'Ruby', 'cache': 'Com Cache', 'usuarios': 50},
        {'arquivo': 'ruby-cache-100user.csv','ambiente': 'Ruby', 'cache': 'Com Cache', 'usuarios': 100},
        
        # Ruby Sem Cache
        {'arquivo': 'ruby-sem-cache-10user.csv', 'ambiente': 'Ruby', 'cache': 'Sem Cache', 'usuarios': 10},
        {'arquivo': 'ruby-sem-cache-50user.csv', 'ambiente': 'Ruby', 'cache': 'Sem Cache', 'usuarios': 50},
        {'arquivo': 'ruby-sem-cache-100user.csv','ambiente': 'Ruby', 'cache': 'Sem Cache', 'usuarios': 100},
    ]
    
    dados_compilados = []
    print(f"Iniciando análise da pasta: '{pasta_planilhas}'...")

    # --- 2. LEITURA E EXTRAÇÃO DOS DADOS (AGORA MAIS SIMPLES) ---
    
    for teste in testes_para_ler:
        caminho_arquivo = os.path.join(pasta_planilhas, teste['arquivo'])
        
        try:
            df_temp = pd.read_csv(caminho_arquivo)
            
            # Pega a linha "Aggregated" que tem o resumo do teste
            df_resumo = df_temp[df_temp['Name'] == 'Aggregated'].iloc[0]
            
            # Adiciona os dados à nossa lista
            dados_compilados.append({
                'Ambiente': teste['ambiente'],
                'Cache': teste['cache'],
                'Cenário': f"{teste['ambiente']} ({teste['cache']})",
                'Usuários': teste['usuarios'],
                'Média (ms)': df_resumo['Average Response Time'],
                'Mediana (ms)': df_resumo['Median Response Time'],
                'p90 (ms)': df_resumo['90%'], # Percentil 90
                'RPS': df_resumo['Requests/s'],
                'Falhas': df_resumo['Failure Count']
            })
        except FileNotFoundError:
            print(f"ERRO: Arquivo não encontrado: '{caminho_arquivo}'. Verifique o nome.")
        except Exception as e:
            print(f"Erro ao processar o arquivo '{teste['arquivo']}': {e}")

    # --- 3. ARMAZENAMENTO (PLANILHA) ---
    
    if len(dados_compilados) != 12:
        print(f"\nAviso: Foram processados {len(dados_compilados)} de 12 arquivos. Verifique os erros acima.")

    if not dados_compilados:
        print("Nenhum dado foi processado com sucesso.")
        return

    # Cria o DataFrame final com todos os resultados
    df_final = pd.DataFrame(dados_compilados)
    df_final = df_final.sort_values(by=['Ambiente', 'Cache', 'Usuários'])
    
    # Salva a planilha compilada
    arquivo_saida = 'resultados_compilados.csv'
    df_final.to_csv(arquivo_saida, index=False)
    
    print("\n--- DADOS COMPILADOS ---")
    print(df_final)
    print(f"\nPlanilha final salva em: '{arquivo_saida}'")

    # --- 4. VISUALIZAÇÃO (GRÁFICOS) ---
    
    print("Gerando novos gráficos de barras...")
    sns.set_theme(style="whitegrid", palette="muted")
    
    fig_size = (14, 8) 
    
    # --- Gráfico 1: Tempo de Resposta (p90) - BARRAS ---
    plt.figure(figsize=fig_size)
    sns.barplot(
        data=df_final,
        x='Cenário',
        y='p90 (ms)',
        hue='Usuários'
    )
    plt.title('Percentil 90 (p90) por Cenário e Carga', fontsize=16, pad=20)
    plt.xlabel('Cenário de Teste', fontsize=12)
    plt.ylabel('Tempo de Resposta p90 (ms)', fontsize=12)
    plt.xticks(rotation=10)
    plt.legend(title='Nº de Usuários', loc='upper left')
    plt.tight_layout()
    plt.savefig('grafico_p90_barras.png')
    print("Gráfico 'grafico_p90_barras.png' salvo.")

    # --- Gráfico 2: Vazão (RPS) - BARRAS ---
    plt.figure(figsize=fig_size)
    sns.barplot(
        data=df_final,
        x='Cenário',
        y='RPS',
        hue='Usuários'
    )
    plt.title('Vazão (RPS) por Cenário e Carga', fontsize=16, pad=20)
    plt.xlabel('Cenário de Teste', fontsize=12)
    plt.ylabel('Requisições por Segundo (RPS)', fontsize=12)
    plt.xticks(rotation=10)
    plt.legend(title='Nº de Usuários', loc='upper left')
    plt.tight_layout()
    plt.savefig('grafico_rps_barras.png')
    print("Gráfico 'grafico_rps_barras.png' salvo.")

    # --- Gráfico 3: Contagem de Falhas - BARRAS ---
    plt.figure(figsize=fig_size)
    sns.barplot(
        data=df_final,
        x='Cenário',
        y='Falhas',
        hue='Usuários'
    )
    plt.title('Total de Falhas por Cenário e Carga', fontsize=16, pad=20)
    plt.xlabel('Cenário de Teste', fontsize=12)
    plt.ylabel('Contagem de Falhas', fontsize=12)
    plt.xticks(rotation=10)
    plt.legend(title='Nº de Usuários', loc='upper right')
    plt.tight_layout()
    plt.savefig('grafico_falhas_barras.png')
    print("Gráfico 'grafico_falhas_barras.png' salvo.")
    print("\nAnálise concluída!")

if __name__ == '__main__':
    resultados()