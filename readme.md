# Voice Enabled Order Processing And Fulfilment System

## Introduction
The program takes the voice command, converts voice signals into text, identify which type of command is given by the user and then extract the information from the given command. 

There can be 3 command types:
1- To Place an order. This type of command will typically contain store name, product name, product quantity and delivery time. System will extract this information and navigate user to checkout screen
2- To View Products from a particular store: This type of command will contain store name. System will extract the store name and display all products of that store.
3- To View Products of a particular category: This type of command will contain category name. System will extract the category name and display all products of that category.

## Tech Stack
1- Flask (Python): To handle apis, get voice command from frontend, process the data and send response to frontend
2- Basic HTML, CSS: For Frontend, to enable user to give voice command and display response


## Installation

To Run This project  install GitBash in VS CODE

in the terminal

source env.sh

*GCP API file is required to run this project*
