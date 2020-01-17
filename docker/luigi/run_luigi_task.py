#! /bin/sh

luigid --background --logdir=./log --port=8082

python data_loader.py LoadDatasetPostgres