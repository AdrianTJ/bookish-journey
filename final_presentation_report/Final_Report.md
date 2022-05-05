# Bookish Journey: Final Report

| Name                           | Email                  | CU     | Github Handler |
|:------------------------------:|:----------------------:|:------:|:--------------:|
| Adrian Tame                    | atamejac@itam.mx       | 142235 | AdrianTJ       |
| Joel Jaramillo Pacheco         | joel.jaramillo@itam.mx | 30615  | joelitam2021   |
| Mónica Altagracia García López | mgarc372@itam.mx       | 203145 | mogarcia62     |
| Juan Carlos Soto Hernández     | jsotoher@itam.mx       | 82616  | JSOHE          |

## Overview

## Problem Definition

The problem that we decided to tackle is, abstractly, to build a recommendation system for some sort of food or drink. After some research in the space, we ended up finding [TheCocktailDB](https://www.thecocktaildb.com/), an open [API](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces) that gave us access to a collected database of some drinks. Recommendation systems are a [very well studied area of Machine Learning](https://www.mdpi.com/2079-9292/11/1/141), generally relying on unsupervised learning techniques or reinforcement learning to achieve a coherent recommendation engine. For our specific problem we decided early on that we liked the idea of a multi-model system, where we leveraged the predictions of different types of models to generate the final recommendations. We ended up choosing two different clustering models to generate the predictions. [Clustering recommendation is well studied](https://towardsdatascience.com/building-a-food-recommendation-system-90788f78691a), so we decided that this task made sense and our goals were interesting and decided to continue with the project. 

## System Design

<img src="./imgs/Architecture_Diagram.png" title="" alt="Architecture_Diagram.png" data-align="center">

We use different technologies and parts of the GCP tech stack to build and deploy the recommendation engine: 

* **VertexAI**: Initially used for prototyping, it became a core component of the way we generate online predictions. We use the [Workbench](https://cloud.google.com/vertex-ai/docs/workbench/) to have JupyterLab up so we can run some of the scripts, and we also use [VertexAI models and endpoints to deploy the model](https://cloud.google.com/vertex-ai/docs/predictions/deploy-model-api) and then call it using the [predictions](https://cloud.google.com/vertex-ai/docs/predictions/online-predictions-custom-models) interface. 

* **Cloud Storage**: We keep everything relevant to the project on cloud storage. We took more of a [data lake](https://cloud.google.com/learn/what-is-a-data-lake#:~:text=A%20data%20lake%20is%20a,of%20it%2C%20ignoring%20size%20limits.) approach where we have two buckets where we store structured and sometimes unstructured data. 

* **BigQuery:** We use this part of the tech stack as our one-stop shop for everything having to do with SQL and data cleaning. We extract the data and save it in a JSON file for each cocktail, so we do some data manipulation to keep the features we want and clean the data up a little. In our [ELT](https://www.integrate.io/blog/what-is-etlt/) pipeline, BigQuery is one of the places where we transform the data, and we further process it and do feature design and extraction in Python. 

* **Airflow**: Our [orchestrator](https://www.element61.be/en/resource/airflow-data-ai-orchestration#:~:text=What%20is%20Airflow%3F,scheduling%2C%20orchestrating%20and%20monitoring%20workflows.) of choice. Batch predictions in our workflow require no interaction from people and the recommendation systems are run automatically. This requires some differences in the tech stack, particularly that we don't use VertexAI when running the airflow instance, but we generate and save the the models the same way. 

* **Python**: The glue that holds everything together, this is the language where we create models, call predictions, generate the tables of batch predictions and prototype. This project is a Python project that uses other components, but first and foremost, this is a Python (and GCP) project. 

An interesting question is why we basically have two stacks or workflows, and this is answered in the difference of the components and parts required to do the types of predictions that we want to do. For [online predictions](https://cloud.google.com/ai-platform/prediction/docs/online-vs-batch-prediction), the orchestration and generation of predictions makes little sense, as we need to be able to access the models with new information at any moment. One use case for online prediction is instead of grabbing a previous cocktail, we want to predict where a list of ingredients not in the database (a new cocktail) would fall and what cocktails we would recommend. If we want a prediction for a cocktail that already exists, then the problem is much simpler, and we can simply refer back to the table of results we had generated the previous day or week and see what cocktails are recommended by the clustrting models, which would be [batch prediction](https://cloud.google.com/ai-platform/prediction/docs/online-vs-batch-prediction). These differing approaches, needs, and goals can be seen in the structure and underlying systems that we use. 

## API Access and Feature Engineering
