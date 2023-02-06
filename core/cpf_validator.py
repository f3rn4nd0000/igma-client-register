class CPF():
    """
        Essa classe é responsável pela validação do CPF de acordo com algoritmo 
        da url: https://www.macoratti.net/alg_cpf.htm#:~:text=O
    """    
    def __init__(self, number=0):
        self.number = None
        if type(number) == str:
            self.number = number
            self.first_cpf_part = self.parse_cpf()
        self.first_verifier_digit = '*'
        self.second_verifier_digit = '*'

    def parse_cpf(self) -> str:  
        """
            Gera uma string contendo apenas os digitos do CPF, 
            sem os caracteres '.' e '-' ou eventualmente quaisquer 
            outros que não sejam dígitos.
        """
        cpf_number:str = self.number
        parsed_number:list = []
        for char in cpf_number:
            if char.isdigit():
                parsed_number.append(char)
        parsed_number = ''.join(parsed_number)

        return parsed_number[:11]

    def get_first_nine_digits(self) -> str:
        """
            Retorna os primeiros 9 digitos do CPF 
            após ser devidamente filtrado para 
            retornar apenas números.
        """
        return self.parse_cpf()[:9]

    def sum_cpf_digits(self, cpf_number:str) -> int:
        """
            Retorna a soma de todos os dígitos do CPF.
        """

        """
            Caso não seja passado por parâmetro o CPF a ser validado é interpretado
            que o número a ser validado será os primeiros nove dígitos armazenados no campo
            self.number
        """

        if(cpf_number == 0):
            number_to_be_validated:str = self.get_first_nine_digits()
        number_to_be_validated = cpf_number
        """
            len(number_to_be_validated) deve ser igual a 9 caso não tenha o primeiro digito verificador validado
            e 10 caso já o tenha validado.
        """
        SUPERIOR_RANGE = len(number_to_be_validated)+1
        INFERIOR_RANGE = 1
        STEP = -1
        
        multiplier_array:list = [iterator for iterator in range(SUPERIOR_RANGE,INFERIOR_RANGE,STEP)]
        number_array = [int(number) for number in number_to_be_validated]
        sum_value = 0
        
        for iterator in range(len(number_to_be_validated)):
            sum_value += number_array[iterator]*multiplier_array[iterator]
        
        return sum_value

    def get_intermediate_verifier_digit_cpf(self) -> str:
        """
            Retorna o primeiro dígito verificador correspondente
            aos 9 primeiros dígitos do CPF
        """
        if self.first_verifier_digit == '*':
            first_cpf_part = self.get_first_nine_digits()
            sum_cpf_digits = self.sum_cpf_digits(first_cpf_part)
            self.first_verifier_digit = self.get_final_digit(sum_cpf_digits)

        print('O valor intermediário é: '+first_cpf_part + self.first_verifier_digit)    
        return first_cpf_part + self.first_verifier_digit

    def get_valid_cpf(self) -> str:
        """
            Realiza a validação do CPF retornando os dois dígitos verificadores
            correspondentes aos 9 primeiros dígitos
        """
        if self.first_verifier_digit == '*':
            first_cpf_part = self.get_first_nine_digits()
            sum_cpf_digits = self.sum_cpf_digits(first_cpf_part)
            self.first_verifier_digit = self.get_final_digit(sum_cpf_digits)

        if self.second_verifier_digit == '*' and self.first_verifier_digit != '*':
            first_cpf_part = self.get_first_nine_digits() + self.first_verifier_digit
            sum_cpf_digits = self.sum_cpf_digits(first_cpf_part)
            self.second_verifier_digit = self.get_final_digit(sum_cpf_digits)
        
        valid_cpf = self.get_first_nine_digits()+self.first_verifier_digit+self.second_verifier_digit
        print('O CPF válido é: '+valid_cpf)
        return valid_cpf

    def get_final_digit(self, sum_cpf_digits:int) -> str:
        """
            Retorna qual seria o verdadeiro dígito final do CPF,
            independente do tamanho do CPF, se será de 9 ou 10 dígitos.
        """
        final_digit = 0
        rest_division = sum_cpf_digits % 11

        if rest_division >= 2:
            final_digit = 11 - rest_division
        return str(final_digit)
