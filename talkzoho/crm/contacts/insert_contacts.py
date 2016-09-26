from talkzoho.regions import US
from talkzoho.crm.insert_records import insert_records
from talkzoho.crm.contacts import MODULE, PRIMARY_FIELD


async def insert_contacts(records,
                          *,
                          auth_token=None,
                          region=US):
    return await insert_records(
        MODULE,
        primary_field=PRIMARY_FIELD,
        records=records,
        auth_token=auth_token,
        region=region)
