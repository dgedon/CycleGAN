import argparse
import torch
import random
from tqdm import tqdm
import os

import utils
from data import EmojiDatamodule
from model import get_model
from trainer import CycleGANTrainer


if __name__ == '__main__':
    # argparser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--seed', type=int, default=42,
                        help='random seed for number generator (default: 42)')

    # get arguments from datamodule and trainer
    parser = EmojiDatamodule.add_model_specific_args(parser)
    parser = CycleGANTrainer.add_model_specific_args(parser)
    args = parser.parse_args()

    # create logging folder
    log_dir = utils.set_log_dir()

    # set seed
    utils.seed_everything(args.seed)

    # Set device
    use_cuda = torch.cuda.is_available() and not args.no_cuda
    args.device = torch.device('cuda:0' if use_cuda else 'cpu')
    tqdm.write("Using {}!\n".format(args.device))

    # get dataloaders
    tqdm.write("Define dataloaders...")
    data_module_windows = EmojiDatamodule(args)
    tqdm.write("Done!\n")

    # load model
    tqdm.write('Define model(s)...')
    my_models = get_model(args)
    tqdm.write('Done!\n')

    # set up Trainer
    tqdm.write("Set up trainer...")
    trainer = CycleGANTrainer(my_models[2], args)
    tqdm.write("Done!\n")

    # training
    tqdm.write("Start training.")
    for epoch in range(1, args.max_epochs + 1):
        # training epoch
        train_loss = trainer.train_model(args, data_module, epoch)

    tqdm.write("Training Finished.\n")
    # save the last model
    trainer.save_model(log_dir, 'model_last.pth')

    # generate images on test data
    #todo