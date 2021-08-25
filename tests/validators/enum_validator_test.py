# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from enum import Enum
import pytest

from wtfjson.exceptions import RequiredValueError, InvalidTypeError, EnumInvalidValueError, InvalidValidatorOptionException
from wtfjson.validators import EnumValidator


class UnitTestStringEnum(Enum):
    """ Example enum class with string values for use in unit tests. """
    APPLE_RED = 'red apple'
    APPLE_GREEN = 'green apple'
    STRAWBERRY = 'strawberry'


class UnitTestIntegerEnum(Enum):
    """ Example enum class with integer values for use in unit tests. """
    RED = 1
    GREEN = 42
    BLUE = 13


class UnitTestMixedEnum(Enum):
    """ Example enum class with mixed string and integer values. """
    FOO = 'foo'
    BAR = 42


class EnumValidatorTest:
    # General tests

    @staticmethod
    @pytest.mark.parametrize('enum_class', [UnitTestStringEnum, UnitTestIntegerEnum, UnitTestMixedEnum])
    def test_enum_invalid_none(enum_class):
        """ Check that EnumValidator raises an exception for None as value. """
        validator = EnumValidator(enum_class)
        with pytest.raises(RequiredValueError) as exception_info:
            validator.validate(None)
        assert exception_info.value.to_dict() == {'code': 'required_value'}

    # Test EnumValidator with string based Enum

    @staticmethod
    def test_string_enum_valid():
        """ Test EnumValidator with string based Enum with valid enum values. """
        validator = EnumValidator(UnitTestStringEnum)
        assert validator.validate('red apple') is UnitTestStringEnum.APPLE_RED
        assert validator.validate('green apple') is UnitTestStringEnum.APPLE_GREEN
        assert validator.validate('strawberry') is UnitTestStringEnum.STRAWBERRY

    @staticmethod
    @pytest.mark.parametrize('input_data', ['', 'bananana', 'APPLE_RED'])
    def test_string_enum_invalid_value(input_data):
        """ Test EnumValidator with string based Enum with invalid enum values. """
        validator = EnumValidator(UnitTestStringEnum)
        with pytest.raises(EnumInvalidValueError) as exception_info:
            validator.validate(input_data)
        assert exception_info.value.to_dict() == {'code': 'enum_invalid_value'}

    @staticmethod
    @pytest.mark.parametrize('input_data', [1, 1.234, True, ['red apple']])
    def test_string_enum_invalid_type(input_data):
        """ Check that EnumValidator with string based Enum raises an exception for values with wrong type. """
        validator = EnumValidator(UnitTestStringEnum)
        with pytest.raises(InvalidTypeError) as exception_info:
            validator.validate(input_data)
        assert exception_info.value.to_dict() == {
            'code': 'invalid_type',
            'expected_type': 'str',
        }

    # Test EnumValidator with integer based Enum

    @staticmethod
    def test_integer_enum_valid():
        """ Test EnumValidator with integer based Enum with valid enum values. """
        validator = EnumValidator(UnitTestIntegerEnum)
        assert validator.validate(1) is UnitTestIntegerEnum.RED
        assert validator.validate(42) is UnitTestIntegerEnum.GREEN
        assert validator.validate(13) is UnitTestIntegerEnum.BLUE

    @staticmethod
    @pytest.mark.parametrize('input_data', [0, 2, -42])
    def test_integer_enum_invalid_value(input_data):
        """ Test EnumValidator with integer based Enum with invalid enum values. """
        validator = EnumValidator(UnitTestIntegerEnum)
        with pytest.raises(EnumInvalidValueError) as exception_info:
            validator.validate(input_data)
        assert exception_info.value.to_dict() == {'code': 'enum_invalid_value'}

    @staticmethod
    @pytest.mark.parametrize('input_data', ['red apple', 'RED', 1.234, True, [1]])
    def test_integer_enum_invalid_type(input_data):
        """ Check that EnumValidator with integer based Enum raises an exception for values with wrong type. """
        validator = EnumValidator(UnitTestIntegerEnum)
        with pytest.raises(InvalidTypeError) as exception_info:
            validator.validate(input_data)
        assert exception_info.value.to_dict() == {
            'code': 'invalid_type',
            'expected_type': 'int',
        }

    # Test EnumValidator with Enum with mixed type values

    @staticmethod
    def test_mixed_enum_valid():
        """ Test EnumValidator with mixed value Enum with valid enum values. """
        validator = EnumValidator(UnitTestMixedEnum)
        assert validator.validate('foo') is UnitTestMixedEnum.FOO
        assert validator.validate(42) is UnitTestMixedEnum.BAR

    @staticmethod
    @pytest.mark.parametrize('input_data', [0, 1, 2, '', 'red apple', 'FOO'])
    def test_mixed_enum_invalid_value(input_data):
        """ Test EnumValidator with mixed value Enum with invalid enum values. """
        validator = EnumValidator(UnitTestMixedEnum)
        with pytest.raises(EnumInvalidValueError) as exception_info:
            validator.validate(input_data)
        assert exception_info.value.to_dict() == {'code': 'enum_invalid_value'}

    @staticmethod
    @pytest.mark.parametrize('input_data', [1.234, True, [1], ['foo']])
    def test_mixed_enum_invalid_type(input_data):
        """ Check that EnumValidator with mixed value Enum raises an exception for values with wrong type. """
        validator = EnumValidator(UnitTestMixedEnum)
        with pytest.raises(InvalidTypeError) as exception_info:
            validator.validate(input_data)
        assert exception_info.value.to_dict() == {
            'code': 'invalid_type',
            'expected_types': ['str', 'int'],
        }

    # Test EnumValidator with explicit allowed_types parameter

    @staticmethod
    @pytest.mark.parametrize(
        'allowed_types, expected_type_str, valid_input, expected_output, invalid_input', [
            # Single allowed type
            (str, 'str', 'foo', UnitTestMixedEnum.FOO, 42),
            (int, 'int', 42, UnitTestMixedEnum.BAR, 'foo'),
            # Single allowed type in list
            ([str], 'str', 'foo', UnitTestMixedEnum.FOO, 42),
            ([int], 'int', 42, UnitTestMixedEnum.BAR, 'foo'),
        ]
    )
    def test_with_specified_allowed_type(allowed_types, expected_type_str, valid_input, expected_output, invalid_input):
        """ Test EnumValidator with mixed value Enum but restricted allowed types via parameter. """
        validator = EnumValidator(UnitTestMixedEnum, allowed_types=allowed_types)

        # Check that allowed type is accepted
        assert validator.validate(valid_input) is expected_output

        # Check that NOT allowed type raises a ValidationError
        with pytest.raises(InvalidTypeError) as exception_info:
            validator.validate(invalid_input)
        assert exception_info.value.to_dict() == {
            'code': 'invalid_type',
            'expected_type': expected_type_str,
        }

    # Invalid validator parameters

    @staticmethod
    def test_enum_cls_invalid():
        """ Check that EnumValidator raises exception when enum_cls is not an Enum. """
        with pytest.raises(InvalidValidatorOptionException) as exception_info:
            EnumValidator('banana')  # noqa
        assert str(exception_info.value) == 'Parameter "enum_cls" must be an Enum class.'

    @staticmethod
    def test_empty_allowed_types():
        """ Check that EnumValidator raises exception when allowed_types is empty. """
        with pytest.raises(InvalidValidatorOptionException) as exception_info:
            EnumValidator(UnitTestMixedEnum, allowed_types=[])
        assert str(exception_info.value) == 'Parameter "allowed_types" is an empty list (or types could not be autodetermined)!'

    @staticmethod
    def test_unsupported_allowed_types_explicit():
        """ Check that EnumValidator raises exception when allowed_types contains unsupported types. """
        with pytest.raises(InvalidValidatorOptionException) as exception_info:
            EnumValidator(UnitTestMixedEnum, allowed_types=[str, float])
        assert str(exception_info.value) == 'Parameter "allowed_types" contains unsupported type "float".'

    @staticmethod
    def test_unsupported_allowed_types_in_enum():
        """ Check that EnumValidator raises exception when allowed_types is autodetermined and the enum contains unsupported types. """

        class UnitTestUnsupportedTypeEnum(Enum):
            FOO = 123
            BAR = 1.234

        with pytest.raises(InvalidValidatorOptionException) as exception_info:
            EnumValidator(UnitTestUnsupportedTypeEnum)
        assert str(exception_info.value) == 'Parameter "allowed_types" contains unsupported type "float".'
