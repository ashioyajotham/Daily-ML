class A:
    def _str_(self):
        return "a"

class B(A):
    def _str_(self):
        return "b"

class C(B):
    pass

o = C
print(o)


try:
    raise Exception(1,2,3)
except Exception as e:
    print(len(e.args))




class A:
  def __str__(self):
   return "a"
class B(A):
  def __str__(self):
   return "b"
class C(B):
   pass
o = C()
print(o)


class A:
  v = 2
class B(A):
  v = 1
class C(B):
  pass
o = C()
print(o.v)



class A:
   def __init__(self):
    pass
a = A(1)
print(hasattr(a,"A"))


def f(x):
  try:
    x = x / x
  except:
   print("a",end="")
  else:
    print("b",end="")
  finally:
    print("c",end="")
f(1)
f(0)



class A:
  def __init__(self,v = 1):
      self.v = v
def set(self,v):
  self.v = v
  return v
a = A()
print(a.set(a.v + 1))



class A:
   X = 0
def __init__(self,v = 0):
   self.Y = v
   A.X += v
a = A()
b = A(1)
c = A(2)
print(c.X)


def o(p):
  def q():
   return "*" * p
   return q
r = o(1)
s = o(2)
print(r() + s())



def I():
    s = "abcdef"
    for c in s[::2]:
        yield C

for x in I():
    print(x, end="")