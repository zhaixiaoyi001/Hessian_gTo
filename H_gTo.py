import numpy as np

# path = "D:/Seafile/H_gTo/"
filename = input("请输入fchk文件名:")
N = 0


def ReadHess():
    list = []
    flag = 0
    k = 0
    # fb = open(path + filename, 'r', encoding='utf8')
    fb = open(filename, 'r', encoding='utf8')
    for line in fb:
        if line.find('Number of atoms') >= 0:
            line_save = line.split(' ')
            N = int(line_save[-1].rstrip('\n'))
            break
    Hess = np.zeros([3 * N, 3 * N])
    for line in fb:
        if line.find('Cartesian Force Constants') >= 0:
            flag = 1
            continue
        if line.find('Nonadiabatic coupling') >= 0:
            flag = 0
        if flag == 1:
            line_save = line.split(' ')
            line_save = [string.replace('\n', '') for string in line_save]
            list = list + line_save
    while '' in list:
        list.remove('')
    for i in range(0, 3 * N):
        for j in range(0, i + 1):
            Hess[i][j] = list[k]
            k = k + 1
    Hess = np.where(Hess, Hess, Hess.T)
    fb.close()
    return Hess


def PrintHess():
    column = 0
    sum = 0
    Hess = ReadHess()
    np.savetxt('Hess.txt', Hess)
    # fb = open(path + filename.split('.')[0] + '.hess', 'w', encoding='utf8')
    fb = open(filename.split('.')[0] + '.hess', 'w', encoding='utf8')
    fb.write('\n$orca_hessian_file\n\n$act_atom\n  0\n\n$act_coord\n  0\n\n$act_energy\n        0.000000\n\n$hessian\n')
    fb.write(str(Hess.shape[0]) + '\n')
    for i in range(0, (Hess.shape[0] * int(Hess.shape[0] / 5 + 1))):
        column = int(i / Hess.shape[0]) * 5
        if i % Hess.shape[0] == 0:
            fb.write((20 - len(str(column))) * ' ' + str(column))
            fb.write((18 - len(str(column + 1))) * ' ' + str(column + 1))
            fb.write((18 - len(str(column + 2))) * ' ' + str(column + 2))
            fb.write((18 - len(str(column + 3))) * ' ' + str(column + 3))
            fb.write((18 - len(str(column + 4))) * ' ' + str(column + 4))
            fb.write(8 * ' ' + '\n')
        for j in range(0, 5):
            column = int(i / Hess.shape[0]) * 5 + j
            if sum == Hess.shape[0]*Hess.shape[0]:
                return
            if j == 0:
                fb.write((4 - len(str(i % Hess.shape[0]))) * ' ' + str(i % Hess.shape[0]) + 5 * ' ')
            if column < Hess.shape[0]:
                if Hess[i % Hess.shape[0]][column] >= 0:
                    fb.write(' ')
                    fb.write(str(Hess[i % Hess.shape[0]][column]))
                else:
                    fb.write(str(Hess[i % Hess.shape[0]][column]))
                fb.write('  ')
                sum = sum + 1
            if j == 4:
                fb.write('\n')
    fb.close()




PrintHess()
