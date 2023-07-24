# import bcrypt
# password = "super secret password".encode('ASCII')
# print(password)
# # Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# print(hashed)
# # Check that an unhashed password matches one that has previously been
# # hashed
# if bcrypt.checkpw(password, hashed):
#     print("It Matches!")
# else:
#     print("It Does not Match :(")
# list_of_numbers = [1,8,5,2,7,7,9,10]
# print("asdf")
# list_of_prime_number = []
# for i in list_of_numbers:
#     print("This is i: ",i)
#     if i == 1:
#         list_of_prime_number.append(i)
#         continue
#     for j in range(2,i):
#         if i%j==0:
#             print("Not prime number",i)
#
#     else:
#         print("its a prime number: ",i)
#
# # print("LIst of prime number: ",list_of_numbers)
#
# dic ={}
# for i in list_of_numbers:
#     if
#
list_of_numbers = [1,8,5,2,7,7,9,10]
# def isprime(number):
#     if number == 1 or number ==2:
#         return True
#     for i in range(2,number):
#         if number%i==0:
#             return False
# for i in range(len(list_of_numbers)):
#     if isprime(list_of_numbers[i]) == False:
#         print("Not a prime number", list_of_numbers[i])
#     else:
#         print("is a prime number", list_of_numbers[i])
def reverse( x: int) -> int:
    string_integer_input = str(x)
    # print(string_integer_input)
    numbers_of_string =str(string_integer_input)
    numbers_of_string1=""

    for i in range(len(numbers_of_string) - 1, -1, -1):

        numbers_of_string1 += numbers_of_string[i]
    string_number = str(numbers_of_string1)
    zeros_in_start = ""
    negative_sign = ""
    normal_str = ""
    if string_number[0] == '0' or string_number[-1] == '-':
        zeros_in_start = string_number[0]
        negative_sign = string_number[-1]
        normal_str = numbers_of_string1.replace("0", "")
        normal_str = numbers_of_string1.replace("-", "")
        if negative_sign == '-':
            result = int(negative_sign + normal_str)
        else:
            result = int(normal_str)

    return result
# def check_for_negative_and_positive(number):
#     string_number = str(number)
#     zeros_in_start = ""
#     negative_sign = ""
#     normal_str = ""
#     if string_number[0] == '0' or  string_number[-1] == '-':
#         zeros_in_start = string_number[0]
#         negative_sign =  string_number[-1]
#         normal_str = number.replace("0","")
#         normal_str = number.replace("-","")
#         if negative_sign =='-':
#             result = int(negative_sign + normal_str)
#         else:
#             result = int(normal_str)
#         return  result

x =-210
print(reverse(x))

