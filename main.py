from ursina import *
import math
#масив для порівняння дистанції на теперішньому та минулих кроках в алгоритмі
mas=[1000,0]
#масив для запису значень центру сфери та точки перетину
mas1=[0,0,0,0,0,0]

def equation_plane(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    #функція яка знаходить коеф рння площини
    # x1, y1, z1, x2, y2, z2, x3, y3, z3 - відповідно коорд трьох точок
    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)
    print("Рівняння площини: ", a, "x +", b, "y +", c, "z +", d, "= 0.")
    return a,b,c,d


def distance(x, y, z, a, b, c, d):
    #функція обраховує відстань від точки до її проекції на площині та повертає це значення
    # a, b, c, d - коеф рння площини x, y, z - коорд точки
    d = abs((a * x + b * y + c * z + d))
    e = (math.sqrt(a * a + b * b + c * c))
    return d/e

def proecziya(a, b, c, d, x, y, z):
    #функція здійснює пошук координат проекції точки на площину під прямим кутом та повертає ці значення
    # a, b, c, d - коеф рння площини x, y, z - коорд точки
    t = -((a * x + b * y + c * z + d) / (a * a + b * b + c * c))
    x1 = a * t + x
    y1 = b * t + y
    z1 = c * t + z

    return x1, y1, z1

def distance_btw_2_points(x, y, z, x2, y2, z2):
    #Функція знаходить відстанб між двома точками у просторі за формулою та повертає її
    #x, y, z, x2, y2, z2 - відповідно коорд двох точок
    return math.sqrt((x -x2) * (x -x2) + (y - y2) * (y- y2) + (z - z2) * (z - z2))

def tochka_peret(a, b, c, d, x, y, z, r, vx, vy, vz):
    #фкція знаходить точку перетину та точку центра сфери при перетині
    #a, b, c, d- коеф рння площини; x, y, z, r- коорд сфери та радіус; vx, vy, vz -знач вектора руху
    global mas
    global mas1
    #обраховуємо значення дистанції (довжина проекції-радіус) та записуємо це значення у масив для порівнянь
    dis = distance(x, y, z, a, b, c, d)-r
    mas[1]=dis
    #перевіряємо чи виконується умова для завершення алгоритму
    #тобто чи дистанція є меншою за точність(0.001) та більше-рівною за 0
    if dis>=0 and dis<=0.001:
        mas1[0] = x
        mas1[1] = y
        mas1[2] = z
        #знаходження точки перетину функцією пошуку координат проеції
        mas1[3],mas1[4],mas1[5]=proecziya(a, b, c, d, x, y, z)
        return
    #якщо умова завершення не виконалась то
    #перевіряємо чи дистанція не є мінусовою
    elif dis<0:
        #повертаємось на 2 кроки назад
        x = x - 2 * vx
        y = y - 2 * vy
        z = z - 2 * vz
        mas[0] = distance(x, y, z, a, b, c, d) - r
        #зменшуємо вектор руху у 2 рази
        vx = vx / 2
        vy = vy / 2
        vz = vz / 2
        # викликаємо рекурсію з новими значеннями
        tochka_peret(a, b, c, d, x, y, z, r, vx, vy, vz)
    #перевіряємо чи довжина проекцції на теперішньому кроці не є більшою за довжину на минулому
    elif mas[0]>=mas[1]:
        #теперішня довж проекції стає проекцією минулого кроку для наступної ітерації
        mas[0]=dis
        #знаходження нових координат центра сфери
        x = x + vx
        y = y + vy
        z = z + vz
        # викликаємо рекурсію з новими значеннями
        tochka_peret(a, b, c, d, x, y, z, r, vx, vy, vz)
    #якщо інші умови не справдились значить теперішня відстань є більшою за попередню
    else:
        #повертаємось на 2 кроки назад
        x = x - 2*vx
        y = y - 2*vy
        z = z - 2*vz
        mas[0]= distance(x, y, z, a, b, c, d)-r
        # викликаємо рекурсію з новими значеннями
        vx = vx / 2
        vy = vy / 2
        vz = vz / 2
        # викликаємо рекурсію з новими значеннями
        tochka_peret(a, b, c, d, x, y, z, r, vx, vy, vz)


#Задання параметрів
#точки площини
x1, y1, z1 = 1, 0, 0
x2, y2, z2 = 0, 0, 0
x3, y3, z3 = 0, 0, 1

#Задання центра сфери та її радіуса
x, y, z = 1, 5, 0
r=1
#Задання швидкості та напрямку руху
V=1
vx,vy,vz=1,-1,0

#Знаходження коеф рння площини
a,b,c,d=equation_plane(x1, y1, z1, x2, y2, z2, x3, y3, z3)

#Виклик алгоритму та виведення результатів

try:
    tochka_peret(a, b, c, d, x, y, z, r, vx, vy, vz)
    print("Точка перетину= ",mas1[3],mas1[4],mas1[5])
    tx,ty,tz=mas1[3],mas1[4],mas1[5]
    dis=distance_btw_2_points(x, y, z, tx, ty, tz)
    print("Відстань від початку руху фігури = ",dis,". Час = ",dis/V)
    ttx,tty,ttz=mas1[0],mas1[1],mas1[2]
    #Графічна реалізація
    app=Ursina()
    window.fullscreen_size=1920,1080
    #Візуалізація площини
    pt_of_plane = ((x1 * 20, y1 * 20, z1 * 20), (x2 * 20, y2 * 20, z2 * 20), (x3 * 20, y3 * 20, z3 * 20))
    toch_peret=((tx, ty, tz), (tx, ty, tz))
    tris = ((0, 1),(1,2),(0,2))
    triangle=(0,1,2)

    lines_of_plane = Entity(model=Mesh(vertices=pt_of_plane, triangles=tris, mode='line', thickness=4), color=color.cyan)
    points_of_plane = Entity(model=Mesh(vertices=pt_of_plane, mode='point', thickness=.05), color=color.green)
    tr=Entity(model=Mesh(vertices=pt_of_plane, triangles=triangle), color=color.pink)

    #вектор руху
    en=Entity(position=Vec3(x,y,z))
    #візуалізація сфери
    sphere=Entity(model='sphere',color=color.red,position=(x,y,z),scale=r*2).add_script(
    SmoothFollow(speed=1,target=en,offset=(0,0,0)))

    EditorCamera()

    def update():
        # при натисканні кнопки сфера починає рух
        if held_keys["q"]:
            en.position = Vec3(ttx, tty, ttz)
            if en.position == Vec3(ttx, tty, ttz):
                # візуалізація точки перетину
                tochka_peretuny = Entity(model=Mesh(vertices=toch_peret, mode='point', thickness=.05), color=color.blue)
    app.run()
#якщо досягнуто максимуму рекурсії то розвязку нема
except(RecursionError):
    print("Перетину нема, введіть інший вектор руху")


