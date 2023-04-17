# This script is a utility to extract an SMT and a DIMACS file from the provided linux kernel version
FROM ubuntu:22.04
# Install all packages
RUN apt-get update && apt-get install -y --allow-unauthenticated \
  git \
  python3 python3-pip python3-venv \
  python3-setuptools \
  python3-dev
WORKDIR /app
RUN git clone https://github.com/ChristianKaltenecker/PerformanceEvolution_Website.git \
  && cd PerformanceEvolution_Website \
  # Install all required packages
  && pip install -r Scripts/requirements.txt
# Execute the python scripts to generate all plots and data
RUN cd /app/PerformanceEvolution_Website/Scripts \
  && python3 ./main.py \
  && python3 ./cumulative_plots.py