variable "project_id" {
  description = "The project ID to host the cluster in"
  type        = string
}

variable "environment" {
  description = "The environment this cluster will handle"
  type        = string
}

variable "cluster_name" {
  description = "The name for the GKE cluster"
  type        = string
}

variable "region" {
  description = "The region to host the cluster in"
  type        = string
}

variable "location" {
  description = "The location (region or zone) to host the cluster in"
  type        = string
}

variable "network_name" {
  description = "The VPC network created to host the cluster in"
  type        = string
}

variable "subnet_name" {
  description = "The subnet created to host the cluster in"
  type        = string
}

variable "subnet_cidr" {
  description = "The subnet CIDR"
  type        = string
}

variable "pod_cidr" {
  description = "The CIDR range of the pods"
  type        = string
}

variable "svc_cidr" {
  description = "The CIDR range of the services"
  type        = string
}

variable "node_pools" {
  description = "List of node pool configurations"
  type = map(object({
    name         = string
    machine_type = string
    node_count   = number
    disk_size_gb = number
    labels       = map(string)
    taints = list(object({
      key    = string
      value  = string
      effect = string
    }))
  }))
} 