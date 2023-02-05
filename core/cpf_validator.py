import pytest

class CPF():
    
    def __init__(self, number=0):
        self.number = None
        if type(number) == str:
            self.number = number
            self.first_cpf_part = self.parse_cpf(self.number)
        self.first_verifier_digit = '*'
        self.second_verifier_digit = '*'
        # self.first_validated_number:bool = False
        # self.length_of_multiplier_array:int = 10

    def parse_cpf(self) -> str:  
        """
            Gera uma string contendo apenas os digitos do CPF, 
            sem os caracteres '.' e '-' ou eventualmente quaisquer 
            outros que não sejam dígitos.
        """
        cpf_number:str = self.number
        # print("cpf_number")
        # print(cpf_number)
        parsed_number:list = []
        for char in cpf_number:
            if char.isdigit():
                parsed_number.append(char)
        parsed_number = ''.join(parsed_number)

        return parsed_number[:11]

    def is_final_digit_valid(self) -> bool:
        return True if self.parse_cpf()[-1] == self.get_final_digit() else False

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
        if(cpf_number == 0):
            number_to_be_validated:str = self.get_first_nine_digits()
        
        # if(int(self.first_verifier_digit) != 0):
        #     number_to_be_validated = self.get_first_nine_digits()+str(self.first_verifier_digit)
        
        number_to_be_validated = cpf_number

        print('number_to_be_validated')
        print(number_to_be_validated)

        SUPERIOR_RANGE = len(number_to_be_validated)+1
        INFERIOR_RANGE = 1
        STEP = -1
        """
            len(number_to_be_validated) deve ser igual a 9 caso não tenha o primeiro digito verificador validado
            e 10 caso já o tenha validado.
        """
        
        multiplier_array:list = [iterator for iterator in range(SUPERIOR_RANGE,INFERIOR_RANGE,STEP)]
        number_array = [int(number) for number in number_to_be_validated]
        sum_value = 0
        
        # print(20*'-')
        # print(multiplier_array)
        # print(number_array)
        # print(20*'-')

        # print(10*'-')
        # print(SUPERIOR_RANGE)
        # print(INFERIOR_RANGE)
        # print(STEP)
        # print(10*'-')

        # print(range(len(number_to_be_validated)))
        # print(number_to_be_validated)

        # print("int(self.first_verifier_digit)")
        # print(int(self.first_verifier_digit))

        for iterator in range(len(number_to_be_validated)):
            sum_value += number_array[iterator]*multiplier_array[iterator]
        # if(self.first_verifier_digit ==)
        # sum_value += int(self.first_verifier_digit)*2
        
        print("sum_value")
        print(sum_value)
        return sum_value

    def get_intermediate_verifier_digit_cpf(self) -> str:
        if self.first_verifier_digit == '*':
            first_cpf_part = self.get_first_nine_digits()
            sum_cpf_digits = self.sum_cpf_digits(first_cpf_part)
            self.first_verifier_digit = self.get_final_digit(sum_cpf_digits)

        print('the intermediate part is '+first_cpf_part + self.first_verifier_digit)    
        return first_cpf_part + self.first_verifier_digit

    def get_valid_cpf(self) -> str:
        if self.first_verifier_digit == '*':
            first_cpf_part = self.get_first_nine_digits()
            sum_cpf_digits = self.sum_cpf_digits(first_cpf_part)
            self.first_verifier_digit = self.get_final_digit(sum_cpf_digits)
        if self.second_verifier_digit == '*' and self.first_verifier_digit != '*':
            first_cpf_part = self.get_first_nine_digits() + self.first_verifier_digit
            sum_cpf_digits = self.sum_cpf_digits(first_cpf_part)
            self.second_verifier_digit = self.get_final_digit(sum_cpf_digits)
        
        valid_cpf = self.get_first_nine_digits()+self.first_verifier_digit+self.second_verifier_digit
        print('the valid cpf is '+valid_cpf)
        return valid_cpf

    def get_final_digit(self, sum_cpf_digits:int) -> str:
        """
            Retorna qual seria o verdadeiro dígito final do CPF,
            trabalha em cima do tamanho do CPF, se será de 9 ou 10 dígitos.
        """
        final_digit = 0
        # rest_division = self.sum_cpf_digits() % 11
        rest_division = sum_cpf_digits % 11

        if rest_division >= 2:
            final_digit = 11 - rest_division
        print("str(final_digit)")
        print(str(final_digit))
        return str(final_digit)

def test_instantiate_class():
    cpf = CPF()

