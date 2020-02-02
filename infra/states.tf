terraform {
  backend "gcs" {
    bucket = "graphium-terraform-state-bucket"
  }
}

