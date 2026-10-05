module "vpc" {
  source = "./modules/vpc"
  name   = var.project
  cidr   = var.vpc_cidr
  azs    = var.azs
}

module "app" {
  source             = "./modules/alb_asg"
  name               = var.project
  vpc_id             = module.vpc.vpc_id
  public_subnet_ids  = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids
  instance_type      = var.instance_type
}

module "db" {
  source             = "./modules/rds"
  name               = var.project
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  app_sg_id          = module.app.app_sg_id
  multi_az           = true
}
