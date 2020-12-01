import time
import numpy as np
import random


class Hashs:
    def __init__(self):
        self.h = [None] * 3
        self.g = [None] * 3
        self.primes = []
        self.col = []
        self.values = [1, 2, 3, 4, 5, 6]
        self.cnt = 0

    def make_coef(self):
        for j in range(6):
            self.values.append(random.randint(1, 30))

    def f1(self, numb):
        numb1 = numb << self.values[0]
        numb2 = numb >> self.values[1]
        numb3 = numb << self.values[2]
        return (numb1 ^ numb2 ^ numb3) % len(self.h)

    def f2(self, numb):
        numb1 = numb << self.values[3]
        numb2 = numb >> self.values[4]
        numb3 = numb << self.values[5]
        return (numb1 ^ numb2 ^ numb3) % len(self.g)

    def insert(self, el):
        if self[el[0]] is None:
            self.cnt += 1
        self.insert_reh(el)

    def insert_reh(self, el):
        a = self.f1(el[0])
        b = self.f2(el[0])
        if self.h[a] is not None and self.h[a][0] == el[0]:
            self.h[a] = el
            return
        if self.g[b] is not None and self.g[b][0] == el[0]:
            self.g[b] = el
            return
        self.col = el[0]
        t = el[0] - 1
        h = random.choice([True, False])
        while self.col != t:
            if h:
                numb = self.f1(el[0])
                if self.h[numb] is None or self.h[numb][0] == el[0]:
                    self.h[numb] = el
                    return
                else:
                    el, self.h[numb] = self.h[numb], el
                    h = False
                    t = el[0]
            else:
                numb = self.f2(el[0])
                if self.g[numb] is None or self.g[numb][0] == el[0]:
                    self.g[numb] = el
                    return
                else:
                    el, self.g[numb] = self.g[numb], el
                    h = True
                    t = el[0]
        else:
            self.rehash(el)

    def rehash(self, el):
        self.values.clear()
        self.make_coef()
        m = int(len(self.h) * np.pi / 2)
        lst1 = self.h.copy()
        lst2 = self.g.copy()
        self.h = [None] * m
        self.g = [None] * m
        self.insert_reh(el)
        for i in range(len(lst1)):
            if lst1[i] is not None:
                self.insert_reh(lst1[i])
            if lst2[i] is not None:
                self.insert_reh(lst2[i])

    def remove(self, key):
        numb1 = self.f1(key)
        numb2 = self.f2(key)
        if self.h[numb1] is not None and self.h[numb1][0] == key:
            self.h[numb1] = None
            self.cnt -= 1
        elif self.g[numb2] is not None and self.g[numb2][0] == key:
            self.g[numb2] = None
            self.cnt -= 1
        else:
            raise KeyError

    def get(self, key):
        numb1 = self.f1(key)
        numb2 = self.f2(key)
        if self.h[numb1] is not None and self.h[numb1][0] == key:
            return self.h[numb1][1]
        elif self.g[numb2] is not None and self.g[numb2][0] == key:
            return self.g[numb2][1]
        return None

    def __contains__(self, item):
        if self.get(item) is None:
            return False
        return True

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.insert((key, value))


# Test 1 (timing, about 1 minute in my tests)


# a = Hashs()
# b = time.time()
# a.get(0)
# for i in range(10000000):
#     k = random.randint(1, 10000)
# # you can also use a[k] = i
#     a.insert((k, i))
# print('---------{} sec----------'.format(time.time() - b))
#
# exit(0)


# Test 2 (a lot of equal values)

# for k in range(10):
#     a = Hashs()
#     b = time.time()
#     real_hash = {}
#
#     for i in range(100000):
#         for j in range(5):
#             if random.choice([True, False]):
#                 a.insert((j, 'abracadabra{}'.format(i)))
#                 real_hash[j] = 'abracadabra{}'.format(i)
#     real_hash_2 = real_hash.copy()
#     for el in real_hash_2:
#         if random.choice([True, False]):
#             a.remove(el)
#             real_hash.pop(el)
#     for el in real_hash:
#         if el not in a or a[el] != real_hash[el]:
#             print('incorrect, there are elements in real_hash, which do not exist in a')
#             break
#     print(a.cnt - len(real_hash), '== count elements in a, which do not exist in real_hash')
#     print('---------{} sec----------'.format(time.time() - b))
#
# exit(0)


# Test 3 (correctness)


# a = Hashs()
# b = time.time()
# n = 1000
# real_hash = {}
# real_hash_2 = {}
#
# for i in range(1, n):
#     key = random.randint(int(-1e7), int(1e7))
#     value = "{}".format(key // i)
#     a[key] = value
#     real_hash[key] = value
#     real_hash_2[key] = value
# for key in real_hash:
#     if key not in a or a[key] != real_hash[key]:
#         print('incorrect')
#         break
# for el in real_hash_2:
#     a.remove(el)
#     real_hash.pop(el)
#     if len(real_hash) != a.cnt:
#         print('incorrect')
#         break
# print('---------{} sec----------'.format(time.time() - b))
