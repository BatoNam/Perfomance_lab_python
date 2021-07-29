import sys
import matplotlib.pyplot as plt
import numpy as np
import re



def is_intersect(sphere, line):
    # x(t) = x0 + t*(x1-x0)
    # y(t) = y0 + t*(y1-y0)
    # z(t) = z0 + t*(z1-z0)
    # R^2 = (x(t)-x_c)^2 + (y(t)-y_c)^2 + (z(t)-z_c)**2

    # Подставляем уравнения прямой в уравнение сферы, получаем квадратное уравнение от t
    # Подставляем обратно в уравнения прямой все полученные решения, получаем координаты.
    x0, y0, z0 = line[0]
    x1, y1, z1 = line[1]
    xc, yc, zc = sphere['center']
    R = sphere['radius']

    a = (x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2
    b = 2*((x1-x0)*(x0-xc) + (y1-y0)*(y0-yc) + (z1-z0)*(z0-zc))
    c = (x0-xc)**2 + (y0-yc)**2 + (z0-zc)**2 - R**2
    
    discriminant = (b**2 - 4*a*c)
    if discriminant < 0:
        return "Коллизий не найдено"
    if round(discriminant, 3) == 0:
        t = -b/(2*a)
        x = x0 + t*(x1-x0)
        y = y0 + t*(y1-y0)
        z = z0 + t*(z1-z0)
        return 1, (x, y, z)
    else:
        t1 = (-b + discriminant**0.5)/(2*a)
        x_1 = x0 + t1*(x1-x0)
        y_1 = y0 + t1*(y1-y0)
        z_1 = z0 + t1*(z1-z0)

        t2 = (-b - discriminant**0.5)/(2*a)
        x_2 = x0 + t2*(x1-x0)
        y_2 = y0 + t2*(y1-y0)
        z_2 = z0 + t2*(z1-z0)
        return 2, (x_1, y_1, z_1), (x_2, y_2, z_2)


if __name__=="__main__":
    if len(sys.argv) != 2:
        print('\n\tПример строки: "python3.8 sphere_line_intersect.py task2.ini(ваш файл)"\n')
        raise Exception('Ошибка в строке запуска')
    filename = sys.argv[1]
    with open(filename) as f:
        structure = f.readline()

    # Файл не хотел форматироваться json-ом (demjson-ом), так что пришлось регулярками парсить...
    num = r'-?\d+\.?\d*'
    sph_center = re.search(r'center:\s?\[(\-?\d+\.?\d*,\s?\-?\d+\.?\d*,\s?\-?\d+\.?\d*)\]', structure)
    sph_radius = re.search(r'radius:\s?(\d+\.?\d*)[\},]', structure)
    line_xyz = re.search(r'line:\s\{\[(\-?\d+\.?\d*,\s?\-?\d+\.?\d*,\s?\-?\d+\.?\d*)\],\s\[(\-?\d+\.?\d*,\s?\-?\d+\.?\d*,\s?\-?\d+\.?\d*)\]\}', structure)

    xc, yc, zc = [float(i) for i in sph_center.group(1).split(',')]
    R = float(sph_radius.group(1))
    x0, y0, z0 = [float(i) for i in line_xyz.group(1).split(',')]
    x1, y1, z1 = [float(i) for i in line_xyz.group(2).split(',')]

    sphere = {'center': [xc, yc, zc], 'radius': R}
    line = ([x0, y0, z0], [x1, y1, z1])
    result = is_intersect(sphere, line)
    
    if isinstance(result, str):
        print(result)
    else:
        for i in range(result[0]):
            print(result[1+i])

    # Extend a line so you can see it outside the sphere
    newline = []
    if (x1-x0) != 0:
        t = (R-x0)/(x1-x0)
    elif (y1-y0) != 0:
        t = (R-y0)/(y1-y0)
    else:
        t = (R-z0)/(z1-z0)
    
    newline.append([x0 + t*(x1-x0), y0 + t*(y1-y0), z0 + t*(z1-z0)])
    newline.append([x0 - t*(x1-x0), y0 - t*(y1-y0), z0 - t*(z1-z0)])
    xyz = list(zip(newline[0], newline[1]))

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # draw sphere
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
    x = R*np.cos(u)*np.sin(v) + xc
    y = R*np.sin(u)*np.sin(v) + yc
    z = R*np.cos(v) + zc
    ax.plot_surface(x, y, z, rstride=1, cstride=1,
                    color='gray', alpha=0.7)

    # draw line
    ax.plot(xyz[0], xyz[1], xyz[2], linewidth=4)
    ax.set_title('Visualisation')

    # draw intersection points
    if not(isinstance(result, str)):
        for i in range(result[0]):
            x_i, y_i, z_i = result[1+i]
            ax.scatter(x_i, y_i, z_i, color='red')


    plt.show()