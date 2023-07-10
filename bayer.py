from PIL import Image
import numpy as np

def get_weighted_avg(_x, _y, arr):
    near_sum, near_count = 0, 0
    far_sum, far_count = 0, 0
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            x, y = _x + dx, _y + dy
            v = arr[x, y]
    #         if x < 0 or x >= arr.shape[0] or y < 0 or y >= arr.shape[1]:
    #             continue
            if not v == 0:
                continue
            if abs(dx) <= 1 and abs(dy) <= 1:
                near_sum += v
                near_count += 1
            else:
                far_sum += v
                far_count += 1
    return (near_sum / near_count) * (2 / 3) + (far_sum / far_count) * (1 / 3)

def debayer(img: Image):
    px = img.load()
    g = np.zeros(img.size)
    r, b = np.zeros(img.size), np.zeros(img.size)
    R, B = np.zeros(img.size), np.zeros(img.size)

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if (i + j) % 2 == 0:
                g[i, j] = px[i, j][1] / 255
            elif i % 2 == 1 and j % 2 == 0:
                R[i, j] = px[i, j][0] / 255
                r[i, j] = R[i, j]
            else:
                B[i, j] = px[i, j][2] / 255
                b[i, j] = B[i, j]
                
    kgr = np.zeros(img.size)
    kgb = np.zeros(img.size)

    for i in range(1, img.size[0] - 1):
        for j in range(1, img.size[1] - 1):
            kgr[i, j] = g[i, j] - (r[i, j - 1] + r[i, j + 1]) / 2
            kgb[i, j] = g[i, j] - (b[i, j - 1] + b[i, j + 1]) / 2

    for i in range(2, img.size[0] - 2):
        print(i)
        for j in range(2, img.size[1] - 2):
            if (i + j) % 2 == 1:
                g[i, j] = (g[i + 1, j] + g[i - 1, j] + g[i, j + 1] + g[i, j - 1]) / 4
            # if R[i, j] == 0:
            r[i, j] = get_weighted_avg(i, j, R)
            # if B[i, j] == 0:
            b[i, j] = get_weighted_avg(i, j, B)
                    
            '''
            if r[i - 1, j] == 0:
                p1 = r[i, j - 1]
                p2 = r[i, j + 1]
                q1 = b[i - 1, j]
                q2 = b[i + 1, j]
            else:
                p1 = r[i - 1, j]
                p2 = r[i + 1, j]
                q1 = b[i, j - 1]
                q2 = b[i, j + 1]

            if (i + j) % 2 == 0:
                r[i, j] = (p1 + p2) / 2  - (g[i, j - 1] + g[i, j + 1]) / 2 + g[i][j]
                b[i, j] = (q1 + q2) / 2  - (g[i - 1, j] + g[i + 1, j]) / 2 + g[i][j]
                continue
            a = abs(g[i, j + 1] - g[i, j - 1])
            be = abs(g[i + 1, j] - g[i - 1, j])
            p = abs(g[i, j + 1] + g[i, j - 1] - g[i + 1, j] - g[i, j - 1]) / 2
            w = abs(g[i, j - 1] + g[i - 1, j] - g[i + 1, j] - g[i, j + 1]) / 2
            if i % 2 == 1 and j % 2 == 0:
                k = kgr
                c = r[i, j]
            else:
                k = kgb
                c = b[i, j]

            m = min(a, be, p, w)
            if m == a:
                flag = 0
            elif m == be:
                flag = 1
            elif m == p:
                flag = 2
            else:
                flag = 3

            match flag:
                case 0:
                    g[i, j] = a * (c + (k[i, j - 1] + k[i, j + 1]) / 2) + be * ((g[i - 1, j] + g[i + 1, j]) / 2)
                case 1:
                    g[i, j] = a * (c + (k[i - 1, j] + k[i + 1, j]) / 2) + be * ((g[i, j - 1] + g[i, j + 1]) / 2)
                case 2:
                    g[i, j] = a * (c + a * (k[i - 1, j] + k[i, j + 1]) / 2) + be * ((g[i, j - 1] + g[i + 1, j]) / 2) + \
                              be * (g[i, j - 1] + g[i - 1, j] + g[i, j + 1] + g[i + 1, j]) / 4
                case 3:
                    g[i, j] = a * (c + a * (k[i, j + 1] + k[i - 1, j]) / 2) + be * ((g[i + 1, j] + g[i, j + 1]) / 2) + \
                              be * (g[i, j - 1] + g[i - 1, j] + g[i, j + 1] + g[i + 1, j]) / 4
            g[i][j] *= 1
            '''

    newImg = Image.new('RGB', img.size)
    newpx = newImg.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            newpx[i, j] = (int(r[i, j] * 255), 0, 0)
    
    return newImg


debayer(Image.open('C:\\Users\\Max\\Downloads\\Joe_Biden_presidential_portrait.jpg')).show()