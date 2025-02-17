# try:
#  num1=10
#  num2=0
#  c=num1/num2
# except ZeroDivisionError:
#  print("cant be divided")

try:
    a=int(input('enter your age:'))
    if a<=0:
        raise ValueError('your age is not valid')
except ValueError:
    print('not valid')

print('valid age ')

