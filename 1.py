from array import array


arr = array("f")
arr.fromlist([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
with open("test.bin", "wb") as f:
    arr.tofile(f)
