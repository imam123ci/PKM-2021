from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(13) as p:
        print(p.map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]))