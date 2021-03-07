# BABD-Scalabale-data-and-processing
 Project for BABD Master @ MIP - Politecnico di Milano
 Designed, developed and tested by:
 * Gabriele Sartor
 * Matteo Canale
 * Matteo Gatto
 * Federico Pomè
 * Fabio Dopudi
 * 
# Main components
 The project aims to exploit scalable technologies both for storing data and processing them.
 A MongoDB instance is populated with data from reddit through a daemon script in python and the data can be accessed using an API developed with the [FastAPI Framework](https://fastapi.tiangolo.com/).
 A Redis cache layer is used to store some reccurent queries on a daily base.
 Eventually, there is a jupyter notebook with some ML models which predict the probability of a company going bankrupt based on their balance-sheet and other financial indicators.

# Quick Setup
 The project is built on Docker using docker-compose to orchestrate containers. Two docker-compose files are available, one for development purposes and one ready for production (considering the nature of the project security concerns are only partially accounted for)

 To quickly run the application some steps are needed:
 1. Create mongo configuration file and fill it with user credentials and starting collections and indexes
    ```bash
    cp mongo/init/mongo-init.example.js mongo/init/mongo-init.js
    ```
 2. Create secrets.env file and fill it with Mongo credentials and an API-key (You can generate one using [uuid4](https://www.uuidgenerator.net/)
 3. Edit docker-compose files with your domain and services/traefik/traefik.prod.toml with your personal email account
 4. Run `docker-compose up -d --build`

# Future possible developments
 * Deploy the ML model and make it available through the API for real-time and custom predictions
 
