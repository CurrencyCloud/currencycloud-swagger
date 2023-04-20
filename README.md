# Currencycloud API Documentation
**Source files for the Currencycloud API Documentation.**

The Currencycloud API documentation is maintained in two document formats:

- Markdown
- OpenAPI Specification (v2) written in YAML

There are three categories of documentation on our developer centre: getting started guides, integration guides and API reference documentation. The getting started guides can be found at `data/local/pages/getting-started`, the integration guides can be found at `data/local/pages/integration-guides` and the OpenApi specification for the API reference docs is at `data/local/swagger`.


Most of the source documentation is written in Markdown. The only exception is the file ``reference.yaml``, which is a [YAML](http://yaml.org/) file that conforms to the [OpenAPI Specification (OAS) v2](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md), a popular API definition language previously known as "Swagger".

The OpenAPI definition file describes individual endpoints in the Currencycloud API. OpenAPI definitions can be written in JSON or YAML. We've chosen YAML as it is the most readable of the two formats.

All source files are UTF-8 encoded with Unix line-endings (``LF``, ``\n``). They can be edited with any good text editor program. However, it is recommended to use [Swagger Editor](http://editor2.swagger.io) to make changes to ``./src/reference.yaml``. As you type, Swagger Editor will validate the document against the OpenAPI v2 specification. Swagger Editor also has a built-in Postman-like interface for interacting with API endpoints, though it is not as good as Postman. You can serve your own local instance of Swagger Editor by following the instructions in the "Tools" section, below.

We maintain a style guide for the Currencycloud API documentation. See [STYLE_GUIDE.md](STYLE_GUIDE.md).

## API Versions
The current version of the API is the [latest tagged release](https://github.com/CurrencyCloud/currencycloud-swagger/releases/latest)
and matches the documentation for the current Currencycloud API. Changes merged in master, but not yet part of a release,
are not available on the API. The latest tagged release should be used instead of the swagger definition in master directly.

### Releases
**Current**

- [2.43.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.43.0)

For details on the contents of releases see [CHANGELOG](CHANGELOG.md)

**Previous**

- [2.36.2](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.36.2)
- [2.36.1](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.36.1)
- [2.36.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.36.0)
- [2.32.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.32.0)
- [2.31.3](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.31.3)
- [2.31.2](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.31.2)
- [2.31.1](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.31.1)
- [2.31.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.31.0)
- [2.30.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.30.0)
- [2.29.1](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.29.1)
- [2.29.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.29.0)
- [2.28.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.28.0)
- [2.27.1](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.27.1)
- [2.27.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.27.0)
- [2.26.1](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.26.1)
- [2.26.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.26.0)
- [2.25.1](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.25.1)
- [2.24.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.24.0)
- [2.23.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.23.0)
- [2.22.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.22.0)
- [2.20.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.20.0)
- [2.19.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.19.0)
- [2.18.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.18.0)
- [2.17.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.17.0)
- [2.16.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.16.0)
- [2.15.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.15.0)
- [2.14.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.14.0)
- [2.13.1](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.13.1)
- [2.13.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.13.0)
- [2.12.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.12.0)
- [2.11.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.11.0)
- [2.10.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.10.0)
- [2.9.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.9.0)
- [2.8.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.8.0)
- [2.7.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.7.0)
- [2.6.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.6.0)
- [2.5.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.5.0)
- [2.4.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.4.0)
- [2.3.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.3.0b)
- [2.2.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.2.0)
- [2.1.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.1.0)
- [2.0.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.0.0)

## Deprecation Policy

Deprecated features will no longer be supported in the next release 3 months after the release that the deprecation notification was 
included. The release that the feature was deprecated in is denoted by the tag _x-deprecation-version_.

For more details see [Developer Center Deprecation Policy](https://www.currencycloud.com/developers/deprecation-policy/)

## Tools

### Local Swagger Editor

Docker provides a simple way to start a local [Swagger Editor](https://github.com/swagger-api/swagger-editor) with the API schema 

```
docker pull swaggerapi/swagger-editor
docker run -p 8866:8080 -v $(pwd)/src:/tmp -e SWAGGER_FILE=/tmp/reference.yaml swaggerapi/swagger-editor
```

which can be accessed then via `http://localhost:8866` and after editing new version can be saved.

Alternatively follow the Swagger Editor's local build procedure.

### Remote Swagger Editor

Online editor is available at [https://editor.swagger.io/](https://editor.swagger.io/).

### Postman

The ``reference.yaml`` file is a "single source of truth" for the Currencycloud API. It can be used to auto-generate documentation, tests, and even mock endpoints for development purposes. The file is also compatible with Postman, a popular app that makes it easy to manually test API endpoints.

For a step-by-step guideline on how to configure Postman, please see [this guide](POSTMAN_README.md)

Once Postman is installed and configured it is not mandatory to configure a Postman environment, since the OpenAPI file contains all the information required to generate client interfaces for the Currencycloud API, but it is still useful to setup some environment variables to prepopulate API input parameters while testing. The following environment variables are recommended:

- ``login_id``: The email address that you use to login to your Currencycloud account.
- ``api_key``: Your unique Currencycloud API key that you retrieved from your Currencycloud account.
- ``X-Auth-Token``: Keep this empty initially. Update it when you have an authentication token from the Login endpoint.

Click on "Collections" on the left side of the Postman UI, and then click the icon to "Import collection". Under "Upload files", select the copy of ``reference.yaml`` on your computer. All of the Currencycloud endpoints defined in the OpenAPI document will be imported into a new Postman collection.
