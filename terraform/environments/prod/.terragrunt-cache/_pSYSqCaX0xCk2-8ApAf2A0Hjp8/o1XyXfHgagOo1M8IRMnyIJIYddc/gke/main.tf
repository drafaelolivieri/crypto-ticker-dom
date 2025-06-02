resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.location
  project  = var.project_id

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  remove_default_node_pool = true
  initial_node_count       = 1

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block = var.master_ipv4_cidr_block
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = "pod-ranges"
    services_secondary_range_name = "service-ranges"
  }

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "0.0.0.0/0"
      display_name = "All"
    }
  }

  depends_on = [
    google_compute_subnetwork.subnet,
    google_compute_router.router,
    google_compute_router_nat.nat
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_container_node_pool" "node_pools" {
  for_each = var.node_pools

  name       = each.value.name
  location   = var.location
  cluster    = google_container_cluster.primary.name
  project    = var.project_id
  node_count = each.value.node_count

  node_config {
    machine_type = each.value.machine_type
    disk_size_gb = each.value.disk_size_gb

    labels = merge(each.value.labels, {
      environment = var.environment
    })

    dynamic "taint" {
      for_each = each.value.taints
      content {
        key    = taint.value.key
        value  = taint.value.value
        effect = taint.value.effect
      }
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  depends_on = [
    google_container_cluster.primary
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_router" "router" {
  name    = var.cloud_router_name
  region  = var.region
  network = google_compute_network.vpc.name
  project = var.project_id

  depends_on = [
    google_compute_network.vpc
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_compute_router_nat" "nat" {
  name                               = var.cloud_nat_name
  router                            = google_compute_router.router.name
  region                            = var.region
  project                           = var.project_id
  nat_ip_allocate_option           = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }

  depends_on = [
    google_compute_router.router
  ]

  lifecycle {
    create_before_destroy = true
  }
} 