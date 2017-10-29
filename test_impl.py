def test_cmd(input):
    if 'second_str' in input:
        second = input['second_str']
    else:
        second = "not found!!"

    print(input['input_str'] + " but second is " + second)