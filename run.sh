#!/bin/sh

PLAYERS="[(10, 1), (10, 10000)]"
N_VALIDATORS=4
N_PROPOSERS=1
N_CONNECTIONS=5
N_HEARTBEATS_IN_ROUND=20
P_TRANSACTIONS=0.1
MEAN_PROP_TIME=0.1

python main.py --players="$PLAYERS" --nvalidators=$N_VALIDATORS --nproposers=$N_PROPOSERS --nconnections=$N_CONNECTIONS --nheartbeatsinround=$N_HEARTBEATS_IN_ROUND --ptransactions=$P_TRANSACTIONS --meanproptime=$MEAN_PROP_TIME


