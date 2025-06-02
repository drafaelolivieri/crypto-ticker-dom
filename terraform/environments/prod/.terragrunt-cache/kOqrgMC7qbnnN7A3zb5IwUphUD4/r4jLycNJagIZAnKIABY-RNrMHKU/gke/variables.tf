variable "project_id" {
  description = "The project ID to host the cluster in"
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

variable "cluster_name" {
  description = "The name of the cluster"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "node_pools" {
  description = "Map of node pool configurations"
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

variable "network_name" {
  description = "The name of the VPC network"
  type        = string
}

variable "subnet_name" {
  description = "The name of the subnet"
  type        = string
}

variable "subnet_cidr" {
  description = "The CIDR range for the subnet"
  type        = string
}

variable "master_ipv4_cidr_block" {
  description = "The IP range in CIDR notation for the master network"
  type        = string
  default     = "172.16.0.0/28"
}

variable "pod_cidr" {
  description = "The CIDR range for pods"
  type        = string
}

variable "svc_cidr" {
  description = "The CIDR range for services"
  type        = string
}

variable "enable_cloud_nat" {
  description = "Whether to enable Cloud NAT for the cluster"
  type        = bool
  default     = true
}

variable "cloud_nat_name" {
  description = "Name of the Cloud NAT"
  type        = string
  default     = "gke-nat"
}

variable "cloud_router_name" {
  description = "Name of the Cloud Router"
  type        = string
  default     = "gke-nat-router"
} 