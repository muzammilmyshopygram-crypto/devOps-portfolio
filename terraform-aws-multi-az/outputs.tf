output "alb_dns_name" {
  value = module.app.alb_dns_name
}

output "db_endpoint" {
  value = module.db.endpoint
}
