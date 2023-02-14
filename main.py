#Começamos importando as bibliotecas que iremos usar, use pip install requests para conseguir realizar a requisição
#É mportante também criar um ambiente virtual para instalar os pacotes e testar seu código, use o comando: "python -m venv env" em seu terminal
import json
import requests

# Vamos consideirar que a função main será a porta de entrada para executar o código
def main():
    # Criamos uma variável que irá receber a Url com os dados JSON
    url = 'https://storage.googleapis.com/raccoon-humane/psel.json'

    # Criaremos blocos para realizar a requisição e executar as funções  
    try:
        # Essas 3 linhas seguintes foram utilizadas no exemplo do case
        request = requests.get(url=url)
        code = request.status_code
        data = json.loads(request.text)

        # Chamaremos a função valida_cpf para fazer a verificação dos cpfs e adicionar os valores booleanos no dicionario
        valida_cpf(data)
        # Chamaremos a função update_employee para adicionar os valores do "Adicional de insalubrilidade" ao dicionario
        update_employee(data)
        # Por fim, imprimiremos os dados com os dois campos acima adicionados ao dicionário
        print(data)
    except: 
        # Caso a requisição falhe, retornará uma mensagem de erro
        return_code = 400
        if code > return_code:
            return {"message": 'error' , "code": code}

# Definimos a função que fará a verificação dos Cpfs
def valida_cpf(data):
    # recebendo "data" como parâmetro, iremos percorrer cada uma das linhas desse dicionário, cada linha corresponde a um dado de funcionário
    for i in data:
        # Formataremos o cpf para que não apareçam caracteres além de números (ou string)
        cpf = i['cpf'].replace("-", "")
        format_cpf = cpf.replace(".", "")

        # 1º digito verificador
        first_digit = int(format_cpf[-2])
        # 2º digito verificador
        second_digit = int(format_cpf[-1])

        # Primeiro intervalo de verificação, os 8 primeiros digitos
        verify_first = format_cpf[0 : 9]
        # Essa lista acompanhará a lista, acima para multiplicar os valores
        list_one = [10, 9, 8, 7, 6, 5, 4, 3, 2]

        # Segundo intervalo de verificação, os 8 primeiros digitos
        verify_second = format_cpf[0 : 10]
        # Essa lista também acompanhará a lista, acima para multiplicar os valores
        list_two = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # Utilizando a formula de multiplicação com base no link: "https://www.somatematica.com.br/faq/cpf.php" será feita a multiplicação e depois será atribuida a variável o resto da divisão por 11
        # Acredito que esse não seja o melhor jeito de fazer essa verificação, talvez criar um looping substituindo as listas seja mais organizado 
        rest_first = (((int(verify_first[0]) * list_one[0]) + (int(verify_first[1]) * list_one[1]) + (int(verify_first[2]) * list_one[2]) + (int(verify_first[3]) * list_one[3]) + (int(verify_first[4]) * list_one[4]) + (int(verify_first[5]) * list_one[5]) + (int(verify_first[6]) * list_one[6]) + (int(verify_first[7]) * list_one[7]) + (int(verify_first[8]) * list_one[8])) % 11)
        rest_second = (((int(verify_second[0]) * list_two[0]) + (int(verify_second[1]) * list_two[1]) + (int(verify_second[2]) * list_two[2]) + (int(verify_second[3]) * list_two[3]) + (int(verify_second[4]) * list_two[4]) + (int(verify_second[5]) * list_two[5]) + (int(verify_second[6]) * list_two[6]) + (int(verify_second[7]) * list_two[7]) + (int(verify_second[8]) * list_two[8]) + (int(verify_second[9]) * list_two[9])) % 11)

        # Faremos a subtraçaõ por 11 para verificar se bate com os dois ultimos digitos
        verify_division_first = 11 - rest_first
        verify_division_second = 11 - rest_second

        # Caso o resto da divisão seja 0 ou 1 e o primeiro digito de verificação seja 0, significa que o cpf é valido!
        if rest_first == 0 or rest_first == 1:
            if first_digit == 0:
                i['cpf_valido'] = True
        # Caso o primeiro digito seja igual a subtração de 11 pelo resto da divisão e o segundo também, significa que o cpf é valido!
        elif first_digit == verify_division_first and second_digit == verify_division_second:
            i['cpf_valido'] = True
        # Caso contrario, significa que o cpf não é valido!
        else:
            i['cpf_valido'] = False

# Definimos a função que irá atualizar o valor de "adicional de insalubridade" ao dicionário
def update_employee(data):
    for i in data:
        # essa função basicamente verifica o campo 'cargo' e faz as alterações de acordo com a tabela passada no case, arrendondando os valores para 2 casas decimais
        cargo = i['cargo']
        if cargo == 'Assassin':
            i['adicional_de_insalubridade'] = round(i['salario'] * 0.05, 2)
          
        elif cargo == 'Batman':
            i['adicional_de_insalubridade'] = round(i['salario'] * 0.1, 2)
    
        elif cargo == 'Butler':
            i['adicional_de_insalubridade'] = "Não há adicional de insalubridade"

        elif cargo == 'Side Kick':
            i['adicional_de_insalubridade'] = round(i['salario'] * 0.15, 2)
    
        elif cargo == 'The Chief Demon':
            i['adicional_de_insalubridade'] = round(i['salario'] * 0.125, 2)

# Por último, chamamos a função main para executar todo o código, caso esse código fosse rodar em uma cloud function, poderiamos criar uma handle_request para usar como gatilho HTTP no GCP
main()
