import argparse
from digital_logic.number_systems.conversions.convertor import Convertor


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(help="convert between number systems")
  converter = subparser.add_parser("converter")
  converter.add_argument("current")
  converter.add_argument("new_sys")
  converter.add_argument("number")
  
  args = parser.parse_args()
  
  print(Convertor().convert(args.current, args.new_sys, args.number))