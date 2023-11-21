# main.tf

provider "google" {
  credentials = file("./reflected-oath-405515-70b04b6190ad.json")
  project = "reflected-oath-405515"
  region  = "europe-west3"
}

resource "google_storage_bucket" "my_gcs_bucket" {
  name     = "data_bucket_raw"
  location = "europe-west3"
  #force_destroy = true
}

resource "google_storage_bucket" "my_gcs_bucket2" {
  name     = "data_bucket_processed"
  location = "europe-west3"
  #force_destroy = true
}

variable "gcp_services_account_key" {
  description = "The GCP service account key"
  default = ""
  sensitive = true
}

