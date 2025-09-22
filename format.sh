#!/bin/bash

black --line-length 120 --exclude protos src
ruff check src --fix-only