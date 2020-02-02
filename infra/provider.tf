provider "google" {
  credentials = var.service_account_key
  project     = "graphium-ml-1"
  region      = "asia-northeast1"
}
