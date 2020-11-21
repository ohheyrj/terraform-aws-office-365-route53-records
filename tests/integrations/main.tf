provider "aws" {
  region  = "eu-west-2"
  version = "2.33.0"
}
resource "aws_route53_zone" "route53_zone" {
  name = "testing.systemsmystery.tech"
}

module "o365" {
  source           = "../.."
  zone_id          = aws_route53_zone.route53_zone.zone_id
  domain_name      = "testing.systemsmystery.tech"
  enable_exchange  = false
  enable_spf       = false
  enable_basic_mdm = false
  enable_s4b       = false
}