import pandas as pd

def processar_planilha(nome_arquivo, limite_velocidade=80):
    # Lendo a planilha (funciona com .xlsx ou .csv)
    df = pd.read_excel(nome_arquivo) if nome_arquivo.endswith('.xlsx') else pd.read_csv(nome_arquivo)
    
    # Organizando os dados
    df['horario'] = pd.to_datetime(df['horario'])
    df = df.sort_values(by=['motorista', 'horario'])

    # Marca quem está acima do limite
    df['acima'] = df['velocidade'] > limite_velocidade

    # Agrupa sequências consecutivas
    df['sequencia'] = (df['acima'] != df['acima'].shift()).cumsum()

    # Filtra só os momentos de excesso e calcula o tempo
    excessos = df[df['acima']].groupby(['motorista', 'sequencia']).agg(
        inicio=('horario', 'min'),
        fim=('horario', 'max')
    )
    
    # Calcula a duração em minutos
    excessos['duracao_minutos'] = (excessos['fim'] - excessos['inicio']).dt.total_seconds() / 60
    
    # Filtra apenas quem ficou 3 minutos ou mais
    infratores = excessos[excessos['duracao_minutos'] >= 3]
    
    return infratores

# Aqui você mudará o nome para o nome da sua planilha depois
resultado = processar_planilha('sua_planilha.xlsx')
print(resultado)
