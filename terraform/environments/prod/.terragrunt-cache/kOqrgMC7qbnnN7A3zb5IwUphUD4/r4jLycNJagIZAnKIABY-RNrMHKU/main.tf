module "gke" {
  source = "./gke"

  project_id   = var.project_id
  environment  = var.environment
  cluster_name = var.cluster_name
  region       = var.region
  location     = var.location

  network_name = var.network_name
  subnet_name  = var.subnet_name
  subnet_cidr  = var.subnet_cidr
  pod_cidr     = var.pod_cidr
  svc_cidr     = var.svc_cidr

  node_pools = var.node_pools
}

module "monitoring" {
  source = "./monitoring"

  project_id    = var.project_id
  cluster_name  = var.cluster_name
  location      = var.location
} 