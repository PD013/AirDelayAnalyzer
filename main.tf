terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

variable "project" {
  description = "Project ID"
  type        = string
  default     = "dtc-de-course-412810"
}

variable "region" {
  description = "Region"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
    description = "Bucket Name"
    type        = string
    default     = "de-project-0921"
}

variable "dataset_id" {
    description = "Dataset ID"
    type        = string
    default     = "project"
}

provider "google" {
# Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
#  credentials = 
  project = var.project
  region  = var.region
}



resource "google_storage_bucket" "data-lake-bucket" {
  name          = var.bucket_name
  location      = "US"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dataset_id
  project    = var.project
  location   = "US"
}
