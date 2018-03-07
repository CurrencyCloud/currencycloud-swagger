# Currencycloud API Documentation: Style Guide
This is a style guide for authors and maintainers of the Currencycloud API documentation.

## Language
All documentation is written in American English.


## Keywords
The keywords "must", "must not", "required", "shall", "shall not", "should", "should not", "recommended", "may", and "optional" have special meaning throughout the Currencycloud API documentation. The nuances in the different meanings of these terms have significance in how we explain the behaviour of our web service, and in how client applications are required to behave.

The words "may" and "optional" mean that a client of the API is permitted to, but not required to, behave as described. The words "should" and "recommended" mean that deviation from the described behaviour is more strongly discouraged. The words "required", "must" and "shall" mean that the behaviour described is an absolute requirement, while the words "must not" and "shall not" mean that the behaviour is absolutely prohibited.

These terms need _not_ be written upper case, as they are sometimes in formal specification documents.

For further clarification of this terminology, please refer to [RFC 2119](http://www.ietf.org/rfc/rfc2119.txt).


## Grammatical Person

The OpenAPI definition file is a formal standards document, and it may be consumed in contexts outside of the Currencycloud Developer Center. Descriptions and summaries in this file must be written in an objective academic style, which means writing in the third person. Do not use first person pronouns such as "we" and "our", instead write "Currencycloud". And do not use second person pronouns such as "you" and "your" to refer to the reader, instead refer to the "authenticating user" and other absolute subjects.

The rest of the documentation is more informal and conversational in tone. First and second person pronouns are preferred here.


## Technical Terminology

Our published [glossary](/glossary) provides definitions for financial terms, but not technical terms that our target audience (software engineers) will already be familiar with. Nevertheless, it is important to use technical terms consistently throughout the documentation.

An **endpoint** is a single resource identified by a unique combination of HTTP method and URI path.

An **API** is a collection of endpoints all served from the same base URL. The term "Currencycloud API" therefore refers to all endpoints served from https://api.currencycloud.com (or https://devapi.currencycloud.com in test mode). The term **APIs** is used in the plural only when referring to distinct web services offered by different vendors.

We no longer refer to the "Balances API" or the "Transactions API". Rather, these are **groups** of endpoints within the Currencycloud API that are bundled together in our documentation only for ease of understanding. In the OpenAPI specification, tags are used to define these groups.

The term **request** refers to an HTTP message in its entirety, including the HTTP method, URI path, query string parameters, headers and message body (payload). The term **response** refers to an HTTP response message in its entirety, including its status code, headers, and message body (payload).

We use the term **payload** to refer exclusively to the body content of an HTTP message, and not the whole HTTP message which may embed further content via headers, status codes, and so on. It is good practice to avoid referring to the content type of a payload (JSON, form data). The term payload refers only to the raw parsed data of an HTTP message body, without respect to the particular document format in which the data was encoded during transport. After all, the particular format in which the message body is encoded is commonly abstracted away by client SDKs.

The term **webhooks** is the preferred term to refer to listener endpoints hosted on a client's own servers and to which Currencycloud posts notifications about the changing state of the client's transactions. Webhooks are a specific implementation of **push notifications**, which is a more general term referring to a wider range of technologies that can be used to push messages from a server to a client in real-time.


## URLs
Hyperlinks may be embedded in any of the source Markdown files and in ``description`` values in the ``openapi.yaml`` API definition file. Links are written using GitHub-Flavoured Markdown syntax.

In the Markdown files, URLs to other pages in the Developer Center may be relative to the base URL of the Developer Center, https://developer.currencycloud.com. Relative URLs must start with a forward slash ``/``, example:

```
[Register for an API Key](/register)
```

The OpenAPI file should be treated as a standalone definition of the Currencycloud API, one that may be consumed outside of the context of the Currencycloud Developer Center. For this reason, all URLs in this file must be absolute.

```
[Register for an API Key](https://developer.currencycloud.com/register)
```
