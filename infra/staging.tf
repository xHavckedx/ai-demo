# Staging efímero por PR — gestionado por la plataforma.
variable "pr" { type = string }
output "url" { value = "https://pr-${var.pr}.staging.local" }
