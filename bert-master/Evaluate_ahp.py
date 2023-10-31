# 层次分析法
import numpy as np
class AHP:
    def __init__(self, data):
        self.data = data
        self.n = data.shape[0]
        self.RI = [0, 0, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]
        self.eigen_value, self.eigen_vector = np.linalg.eig(self.data)
        self.max_eigen_value = np.max(self.eigen_value)
        self.CI = (self.max_eigen_value - self.n) / (self.n - 1)
        self.CR = self.CI / self.RI[self.n - 1]

    def consistant_test(self):
        if self.CR < 0.1:
            print("CR = " + str(self.CR) + "通过一致性检验")
            return True
        else:
            print("CR = " + str(self.CR) + "未能通过一致性检验")
            return False

    def cal_weight_eig_method(self):
        weight = self.max_eigen_value / np.sum(self.eigen_vector)
        v = []
        print(weight)
        return weight

if __name__ == "__main__":
    b = np.array([[1, 1/9, 1, 1, 1/3, 1/3, 1, 1/6],
                  [9, 1, 9, 9, 3, 3, 9, 3/2],
                  [1, 1/9, 1, 1, 1/3, 1/3, 1, 1/6],
                  [1, 1/9, 1, 1, 1/3, 1/3, 1, 1/6],
                  [3, 1/3, 3, 3, 1, 1, 3, 1/2],
                  [3, 1 / 3, 3, 3, 1, 1, 3, 1 / 2],
                  [1, 1 / 9, 1, 1, 1 / 3, 1 / 3, 1, 1 / 6],
                  [6, 2/3, 6, 6, 2, 2, 6, 1]])
    b = np.array([[1, 6, 1, 1, 2, 2, 1, 6],
    [1 / 6, 1, 1 / 6, 1 / 6, 1 / 2, 1 / 2, 1 / 6, 1],
    [1, 6, 1, 1, 2, 2, 1, 6],
    [1, 6, 1, 1, 2, 2, 1, 6],
    [1 / 2, 2, 1 / 6, 1 / 6, 1, 1, 1 / 2, 2],
    [1 / 2, 2, 1 / 6, 1 / 6, 1, 1, 1 / 2, 2],
    [1, 6, 1, 1, 2, 2, 1, 6],
    [1 / 6, 1, 1 / 6, 1 / 6, 1 / 2, 1 / 2, 1 / 6, 1]])
    weight1 = AHP(b).cal_weight_eig_method()
    print(AHP(b).consistant_test())