# def test_return_parsed_cpf():
    # new_cpf = CPF()

    # new_cpf.number = '828.048.730-13'
    # assert isinstance(new_cpf.parse_cpf(), str) == True
    # assert new_cpf.parse_cpf() == '82804873013'

    # new_cpf.number = '257.495.570-65'
    # assert isinstance(new_cpf.parse_cpf(), str) == True
    # assert new_cpf.parse_cpf() == '25749557065'

    # new_cpf.number = '852.845.420/70'
    # assert isinstance(new_cpf.parse_cpf(), str) == True
    # assert new_cpf.parse_cpf() == '85284542070'

    # new_cpf.number = '248.023/410*08'
    # assert isinstance(new_cpf.parse_cpf(), str) == True
    # assert new_cpf.parse_cpf() == '24802341008'

    # new_cpf.number = '248*023/410108'
    # assert isinstance(new_cpf.parse_cpf(), str) == True
    # assert new_cpf.parse_cpf() == '24802341010'

def test_validate_cpf():
    new_cpf = CPF()

    new_cpf.number = '11144477705'
    intermediate_valid_number = '1114447773'
    cpf_valid_number = '11144477735'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

    # NOVOS TESTES
    new_cpf = CPF()
    # new_cpf.number = '791.957.960-02'
    new_cpf.number = '79195796013'
    intermediate_valid_number = '7919579600'
    cpf_valid_number = '79195796002'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number
    new_cpf = CPF()
    # new_cpf.number = '552.457.280-60'
    new_cpf.number = '55245728091'
    intermediate_valid_number = '5524572806'
    cpf_valid_number = '55245728060'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

    # new_cpf.number = '811.182.630-30'
    new_cpf.number = '81118263045'
    intermediate_valid_number = '8111826303'
    cpf_valid_number = '81118263030'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

    # new_cpf.number = '944.718.790-06'

    # new_cpf.number = '878.626.420-66'

    # new_cpf.number = '876.046.050-44'



if __name__ == "__main__":
    pytest.main(["-x", __file__])
    # cpf = CPF('11144477705')
    # cpf.get_valid_cpf()
    # cpf = CPF('111.444.777-05')
    # # teste = cpf.number
    # cpf.validate_cpf_number()
    

    # validate_1st_digit = cpf.validate_first_cpf_digit(cpf.number)
    # validate_2nd_digit = cpf.validate_second_cpf_digit(validate_1st_digit)


# def get_cpf_correct_size(self) -> str:
    #     correct_size_cpf = self.get_cpf_digits()
    #     """
    #         Se por um acaso o usuário digitar um número excessivo
    #         de caracteres, então o tamanho da string do CPF
    #         será limitado a 11 caracteres.
    #     """
    #     return correct_size_cpf if len(correct_size_cpf) == 11 else correct_size_cpf[:11]

    # def parse_cpf(self) -> str:
    #     """
    #         Aplica operações de retornar apenas os dígitos do CPF
    #         e no tamanho correto.
    #     """
    #     parsed_cpf = self.get_cpf_digits()
    #     parsed_cpf = self.get_cpf_correct_size()

    #     return parsed_cpf


# def validate_cpf(self, number_to_be_validated):

    #     print("len(number_to_be_validated)")
    #     print(len(number_to_be_validated))
    #     print(type(len(number_to_be_validated)))
    #     multiplier_array:list = [iterator for iterator in range(len(number_to_be_validated)+1,1,-1)]

    #     print(multiplier_array)
    #     number_array = [int(number) for number in number_to_be_validated]
    #     print(number_array)
    #     sum_value = 0
    #     for iterator in range(len(number_to_be_validated)):
    #         sum_value += number_array[iterator]*multiplier_array[iterator]
        
    #     print(sum_value)

    #     final_digit = 0
    #     rest_division = sum_value % 11

    #     if rest_division >= 2:
    #         final_digit = 11 - rest_division

    #     self.first_validated_number = True
    #     return number_to_be_validated+str(final_digit)


# def create_multiplier_array(self) -> list:
    #     """
    #         Cria uma array com números de ordem decrescente
    #         para serem multiplicados pelos dígitos do CPF.
    #     """
    #     if self.first_validated_number == True:
    #         self.length_of_multiplier_array += 1
        
    #     multiplier_array = []
    #     print("len(self.parse_cpf())")
    #     print(len(self.parse_cpf()))
    #     multiplier_array = [iterator for iterator in range(self.length_of_multiplier_array,1,-1)]

    #     return multiplier_array

# def check_if_last_digit_is_valid(self, number_to_be_checked):
    #     last_number = number_to_be_checked[-1]
    #     if (last_number) == self.get_final_digit():



##########################################################################
# FAZ PARTE DE OUTRA FUNCAO
        # else:

        #     if int(self.first_verifier_digit) == 0:
        #         self.first_verifier_digit = final_digit
        #     elif int(self.first_verifier_digit) != 0 and int(self.second_verifier_digit) == 0:
        #         self.second_verifier_digit = final_digit
