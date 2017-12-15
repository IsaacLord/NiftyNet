# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from niftynet.layer.activation import ActiLayer as Acti
from niftynet.layer.base_layer import TrainableLayer
from niftynet.layer.convolution import ConvolutionalLayer as Conv
from niftynet.layer.downsample import DownSampleLayer as Down


class DownBlock(TrainableLayer):
    def __init__(self,
                 n_output_chns=4,
                 kernel_size=3,
                 downsample_kernel_size=2,
                 downsample_stride=2,
                 acti_func='relu',
                 w_initializer=None,
                 w_regularizer=None,
                 name='res-downsample'):
        super(TrainableLayer, self).__init__(name=name)
        self.n_output_chns = n_output_chns
        self.kernel_size = kernel_size
        self.downsample_kernel_size = downsample_kernel_size
        self.downsample_stride = downsample_stride
        self.acti_func = acti_func
        self.conv_param = {'w_initializer': w_initializer,
                           'w_regularizer': w_regularizer}

    def layer_op(self, inputs, is_training=True):
        """
        Consists of::

            (inputs)--conv_0-+-conv_1--conv_2-+-down_sample--
                             |                |
                             o----------------o

        conv_0 is also returned for feature forwarding purpose
        """
        conv_0 = Conv(n_output_chns=self.n_output_chns,
                      kernel_size=self.kernel_size,
                      acti_func=self.acti_func,
                      with_bias=False, with_bn=True,
                      **self.conv_param)(inputs, is_training)
        conv_1 = Conv(n_output_chns=self.n_output_chns,
                      kernel_size=self.kernel_size,
                      acti_func=self.acti_func,
                      with_bias=False, with_bn=True,
                      **self.conv_param)(conv_0, is_training)
        conv_2 = Conv(n_output_chns=self.n_output_chns,
                      kernel_size=self.kernel_size,
                      acti_func=None,
                      with_bias=False, with_bn=True,
                      **self.conv_param)(conv_1, is_training)
        conv_res = Acti(self.acti_func)(conv_2 + conv_0)
        conv_down = Down('Max',
                         kernel_size=self.downsample_kernel_size,
                         stride=self.downsample_stride)(conv_res)
        return conv_down, conv_0
