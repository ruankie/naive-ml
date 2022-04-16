# The naivety of ML models and how to avoid the naive trap

Read the accompanying [blog post](https://medium.com/@ruankie/on-the-naivety-of-ml-models-and-how-to-avoid-the-naive-trap-aca90f5924e0) for more details.

When forecasting stock price movements with fancy ML models, you want your models to learn something useful from the provided data that humans might not be aware of so you have a competitive edge. This repo shows examples of where those fancy ML models learn something dumb that looks intelligent and how to check if your models are doing the same.

# How to use
1. Clone this repo onto your machine
2. Open development environment using one of the following methods:
    * Open in VS code using the `Remote-Containers` extension
    * Manually reproduce the development environment using the Dockerfile in `.devcontainer/`
    * Install the requiremetns your local environment by running `pip install -r requirements.txt`
3. Navigate to `notebooks/full-example.ipynb` to see a step-by-step example or to reproduce the results
4. (Optional) Browse through the code in `src/`
5. (Optional) Add your own custom models to `src/models.py`
