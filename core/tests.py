from django.test import TestCase
import pytest
from cpf_validator import CPF
# Create your tests here.

def test_instantiate_class():
    cpf = CPF()

def test_return_parsed_cpf():
    new_cpf = CPF()

    new_cpf.number = '828.048.730-13'
    assert isinstance(new_cpf.parse_cpf(), str) == True
    assert new_cpf.parse_cpf() == '82804873013'

    new_cpf.number = '257.495.570-65'
    assert isinstance(new_cpf.parse_cpf(), str) == True
    assert new_cpf.parse_cpf() == '25749557065'

    new_cpf.number = '852.845.420/70'
    assert isinstance(new_cpf.parse_cpf(), str) == True
    assert new_cpf.parse_cpf() == '85284542070'

    new_cpf.number = '248.023/410*08'
    assert isinstance(new_cpf.parse_cpf(), str) == True
    assert new_cpf.parse_cpf() == '24802341008'

    new_cpf.number = '248*023/410108'
    assert isinstance(new_cpf.parse_cpf(), str) == True
    assert new_cpf.parse_cpf() == '24802341010'

def test_validate_cpf():
    new_cpf = CPF()

    new_cpf.number = '11144477705'
    intermediate_valid_number = '1114447773'
    cpf_valid_number = '11144477735'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

    # new_cpf.number = '791.957.960-02'
    new_cpf = CPF()
    new_cpf.number = '79195796013'
    intermediate_valid_number = '7919579600'
    cpf_valid_number = '79195796002'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number
    
    # new_cpf.number = '552.457.280-60'
    new_cpf = CPF()
    new_cpf.number = '55245728091'
    intermediate_valid_number = '5524572806'
    cpf_valid_number = '55245728060'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

    # new_cpf.number = '811.182.630-30'
    new_cpf = CPF()
    new_cpf.number = '81118263045'
    intermediate_valid_number = '8111826303'
    cpf_valid_number = '81118263030'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

    # new_cpf.number = '944.718.790-06'
    new_cpf = CPF()
    new_cpf.number = '94471879021'
    intermediate_valid_number = '9447187900'
    cpf_valid_number = '94471879006'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

    # new_cpf.number = '878.626.420-66'
    new_cpf = CPF()
    new_cpf.number = '87862642032'
    intermediate_valid_number = '8786264206'
    cpf_valid_number = '87862642066'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number


    # new_cpf.number = '876.046.050-44'
    new_cpf = CPF()
    new_cpf.number = '87604605023'
    intermediate_valid_number = '8760460504'
    cpf_valid_number = '87604605044'
    assert new_cpf.get_intermediate_verifier_digit_cpf() == intermediate_valid_number
    assert new_cpf.get_valid_cpf() == cpf_valid_number

if __name__ == "__main__":
    pytest.main(["-x", __file__])


