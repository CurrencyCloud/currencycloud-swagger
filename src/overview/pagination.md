# Pagination and Sorting
Some endpoints that return collections allow the number of results to be controlled via the ``page`` and ``per_page`` parameters. These are typically inputted via the URI query string, through in some cases they are included in the body of the HTTP request message. Example:

```
GET /v2/balances/find?page=2&per_page=50
```

The first page of results is page 1, not 0.

Some endpoints also support the sorting and ordering of results, which is controlled via the ``order`` and ``order_asc_desc`` parameters. Example:

```
GET /v2/balances/find?page=2&per_page=50&order=currency&order_asc_desc=desc
```

Where results are paginated, the response payload will include a top-level ``pagination`` object with the following properties:

- ``total_entries``: The total number of items in the complete result set.
- ``total_pages``: The total number of pages of results, which will be 1 or more if the result set is paginated.
- ``current_page``: The current page number.
- ``per_page``: The maximum number of results grouped into a page.
- ``previous_page``: The number of the previous page in the sequence.
- ``next_page``: The number of the next page in the sequence.
- ``order``: The name of the field by which results are ordered.
- ``order_asc_desc``: A value of "asc" or "desc" to indicate whether the results are in ascending or descending order.
