provider "aws" {
  region  = "eu-west-2"
  version = "2.33.0"
}

terraform {
  backend "s3" {
    bucket  = "systemsmystery-terraform-testing-statefiles"
    key     = "terraform-s3-backup-bucket/terraform.tfstate"
    region  = "eu-west-2"
    encrypt = "true"
  }
}
resource "aws_route53_zone" "route53_zone" {
  name = "testing.systemsmystery.tech"
}

module "o365" {
  source           = "../.."
  zone_id          = aws_route53_zone.route53_zone.zone_id
  domain_name      = "testing.systemsmystery.tech"
  enable_exchange  = true
  enable_spf       = true
  enable_basic_mdm = true
  enable_s4b       = true
}