import base64
import json
import os

from io import BytesIO

from nltk.corpus import stopwords
from wordcloud import WordCloud 


class GeoJsonSingleton:
    _instance = None    

    def __new__(cls):

        if cls._instance is None:
            BASE_DIR = os.getcwd()
            FILE_PATH_GEO_JSON = os.path.join(BASE_DIR, 'components/datasets', 'brasil_estados.json')   
            
            with open(FILE_PATH_GEO_JSON, 'r', encoding='utf-8') as f:
                cls._instance = json.load(f)
        
        return cls._instance


class DataProcessing:
    '''
    Faz o tratamento e processamento de um dataframe com dados
    do Reclame A do HAPVIDA

    Divide a coluna "LOCAL" no formato 'Cidade - UF' 
    em duas colunas separadas: 'Cidade' e 'UF'.

    Gerando coluna com tamanho do texto da variavel DESCRICAO

    removendo linas que não tem estado

    Convertendo coluna ANO para STR
    '''

    def __init__(self, df):        
        
        df[['CIDADE', 'ESTADO']] = df['LOCAL'].str.split(' - ', expand=True)
        df['TAMANHO_TEXTO'] = df['DESCRICAO'].str.len()        
        df = df[~(df['ESTADO'] == '--')]
        df['ANO'] = df['ANO'].astype(str)

        self.df = df

    
    def series_temporal(self):
        '''
        Gera dados para gráfico serie temporal.
        '''
        return self.df.groupby('MES').size().reset_index(name='CONTAGEM')
        
 
    def data_estado(self):
        '''
        Gera dados para gráfico reclamação por estado
        '''
        return self.df['ESTADO'].value_counts().reset_index()


    def data_status(self):
        '''
        Gera dados para gráfico distribuição por status
        '''
        return self.df['STATUS'].value_counts().reset_index()


    def data_texto(self):
        '''
        Gera dados para gráfico distribuição do tamanho do texto
        '''
        return self.df


    def data_mapa(self, ano_mapa: str | None):
        
        '''
        Completa os estados que não tem dados no dataframe com 0, 
        após groupby extrair os dados, para que o grafico de mapa
        mostre o estado.

        Adiciona a sigla e contagem em zero do estado que não tem no dataframe

        Adiciona nomes aos estados.
        '''        

        # Dados do estados para exibição de todos os estados mesmo sem dados do estado
        dict_estados = {
            'AC': 'Acre', 
            'AL': 'Alagoas', 
            'AP': 'Amapá', 
            'AM': 'Amazonas', 
            'BA': 'Bahia',
            'CE': 'Ceará',
            'DF': 'Distrito Federal', 
            'ES': 'Espírito Santo', 
            'GO': 'Goiás',
            'MA': 'Maranhão', 
            'MT': 'Mato Grosso', 
            'MS': 'Mato Grosso do Sul', 
            'MG': 'Minas Gerais',
            'PA': 'Pará', 
            'PB': 'Paraíba', 
            'PR': 'Paraná', 
            'PE': 'Pernambuco', 
            'PI': 'Piauí',
            'RJ': 'Rio de Janeiro',
            'RN': 'Rio Grande do Norte', 
            'RS': 'Rio Grande do Sul',
            'RO': 'Rondônia', 
            'RR': 'Roraima', 
            'SC': 'Santa Catarina', 
            'SP': 'São Paulo',
            'SE': 'Sergipe', 
            'TO': 'Tocantins'
        }
        
        df_contagem_estado = self.df.loc[self.df['ANO'] == ano_mapa].groupby('ESTADO').size().reset_index(name='CONTAGEM')

        # checa de ano_mapa vem preenchido, para não exibir dados em 0.        
        if ano_mapa:
            for sigla in dict_estados.keys():
                if sigla not in set(df_contagem_estado['ESTADO'].unique()):
                    df_contagem_estado.loc[len(df_contagem_estado)] = {'ESTADO': sigla, 'CONTAGEM': 0}
                
        df_contagem_estado['NOME'] = df_contagem_estado['ESTADO'].map(dict_estados)        
        
        return df_contagem_estado
    

    def data_wordcloud(self):        

        # Obter a lista de stopwords em português
        stopwords_portugues = stopwords.words('portuguese')

        stopwords_planos_saude = {
            # Termos Gerais de Planos de Saúde
            'plano', 'planos', 'saúde', 'convênio', 'convênios', 'seguro', 'seguros',
            'operadora', 'operadoras', 'benefício', 'benefícios', 'serviço', 'serviços',
            'contrato', 'contratos', 'apólice', 'apólices', 'cobertura', 'coberturas',
            'rede', 'redes', 'credenciada', 'credenciadas', 'atendimento', 'atendimentos',
            'assistência', 'assistências', 'médico', 'médica', 'médicos', 'médicas',
            'hospital', 'hospitais', 'clínica', 'clínicas', 'exame', 'exames', 'consulta',
            'consultas', 'procedimento', 'procedimentos', 'reembolso', 'reembolsos',
            'carência', 'carências', 'mensalidade', 'mensalidades', 'custo', 'custos',
            'preço', 'preços', 'valor', 'valores', 'pagamento', 'pagamentos', 'titular',
            'dependentes', 'adesão', 'portabilidade', 'urgência', 'emergência', 'ans',
            'agência', 'nacional',

            # Termos Relacionados/Descritivos Comuns - podem não ser o foco
            'cliente', 'clientes', 'usuário', 'usuários', 'paciente', 'pacientes',
            'doutor', 'doutora', 'doutores', 'doutoras', 'equipe', 'equipes',
            'empresa', 'empresas', 'filho', 'filha', 'vc',    
            'bom', 'boa', 'bons', 'boas', 'ruim', 'ruins', 'ótimo', 'ótima',
            'excelente', 'péssimo', 'péssima', 'muito', 'pouco', 'mais', 'menos',
            'assim', 'porém', 'entanto', 'também', 'ainda', 'já', 'sempre', 'nunca',
            'alguns', 'algumas', 'todo', 'toda', 'todos', 'todas', "pois", "outro", 
            "outra", "dia", "dias", "entrega", "reclame", "aqui", "problema",
            'q', 'fiz', ',', 'Hapvida', "não", 'nao', "pra", "tive", "minha", 'contato',
            'fazer', 'nada', 'ter', 'preciso', 'ano', 'onde', 'vai', 'após',
            'hoje', 'SAC', 'vez', 'pode', 'lá', 'por que', 'porque','pq', 'faz', 'vou',
            'quero', 'disse', 'data', 'então', 'ir', 'desde', 'sendo', 'agora',
            'meses', 'entrei', 'consegui', 'passar', 'pessoa', 'entrar', 'semana',
            'sobre', 'horário', 'hora', 'mês', 'min', 'ja', 'mesma', 'pago', 'passou',
            'bem', 'atendente', 'bem', 'anos', 'liguei', 'mail', 'saber', 'ligar',
            'quase', 'mim', 'apenas','muito', 'pouco', 'mais', 'menos', 'bastante', 
            'quase', 'tão', 'tão', 'demais', 'suficiente', 'suficientes', 'totalmente', 
            'parcialmente', 'completamente', 'absolutamente', 'relativamente', 
            'excessivamente', 'apenas', 'só','bom', 'boa', 'bons', 'boas', 'ruim', 'ruins', 
            'excelente', 'excelentes', 'péssimo', 'péssima', 'péssimos', 'péssimas',
            'melhor', 'melhores', 'pior', 'piores', 'grande', 'grandes', 'pequeno', 'pequena',
            'pequenos', 'pequenas', 'certo', 'certa', 'certos', 'certas', 'errado', 'errada',
            'errados', 'erradas', 'positivo', 'positiva', 'positivos', 'positivas',
            'negativo', 'negativa', 'negativos', 'negativas', 'legal', 'legais',
            'incrível', 'incríveis', 'horrível', 'horríveis', 'razoável', 'razoáveis',
            'bom', 'má', 'maus', 'más', 'grande', 'pequeno', 'novo', 'nova', 'novos', 
            'novas', 'velho', 'velha', 'velhos', 'velhas', 'ótimo', 'ótima', 'ótimos', 'ótimas',    
            'sempre', 'nunca', 'jamais', 'às vezes', 'frequentemente', 'raramente', 'constantemente',
            'diariamente', 'semanalmente', 'mensalmente', 'anualmente', 'hoje', 'ontem', 'amanhã',
            'agora', 'depois', 'antes', 'cedo', 'tarde', 'logo', 'já', 'ainda', 'durante',    
            'assim', 'bem', 'mal', 'melhor', 'pior', 'rapidamente', 'lentamente', 'facilmente',
            'dificilmente', 'geralmente', 'especialmente', 'principalmente', 'claro', 'clara',
            'claramente', 'verdadeiro', 'verdadeira', 'verdadeiros', 'verdadeiras', 'falso',
            'falsa', 'falsos', 'falsas', 'possível', 'possíveis', 'impossível', 'impossíveis',    
            'porém', 'contudo', 'entretanto', 'todavia', 'assim', 'portanto', 'logo', 'daí',
            'além', 'ainda', 'inclusive', 'mesmo', 'embora', 'apesar', 'conforme', 'segundo',
            'exceto', 'salvo', 'inclusive', 'além disso', 'em vez de', 'ao invés de', 'ou seja',    
            'aqui', 'lá', 'ali', 'cá', 'perto', 'longe', 'dentro', 'fora', 'em cima', 'em baixo',
            'atrás', 'frente', 'lado', 'ao lado', 'direita', 'esquerda', 'meio',    
            'próprio', 'própria', 'próprios', 'próprias', 'outro', 'outra', 'outros', 'outras',
            'mesmo', 'mesma', 'mesmos', 'mesmas', 'todo', 'toda', 'todos', 'todas',
            'algum', 'alguma', 'alguns', 'algumas', 'nenhum', 'nenhuma', 'nenhuns', 'nenhumas',
            'vários', 'várias', 'diversos', 'diversas', 'certo', 'certa', 'certos', 'certas',
            'tal', 'tais', 'qualquer', 'quaisquer', 'cujo', 'cuja', 'cujos', 'cujas',
            'primeiro', 'primeira', 'segundo', 'segunda', 'último', 'última',
            'único', 'única', 'únicos', 'únicas', 'sistema', 'atende', 'momento', 'telefone',
            'vezes'
        }

        for palavra in stopwords_planos_saude:
            stopwords_portugues.append(palavra)

        texto = " ".join(self.df['DESCRICAO'].astype(str).tolist())

        wordcloud =  WordCloud(
            width=800,
            height=400,
            background_color='white',
            stopwords=stopwords_portugues,
            colormap='viridis', 
            max_words=50
        ).generate(texto)

        img_io = BytesIO()
        wordcloud.to_image().save(img_io, format='PNG')

        return 'data:image/png;base64,{}'.format(base64.b64encode(img_io.getvalue()).decode())
