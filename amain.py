import csv
import os
import glob
from datetime import datetime, timedelta

# DONE


def validarHorario(mensagem):
    """
    Valida horário no formato HH:MM, incluindo horas (00-23) e minutos (00-59).
    """
    while True:
        horario = input(f"{mensagem} (Ex: 23:59)\n> ")
        if (
            len(horario) == 5
            and horario[2] == ':'
            and horario[:2].isdigit()
            and horario[3:].isdigit()
        ):
            horas = int(horario[:2])
            minutos = int(horario[3:])
            if 0 <= horas <= 23 and 0 <= minutos <= 59:
                return horas, minutos
        print("Horário inválido! Use o formato HH:MM (Ex: 14:30).")

# DONE


def calcularDuracao(hInicio, minInicio, hFim, minFim, qtdDias):
    """Calcula a diferença entre dois horários, multiplica pelos dias e retorna a duração total
    e 75% dessa duração em horas e minutos."""

    # Converter horários para minutos usando paraMinutos()
    total_inicio = HMparaMinutos(hInicio, minInicio)
    total_fim = HMparaMinutos(hFim, minFim)

    # Calcular diferença diária (tratando caso em que passa para o dia seguinte)
    if total_fim < total_inicio:
        total_fim += 24 * 60

    # Aqui tem, em minutos, o total diario em M
    diferenca_diaria = total_fim - total_inicio

    # Calcular total acumulado para todos os dias
    total_acumulado = diferenca_diaria * qtdDias

    # Converter total acumulado para horas e minutos
    # horas_total, minutos_total = minutosParaHoraMinuto(total_acumulado)

    # Calcular 75% do total acumulado
    total_75 = total_acumulado * 0.75
    # horas_75 = int(total_75 // 60)
    # minutos_75 = int(total_75 % 60)

    # retorna o total da reunião, 75% do total e total por dia

    return paraDecimal(total_acumulado), paraDecimal(total_75), paraDecimal(diferenca_diaria)

# ==================================== #
# ============ Time Utils ============ #
# =============== Begin ============== #


def minutosParaHoraMinuto(total_minutos):
    """Converte minutos totais para (horas, minutos)"""
    return divmod(total_minutos, 60)


def HMparaMinutos(horas, minutos=0):
    return int(horas * 60 + minutos)


def paraDecimal(*args):
    """Converte para formato decimal."""
    if len(args) == 2:  # Recebeu horas E minutos
        horas, minutos = args
        return horas + minutos / 60
    elif len(args) == 1:  # Assume ser minutos totais
        return args[0] / 60
    else:
        raise ValueError("Use: (horas, minutos) OU (minutos_totais)")


def decimalParaMinutos(horas_decimal):
    """Converte horas em formato decimal para minutos totais."""
    return int(round(horas_decimal * 60))


def printDecimalParaHora(horas_decimal):
    """Converte horas decimais para formato HH:MM e retorna como string."""
    minutos_totais = round(horas_decimal * 60)
    horas = minutos_totais // 60
    minutos = minutos_totais % 60
    return f"{horas:02d}:{minutos:02d}"

# ================ End =============== #
# ============ Time Utils ============ #
# ==================================== #


# DONE
def imprimir_conteudo_cru(linhas):
    print("\n" + ("=" * 50))
    print("Conteúdo cru completo do arquivo:")
    print(("=" * 23) + " INÍCIO " + ("=" * 23))
    for linha in linhas:
        print(linha)
    print(("=" * 25) + " FIM " + ("=" * 25))

# DONE


def listarArquivosCSV():
    """Lista todos os arquivos CSV no diretório atual"""
    arquivosCSV = glob.glob("*.csv")
    if not arquivosCSV:
        print("\nNenhum arquivo CSV encontrado no diretório atual.")
        return None

    print("\nArquivos CSV encontrados no diretório atual:")
    for i, arquivo in enumerate(arquivosCSV, start=1):
        print(f"{i}. {arquivo}")

    return arquivosCSV

