#coding:utf-8
import numpy
import sys
import six
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import pulp
import math

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import cuda
from chainer import optimizers
from chainer import serializers
from chainer import Link, Chain, ChainList

class LocalBayes():

    def __init__(self, nn_num, data_dim, max_dist):
        self.nn_num = nn_num
        self.data_dim = data_dim
        self.max_dist = max_dist


    def get_nearest_n(self, train, test):
        """
        :param train: Training dataset. Must be pandas object.
        :param test: Some point of test data. Must be numpy array object.
        :param n: Number of training data in the neighborhood of one test data point.
        :param max_dist: Max distance between train and test.
        :return: The nearest points of training dataset (with DTW metrics).
        """
        nn_dist_ls, nn_ts_ls = numpy.array([]), []
        te_ele = numpy.array(test).reshape(-1, 1)

        for i, tr_ele in enumerate(train):

            # sys.stdout.write('\r%d' % i)
            # sys.stdout.flush()

            tr_ele_ls = tr_ele.tolist()
            tr_ele = numpy.array(tr_ele).reshape(-1, 1)
            dist, path = fastdtw(te_ele, tr_ele, dist=euclidean)

            if len(nn_dist_ls) < self.nn_num:
                nn_dist_ls = numpy.append(nn_dist_ls, dist)
                nn_ts_ls.append(tr_ele_ls)
            elif numpy.max(nn_dist_ls) > dist:

                if numpy.max(nn_dist_ls) < self.max_dist:
                    break

                max_ind = numpy.argmax(nn_dist_ls)
                nn_dist_ls[max_ind] = dist
                nn_ts_ls[max_ind] = tr_ele_ls
            else:
                continue

        nn_ts_array = numpy.array(nn_ts_ls)

        return nn_dist_ls, nn_ts_array


    def cal_prediction_nearest_n(self, test_data, nn_ts_array, learner_name_ls, model_dict):
        """
        todo: local_bayes_predictと被ってる・・・
        :param nn_ts_ls: Nearest n data. Must be numpy.array object.
        :param learner_name_ls: List of learner name. For example, cnn, gbdt, logi, and more.
        :param model_dict: Dict of trained models.
        :return:
        """
        nn_pred_dict = {}
        for learner in learner_name_ls:
            if learner == 'cnn':
                x = nn_ts_array.reshape((self.nn_num, 1, 1, self.data_dim)).astype(numpy.float32)
                pred = F.softmax(model_dict['cnn'].predictor(chainer.Variable(x))).data[:, 1]
            elif learner == 'gbdt':
                pred = numpy.squeeze(model_dict['gbdt'].predict_proba(nn_ts_array))[:, 1]
            else:
                print "not enough parameters"
                break

            nn_pred_dict.update({'%s' % learner:pred})

        return nn_pred_dict


    def local_bayes_estimation(self, pred_proba_dict, learner_name_ls):

        problem = pulp.LpProblem('localbayes', pulp.LpMaximize)
        var = pulp.LpVariable.dicts('w', (learner_name_ls), 0, 1, 'Continuous')

        ## objective
        for i in six.moves.range(20):
            model_sum = 0

            for learner in learner_name_ls:
                model_sum += var[learner] * math.log(pred_proba_dict[learner][i] + 0.000000001)

            problem += model_sum

        ##  constraint
        problem_ = 0
        for learner in learner_name_ls:
            problem += var[learner] >= 0
            problem_ += var[learner]

        problem += problem_ == 1
        problem.solve()

        w_dict = {}
        for learner in learner_name_ls:
            w_dict.update({'%s' % learner:var[learner].value()})

        return w_dict


    def local_bayes_predict(self, test_data, learner_name_ls, w_dict, model_dict):

        lb_pred = 0
        for learner in learner_name_ls:

            if learner == 'cnn':
                x = test_data.reshape((1, 1, 1, self.data_dim)).astype(numpy.float32)
                lb_pred += w_dict[learner] * F.softmax(model_dict[learner].predictor(chainer.Variable(x))).data[0][1]
            elif learner == 'gbdt':
                lb_pred += w_dict[learner] * numpy.squeeze(model_dict[learner].predict_proba(test_data.reshape(1, -1))).tolist()[1] ## singleデータなのでtest_data.reshape(1, -1)が必要
            else:
                print "not enough parameters"
                break

        return lb_pred