resource "ovh_domain_zone_record" "test" {
    zone = "rouages.xyz"
    subdomain = "test"
    fieldtype = "A"
    target = "91.121.210.84"
}


resource "ovh_domain_zone_record" "forge" {
    zone = "rouages.xyz"
    subdomain = "forge"
    fieldtype = "A"
    target = "91.121.210.84"
    ttl = 0
}
