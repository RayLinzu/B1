import numpy as np
import math
from keras import initializers
from keras.initializers import identity
from keras.models import model_from_json
from keras.models import Sequential, Model
#from keras.engine.training import collect_trainable_weights
from keras.models import Sequential, Model
from keras.layers import PReLU, LeakyReLU, Input, concatenate
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
import tensorflow as tf
import keras.backend as K


class ActorNetwork(object):
    def __init__(self, sess, state_size, action_size, TAU, LEARNING_RATE):
        self.sess = sess
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        K.set_session(sess)

        #Now create the model
        self.model , self.weights, self.state = self.create_actor_network(state_size, action_size)   
        self.target_model, self.target_weights, self.target_state = self.create_actor_network(state_size, action_size) 
        self.action_gradient = tf.placeholder(tf.float32,[None, action_size])
        self.params_grad = tf.gradients(self.model.output, self.weights, -self.action_gradient)
        grads = zip(self.params_grad, self.weights)
        self.optimize = tf.train.AdamOptimizer(LEARNING_RATE).apply_gradients(grads)
        #self.optimize = tf.contrib.opt.NadamOptimizer(LEARNING_RATE).apply_gradients(grads)
        self.sess.run(tf.global_variables_initializer())

    def train(self, states, action_grads):
            self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.action_gradient: action_grads
        })

    def target_train(self):
        actor_weights = self.model.get_weights()
        actor_target_weights = self.target_model.get_weights()
        for i in range(len(actor_weights)):
            actor_target_weights[i] = self.TAU * actor_weights[i] + (1 - self.TAU)* actor_target_weights[i]
        self.target_model.set_weights(actor_target_weights)

    def create_actor_network(self, state_size,action_size):
        #print("Now we build the model")
        S = Input(shape=[state_size])
        H1= Dense(512,activation=PReLU())(S)
        H2= Dense(256,activation=PReLU())(H1)
        H3= Dense(256,activation=PReLU())(H2)
        H4= Dense(128,activation=PReLU())(H3)
        V = Dense(action_size,activation='linear')(H4)
        
        model=Model(inputs=S, outputs=V)
        adam = Adam(lr=self.LEARNING_RATE)
        model.compile(loss='mse',optimizer=adam,metrics=['mape'])

        return model, model.trainable_weights, S