# DONE

def verificarQtdCSV(arquivosCSV, qtdDias):
    if not arquivosCSV:
        print("\nNão existem arquivos para serem lidos nessa pasta, por favor tente novamente.")
        return False
    
    if qtdDias > len(arquivosCSV):
        print(f"\nA quantidade de dias ({qtdDias}) é maior do que o número de CSVs nesta pasta: ({len(arquivosCSV)}), por favor tente novamente.")
        return False  # indica que deve sair do while
    
    return True  # condições OK, pode continuar no while

# DONE


def selecionarMultiplosArquivos(qtdDias, arquivosCSV):
    """Permite ao usuário selecionar vários arquivos da lista com base no número de dias do curso """
    while True:
        try:
            selecionados = []
            print(f"\nSelecione {qtdDias} arquivo(s) da lista acima:")
            # for i, arquivo in enumerate(arquivosCSV, start=1):
            #     print(f"{i}. {arquivo}")
            for _ in range(qtdDias):
                while True:
                    try:
                        escolha = input(
                            f"Digite o número do arquivo {_+1}/{qtdDias}: "
                        )
                        escolha_num = int(escolha)
                        if 1 <= escolha_num <= len(arquivosCSV):
                            arquivo = arquivosCSV[escolha_num - 1]
                            if arquivo not in selecionados:
                                selecionados.append(arquivo)
                                break
                            else:
                                print(
                                    "Este arquivo já foi selecionado. Escolha outro.")
                        else:
                            print(
                                f"Por favor, digite um número entre 1 e {len(arquivosCSV)}"
                            )
                    except ValueError:
                        print("Entrada inválida. Por favor, digite um número.")

            return selecionados
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

# TODO


def lerArquivoCSV(arquivos_selecionados):
    # Inicializa listas para armazenar dados de todos os arquivos
    todos_nomes = []
    todas_entradas = []
    todas_saidas = []
    todas_duracoes = []
    todos_outros_dados = []

    # Verifica se arquivos_selecionados é uma lista ou um único arquivo (str)
    if isinstance(arquivos_selecionados, str):
        arquivos_selecionados = [arquivos_selecionados]  # Transforma em lista

    for nome_arquivo in arquivos_selecionados:
        try:
            with open(nome_arquivo, mode="r", encoding="utf-16") as arquivo:
                leitor = csv.reader(arquivo, delimiter="\t")
                rawMatrix = list(leitor)

                # --- PRIMEIRAS LINHAS (CAMPOS ESPECÍFICOS) ---
                outros_dados = {}
                for linha in rawMatrix[1:7]:  # Linhas 2 a 7
                    if len(linha) >= 2:
                        campo = linha[0].strip()
                        valor = linha[1].strip()
                        outros_dados[campo] = valor

                # --- DADOS DOS PARTICIPANTES (VETORES) ---
                nomes = []
                entradas = []
                saidas = []
                duracoes = []

                for linha in rawMatrix[9:]:  # Linhas 10 em diante
                    if len(linha) <= 1:  # Linha vazia ou sem dados relevantes
                        break

                    if len(linha) >= 4:
                        nomes.append(linha[0].strip())
                        entradas.append(linha[1].strip())
                        saidas.append(linha[2].strip())
                        duracoes.append(linha[3].strip())

                # Adiciona os dados deste arquivo às listas principais
                todos_nomes.append(nomes)
                todas_entradas.append(entradas)
                todas_saidas.append(saidas)
                todas_duracoes.append(duracoes)
                todos_outros_dados.append(outros_dados)

        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado: {nome_arquivo}")
            continue  # Pula para o próximo arquivo
        except Exception as e:
            print(f"Erro inesperado ao processar {nome_arquivo}: {str(e)}")
            continue

    return { # TODO Checar isso aqui
        "nomes": todos_nomes,          # Matriz: cada linha = lista de nomes de um CSV
        "entradas": todas_entradas,    # Matriz: cada linha = lista de entradas de um CSV
        "saidas": todas_saidas,        # Matriz: cada linha = lista de saídas de um CSV
        "duracoes": todas_duracoes,    # Matriz: cada linha = lista de durações de um CSV
        "outros_dados": todos_outros_dados,  # Lista de dicionários (um por CSV)
    }


