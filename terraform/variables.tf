# variables.tf

variable "credentials_file" {
  description = "Path to the Google Cloud service account key file"
}

variable "project_id" {
  description = "Google Cloud Project ID"
}

variable "region" {
  description = "Google Cloud region"
}

variable "bucket_name" {
  description = "Name of the Google Cloud Storage bucket"
}
