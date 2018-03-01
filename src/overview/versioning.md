# Versioning
We have a strict versioning policy that prevents breaking changes.

The current version of the Currencycloud API is v2. We may continue to extend the current version with new functionality, but never in a way that breaks compatibility with existing clients. When backwards compatibility needs to be broken, we will publish a new version of the API, which will be served alongside the existing version. Old versions of the API will continue to be supported and maintained long after they are superseded by new versions. It is our policy to maintain legacy API versions for at least one year.

This policy of long-term support for all major API versions will significantly minimize the cost of integrating our API into your own applications.

But eventually legacy versions of the Currencycloud API will be deprecated. The endpoints will stop working and return a ``410 Gone`` status.


## Currencycloud API lifecycle

To summarize, each major API version moves through the following stages in its lifecycle:

1. Beta: in development, probably buggy.
2. Latest: the recommended version for new clients.
3. Maintained: no new features, but we'll fix bugs and continue to support clients.
4. Deprecated: all endpoints return 410 Gone.
