## Working with the Planet Tasking API using Python

These guides are to provide working examples of how to use and interact with Planet's [Tasking API](https://developers.planet.com/docs/tasking/). The Planet Tasking API provides the ability to create and manage orders that will provide tasks for Planets satellites which will return beautiful high-resolution imagery. Currently these notebooks will focus on working directly with the API REST endpoints, but never fear, a Python client is on its way.

These guides will show how to create an Order, explaining the various order types available and the differences between them, how to edit or even cancel orders that have been created and the restrictions that apply. The guides will also show how to batch large numbers of orders together using the bulk endpoint.

### The Notebooks
* [Create/Edit/Cancel a basic order](planet_tasking_api_order_creation.ipynb)
* [Different types of order](planet_tasking_api_order_types.ipynb)
* [See existing orders and their current status](planet_tasking_api_order_status.ipynb)
* [Create multiple orders using the /bulk endpoint](planet_tasking_api_bulk_creation.ipynb)