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
    pasta_planilhas = 'naboa\planilhas'
    
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
            
            df_resumo = df_temp[df_temp['Name'] == 'Aggregated'].iloc[0]
            
            dados_compilados.append({
                'Ambiente': teste['ambiente'],
                'Cache': teste['cache'],
                'Cenário': f"{teste['ambiente']} ({teste['cache']})",
                'Usuários': teste['usuarios'],
                'Média (ms)': df_resumo['Average Response Time'],
                'Mediana (ms)': df_resumo['Median Response Time'],
                'p90 (ms)': df_resumo['90%'],
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

    df_final = pd.DataFrame(dados_compilados)
    df_final = df_final.sort_values(by=['Ambiente', 'Cache', 'Usuários'])
    
    arquivo_saida = 'resultados_compilados.csv'
    df_final.to_csv(arquivo_saida, index=False)
    
    print("\n--- DADOS COMPILADOS ---")
    print(df_final)
    print(f"\nPlanilha final salva em: '{arquivo_saida}'")

    # --- 4. VISUALIZAÇÃO (GRÁFICOS - AGORA COM FACETAS) --- 
    print("Gerando novos gráficos com facetas...")
    sns.set_theme(style="whitegrid", palette="muted")

    g_p90 = sns.catplot(
        data=df_final,
        x='Cenário',
        y='p90 (ms)',
        col='Usuários',   
        kind='bar',       
        sharey=False,     
        height=6,         
        aspect=1.1     
    )

    g_p90.fig.suptitle('Percentil 90 (p90) por Cenário e Carga', fontsize=16, y=1.03)
    g_p90.set_axis_labels('Cenário de Teste', 'Tempo de Resposta p90 (ms)')
    g_p90.set_titles("Carga: {col_name} Usuários") 
    g_p90.set_xticklabels(rotation=10) 

    plt.tight_layout()
    g_p90.savefig('grafico_p90_facetas.png')
    print("Gráfico 'grafico_p90_facetas.png' salvo.")
    plt.close(g_p90.fig) 

    g_rps = sns.catplot(
        data=df_final,
        x='Cenário',
        y='RPS',
        col='Usuários',
        kind='bar',
        sharey=False,
        height=6,
        aspect=1.1
    )
    g_rps.fig.suptitle('Vazão (RPS) por Cenário e Carga', fontsize=16, y=1.03)
    g_rps.set_axis_labels('Cenário de Teste', 'Requisições por Segundo (RPS)')
    g_rps.set_titles("Carga: {col_name} Usuários")
    g_rps.set_xticklabels(rotation=10)

    plt.tight_layout()
    g_rps.savefig('grafico_rps_facetas.png')
    print("Gráfico 'grafico_rps_facetas.png' salvo.")
    plt.close(g_rps.fig)

    g_falhas = sns.catplot(
        data=df_final,
        x='Cenário',
        y='Falhas',
        col='Usuários',
        kind='bar',
        sharey=False,
        height=6,
        aspect=1.1
    )

    g_falhas.fig.suptitle('Total de Falhas por Cenário e Carga', fontsize=16, y=1.03)
    g_falhas.set_axis_labels('Cenário de Teste', 'Contagem de Falhas')
    g_falhas.set_titles("Carga: {col_name} Usuários")
    g_falhas.set_xticklabels(rotation=10)

    plt.tight_layout()
    g_falhas.savefig('grafico_falhas_facetas.png')
    print("Gráfico 'grafico_falhas_facetas.png' salvo.")
    plt.close(g_falhas.fig)

    print("\nAnálise concluída!")

if __name__ == '__main__':
    resultados()