def ordenarDadosPorNome(dados_formatados):
    """Ordena todos os dados alfabeticamente pelo nome (mantendo a correspondência entre listas)"""
    dados_ordenados = {
        "nomes": [],
        "entradas": [],
        "saidas": [],
        "duracoes": [],
        "outros_dados": dados_formatados["outros_dados"]  # Metadados não são ordenados
    }

    for idx_arquivo in range(len(dados_formatados["nomes"])):
        # Junta os dados em uma lista de tuplas (nome, entrada, saida, duracao)
        dados_agrupados = list(zip(
            dados_formatados["nomes"][idx_arquivo],
            dados_formatados["entradas"][idx_arquivo],
            dados_formatados["saidas"][idx_arquivo],
            dados_formatados["duracoes"][idx_arquivo]
        ))

        # Ordena pelo nome (primeiro elemento da tupla)
        dados_agrupados.sort(key=lambda x: x[0].lower())  # Case-insensitive

        # Desempacota os dados ordenados de volta para as listas
        nomes_ordenados, entradas_ordenadas, saidas_ordenadas, duracoes_ordenadas = zip(*dados_agrupados)

        # Converte de tuplas para listas (se necessário)
        dados_ordenados["nomes"].append(list(nomes_ordenados))
        dados_ordenados["entradas"].append(list(entradas_ordenadas))
        dados_ordenados["saidas"].append(list(saidas_ordenadas))
        dados_ordenados["duracoes"].append(list(duracoes_ordenadas))

    return dados_ordenados

# def nomeUnico(CSV):


# =======================#

# TODO


