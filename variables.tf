variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "FLASK_APP" {
    description = "Location of flask app.py "
}

variable "OAUTH_CLIENT_ID" {
    description = "OAuth client id"
    sensitive = true
}

variable "OAUTH_CLIENT_SECRET" {
    description = "OAuth client secret"
    sensitive = true
}

variable "SECRET_KEY" {
    description = "Azure/Flask var"
    sensitive = true
}

variable "WEBSITES_ENABLE_APP_SERVICE_STORAGE" {
    description = "Azure var"
}

variable "WEBSITES_PORT" {
    description = "Azure/Docker var"
}

variable "LOGGLY_TOKEN" {
    description = "loggly token"
}

variable "LOG_LEVEL" {
    description = "log level"
}
