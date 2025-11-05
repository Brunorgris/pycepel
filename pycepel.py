# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:22:33 2024

@author: brgris
"""

import re
import pandas as pd
import os
from subprocess import Popen, PIPE

config_cepel = {
    "DBAR": {
        "Nb": {"start": 0, "end": 5, "type": int},
        "O": {"start": 5, "end": 6, "type": str},
        "E": {"start": 6, "end": 7, "type": str},
        "T": {"start": 7, "end": 8, "type": int},
        "Gb": {"start": 8, "end": 10, "type": str},
        "Nome": {"start": 10, "end": 22, "type": str},
        "Gl": {"start": 22, "end": 24, "type": str},
        "V": {"start": 24, "end": 28, "type": int},
        "A": {"start": 28, "end": 32, "type": float},
        "Pg": {"start": 32, "end": 37, "type": float},
        "Qg": {"start": 37, "end": 42, "type": float},
        "Qn": {"start": 42, "end": 47, "type": float},
        "Qm": {"start": 47, "end": 52, "type": float},
        "Bc": {"start": 52, "end": 58, "type": int},
        "Pl": {"start": 58, "end": 63, "type": float},
        "Ql": {"start": 63, "end": 68, "type": float},
        "Sh": {"start": 68, "end": 73, "type": float},
        "Are": {"start": 73, "end": 76, "type": int},
        "Vf": {"start": 76, "end": 80, "type": int},
        "M": {"start": 80, "end": 81, "type": int}
            },
    "DLIN": {
        "De": {"start": 0, "end": 5, "type": int},
        "d_De": {"start": 5, "end": 6, "type": str},
        "O": {"start": 6, "end": 8, "type": str},
        "d_Pa": {"start": 8, "end": 10, "type": str},
        "Pa": {"start": 10, "end": 15, "type": int},
        "Nc": {"start": 15, "end": 17, "type": int},
        "E": {"start": 17, "end": 18, "type": str},
        "P": {"start": 18, "end": 19, "type": str},
        "M": {"start": 19, "end": 20, "type": str},
        "R": {"start": 20, "end": 26, "type": float},
        "X": {"start": 26, "end": 32, "type": float},
        "Mvar": {"start": 32, "end": 38, "type": float},
        "Tap": {"start": 38, "end": 43, "type": float},
        "Tmn": {"start": 43, "end": 48, "type": float},
        "Tmx": {"start": 48, "end": 53, "type": float},
        "Phs": {"start": 53, "end": 58, "type": float},
        "Bc": {"start": 58, "end": 64, "type": int},
        "Cn": {"start": 64, "end": 68, "type": float},
        "Ce": {"start": 68, "end": 72, "type": float},
        "Ns": {"start": 72, "end": 74, "type": int},
        "Cq": {"start": 74, "end": 78, "type": float}
            },
    "DCCV": {
        "No": {"start": 0, "end": 4, "type": int},
        "O": {"start": 4, "end": 6, "type": str},
        "F": {"start": 6, "end": 7, "type": str},
        "MC": {"start": 7, "end": 9, "type": str},
        "C": {"start": 9, "end": 10, "type": str},
        "Vsp": {"start": 10, "end": 17, "type": float},
        "Marg": {"start": 17, "end": 23, "type": float},
        "Imax": {"start": 23, "end": 29, "type": float},
        "Dsp": {"start": 29, "end": 35, "type": float},
        "Dtn": {"start": 35, "end": 41, "type": float},
        "Dtm": {"start": 41, "end": 47, "type": float},
        "Tmn": {"start": 47, "end": 53, "type": float},
        "Tmx": {"start": 53, "end": 59, "type": float},
        "S": {"start": 59, "end": 62, "type": float},
        "Vmn": {"start": 62, "end": 67, "type": float},
        "Tmh": {"start": 67, "end": 73, "type": float},
        "Ttr": {"start": 73, "end": 48, "type": float},
            },
    "DCER": {
        "No": {"start": 0, "end": 5, "type": int},
        "O": {"start": 6, "end": 7, "type": int},
        "Gr": {"start": 8, "end": 10, "type": int},
        "Un": {"start": 11, "end": 13, "type": int},
        "Kb": {"start": 14, "end": 19, "type": int},
        "Incl": {"start": 20, "end": 26, "type": float},
        "Qg": {"start": 27, "end": 32, "type": float},
        "Qn": {"start": 32, "end": 37, "type": float},
        "Qm": {"start": 37, "end": 42, "type": float},
        "C": {"start": 43, "end": 44, "type": str},
        "E": {"start": 45, "end": 46, "type": str},
        "L": {"start": 47, "end": 48, "type": str},
            }
    }


config_header = {
    "DBAR": "(Num)OETGb(   nome   )Gl( V)( A)( Pg)( Qg)( Qn)( Qm)(Bc  )( Pl)( Ql)( Sh)Are(Vf)M(1)(2)(3)(4)(5)(6)(7)(8)(9)(10   \n",
    "DLIN": "(De )d O d(Pa )NcEPM( R% )( X% )(Mvar)(Tap)(Tmn)(Tmx)(Phs)(Bc  )(Cn)(Ce)Ns(Cq)(1)(2)(3)(4)(5)(6)(7)(8)(9)(10   \n",
    "DCCV": "(No) O FMC (Vsp) (Marg (IMax (Dsp) (Dtn) (Dtm) (Tmn) (Tmx) (S (Vmn (Tmh) (Ttr)   \n"
    }


class FuncsCepel:
    def __init__(self, type_cepel='DBAR'):
        """
        Inicializa a classe FuncsCepel com um tipo padrão para as seções do arquivo.
        
        Parâmetros:
        - type_cepel (str): Tipo padrão das seções do arquivo (exemplo: 'DBAR', 'DLIN').
        """
        global config  # Configuração global
        self.config = config_cepel
        self.type_cepel = type_cepel

    def extrair_secao(self, type_cepel=None, text=None):
        """
        Retorna uma seção contida entre {seção_nome} e a terminação 99999 no texto fornecido.

        Parâmetros:
        - type_cepel (str): Tipo da seção a ser extraída (default: `self.type_cepel`).
        - text (str): Texto do qual a seção será extraída (default: `self.conteudo`).

        Retorno:
        - str: Conteúdo da seção extraída ou None se não encontrado.
        """
        type_cepel = type_cepel or self.type_cepel
        padrao = rf"{type_cepel}(.*?)(\n\s*99999.*?\n\s*99999)"
        if text is None:
            resultado = re.search(padrao, self.conteudo, re.DOTALL)
        else:
            resultado = re.search(padrao, text, re.DOTALL)
        if resultado:
            return resultado.group(1).strip()
        return None

    def dict_to_df(self, type_cepel=None):
        """
        Converte uma seção de um arquivo PWF em um DataFrame.

        Parâmetros:
        - type_cepel (str): Tipo da seção a ser convertida (default: `self.type_cepel`).

        Retorno:
        - pd.DataFrame: DataFrame contendo os dados extraídos.
        """
        type_cepel = type_cepel or self.type_cepel
        try:
            data_raw = self.extrair_secao(type_cepel)
            if not data_raw:
                print(f"Não foi possível obter os dados contidos em {type_cepel}. Verifique se o arquivo contém {type_cepel}.")
                return None

            config_data = self.config.get(type_cepel)
            data_dict = {key: [] for key in config_data.keys()}

            for line in data_raw.split('\n'):
                for key, value in config_data.items():
                    start, end, dtype = value["start"], value["end"], value["type"]
                    try:
                        data_dict[key].append(dtype(line[start:end].strip()))
                    except ValueError:
                        if dtype is float:
                            data_dict[key].append(0.0)
                        elif dtype in (str, int):
                            data_dict[key].append("")
                        else:
                            data_dict[key].append("-")  # Caso dtype seja algo inesperado

            df = pd.DataFrame(data_dict)
            df = df.drop(index=0)  # Ajuste caso precise descartar a primeira linha
            return df
        except Exception as e:
            print(f"Ocorreu um erro ao converter para DataFrame: {e}")
            return None


    def get_df_dbar(self, report_path):
        """
        Converte a seção DBAR do arquivo PWF para DataFrame.

        Args:
            report_path: Corresponde ao caminho associado ao arquivo PWF.

        Returns:
            DataFrame: Dados da seção DBAR no formato DataFrame.
        """
        self.report_path = report_path
        try:
            try:
                # Primeiro tenta abrir o arquivo sem especificar a codificação
                with open(self.report_path, "r") as arquivo:
                    self.conteudo = arquivo.read()
            except UnicodeDecodeError:
                # Caso falhe, tenta abrir o arquivo com encoding 'cp1252'
                with open(self.report_path, "r", encoding="cp1252") as arquivo:
                    self.conteudo = arquivo.read()
            # Converte o conteúdo para DataFrame
            self.df_dbar = self.dict_to_df("DBAR")
            return self.df_dbar
        except FileNotFoundError:
            print("Não foi possí­vel encontrar o relatório")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo: {e}")
            return None

    def get_df_dcer(self, report_path):
        """
        Converte a seção DCER do arquivo PWF para DataFrame.

        Args:
            report_path: Corresponde ao caminho associado ao arquivo PWF.

        Returns:
            DataFrame: Dados da seção DCER no formato DataFrame.
        """
        self.report_path = report_path
        try:
            try:
                # Primeiro tenta abrir o arquivo sem especificar a codificação
                with open(self.report_path, "r") as arquivo:
                    self.conteudo = arquivo.read()
            except UnicodeDecodeError:
                # Caso falhe, tenta abrir o arquivo com encoding 'cp1252'
                with open(self.report_path, "r", encoding="cp1252") as arquivo:
                    self.conteudo = arquivo.read()
            # Converte o conteúdo para DataFrame
            self.df_dcer = self.dict_to_df("DCER")
            return self.df_dcer
        except FileNotFoundError:
            print("Não foi possí­vel encontrar o relatório")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo: {e}")
            return None

    def get_df_by_key(self, report_path, type_cepel=None):
        """
        Converte a seção DCER do arquivo PWF para DataFrame.

        Args:
            report_path: Corresponde ao caminho associado ao arquivo PWF.

        Returns:
            DataFrame: Dados da seção DCER no formato DataFrame.
        """
        # adaptar o código para analisar os tipos válidos
        self.report_path = report_path
        type_cepel = type_cepel or self.type_cepel
        try:
            try:
                # Primeiro tenta abrir o arquivo sem especificar a codificação
                with open(self.report_path, "r") as arquivo:
                    self.conteudo = arquivo.read()
            except UnicodeDecodeError:
                # Caso falhe, tenta abrir o arquivo com encoding 'cp1252'
                with open(self.report_path, "r", encoding="cp1252") as arquivo:
                    self.conteudo = arquivo.read()
            # Converte o conteúdo para DataFrame
            self.df_type_cepel = self.dict_to_df(type_cepel)
            return self.df_type_cepel
        except FileNotFoundError:
            print("Não foi possí­vel encontrar o relatório")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo: {e}")
            return None


    def ajusta_float_string(self, value_key, valor, largura_valor):
        self.value_key = value_key
        self.valor = valor
        self.largura_valor = largura_valor
        if self.value_key  == 'V':
            self.valor= self.valor*1000
        self.valor = round(self.valor, 1)    
        parte_fracionaria = str(abs(self.valor)).split('.')[1]
        primeiro_digito = parte_fracionaria[0]
        # Formata o novo valor de `Pg` com uma casa decimal
        valor_formatado = ""
        if self.valor == 0:
            valor_formatado = "".rjust(self.largura_valor)[:self.largura_valor]
        elif primeiro_digito == '0' or abs(self.valor)/(10**(self.largura_valor-1))>=1: #ajustar para que 10000 seja dependente da largura do float
            if self.value_key == 'V':
                valor_formatado = f"{self.valor:.0f}".rjust(self.largura_valor)[:self.largura_valor]
            else:
                valor_formatado = f"{self.valor:.0f}.".rjust(self.largura_valor)[:self.largura_valor]
        if abs(self.valor) > 0 and primeiro_digito != '0': 
            valor_formatado = f"{self.valor:.1f}".rjust(self.largura_valor)[:self.largura_valor]
        return valor_formatado


    def atualizar_valores_dbar(self, value_key:str, str_dbar: str, novos_valores: pd.DataFrame, operacao=True) -> str:
        """
        Atualiza valores no arquivo DBAR baseado nos valores fornecidos.

        Args:
            value_key: Corresponde a variável que será alterada. Ex: "Pg" Qg, V.
            str_dbar (str): String associada ao conteúdo completo do arquivo .PWF. É possí­vel obter str_dbar com a função extrair_secao
            novos_valores (pd.DataFrame): DataFrame com colunas `Nb` (número da barra) e valor tipo float a ser atualizado: Pg, Qg, etc.

        Returns:
            str: String contendo o arquivo DBAR atualizado.
        """
        self.value_key = value_key
        self.str_dbar = str_dbar
        self.novos_valores = novos_valores
        self.operacao = operacao
        
        dbar_dict = config_cepel.get("DBAR")
        valid_value_key = list(dbar_dict.keys())
        if self.value_key not in valid_value_key:
           raise ValueError("O parâmetro a ser alterado não é valido. Os valores válidos sãoo Pg, Qg, Pl, Ql, e V")
        else:
            dbar_dict = config_cepel.get("DBAR")
            # Converter `novos_valores` para um dicionário para acesso rápido
            valores_dict = self.novos_valores.set_index("Nb")[self.value_key].to_dict()
            linhas_atualizadas = []
            linhas_modificadas = []
            value_start = dbar_dict[self.value_key]["start"]
            value_end = dbar_dict[self.value_key]["end"]
            value_length = value_end - value_start
            operador_start = dbar_dict["O"]["start"]
            operador_end = dbar_dict["O"]["end"]
            for linha in self.str_dbar.splitlines():
                linha = linha.ljust(81)
                # Verifica se a linha contém um valor de barra ('Nb') válido
                nb_start = dbar_dict["Nb"]["start"]
                nb_end = dbar_dict["Nb"]["end"]
                try:
                    nb = int(linha[nb_start:nb_end].strip())
                except ValueError:
                    # Ignorar linhas que não tem número de barra válido
                    linhas_atualizadas.append(linha)
                    continue
        
                if nb in valores_dict:
                    # Atualiza a coluna 'Pg' com o novo valor
                    new_value = valores_dict[nb]
                    if type(new_value) is float:
                        new_value_formatted = self.ajusta_float_string(self.value_key, new_value, value_length)
                    else:
                        new_value_formatted = str(new_value)
                        new_value_formatted = new_value_formatted.rjust(value_length)[:value_length]
                    
                    linha = linha[:value_start] + new_value_formatted + linha[value_end:]
                    # print(linha)
                    linha_mod = linha[:operador_start]+"2"+ linha[operador_end:]
                    linhas_modificadas.append(linha_mod)
                # Adiciona a linha (atualizada ou não) a lista de saÃ­da
                linhas_atualizadas.append(linha)
        
            # Retorna as linhas atualizadas como uma única string
            if self.operacao:
                return "\n".join(linhas_modificadas)
            else:
                return "\n".join(linhas_atualizadas)

    def get_value_length(self, type_cepel=None):
        type_cepel = type_cepel or self.type_cepel
        config_data = config_cepel.get(type_cepel)
        # Inicializando o dicionário resultante
        result_dict = {}
        # Iterando sobre os itens do dicionário de configuração
        for key, value_dict in config_data.items():
            value_start, value_end, dtype = value_dict["start"], value_dict["end"], value_dict["type"]
            value_length = value_end - value_start
            # Adicionando ao dicionário de resultados
            result_dict[key] = {
                "value_length": value_length,
                "dtype": dtype
            }
        return result_dict

     
    def initializing_str(self, df, type_cepel=None):      
        self.df = df
        type_cepel = type_cepel or self.type_cepel
        config_data = config_cepel.get(type_cepel)
        linhas = []
        if type_cepel == "DBAR":
            dbar_dict = config_data
            value_start = dbar_dict["Nb"]["start"]
            value_end = dbar_dict["Nb"]["end"]
            value_length = value_end - value_start
            value_items = self.df["Nb"]
            for item in value_items:
                linha = str(item).rjust(value_length)
                linhas.append(linha)   
            return "\n".join(linhas)    
        else:
            print("O método ainda não está configurado para entrada de dados diferente de DBAR")
            return None
            

    def generate_string(self, df, type_cepel=None):
        type_cepel = type_cepel or self.type_cepel
        """
        Converte um Dataframe para um str no padrão CEPEL.
        Método ainda não está configurado para entrada de dados diferente de DBAR
        Args:
            df(DataFrame): Corresponde a variável que será alterada. Ex: "Pg" Qg, V.
            type cepel(str): é o tipo do código de execução. Ex: DBAR

        Returns:
            str: String da seção no formato .PWF
        """
        self.df = df
        self.type_cepel = type_cepel # type_cepel: DBAR, DLIN, etc..
        if type_cepel != "DBAR":
            print("O método ainda não está configurado para entrada de dados diferente de DBAR")
        else:    
            # valid_value_key = ['Pg', 'Qg', 'Pl', 'Ql', 'V', 'Qn', 'Qm']
            config_data = config_cepel.get(type_cepel)
            config_keys = config_data.keys()
            if set(list(df.columns)) != set(list(config_keys)):
               print("Não é possível converter todos os elementos do DataFrame") 
            if all(item in list(config_keys) for item in list(df.columns)):           
                output = ""
                output += f'{self.type_cepel}\n'
                output += config_header.get(type_cepel)
                if "Nb" not in self.df.columns:
                    raise ValueError("Não é possível realizar a conversão dos dados sem a coluna: Nb")
                else:    
                    output += self.initializing_str(self.df, type_cepel)
                    value_keys = [col for col in self.df.columns if col != "Nb"]
                    # output = self.atualizar_valores_dbar(value_key , output, df, False)
                    for value_key in value_keys:
                        output = self.atualizar_valores_dbar(value_key, output, df, False)
                    output += '\n99999\n'
                    return output
            else:
                raise ValueError(f"O DataFrame contém colunas que não correspondem ao {type_cepel}")
    
    
    def condicionar_pg(self, caminho_arquivo: str, bus_to_query: list, interc_new: float, ug_data: pd.DataFrame) -> pd.DataFrame:
            """
            Ajusta os valores de Pg no arquivo de entrada com base em fatores de participação.
    
            Parâmetros:
            - caminho_arquivo: str -> Caminho para o arquivo que contém dados do tipo DBAR.
            - bus_to_query: list -> Lista de IDs das barras a serem filtrados.
            - interc_new: float -> Valor de ajuste de intercâmbio.
            - ug_data: pd.DataFrame -> DataFrame com os valores mínimos e máximos de geração das usinas.
    
            Retorna:
            - pd.DataFrame -> DataFrame ajustado com os novos valores de Pg.
            """
            # Verificar se a lista bus_to_query está vazia
            if not bus_to_query:
                raise ValueError("A lista bus_to_query não pode estar vazia.")
    
            # Verificar se o ug_data contém as colunas necessárias
            colunas_necessarias = {'Nb', 'PMin (MW)', 'PMax (MW)'}
            if not colunas_necessarias.issubset(ug_data.columns):
                raise ValueError(f"O DataFrame ug_data deve conter as colunas: {colunas_necessarias}")
    
            # Verificar se o arquivo existe
            if not os.path.exists(caminho_arquivo):
                raise ValueError(f"O arquivo {caminho_arquivo} não existe.")
    
            # Obter o DataFrame a partir do arquivo
            df_dbar = self.get_df_dbar(caminho_arquivo)
            if df_dbar is None:
                raise ValueError("Verifique se o arquivo contém dados do tipo DBAR")
    
            # Filtrar o DataFrame com base na lista de IDs
            df_dbar['Nb'] = df_dbar['Nb'].astype(int)
            ug_data['Nb'] = ug_data['Nb'].astype(int)
    
            df_dbar_filtered = df_dbar[df_dbar['Nb'].isin(bus_to_query)]
            ug_data_filtered = ug_data[ug_data['Nb'].isin(bus_to_query)]
            diff_dbar_filtered = set(df_dbar_filtered['Nb']).difference(set(ug_data_filtered['Nb'])) 
            diff_ug_data = set(ug_data_filtered['Nb']).difference(set(df_dbar_filtered['Nb'])) 
            if len(df_dbar_filtered) > len(ug_data_filtered): 
                print(f"Um DataFrame possui mais elementos: {diff_dbar_filtered}") 
            elif len(df_dbar_filtered) < len(ug_data_filtered): 
                print(f"Um DataFrame possui mais elementos: {diff_ug_data}") 
            
            # Verificar se df_dbar_filtered e ug_data contêm exatamente os mesmos valores de bus_to_query
            if set(df_dbar_filtered['Nb']) != set(bus_to_query) or set(ug_data_filtered['Nb']) != set(bus_to_query):
                raise ValueError("df_dbar e ug_data devem conter os valores de Nb da lista bus_to_query.")
    
            # Calcular o total de Pg e o intercâmbio atual
            pg_total = df_dbar_filtered['Pg'].sum()
            interc_atual = float(df_dbar.query("T == 2")['Pg'].iloc[0])
            interc_ajuste = interc_new + interc_atual
            interc_ajuste = round(interc_ajuste, 3)
    
            # Calcular o fator de participação
            pg_min_total = ug_data_filtered['PMin (MW)'].sum()
            pg_max_total = ug_data_filtered['PMax (MW)'].sum()
            fator_part = (interc_ajuste + pg_total - pg_min_total) / (pg_max_total - pg_min_total)
    
            # Criar um novo DataFrame com Nb e Pg ajustados
            df_dbar_new_pg = pd.DataFrame({
                'Nb': ug_data_filtered['Nb'],
                'Pg': ug_data_filtered['PMin (MW)'] + fator_part * (ug_data_filtered['PMax (MW)'] - ug_data_filtered['PMin (MW)'])
            })
            # Ajustar Pg para não ser menor que PMin (MW)
            df_dbar_new_pg['Pg'] = df_dbar_new_pg['Pg'].clip(lower=ug_data_filtered['PMin (MW)'])
            return df_dbar_new_pg


class TemplateCepel:
    def __init__(
        self, 
        file_path, 
        save_name=None, 
        rest_save_case=True, 
        case_number=None,
        save_name_to_save=None, 
        case_number_to_save=None, 
        content_flag=True, 
        content_text="", 
        save_pwf_report=False, 
        name_pwf_report=None, 
        close_anarede=True,
        save_cartao_pwf=True,
        name_cartao_pwf=None
    ):
        self.file_path = file_path
        self.save_name = save_name
        self.rest_save_case = rest_save_case
        self.case_number = case_number
        self.save_name_to_save = save_name_to_save
        self.case_number_to_save = case_number_to_save
        self.content_flag = content_flag
        self.content_text = content_text
        self.save_pwf_report = save_pwf_report
        self.name_pwf_report = name_pwf_report
        self.close_anarede = close_anarede
        self.save_cartao_pwf=save_cartao_pwf
        self.name_cartao_pwf=name_cartao_pwf

    def create_template(self):
        # Inicia o template vazio
        template = ""
        
        # Verifica se rest_save_case está habilitado e se save_name e case_number foram fornecidos
        if self.rest_save_case:
            if not self.save_name or self.case_number is None:
                raise ValueError("Para 'rest_save_case=True', 'save_name' e 'case_number' devem ser fornecidos.")
            
            # Adiciona as linhas de restauração ao template
            template += (
                "ULOG                                                                \n"
                " 2\n"
                f"{self.file_path}{self.save_name}.SAV\n"
                "ARQV REST\n"
                f"{self.case_number}\n"
                "\n"
            )
        
        # Adiciona outras configuraÃ§Ãµes ao template como linhas adicionais
        if self.content_flag:
            template += self.content_text
            template += "\n"
        # if self.content_text:
        #     template += f"DBAR {self.content_text}\n"
        if self.save_name_to_save and self.case_number_to_save is not None:
            template += (
                f"TITU\n"
                f"{self.save_name_to_save}\n"
                f"ARQV GRAV SUBS AREG NOVO\n"
                f"{self.case_number_to_save}\n"
                "\n"
            )
        if self.save_pwf_report:
            if not self.name_pwf_report is not None:
                raise ValueError("Para 'save_pwf_report=True', 'name_pwf_report' deve ser fornecido.")
            template += (
                "ULOG                                                                \n"
                 " 7\n"
                f"{self.file_path}{self.name_pwf_report}.pwf\n"
                "CART                                                                \n"
                "\n"
                )
        if self.close_anarede:
            template += (
            "( Fecha ANAREDE \n"
            "DOSC \n"
            # Remova o comentário caso queira usar a linha abaixo
            # f"DEL {PWD}{json_template.get('fileDGEI')}\n"
            "TASKKILL /T /F /IM ANAREDE.EXE \n"
            "99999 \n"
            "FIM\n")
        
        if self.save_cartao_pwf and self.name_cartao_pwf is not None:
            pwf_name = f"{self.file_path}{self.name_cartao_pwf}.pwf"
            with open(pwf_name, 'w') as fileID:
                fileID.write(template)
            return {pwf_name: template}
        else:
            return template

    # def save_template(self, template, name_cartao_pwf):


def run_anarede(ANAREDE, PWD, fileNAME): 
    try:
        # Obtém a extensão do arquivo
        file_type = os.path.splitext(fileNAME)[1]
        if file_type != '.pwf':
            raise ValueError(f"A extensão do arquivo {fileNAME} é incorreta ou não foi fornecida")
        
        # Verifica se o arquivo existe
        if not os.path.isfile(os.path.join(PWD, fileNAME)):
            raise ValueError(f"Verifique se o arquivo {fileNAME} se encontra no diretório {PWD}")
        
        def normalize_path(path):
            if os.name == 'nt':  # Somente no Windows
                return path[0].upper() + path[1:] if ':' in path else path
            return path  # Em outros sistemas, o case não importa
        
        # Executa o comando ANAREDE
        # proc = Popen(f'{ANAREDE} "{os.path.join(PWD, fileNAME)}"', stdout=PIPE, stderr=PIPE, shell=True)
        file_path_pwf = normalize_path(os.path.join(PWD, fileNAME))
        proc = Popen([ANAREDE, file_path_pwf], stdout=PIPE, stderr=PIPE, shell=True)
        proc.communicate()
        proc.wait()  # Aguarda o término do processo antes de continuar
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"Não foi possí­vel identificar a extensão do arquivo {fileNAME}: {e}")






# Exemplo de uso
# if __name__=='__main__':
    
# # Inserir mais exemplos de uso
    
#     content_text = (
#         'DBAR\n'
#         '    12L1 GERRO---IPU50 G           0.   0.-999999999                     10010000\n'
#         '430002L2 NAYO B1   500 N1050  0.   0.   0.-999999999                     10310260\n'
#         '99999\n'
#         'EXLF NEWT CREM CTAP VLIM STEP RMON MFCT RCVG\n')
    
#     file_path = (os.getcwd() + '\\').replace("\\", "/")
#     save_name = "ajusta_caso"
#     case_number = 1
#     save_name_to_save = "ajusta_caso_exe"
#     case_number_to_save = 98
#     name_pwf_report = "resultado"
    
#     template_cepel = TemplateCepel(
#         file_path=file_path,
#         save_name=save_name,
#         case_number=case_number_to_save,
#         save_name_to_save=save_name_to_save,
#         case_number_to_save=case_number_to_save,
#         content_text=content_text,
#         save_pwf_report=True,
#         name_pwf_report=name_pwf_report,
#         close_anarede=True,
#         save_cartao_pwf=True,
#         name_cartao_pwf='exemplo'

#     )
#     template = template_cepel.create_template()
    
#     print("Template gerado:")
#     print(template)