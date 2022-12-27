import numpy as np


filename = input("请输入fchk文件名:")
gjffilename = input("请输入gjf文件名:")

N = 0
C = '12.01100'
H = '1.00800'
n = '14.00700'
O = '15.99900'
S = '32.06640'
F = '18.99840'
Cl = '35.45300'
Br = '79.90410'
I = '126.90450'
P = '30.97380'
bohrTA = 0.529177249

def ReadAtom():
    flag = 2
    list =[]
    fg = open(gjffilename, 'r', encoding='utf8')
    for line in fg:
        if line == '\n':
            flag = flag - 1
        if flag == 0:
            line_save = line.rstrip('\n').split(' ')
            list = list + line_save
    while '' in list:
        list.remove('')
    del list[0:2]
    fg.close()
    return list


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
                break
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
    atoms = ReadAtom()
    Natoms = int(len(atoms)/4)
    SumAtoms = 0
    fb.write('\n\n')
    fb.write('$atoms\n')
    fb.write(str(Natoms)+'\n')
    for i in range(0, Natoms):
        for j in range(0, 4):
            if j == 0:
                fb.write(atoms[SumAtoms])
                fb.write('    ')
                if atoms[SumAtoms] == 'C':
                    fb.write(C)
                    fb.write('    ')
                if atoms[SumAtoms] == 'H':
                    fb.write(H)
                    fb.write('    ')
                if atoms[SumAtoms] == 'O':
                    fb.write(O)
                    fb.write('    ')
                if atoms[SumAtoms] == 'N':
                    fb.write(n)
                    fb.write('    ')
                if atoms[SumAtoms] == 'P':
                    fb.write(P)
                    fb.write('    ')
                if atoms[SumAtoms] == 'S':
                    fb.write(S)
                    fb.write('    ')
                if atoms[SumAtoms] == 'F':
                    fb.write(F)
                    fb.write('    ')
                if atoms[SumAtoms] == 'Cl':
                    fb.write(Cl)
                    fb.write('    ')
                if atoms[SumAtoms] == 'Br':
                    fb.write(Br)
                    fb.write('    ')
                if atoms[SumAtoms] == 'I':
                    fb.write(I)
                    fb.write('    ')
                SumAtoms = SumAtoms + 1
            else:
                fb.write(str(float(atoms[SumAtoms])/bohrTA))
                fb.write('    ')
                SumAtoms = SumAtoms + 1
            if j == 3:
                fb.write('\n')
    fb.close()




PrintHess()
