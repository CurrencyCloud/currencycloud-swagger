# Test the Currencycloud API

## Step 1: [Register](/register)
Create a Currencycloud account. It's free and painless.


## Step 2: [Get your API key](/account/api-key)
Login to your Currencycloud account to get your unique API key.


## Step 3: [Download our API definition](https://devapi.currencycloud.com/v2/openapi.yaml)
The Currencycloud API is specified in the [OpenAPI v2](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) format, also known as Swagger. Download the specification file to your computer.


## Step 4: Import the API definition into an HTTP client
[Postman](https://www.getpostman.com/) is a popular client application for testing HTTP APIs. Download, install, and run Postman. Click on "Collections" on the left side of the Postman GUI, then click the icon to "Import collection". Under "Upload files", select the ``openapi.yaml`` file that you downloaded to your computer. All the Currencycloud API endpoints will be imported into a new Postman collection.

Click on the gear icon on the right side of the Postman GUI. Select "Manage Environments". Click "Add". Type "Currencycloud Sandbox" for the environment name and add the following environment variables:

- ``login_id``: The email address that you use to login to your Currencycloud account.
- ``api_key``: Your unique Currencycloud API key that you retrieved from your Currency cloud account.
- ``X-Auth-Token``: Keep this empty for now.

Click "Add" and double check that the new environment is selected in the dropdown box in the top-right corner of Postman.


## Step 5: Login
Click "Collections" on the left side of the Postman GUI. Select "Currencycloud API". Select "authenticate" and open "Login". The input parameters for this endpoint will be automatically populated, so just go ahead and click "Send" to make an HTTP request to the endpoint.

If everything is setup correctly, you'll get a response containing an ``auth_token``. Copy the value of the authentication token as the ``X-Auth-Token`` environment parameter value that you left empty in the previous step.

You can now test any of the other endpoints in the Currencycloud API collection. Your authentication token will expire after half an hour of inactivity, in which case you will need to hit the "Login" endpoint again to get a fresh token.

You will be connected to our test infrastructure rather than our live environment. The test API returns real time data, but executes trades in a fictional marketplace, so no real payments are made. When you are ready to transfer real money around the world, just [get in touch with our support team](/support) to upgrade your Currencycloud account.

For convenience, you may add additional default input parameters to your Currencycloud Sandbox environment. For example, to test a client sub-account, you can have the ``{{on_behalf_of}}`` placeholder prepopulated with the sub-account UUID.
