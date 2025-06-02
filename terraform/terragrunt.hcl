# Configuração do backend local
terraform {
  # Configuração para armazenamento local do estado
  extra_arguments "init_args" {
    commands = [
      "init"
    ]
    arguments = [
      "-backend=true"
    ]
  }
}

# Configuração dos providers
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "google" {
  project = "entrevista-nemesisrfl"
  region  = "us-central1"
  credentials = "${get_parent_terragrunt_dir()}/credentials/service-account.json"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}
EOF
}

# Configuração das versões do Terraform e providers
generate "versions" {
  path      = "versions.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}
EOF
} 