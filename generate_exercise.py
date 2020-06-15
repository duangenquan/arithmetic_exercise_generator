import cv2
import numpy as np
import random
from datetime import datetime
random.seed(datetime.now())
import argparse


def generate_one_page(page_name, first_max, operators, second_max):
  numbers = 36  # number of equations to generate.
  first_op_range = (0, first_max)  # first operands range in [0, 10]
  second_op_range = (0, second_max)  # second operands range in [0, 100]
  numbers = numbers // 2 * 2  # Make it even so each line can contain two equations.
  rand_num = numbers * 2

  height = 1280
  width = 960
  line_per_page = 20
  line_height = height // line_per_page
  im = np.ones((height, width, 3), np.uint8) * 255
  font = cv2.FONT_HERSHEY_SIMPLEX 
  fontScale = 1
  color = (0, 0, 0)   
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


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--pages', type=int, default=1)
  parser.add_argument('--first_max', type=int, default=20)
  parser.add_argument('--operators', type=str, default='+-')
  parser.add_argument('--second_max', type=int, default=20)
  args = parser.parse_args()
  for page in range(args.pages):
    generate_one_page('numbers{:02d}'.format(page), args.first_max, args.operators, args.second_max)


if __name__ == '__main__':
  main()