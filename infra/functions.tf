resource "google_storage_bucket" "bucket" {
  name     = var.bucket_name
  location = var.region
}

resource "google_cloudfunctions_function" "function" {
  name    = "function-main"
  runtime = "python37"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = "src_${var.release_version}.zip"
  trigger_http          = true
  timeout               = 15
  entry_point           = "add_card_to_trello"
  environment_variables = {
    TRELLO_KEY              = var.trello_key
    TRELLO_TOKEN            = var.trello_token
    TRELLO_LIST_ID_SHOPPING = var.trello_list_shopping
    TRELLO_LIST_ID_TODO     = var.trello_list_todo
  }
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
