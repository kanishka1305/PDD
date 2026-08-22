$base = "c:\Users\skani\Downloads\pdd_app\dental-ai-frontend"
$dirs = @(
  "$base\src\components\layout",
  "$base\src\components\ui",
  "$base\src\pages",
  "$base\src\hooks",
  "$base\src\lib",
  "$base\src\types",
  "$base\public"
)
foreach ($d in $dirs) {
  New-Item -ItemType Directory -Force -Path $d | Out-Null
}
Write-Host "All directories created"
