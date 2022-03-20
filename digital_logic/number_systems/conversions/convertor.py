from collections import deque
from curses.ascii import isalpha
import re

FORMAT_PATTERN = re.compile(r'\((.*?)\).*')

class NumberSystem:
  base: int = 0
  name: str = ""
  values: dict = {}


class Binary(NumberSystem):
  base: int = 2
  name: str = "binary"
  values: dict = { i:i for i in range(2) }


class Octal(NumberSystem):
  base: int = 8
  name: str = "octal"
  values: dict = { i:i for i in range(8) }
  

class Decimal(NumberSystem):
  base: int = 10
  name: str = "decimal"
  values: dict = { i:i for i in range(10) }


class Hexadecimal(NumberSystem):
  base: int = 16
  name: str = "hexadecimal"
  values: dict = { 
    "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15,
    10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 
    **{i:i for i in range(10)} 
  }
  

class DecimalConvertor:
  def _get_unicode_for_base(self, base) -> str:
    unicode = deque()
    
    while base:
      unicode.appendleft(f"\\u{2080 + (base % 10)}")
      base //=10
    
    return "".join(unicode)
  
  def convert_to_decimal_system(self, number: str, group_seperator: str, 
                                decimal_part_length: int) -> str:
    base = self.from_number_system.base
    values = self.from_number_system.values
    converted_number = 0
    index = decimal_part_length
    
    for token in number:
      if token != group_seperator:
        index -= 1
        if isalpha(token):
          token = int(values[token])
        converted_number += (int(token) * (base ** index))
    
    return str(converted_number)
    
  def convert_decimal_part_to_new_base(self, number: int) -> str:
    if number == 0:
      return "0"
    
    converted_number = deque()
    base = self.to_number_system.base
    values = self.to_number_system.values
    
    while number > 0:
      converted_number.appendleft(str(values[number % base]))
      number //= base
    
    return "".join(converted_number)
  
  def convert_fractional_part_to_new_base(self, number: float, group_seperator: str) -> str:
    converted_number = []
    
    base = self.to_number_system.base
    values = self.to_number_system.values
    count = 10
    while number != 0 and count:
      count -= 1
      temp = number * base
      integer_portion = int(temp)
      number = temp - integer_portion
      converted_number.append(str(values[integer_portion]))
    
    if converted_number:
      return f"{group_seperator}{''.join(converted_number)}"
    return ""
  
  def convert(self, from_number_system: NumberSystem, to_number_system: NumberSystem, number: str) -> str:
    group_seperator = "."
    self.to_number_system = to_number_system
    self.from_number_system = from_number_system
    decimal_part, *fractional_part = number.split(group_seperator)
    fractional_part = "".join(fractional_part)
    
    if from_number_system.name == "decimal":
      decimal_part = self.convert_decimal_part_to_new_base(int(decimal_part))
      
      if fractional_part:
        fractional_part = self.convert_fractional_part_to_new_base(float(f"0.{fractional_part}"), group_seperator)
      converted_number = f"{decimal_part}{fractional_part}"     
    else:
      converted_number = self.convert_to_decimal_system(number, group_seperator, len(decimal_part))
    
    return bytes(f"({converted_number}){self._get_unicode_for_base(to_number_system.base)}", "utf-8").decode("unicode-escape")
      

class Convertor:
  supported_number_systems = {
    "binary": Binary(),
    "octal": Octal(),
    "decimal": Decimal(),
    "hexadecimal": Hexadecimal()
  }
  
  def get_number_system(self, system):
    if system not in self.supported_number_systems:
      raise ValueError(f"{system} is not supported")
    
    return self.supported_number_systems[system]
  
  def convert(self, from_number_system: str, to_number_system: str, number: str) -> str:
    current_system = self.get_number_system(from_number_system)
    conversion_system = self.get_number_system(to_number_system)
    
    convertor = DecimalConvertor()
    if from_number_system != "decimal" and to_number_system != "decimal":
      decimal_system = self.get_number_system("decimal")  
      number = FORMAT_PATTERN.findall(convertor.convert(current_system, decimal_system, number))[0]
      current_system = decimal_system
    return convertor.convert(current_system, conversion_system, number)