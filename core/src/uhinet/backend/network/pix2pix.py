'''
UHINET Network Pix2Pix Module

@credit: Google (https://www.tensorflow.org/tutorials/generative/pix2pix)
'''
from __future__ import absolute_import, division, print_function, \
    unicode_literals
from IPython.display import clear_output

import tensorflow as tf
import time

from .data_helpers import load, resize, random_crop, normalize, random_jitter,\
    load_image_train, load_image_test, downsample, upsample


class Pix2Pix():
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return 'Pix2Pix'

    @staticmethod
    def generator(output_channels: int) -> tf.keras.Model:
        down_stack = [
            downsample(64, 4, apply_batchnorm=False),  # (bs, 128, 128, 64)
            downsample(128, 4),  # (bs, 64, 64, 128)
            downsample(256, 4),  # (bs, 32, 32, 256)
            downsample(512, 4),  # (bs, 16, 16, 512)
            downsample(512, 4),  # (bs, 8, 8, 512)
            downsample(512, 4),  # (bs, 4, 4, 512)
            downsample(512, 4),  # (bs, 2, 2, 512)
            downsample(512, 4),  # (bs, 1, 1, 512)
        ]

        up_stack = [
            upsample(512, 4, apply_dropout=True),  # (bs, 2, 2, 1024)
            upsample(512, 4, apply_dropout=True),  # (bs, 4, 4, 1024)
            upsample(512, 4, apply_dropout=True),  # (bs, 8, 8, 1024)
            upsample(512, 4),  # (bs, 16, 16, 1024)
            upsample(256, 4),  # (bs, 32, 32, 512)
            upsample(128, 4),  # (bs, 64, 64, 256)
            upsample(64, 4),  # (bs, 128, 128, 128)
        ]

        initializer = tf.random_normal_initializer(0., 0.02)
        last = tf.keras.layers.Conv2DTranspose(
            output_channels, 4,
            strides=2,
            padding='same',
            kernel_initializer=initializer,
            activation='tanh')  # (bs, 256, 256, 3)

        concat = tf.keras.layers.Concatenate()

        inputs = tf.keras.layers.Input(shape=[None, None, 3])
        x = inputs

        # Downsampling through the model
        skips = []
        for down in down_stack:
            x = down(x)
            skips.append(x)

        skips = reversed(skips[:-1])

        # Upsampling and establishing the skip connections
        for up, skip in zip(up_stack, skips):
            x = up(x)
            x = concat([x, skip])

        x = last(x)

        return tf.keras.Model(inputs=inputs, outputs=x)

    @staticmethod
    def discriminator() -> tf.keras.Model:
        initializer = tf.random_normal_initializer(0., 0.02)

        inp = tf.keras.layers.Input(shape=[None, None, 3], name='input_image')
        tar = tf.keras.layers.Input(shape=[None, None, 3], name='target_image')

        x = tf.keras.layers.concatenate(
            [inp, tar])  # (bs, 256, 256, channels*2)

        down1 = downsample(64, 4, False)(x)  # (bs, 128, 128, 64)
        down2 = downsample(128, 4)(down1)  # (bs, 64, 64, 128)
        down3 = downsample(256, 4)(down2)  # (bs, 32, 32, 256)

        zero_pad1 = tf.keras.layers.ZeroPadding2D()(down3)  # (bs, 34, 34, 256)
        conv = tf.keras.layers.Conv2D(
            512, 4, strides=1,
            kernel_initializer=initializer,
            use_bias=False)(zero_pad1)  # (bs, 31, 31, 512)

        batchnorm1 = tf.keras.layers.BatchNormalization()(conv)

        leaky_relu = tf.keras.layers.LeakyReLU()(batchnorm1)

        # (bs, 33, 33, 512)
        zero_pad2 = tf.keras.layers.ZeroPadding2D()(leaky_relu)

        # (bs, 30, 30, 1)
        last = tf.keras.layers.Conv2D(
            1, 4, strides=1,
            kernel_initializer=initializer)(zero_pad2)

        return tf.keras.Model(inputs=[inp, tar], outputs=last)

    @staticmethod
    def discriminator_loss(
            disc_real_output: tf.keras.Model,
            disc_generated_output: tf.keras.Model,
    ) -> tf.losses.BinaryCrossentropy:
        loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        real_loss = loss_object(tf.ones_like(
            disc_real_output), disc_real_output)

        generated_loss = loss_object(tf.zeros_like(
            disc_generated_output), disc_generated_output)

        total_disc_loss = real_loss + generated_loss

        return total_disc_loss

    @staticmethod
    def generator_loss(
            disc_generated_output: tf.keras.Model,
            gen_output: tf.keras.Model,
            target: tf.data.Dataset,
            _lambda: int) -> tf.losses.BinaryCrossentropy:
        loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        gan_loss = loss_object(tf.ones_like(
            disc_generated_output), disc_generated_output)

        # mean absolute error
        l1_loss = tf.reduce_mean(tf.abs(target - gen_output))

        total_gen_loss = gan_loss + (_lambda * l1_loss)

        return total_gen_loss

    # @staticmethod
    # def generate_images(
    #         model: tf.keras.Model,
    #         test_input,
    #         tar):
    #     # the training=True is intentional here since
    #     # we want the batch statistics while running the model
    #     # on the test dataset. If we use training=False, we will get
    #     # the accumulated statistics learned from the training dataset
    #     # (which we don't want)
    #     prediction = model(test_input, training=True)
    #     plt.figure(figsize=(15, 15))

    #     display_list = [test_input[0], tar[0], prediction[0]]
    #     title = ['Input Image', 'Ground Truth', 'Predicted Image']

    #     for i in range(3):
    #         plt.subplot(1, 3, i+1)
    #         plt.title(title[i])
    #         # getting the pixel values between [0, 1] to plot it.
    #         plt.imshow(display_list[i] * 0.5 + 0.5)
    #         plt.axis('off')

    @tf.function
    def train_step(
            input_image: tf.data.Dataset,
            target: tf.data.Dataset,
            generator: tf.keras.Model,
            discriminator: tf.keras.Model,
            generator_optimizer: tf.keras.optimizers.Optimizer,
            discriminator_optimizer: tf.keras.optimizers.Optimizer) -> None:
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            gen_output = generator(input_image, training=True)

            disc_real_output = discriminator(
                [input_image, target], training=True)
            disc_generated_output = discriminator(
                [input_image, gen_output], training=True)

            gen_loss = Pix2Pix.generator_loss(
                disc_generated_output, gen_output, target)
            disc_loss = Pix2Pix.discriminator_loss(
                disc_real_output, disc_generated_output)

        generator_gradients = gen_tape.gradient(gen_loss,
                                                generator.trainable_variables)
        discriminator_gradients = disc_tape.gradient(
            disc_loss,
            discriminator.trainable_variables)

        generator_optimizer.apply_gradients(zip(generator_gradients,
                                                generator.trainable_variables))
        discriminator_optimizer.apply_gradients(
            zip(discriminator_gradients,
                discriminator.trainable_variables))

    @staticmethod
    def fit(train_ds: tf.data.Dataset,
            test_ds: tf.data.Dataset,
            epochs: int,
            generator: tf.keras.Model,
            checkpoint_path: str,) -> None:
        for epoch in range(epochs):
            start = time.time()

            # Train
            for input_image, target in train_ds:
                Pix2Pix.train_step(input_image, target)

            clear_output(wait=True)
            # Test on the same image so that the progress of the model can be
            # easily seen.
            for example_input, example_target in test_ds.take(1):
                Pix2Pix.generate_images(
                    generator, example_input, example_target)

            # saving (checkpoint) the model every 20 epochs
            if (epoch + 1) % 20 == 0:
                checkpoint.save(file_prefix=checkpoint_prefix)

            print(
                'Time taken for epoch {} is {} sec\n'.format(
                    epoch + 1,
                    time.time()-start))
