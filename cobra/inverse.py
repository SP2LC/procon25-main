from multiprocessing import Pool

def inverse(resultAToB):
  resultBToA = {}
  for k, v in resultAToB.items():
    for candicate in v:
      if True:
        if not candicate[0] in resultBToA:
          resultBToA[candicate[0]] = []
        resultBToA[candicate[0]].append((k, candicate[1]))
        #resultBToA[candicate[0]].sort(key=lambda a: a[1])
  for key in resultBToA.keys():
    resultBToA[key].sort(key=lambda a: a[1])
  return resultBToA

def inverse2(resultAToBWidth, resultAToBHeight):
  pool = Pool(4)
  results = pool.map(inverse, [resultAToBWidth, resultAToBHeight])
  pool.close()
  return results
