"""Run checks for terraform-aws-office-365-records."""
import boto3
from botocore.exceptions import ClientError
import logging
import sys
import argparse

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TEST_RESULTS = []


def get_zone_id(domain_name: str) -> tuple:
    """
    Get the zone ID for a given domain name.

    Parameters
    ----------
    domain_name : str
        Domain name to lookup the zone ID for.

    Returns
    -------
    tuple
        Return the ID and the name (as per route53).

    """
    client = boto3.client('route53')
    hosted_zones = client.list_hosted_zones()['HostedZones']
    for zone in hosted_zones:
        if zone['Name'] == f'{domain_name}.':
            return (zone['Id'], zone['Name'])


def get_all_records(zone_id: str) -> list:
    """
    Get all Route53 records for a given zone ID.

    Parameters
    ----------
    zone_id : str
        The zone ID to look up the records for.

    Returns
    -------
    list
        A list of all records for the zone ID.

    """
    client = boto3.client('route53')
    try:
        log.debug(f'Getting records for zone ID {zone_id}')
        response = client.list_resource_record_sets(
            HostedZoneId=zone_id
        )['ResourceRecordSets']

        return response
    except ClientError as err:
        log.error(f'Error getting records: {err}')


def get_records_of_type(records: list, record_type: str) -> list:
    """
    Return a list of records for a given type.

    Parameters
    ----------
    records : list
        All the records for the zone ID.
    record_type : str
        The record type to return.

    Returns
    -------
    list
        The list of records for the given type.

    """
    return [r for r in records if r['Type'] == record_type]


def check_required_records(
        all_records: list, record_type: str, required_records: list):
    """
    Check required records against returned records.

    Parameters
    ----------
    all_records : list
        The result of all records
    record_type : str
        The type of records to check
    required_records : list
        The list of required records

    """
    records = get_records_of_type(all_records, record_type)
    for required in required_records:
        required_name = required['Name']
        required_value = required['Value']
        for r in records:
            if r['Name'] == required['Name']:
                log.debug(
                    f'Found record for {record_type} record { required_name }')
                for rs in r['ResourceRecords']:
                    if rs['Value'] == required_value:
                        required['Result'] = True
        if required['Result'] is True:
            log.info(
            f'\u2713: Found the correct {record_type} record called {required_name} for { required_value }') # noqa: E501
        else:
            log.error(
                f'\u2717: Did not find the correct {record_type} record called {required_name} for { required_value }') # noqa: E501
            log.error(f'These were the records checked: {records}')
        TEST_RESULTS.append(required)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Route53 tests for terraform-aws-office-365-records.') # noqa: E501
    parser.add_argument(
        'domain_name', metavar='D', type=str, help='domain name to use')
    args = parser.parse_args()

    domain_name = args.domain_name
    zone_id, fqdn_domain = get_zone_id(domain_name=domain_name)

    records = get_all_records(zone_id)

    required_txt_records = [
        {
            "Name": fqdn_domain,
            "Value": "\"v=spf1 include:spf.protection.outlook.com -all\"",
            "Result": False
        }
    ]

    check_required_records(
        all_records=records,
        record_type='TXT',
        required_records=required_txt_records)

    required_mx_records = [
        {
            "Name": fqdn_domain,
            "Value": f"0 {domain_name.replace('.', '-')}.mail.protection.outlook.com.", # noqa: E501
            "Result": False
        }
    ]

    check_required_records(
        all_records=records,
        record_type='MX',
        required_records=required_mx_records)

    required_cname_records = [
        {
            "Name": f"sip.{fqdn_domain}",
            "Value": "sipdir.online.lync.com",
            "Result": False
        },
        {
            "Name": f"autodiscover.{fqdn_domain}",
            "Value": "autodiscover.outlook.com",
            "Result": False
        },
        {
            "Name": f"lyncdiscover.{fqdn_domain}",
            "Value": "webdir.online.lync.com",
            "Result": False
        },
        {
            "Name": f"enterpriseregistration.{fqdn_domain}",
            "Value": "enterpriseregistration.windows.net",
            "Result": False
        },
        {
            "Name": f"enterpriseenrollment.{fqdn_domain}",
            "Value": "enterpriseenrollment.manage.microsoft.com",
            "Result": False
        }
    ]

    check_required_records(
        all_records=records,
        record_type='CNAME',
        required_records=required_cname_records
    )

    required_srv_records = [
        {
            "Name": f"_sipfederationtls._tcp.{fqdn_domain}",
            "Value": "100 1 5061 sipfed.online.lync.com.",
            "Result": False
        },
        {
            "Name": f"_sip._tls.{fqdn_domain}",
            "Value": "100 1 443 sipdir.online.lync.com.",
            "Result": False
        }
    ]
    check_required_records(
        all_records=records,
        record_type='SRV',
        required_records=required_srv_records
    )

    for test in TEST_RESULTS:
        if test['Result'] is False:
            log.error('Tests did not complete as expected \u2717')
            sys.exit(1)

    log.info('All Tests Passed \u2713')
