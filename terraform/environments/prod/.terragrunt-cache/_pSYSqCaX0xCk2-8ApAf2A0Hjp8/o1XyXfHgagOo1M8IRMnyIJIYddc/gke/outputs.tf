output "cluster_name" {
  description = "Nome do cluster GKE"
  value       = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  description = "The IP address of the cluster master"
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

output "cluster_ca_certificate" {
  description = "The public certificate that is the root of trust for the cluster"
  value       = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

output "node_pools" {
  description = "Informações dos node pools criados"
  value = {
    for name, pool in google_container_node_pool.node_pools : name => {
      name         = pool.name
      node_count   = pool.node_count
      machine_type = pool.node_config[0].machine_type
      labels       = pool.node_config[0].labels
    }
  }
} 