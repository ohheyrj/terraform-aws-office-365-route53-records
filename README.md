
# Terraform AWS Office 365 DNS Records

![GitHub release (latest by date)](https://img.shields.io/github/v/release/rj175/terraform-aws-office-365-dns-records?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rj175/terraform-aws-office-365-dns-records/Deployment_test?label=deployment&logo=github&style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rj175/terraform-aws-office-365-dns-records/Linting?label=linting&logo=github&style=flat-square)
![GitHub](https://img.shields.io/github/license/rj175/terraform-aws-office-365-dns-records?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/rj175/terraform-aws-office-365-dns-records?style=flat-square)

This module will create all DNS records required for Office 365. Each component can be turned off individually.


<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Providers

| Name | Version |
|------|---------|
| aws | n/a |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| domain\_name | The full domain name that is being setup | `string` | n/a | yes |
| enable\_basic\_mdm | Create Route53 basic MDM records. | `bool` | `true` | no |
| enable\_exchange | Create Route53 records for exchange. | `bool` | `true` | no |
| enable\_s4b | Create Route53 records for Skype for Business. | `bool` | `true` | no |
| enable\_spf | Create Route53 SPF record for O365. | `bool` | `true` | no |
| verify\_id | The unique ID Microsoft provides to verify your domain, e.g. MS=ms########. Only the numbers are required. | `string` | `""` | no |
| zone\_id | Route53 Zone ID | `any` | n/a | yes |

## Outputs

No output.

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->