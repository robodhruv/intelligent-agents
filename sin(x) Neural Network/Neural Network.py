'''
Function Approximator
This neural network uses Universal Approximator technique to predict the value of function in a closed domain. 
This works on the theorem that any function in a closed domain which is continuous or discontinuous at finitely many points
can be approximated using piece-wise constant functions. 
It comprises of one hidden layer with variable number of neurons (default 50)
'''
#from sys import argv
import tensorflow as tf
import numpy as np
import tflearn
import matplotlib.pyplot as plt

#script , hid_dim = argv

def univAprox(x, hidden_dim=50):
    input_dim = 1 
    output_dim = 1

    with tf.variable_scope('UniversalApproximator'):
        ua_w = tf.get_variable(
            name='ua_w'
            , shape=[input_dim, hidden_dim]
            , initializer=tf.random_normal_initializer(stddev=.1)
        )
        ua_b = tf.get_variable(
            name='ua_b'
            , shape=[hidden_dim]
            , initializer=tf.constant_initializer(0.)
        )
        z = tf.matmul(x, ua_w) + ua_b
        a = tf.nn.relu(z) 
        ua_v = tf.get_variable(
            name='ua_v'
            , shape=[hidden_dim, output_dim]
            , initializer=tf.random_normal_initializer(stddev=.1)
        )
        z = tf.matmul(a, ua_v)

    return z

def func_to_approx(x):
    return tf.sin(x)

def main():
    with tf.variable_scope('Graph') as scope:
        x = tf.placeholder(tf.float32, shape=[None, 1], name="x")
        y_true = func_to_approx(x)
        y = univAprox(x,500)
        with tf.variable_scope('Loss'):
            loss = tf.reduce_mean(tf.square(y - y_true))
            loss_summary_t = tf.summary.scalar('loss', loss)
        adam = tf.train.AdamOptimizer(learning_rate=1e-2)
        train_op = adam.minimize(loss)

    #saver = tf.train.Saver()

	
    with tf.Session() as sess:
        print "Training our universal approximator"
        sess.run(tf.global_variables_initializer())
        for i in range(1000):
            x_in = np.random.uniform(-10, 10, [100000, 1])
            current_loss, loss_summary, _ = sess.run([loss, loss_summary_t, train_op], feed_dict={ x: x_in })
            if (i+1) % 100 == 0 :
                print ('batch: %d, loss %f' % (i+1,current_loss))
        saver_path = saver.save(sess , 'model.ckpt')
    
    print '\n' , "Plotting Graph"
    with tf.Session() as sess:
        saver.restore(sess, 'model.ckpt')
        print "Model Restored"
        x_p = np.array([[(i - 1000)/100] for i in range(2000)])
        y_p = sess.run(y , feed_dict= {x:x_p})
    plt.plot(x_p , y_p , 'k' )
    plt.axis([-12 , 12 , -2 , 2])
    plt.show()
    return

if __name__ == '__main__':
    main()