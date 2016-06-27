from talkzoho.regions import US
from talkzoho.crm.filter_module import filter_module
from talkzoho.crm.accounts import MODULE


async def filter_accounts(*,
                          auth_token,
                          term=None,
                          region=US,
                          columns=None,
                          offset=0,
                          limit=None):
    return await filter_module(
        MODULE,
        auth_token=auth_token,
        term=term,
        region=region,
        columns=columns,
        offset=offset,
        limit=limit)