def calcularTempo(inicio_str, fim_str):
    # Função para converter string HH:MM para objeto datetime (com data fictícia)
    def parse_time(time_str):
        hora, minuto = map(int, time_str.split(":"))
        # Usamos uma data arbitrária (hoje) apenas para criar o objeto datetime
        hoje = datetime.now().date()
        return datetime.combine(hoje, datetime.time(hora, minuto))

    # Converte as strings para datetime
    inicio_dt = parse_time(inicio_str)
    fim_dt = parse_time(fim_str)

    # Calcula a diferença
    diferenca = fim_dt - inicio_dt

    # Converte para horas, minutos e segundos
    total_segundos = diferenca.total_seconds()
    horas = int(total_segundos // 3600)
    minutos = int((total_segundos % 3600) // 60)
    segundos = int(total_segundos % 60)

    return total_segundos, horas, minutos, segundos

# TODO

def calcularTempoLimitado(entrada_str, saida_str, inicio_limite_str, fim_limite_str):
    # Converte strings para objetos datetime
    def parse_datetime(dt_str):
        parts = dt_str.strip().split(', ')
        date_part = parts[0]
        time_part = parts[1].split(' ')
        time_value = time_part[0]
        ampm = time_part[1]

        day, month, year = date_part.split('/')
        hour, minute, second = time_value.split(':')

        hour = int(hour)
        if ampm.upper() == 'PM' and hour != 12:
            hour += 12
        elif ampm.upper() == 'AM' and hour == 12:
            hour = 0

        return datetime(int('20' + year), int(month), int(day), hour, int(minute), int(second))

    # Converte horários de limite (HH:MM) para datetime (usando a mesma data da entrada)
    def parse_limite(time_str, base_date):
        hour, minute = map(int, time_str.split(':'))
        return datetime(base_date.year, base_date.month, base_date.day, hour, minute)

    entrada_dt = parse_datetime(entrada_str)
    saida_dt = parse_datetime(saida_str)

    # Pega a data da entrada para aplicar os limites
    inicio_limite_dt = parse_limite(inicio_limite_str, entrada_dt)
    fim_limite_dt = parse_limite(fim_limite_str, entrada_dt)

    # Ajusta entrada_dt e saida_dt para ficarem dentro dos limites
    entrada_ajustada = max(entrada_dt, inicio_limite_dt)
    saida_ajustada = min(saida_dt, fim_limite_dt)

    # Se a saída for antes do início ajustado, tempo é zero
    if saida_ajustada <= entrada_ajustada:
        return 0.0, 0, 0, 0

    # Calcula a diferença
    diferenca = saida_ajustada - entrada_ajustada
    total_segundos = diferenca.total_seconds()

    horas = int(total_segundos // 3600)
    minutos = int((total_segundos % 3600) // 60)
    segundos = int(total_segundos % 60)

    return total_segundos, horas, minutos, segundos
# =======================#


def main():
    print("\n===== Leitor de Arquivos CSV =====")
    print("feito por: @dominicnsg")
    print("contato comercial: douglasnicsg@hotmail.com")
    
    # lembrar do /r
    while True:

        while True:
            # Leitura e Calculo da duracao da reunião
            hInicio, mInicio = validarHorario("\nQue horas começou a reunião?")
            hFim, mFim = validarHorario("\nQue horas terminou a reunião?")

            # tratar 0 aqui
            qtdDias = int(
                input("\nQuantos dias (listas de presença) teve o curso?:\n> "))
            # if qtdDias <= 0:
            # print("Por favor, tente novamente digitando a quantidade de dias positiva")
            # return 0

            totalDuracao, total75, totalDiario = calcularDuracao(
                hInicio, mInicio, hFim, mFim, qtdDias)

            print(f"\n# Duração total: {printDecimalParaHora(totalDuracao)}")
            print(f"# 75% do total: " + printDecimalParaHora(total75))
            print(f"# Duração por dia: " + printDecimalParaHora(totalDiario))

            resp = input(
                "\nAs informacoes acima estao corretas? (s/n) \n> ").strip().lower()

            if resp == 's':
                break
            print("\nVamos ajustar os horários novamente...")


        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
        print("-Limpando a tela...")

        print("\n-Lendo arquivos CSV disponíveis...")
        arquivosCSV = listarArquivosCSV()
        if not verificarQtdCSV(arquivosCSV, qtdDias):
            break
        
        arquivosSelecionados = selecionarMultiplosArquivos(
            qtdDias, arquivosCSV)  # guarda em CSV
        if not arquivosSelecionados:
            break

        # print("===================================================")
        # print(arquivosSelecionados)
        # print("===================================================")

        dadosFormatados = lerArquivoCSV(arquivosSelecionados)
        dadosFormatados = ordenarDadosPorNome(dadosFormatados)

        for i in range(len(arquivosSelecionados)):
            print(f"\n=== Dados do Arquivo {i+1}: {arquivosSelecionados[i]} ===")
            print("Nomes:", dadosFormatados["nomes"][i])
            print("Entradas:", dadosFormatados["entradas"][i])
            print("Saídas:", dadosFormatados["saidas"][i])
            print("Durações:", dadosFormatados["duracoes"][i])
            print("Metadados:", dadosFormatados["outros_dados"][i])

        # for arquivo in arquivosSelecionados:
            # mudar lerarquivo para receber arquivos selecionados e realizar um
            # for dentro da funcao para guardar as informacoes de todos os arquivos
            # passar por cada arquivo para perguntar se tem nomes repetidos e juntar

            # dadosFormatados = lerArquivoCSV(arquivo)
            # dadosTratados = tratarDados(dadosFormatados)
            # listaPresenca(montarTabela(dadosTratados))

        continuar = input(
            "\nDeseja repetir o processo? (s/n): ").strip().lower()

        if continuar != "s":
            break


if __name__ == "__main__":
    main()
