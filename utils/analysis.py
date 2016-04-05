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

