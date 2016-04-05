#coding:utf-8
import numpy
import sys
import six
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import pulp

class LocalBayes():

    def __init__(self, nn_num, data_dim):
        self.nn_num = nn_num
        self.data_dim = data_dim


    def get_nearest_n(self, train, test, n=20, max_dist=50):
        """
        :param train: Training dataset. Must be pandas object.
        :param test: Some point of test data. Must be numpy array object.
        :param n: Number of training data in the neighborhood of one test data point.
        :param max_dist: Max distance between train and test.
        :return: The nearest points of training dataset (with any metrics).
        """
        nn_dist_ls, nn_ts_ls = numpy.array([]), []
        te_ele = numpy.array(test).reshape(-1, 1)

        for i, tr_ele in enumerate(train):
            sys.stdout.write('\r%d' % i)
            sys.stdout.flush()
            tr_ele_ls = tr_ele.tolist()
            tr_ele = numpy.array(tr_ele).reshape(-1, 1)
            dist, path = fastdtw(te_ele, tr_ele, dist=euclidean)

            if len(nn_dist_ls) < n:
                nn_dist_ls = numpy.append(nn_dist_ls, dist)
                nn_ts_ls.append(tr_ele_ls)
            elif numpy.max(nn_dist_ls) > dist:
                if numpy.max(nn_dist_ls) < max_dist:
                    break
                max_ind = numpy.argmax(nn_dist_ls)
                nn_dist_ls[max_ind] = dist
                nn_ts_ls[max_ind] = tr_ele_ls
            else:
                continue

        return nn_dist_ls, nn_ts_ls


    def cal_prediction_nearest_n(self):



    def local_bayes_estimation(self, pred_proba_ls, learner_name_ls):

        problem = pulp.LpProblem('localbayes', pulp.LpMaximize)
        var = pulp.LpVariable.dicts('w', (learner_name_ls), 0, 1, 'Continuous')

        for i in six.moves.range(20):
            cnn = pred_[i] + 0.0000001
            gbdt = pred_proba[i][1]
            model_sum = var[1] * math.log(cnn) + var[2] * math.log(gbdt)
            problem += model_sum

        for learner in learner_name:
            problem += var[learner] >= 0

        for learner in learner_name:
            problem += var[learner]
        problem == 1

        return


    def local_bayes_predict(self):
        pass