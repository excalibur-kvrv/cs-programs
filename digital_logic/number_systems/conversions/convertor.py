from collections import deque

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
    count = 4
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
    decimal_part, *fractional_part = number.split(group_seperator)
    fractional_part = "".join(fractional_part)
    
    if from_number_system.name == "decimal":
      decimal_part = self.convert_decimal_part_to_new_base(int(decimal_part))
      
      if fractional_part:
        fractional_part = self.convert_fractional_part_to_new_base(float(f"0.{fractional_part}"), group_seperator)    
    else:
      pass
    
    return bytes(f"({decimal_part}{fractional_part}){self._get_unicode_for_base(to_number_system.base)}", "utf-8").decode("unicode-escape")
      

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
      
    decimal = DecimalConvertor()
    return decimal.convert(current_system, conversion_system, number)


print(Convertor().convert("decimal", "hexadecimal", "18.675"))