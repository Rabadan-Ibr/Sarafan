def generate_seq(n):
    number = 1
    cur_count = 0
    result = []
    while True:
        for _ in range(number):
            if cur_count == n:
                return result
            result.append(number)
            cur_count += 1
        number += 1


if __name__ == '__main__':
    assert generate_seq(15) == [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5], 'Error for 15'
    assert generate_seq(10) == [1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 'Error for 10'
    assert generate_seq(5) == [1, 2, 2, 3, 3], 'Error for 5'
    print('OK')
