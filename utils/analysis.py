#coding:utf-8
import numpy
import six

class Analysis():

    def __init__(self):
        pass


    def find_pattern(self, test, pred_proba, type='miss'):

        N_test = test['y'].shape[0]
        pattern_x, pattern_y = [], []

        for i in six.moves.range(N_test):
            pred = numpy.argmax(pred_proba[i])

            if type == 'miss':

                if pred == test['y'][i]:
                    continue
                else:
                    pattern_x.append(test['x'][i])
                    pattern_y.append(test['y'][i])
            else:

                if pred != test['y'][i]:
                    continue
                else:
                    pattern_x.append(test['x'][i])
                    pattern_y.append(test['y'][i])

        return pattern_x, pattern_y


    def model_diff(self, model_pred1, model_pred2, label):

        diff, sum = 0, 0
        for pred1, pred2 in zip(model_pred1, model_pred2):
            sum += 1
            if pred1 == pred2:
                diff += 1
        diff_rate = diff / sum

        return diff_rate

