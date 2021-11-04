import numpy as np
import tensorflow as tf

tf.get_logger().setLevel('INFO')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from tensorflow.keras.layers import BatchNormalization, Activation, Flatten, Conv2D, Add, Dense, Dropout,Add, Dense, Multiply, Concatenate, Lambda
import tensorflow.keras.backend as K
from stable_baselines.common.policies import ActorCriticPolicy
from stable_baselines.common.distributions import CategoricalProbabilityDistribution
from environments.blobwar.board_size import get_size


class CustomPolicy(ActorCriticPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=False, **kwargs):
        super(CustomPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=reuse, scale=True)

        size=get_size()
        self.size=size
        self.xsize=size
        self.ysize=size
        self.actions=(self.xsize**2)*(self.xsize**2)


        with tf.variable_scope("model", reuse=reuse):
            observations, legal_actions = self.split_input(self.processed_obs)
            extracted_features = resnet_extractor(observations,self.size, **kwargs)
            self._policy = policy_head(extracted_features,legal_actions,self.size)
            self._value_fn, self.q_value = value_head(extracted_features,self.size)
            self._proba_distribution = CategoricalProbabilityDistribution(self._policy)


        self._setup_init()

    def step(self, obs, state=None, mask=None, deterministic=False):
        if deterministic:
            action, value, neglogp = self.sess.run([self.deterministic_action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        else:
            action, value, neglogp = self.sess.run([self.action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        return action, value, self.initial_state, neglogp

    def proba_step(self, obs, state=None, mask=None):
        return self.sess.run(self.policy_proba, {self.obs_ph: obs})

    def value(self, obs, state=None, mask=None):
        return self.sess.run(self.value_flat, {self.obs_ph: obs})

    def split_input(self,obs):
        ##Extract observation and legal actions from env obs (env obs = observation  + legal actions)
        observations = obs[:, :self.xsize, :, :]
        legal_actions = obs[:, self.xsize:, :, :]  ##The none action is always legal
        return observations, legal_actions

def value_head(y,size):
    y = convolutional(y, 4, 1,name="")
    actions=size**4
    y = Flatten()(y)
    y = dense(y, actions * 2)
    vf = dense(y, 1, batch_norm=False, activation='tanh', name='vf')
    q = dense(y, actions, batch_norm=False, activation='tanh', name='q')
    return vf, q

def policy_head(y,legal_actions,size):
    y = convolutional(y, 4, 1,name="POLICY_CONV")
    actions = size ** 4
    y = Flatten()(y)
    y=dense(y,actions*2)
    policy = dense(y, actions, batch_norm=False, name='pi')
    mask=Flatten()(legal_actions)
    mask = Lambda(lambda x: (1 - x) * -1e8)(mask)
    policy = Add()([policy, mask])

    return policy

def resnet_extractor(y,size, **kwargs):
    y = convolutional(y, 32,2,name="RESNET_CONV")
    y = residual(y, 32,3)
    y = residual(y, 32, 3)
    y = residual(y, 32, 3)
    return y

def convolutional(y, filters, kernel_size,name=None):
    y = Conv2D(filters, kernel_size=kernel_size, strides=1, padding='same',name=name)(y)
    y = BatchNormalization(momentum=0.9)(y)
    y = Activation('relu')(y)
    return y

def residual(y, filters, kernel_size):
    """:
    Residual network with two conv blocks
    """
    shortcut = y
    y = Conv2D(filters, kernel_size=kernel_size, strides=1, padding='same')(y)
    y = BatchNormalization(momentum=0.9)(y)
    y = Activation('relu')(y)
    y = Conv2D(filters, kernel_size=kernel_size, strides=1, padding='same')(y)
    y = BatchNormalization(momentum=0.9)(y)
    y = Add()([shortcut, y])
    y = Activation('relu')(y)
    return y

def dense(y, filters, batch_norm=True, activation='relu', name=None):
    """
    Standard Dense layer
    :param y:
    :type y:
    :param filters:
    :type filters:
    :param batch_norm:
    :type batch_norm:
    :param activation:
    :type activation:
    :param name:
    :type name:
    :return:
    :rtype:
    """
    if batch_norm or activation:
        y = Dense(filters)(y)
    else:
        y = Dense(filters, name=name)(y)
    if batch_norm:
        if activation:
            y = BatchNormalization(momentum=0.9)(y)
        else:
            y = BatchNormalization(momentum=0.9, name=name)(y)
    if activation:
        y = Activation(activation, name=name)(y)
    return y

