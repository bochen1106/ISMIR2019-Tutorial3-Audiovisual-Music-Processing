
"""
Created on Wed Oct 23 22:45:50 2019

@author: bochenli
"""

import chainer


class Model(chainer.Chain):

    def __init__(self):
        super(Model,self).__init__()
        
        with self.init_scope():

            self.conv_1 = chainer.links.Convolution2D( 1, 10, ksize=tuple([5,5]), stride=tuple([1,1]) )
            self.bn_1 = chainer.links.BatchNormalization(10)
            
            self.conv_2 = chainer.links.Convolution2D( 10, 20, ksize=tuple([5,5]), stride=tuple([1,1]) )
            self.bn_2 = chainer.links.BatchNormalization(20)
            
            self.linear_1 = chainer.links.Linear(None, 50)
            
            self.lstm_1 = chainer.links.LSTM(50, 128)
            self.lstm_2 = chainer.links.LSTM(128, 50)
            self.fc_out = chainer.links.Linear(50, 16)
        
            
    def reset(self):
        
        self.lstm_1.reset_state()
        self.lstm_2.reset_state()
        
    def __call__(self, x):
            
        x = x[:, :, :128, :]
        
        lr = chainer.functions.leaky_relu
        
        x = lr(self.bn_1(self.conv_1(x)))
        x = chainer.functions.max_pooling_2d( x, tuple([3,2]) )
        
        x = lr(self.bn_2(self.conv_2(x))) 
        x = chainer.functions.max_pooling_2d( x, tuple([2,2]) )
        
        x = lr(self.linear_1(x)) 
            
        
        x = self.lstm_1(x)
        x = self.lstm_2(x)
        x = self.fc_out(x)
        
        return x
    
    def load(self, filename_weights):
        
        chainer.serializers.load_npz(filename_weights, self)
        
        
