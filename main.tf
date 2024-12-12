terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "Cohort31_AriGib_ProjectExercise"
    storage_account_name = "satfstateagtodo"
    container_name       = "todo-tf-state"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name     = "Cohort31_AriGib_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-tf-wa-ag-todoapp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name     = "agib1/todo-app:latest"
      docker_registry_url   = "https://index.docker.io"
    }
  }

  app_settings = {
    "CONNECTION_STRING" = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
    "DATABASE_NAME" = resource.azurerm_cosmosdb_mongo_database.main.name
    "FLASK_APP" = "${var.FLASK_APP}"
    "OAUTH_CLIENT_ID" = "${var.OAUTH_CLIENT_ID}"
    "OAUTH_CLIENT_SECRET" = "${var.OAUTH_CLIENT_SECRET}"
    "SECRET_KEY" = "${var.SECRET_KEY}"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "${var.WEBSITES_ENABLE_APP_SERVICE_STORAGE}"
    "WEBSITES_PORT" = "${var.WEBSITES_PORT}"
    "LOGGLY_TOKEN" = "{var.LOGGLY_TOKEN}"
    "LOG_LEVEL" = "{var.LOG_LEVEL}"
  }

}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-tf-agib1"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  automatic_failover_enabled = true

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-tf-to-do-db"
  resource_group_name = resource.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = resource.azurerm_cosmosdb_account.main.name

  lifecycle { prevent_destroy = true }
}

