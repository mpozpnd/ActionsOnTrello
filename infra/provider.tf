provider "google" {
  credentials = "${file("~/credentials.json")}"
  project     = "graphium-ml-1"
  region      = "asia-northeast1"
}
