resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-db-subnets"
  subnet_ids = var.private_subnet_ids
}

resource "aws_security_group" "db" {
  name_prefix = "${var.name}-db-"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [var.app_sg_id]
  }
}

resource "aws_db_instance" "this" {
  identifier                  = "${var.name}-db"
  engine                      = "mysql"
  engine_version              = "8.0"
  instance_class              = "db.t3.micro"
  allocated_storage           = 20
  storage_encrypted           = true
  db_name                     = "appdb"
  username                    = "admin"
  manage_master_user_password = true # password stored in Secrets Manager, not in code
  multi_az                    = var.multi_az
  db_subnet_group_name        = aws_db_subnet_group.this.name
  vpc_security_group_ids      = [aws_security_group.db.id]
  backup_retention_period     = 7
  skip_final_snapshot         = true # demo only
}
