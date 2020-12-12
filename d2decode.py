class Result:

    def __init__(self, errorCount, result):
        self.errorCount = errorCount
        self.result = result

def decode(data1, data2, data3, data4, measure1, measure2):
    errorCount = 0
    result = None

    if measure1 == 1:
        errorCount = errorCount + 1
    if measure2 == 1:
        errorCount = errorCount + 1

    if errorCount == 0:
        if ((data1 == 1 and data2 == 1 and data3 == 0 and data4 == 0) or
            (data1 == 0 and data2 == 0 and data3 == 1 and data4 == 1)):
            result = 1
        elif ((data1 == 0 and data2 == 0 and data3 == 0 and data4 == 0) or
              (data1 == 1 and data2 == 1 and data3 == 1 and data4 == 1)):
            result = 0

    return Result(errorCount, result)
