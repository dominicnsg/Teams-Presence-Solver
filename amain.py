import csv
import os
import glob
from datetime import datetime, timedelta

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
def selecionarMultiplosArquivos():
    """Permite ao usuário selecionar vários arquivos da lista com base no número de dias do curso """
    
    print("\nLendo arquivos CSV disponíveis...")
    arquivosCSV = listarArquivosCSV()
    if not arquivosCSV:
        print("\nNão existem arquivos para serem lidos nessa pasta, por favor tente novamente.")
        return None

    while True:
        try:
            print(f"\nExistem {len(arquivosCSV)} arquivos disponíveis.")
            qtdDias = input("Quantos dias (listas de presença) teve o curso?:\n> ")

            if qtdDias.lower() == "0":
                return None

            qtdDias = int(qtdDias)
            if qtdDias <= 0:
                print("Por favor, digite um número positivo.")
                continue
            if qtdDias > len(arquivosCSV):
                print(f"Por favor, digite um número até {len(arquivosCSV)}")
                continue

            selecionados = []
            print(f"\nSelecione {qtdDias} arquivo(s) da lista:")
            for i, arquivo in enumerate(arquivosCSV, start=1):
                print(f"{i}. {arquivo}")
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
                                print("Este arquivo já foi selecionado. Escolha outro.")
                        else:
                            print(
                                f"Por favor, digite um número entre 1 e {len(arquivosCSV)}"
                            )
                    except ValueError:
                        print("Entrada inválida. Por favor, digite um número.")

            return selecionados
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

# DONE
def imprimir_conteudo_cru(linhas):
    print("\n" + ("=" * 50))
    print("Conteúdo cru completo do arquivo:")
    print(("=" * 23) + " INÍCIO " + ("=" * 23))
    for linha in linhas:
        print(linha)
    print(("=" * 25) + " FIM " + ("=" * 25))

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

# TODO
def lerArquivoCSV(nome_arquivo):
    # Inicializa os vetores (listas) para cada campo
    nomes = []
    entradas = []
    saidas = []
    duracoes = []
    outros_dados = {}  # Para as primeiras linhas (caso ainda queira mantê-las)

    try:
        with open(nome_arquivo, mode="r", encoding="utf-16") as arquivo:
            leitor = csv.reader(arquivo, delimiter="\t")
            rawMatrix = list(leitor)  # Matriz com todas as linhas

            # --- PRIMEIRAS LINHAS (CAMPOS ESPECÍFICOS) ---
            print("\n" + "=" * 50)
            print("Dados processados (7 primeiras linhas):")
            print("=" * 50)
            for linha in rawMatrix[1:7]:  # Linhas 2 a 7
                if len(linha) >= 2:
                    campo = linha[0].strip()
                    valor = linha[1].strip()
                    outros_dados[campo] = valor
                    print(f"{campo}: {valor}")

            # --- DADOS DOS PARTICIPANTES (VETORES) ---
            print("\n" + "=" * 50)
            print("Dados dos participantes (vetores):")
            print("=" * 50)
            for linha in rawMatrix[9:]:  # Linhas 10 em diante
                # Verifica se a linha começa com "3. Atividades" e interrompe o loop
                if len(linha) <=1: # and linha[0].strip() == "3. Atividades":
                    break
                    
                if len(linha) >= 4:
                    # Adiciona cada campo ao seu respectivo vetor
                    nomes.append(linha[0].strip())
                    entradas.append(linha[1].strip())
                    saidas.append(linha[2].strip())
                    duracoes.append(linha[3].strip())

            print("\nExemplo de acesso aos vetores:")
            for i in range(len(nomes)):
                print(f"Participante {i + 1}:")
                print(f"  Nome: {nomes[i]}")
                print(f"  Entrada: {entradas[i]}")
                print(f"  Saída: {saidas[i]}")
                print(f"  Duração: {duracoes[i]}\n")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {nome_arquivo}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

    # Retorna os vetores (opcional)
    return {
        "nomes": nomes,
        "entradas": entradas,
        "saidas": saidas,
        "duracoes": duracoes,
        "outros_dados": outros_dados,
    }
    
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

# TODO
def calcularDuracao(hInicio, minInicio, hFim, minFim):
    """Calcula a diferença entre dois horários e retorna a duração em horas e minutos,
    bem como 75% dessa duração."""
    # Converter tudo para minutos
    total_inicio = hInicio * 60 + minInicio
    total_fim = hFim * 60 + minFim
    
    # Calcular diferença (tratando caso em que passa para o dia seguinte)
    if total_fim < total_inicio:
        total_fim += 24 * 60  # Adiciona 24 horas se terminar no dia seguinte
    
    diferenca = total_fim - total_inicio
    
    # Converter de volta para horas e minutos
    horas = diferenca // 60
    minutos = diferenca % 60
    
    # Calcular 75% da duração (em minutos)
    diferenca_75 = diferenca * 0.75
    horas_75 = int(diferenca_75 // 60)
    minutos_75 = int(diferenca_75 % 60)
    
    return horas, minutos, horas_75, minutos_75

def main():
    print("\n=== Leitor de Arquivos CSV ===")

    while True:
        
        while True:
            # Leitura e Calculo da duracao da reunião
            hInicio, mInicio = validarHorario("\nQue horas começou a reunião?")
            hFim, mFim = validarHorario("\nQue horas terminou a reunião?")
            
            hTotal, mTotal, h75, m75 = calcularDuracao(hInicio, mInicio, hFim, mFim)
            
            print(f"\n⏳ Duração calculada: {hTotal:02d}:{mTotal:02d}")
            print(f"75% da duração: {h75} horas e {m75} minutos")
            
            resp = input("\nA duração está correta? (s/n) \n> ").strip().lower()
            
            if resp == 's':
                break
            print("\nVamos ajustar os horários novamente...")
        
        arquivosSelecionados = selecionarMultiplosArquivos() # guarda em CSV
        if not arquivosSelecionados:
            break

        # print("===================================================")
        # print(arquivosSelecionados)
        # print("===================================================")



        
        for arquivo in arquivosSelecionados:
            #mudar lerarquivo para receber arquivos selecionados e realizar um
            #for dentro da funcao para guardar as informacoes de todos os arquivos
            # passar por cada arquivo para perguntar se tem nomes repetidos e juntar
            
            dadosFormatados = lerArquivoCSV(arquivo)
            #dadosTratados = tratarDados(dadosFormatados)
            #listaPresenca(montarTabela(dadosTratados))

        continuar = input("\nDeseja repetir o processo? (s/n): ").strip().lower()
        
        if continuar != "s":
            break


if __name__ == "__main__":
    main()
