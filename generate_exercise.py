import cv2
import numpy as np
import random
from datetime import datetime
random.seed(datetime.now())
import argparse

color = (50, 50, 50)   


def generate_one_page(page_name, first_max, operators, second_max):
  numbers = 36  # number of equations to generate.
  numbers = numbers // 2 * 2  # Make it even so each line can contain two equations.
  first_op_range = (0, first_max)  # first operands range in [0, 10]
  second_op_range = (0, second_max)  # second operands range in [0, 100]

  height = 1280
  width = 960
  line_per_page = 20
  line_height = height // line_per_page
  im = np.ones((height, width, 3), np.uint8) * 255
  font = cv2.FONT_HERSHEY_SIMPLEX 
  fontScale = 1
  thickness = 2

  dx = 50
  dy = 100
  for i in range(numbers):
    a = random.randint(*first_op_range)
    b = random.randint(*second_op_range)
    sign = random.choice(operators)
    if sign == '-' or sign == '/' :
      if a < b:
        a, b = b, a
    if sign == '/':
      if b == 0:
        b = 1
      a = (a // b) * b
    if i % 2 == 0:
      x = dx
    else:
      x = dx + width // 2
    y = dy + (i//2) * line_height
    ops = '{:<5d}{}{:5d}  =     '.format(a, sign, b) 
    im = cv2.putText(im, ops,(x,y), font, fontScale, color, thickness, cv2.LINE_AA)
    print(ops)
  cv2.imwrite(page_name + '.png', im)


def calc(a, op, b):
  if op == '+':
    return a + b
  elif op == '-':
    return a - b
  elif op == '/':
    return a / b;
  else:
    return a * b;


def generate_one_page_3ops(page_name, first_max, operators, second_max, third_max):
  numbers = 36  # number of equations to generate.
  numbers = numbers // 2 * 2  # Make it even so each line can contain two equations.
  first_op_range = (0, first_max)
  second_op_range = (0, second_max)
  third_op_range = (0, third_max)

  height = 1280
  width = 960
  line_per_page = 20
  line_height = height // line_per_page
  im = np.ones((height, width, 3), np.uint8) * 255
  font = cv2.FONT_HERSHEY_SIMPLEX 
  fontScale = 1   
  thickness = 2

  dx = 50
  dy = 50
  i = 1
  while i <= numbers:
    i = i + 1
    a = random.randint(*first_op_range)
    b = random.randint(*second_op_range)
    c = random.randint(*third_op_range)
    sign1 = random.choice(operators)
    sign2 = random.choice(operators)

    if calc( calc(a, sign1, b), sign2, c ) < 0:
      i = i - 1
      continue
    if i % 2 == 0:
      x = dx
    else:
      x = dx + width // 2
    y = dy + (i//2) * line_height
    ops = '{:<3d}{}{:3d}  {}{:3d}  =     '.format(a, sign1, b, sign2, c) 
    im = cv2.putText(im, ops,(x,y), font, fontScale, color, thickness, cv2.LINE_AA)
    print(ops)
  cv2.imwrite(page_name + '.png', im)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--pages', type=int, default=1)
  parser.add_argument('--first_max', type=int, default=20)
  parser.add_argument('--operators', type=str, default='+-')
  parser.add_argument('--second_max', type=int, default=20)
  parser.add_argument('--third_max', type=int, default=-1)
  args = parser.parse_args()
  for page in range(args.pages):
    if args.third_max < 0:
      generate_one_page('numbers{:02d}'.format(page), args.first_max, args.operators, args.second_max)
    else:
      generate_one_page_3ops('numbers{:02d}'.format(page), args.first_max, args.operators, args.second_max, args.third_max)


if __name__ == '__main__':
  main()