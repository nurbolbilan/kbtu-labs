def my_generator():
    for i in range(10):
      yield i
for value in my_generator():
  print(value)

# Iterator and generator exercises