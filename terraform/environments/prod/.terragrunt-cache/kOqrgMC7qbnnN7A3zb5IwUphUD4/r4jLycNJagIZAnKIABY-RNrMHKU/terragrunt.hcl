include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_parent_terragrunt_dir()}/modules//."

  extra_arguments "provider_vars" {
    commands = ["plan", "apply", "destroy"]
    env_vars = {
      KUBE_CONFIG_PATH = "~/.kube/config"
    }
  }
}

inputs = {
  project_id   = "entrevista-nemesisrfl"
  environment  = "prod"
  cluster_name = "crypto-ticker-entrevista"
  region       = "us-central1"
  location     = "us-central1-a"

  network_name = "gke-network"
  subnet_name  = "gke-subnet"
  subnet_cidr  = "10.0.0.0/24"
  pod_cidr     = "192.168.0.0/18"
  svc_cidr     = "192.168.64.0/18"

  node_pools = {
    "prod-pool" = {
      name         = "prod-pool"
      machine_type = "e2-medium"
      node_count   = 1
      disk_size_gb = 30
      labels = {
        "environment" = "prod"
        "pool-type"  = "production"
      }
      taints = [
        {
          key    = "nodeType"
          value  = "prod"
          effect = "PREFER_NO_SCHEDULE"
        }
      ]
    },
    "staging-pool" = {
      name         = "staging-pool"
      machine_type = "e2-medium"
      node_count   = 1
      disk_size_gb = 30
      labels = {
        "environment" = "staging"
        "pool-type"  = "staging"
      }
      taints = [
        {
          key    = "nodeType"
          value  = "staging"
          effect = "PREFER_NO_SCHEDULE"
        }
      ]
    }
  }
} 