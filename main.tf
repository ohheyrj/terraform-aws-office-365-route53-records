locals {
    txt_verify_record = "MS=ms${var.verify_id}"

    spf_record = "v=spf1 include:spf.protection.outlook.com -all"

    txt_records = concat(
        [local.txt_verify_record],
        var.enable_exchange ? [local.spf_record] : []
    )
}

resource "aws_route53_record" "txt" {
  count   = length(var.verify_id) > 0 ? 1 : 0
  zone_id = var.zone_id
  name    = ""
  ttl     = 3600
  records = local.txt_records
  type = "TXT"
}

# Exchange Online

resource "aws_route53_record" "mx_record" {
  count   = var.enable_exchange == true ? 1 : 0
  zone_id = var.zone_id
  name    = ""
  ttl     = 3600
  records = [
    "0 ${replace(var.domain_name, ".", "-")}.mail.protection.outlook.com"
  ]
  type = "MX"
}

resource "aws_route53_record" "cname_autodiscovery" {
  count   = var.enable_exchange == true ? 1 : 0
  zone_id = var.zone_id
  name    = "autodiscover"
  ttl     = 3600
  records = [
    "autodiscover.outlook.com"
  ]
  type = "CNAME"
}

# Skype for Business

resource "aws_route53_record" "cname_sip" {
  count   = var.enable_s4b == true ? 1 : 0
  zone_id = var.zone_id
  name    = "sip"
  ttl     = 3600
  records = [
    "sipdir.online.lync.com"
  ]
  type = "CNAME"
}

resource "aws_route53_record" "cname_lyncdiscover" {
  count   = var.enable_s4b == true ? 1 : 0
  zone_id = var.zone_id
  name    = "lyncdiscover"
  ttl     = 3600
  records = [
    "webdir.online.lync.com"
  ]
  type = "CNAME"
}

resource "aws_route53_record" "srv_sip" {
  count   = var.enable_s4b == true ? 1 : 0
  zone_id = var.zone_id
  name    = "_sip._tls"
  ttl     = 3600
  records = [
    "100 1 443 sipdir.online.lync.com"
  ]
  type = "SRV"
}

resource "aws_route53_record" "srv_sipfederationtls" {
  count   = var.enable_s4b == true ? 1 : 0
  zone_id = var.zone_id
  name    = "_sipfederationtls._tcp"
  ttl     = 3600
  records = [
    "100 1 5061 sipfed.online.lync.com"
  ]
  type = "SRV"
}

# Basic Mobility & Security

resource "aws_route53_record" "cname_enterpriseregistration" {
  count   = var.enable_basic_mdm == true ? 1 : 0
  zone_id = var.zone_id
  name    = "enterpriseregistration"
  ttl     = 3600
  records = [
    "enterpriseregistration.windows.net"
  ]
  type = "CNAME"
}

resource "aws_route53_record" "cname_enterpriseenrollment" {
  count   = var.enable_basic_mdm == true ? 1 : 0
  zone_id = var.zone_id
  name    = "enterpriseenrollment"
  ttl     = 3600
  records = [
    "enterpriseenrollment.manage.microsoft.com"
  ]
  type = "CNAME"
}