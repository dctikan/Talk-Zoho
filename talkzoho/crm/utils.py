from tornado.web import HTTPError


def select_columns(resource, *columns):
    return resource.lower() + '(' + ','.join(columns) + ')'


def unwrap_items(response):
    try:
        result   = response['response']['result']

        # Dont know the resource name but should be the only key
        assert len(result) == 1
        resource = list(result.values())[0]

        # wrap single resource results in array
        rows  = resource['row']
        items = rows if isinstance(rows, list) else [rows]

        return [translate_item(i) for i in items]
    except (AssertionError, KeyError):
        unwrap_error(response)


def unwrap_error(zoho_error):
    try:
        response   = zoho_error['response']
        filtered   = [value for key, value in response.items() if key.lower() != 'url']  # noqa

        # Dont know the error name but should ony be one key left
        assert len(filtered) == 1
        code, message = filtered[0]['code'], filtered[0]['message']

        status_code = http_status_code(zoho_code=code)
        raise HTTPError(status_code, message=message)
    except (AssertionError, KeyError, IndexError):
        raise ValueError("Couldn't parse zoho result")


def http_status_code(*, zoho_code):
    zoho_code = str(zoho_code)

    if zoho_code in ["4000", "4401", "4600", "4831", "4832", "4835", "4101", "4420"]:  # noqa
        return 400  # bad request
    elif zoho_code in ["4501", "4834"]:
        return 401  # unauthorised
    elif zoho_code in ["4502", "4890"]:
        return 402  # payment required
    elif zoho_code in ["4487", "4001", "401", "401.1", "401.2", "401.3"]:
        return 403  # forbidden
    elif zoho_code in ["4102", "4103", "4422"]:
        return 404  # not found
    elif zoho_code in []:
        return 405  # method not allowed
    elif zoho_code in ["4807"]:
        return 413  # payload too large
    elif zoho_code in ["4424"]:
        return 415  # payload too large
    elif zoho_code in ["4101", "4809"]:
        return 423  # locked
    elif zoho_code in ["4820", "4421", "4423"]:
        return 429  # too many requests
    else:
        return 500  # internal server error


def translate_item(item):
    return {kwarg['val']: kwarg['content'] for kwarg in item.get('fl', item.get('FL'))}  # noqa
