def del_pos_from_file(filename, pos):
    with open(filename, 'r+') as file:
        lines = converter(filename)
        print(lines)
        filtered_lines = list()
        filtered_lines = [i for i in lines if i not in filtered_lines and i != pos]
        file.seek(0)
        file.truncate()
        for line in filtered_lines:
            print(line)
            file.writelines(str(line)+'\n')

def converter(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        tup_list = list()
        for tup in lines:
            tup_list.append(tuple(list(map(int, tup.strip('\n').replace('(', '').replace(')', '').replace(',', '').split()))))
        return tup_list

del_pos_from_file('test.txt', (69, 69, 69))