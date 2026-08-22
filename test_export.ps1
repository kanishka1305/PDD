Start-Sleep -Seconds 4

Write-Host "=== Testing STL region endpoint ==="
try {
    $r = Invoke-WebRequest -Uri "http://localhost:8000/stl-region/5/condyles" -UseBasicParsing
    Write-Host "STL condyles: Status=$($r.StatusCode)  ContentType=$($r.Headers['Content-Type'])  Bytes=$($r.RawContentLength)"
} catch {
    $msg = $_.Exception.Response
    Write-Host "STL condyles FAILED: $($_.Exception.Message)"
}

Write-Host "=== Testing DICOM export endpoint ==="
try {
    $r2 = Invoke-WebRequest -Uri "http://localhost:8000/export-dicom/5/condyles" -UseBasicParsing
    Write-Host "DICOM condyles: Status=$($r2.StatusCode)  ContentType=$($r2.Headers['Content-Type'])  Bytes=$($r2.RawContentLength)"
} catch {
    Write-Host "DICOM condyles FAILED: $($_.Exception.Message)"
}

Write-Host "=== Testing full STL ==="
try {
    $r3 = Invoke-WebRequest -Uri "http://localhost:8000/stl-region/5/full" -UseBasicParsing
    Write-Host "STL full: Status=$($r3.StatusCode)  Bytes=$($r3.RawContentLength)"
} catch {
    Write-Host "STL full FAILED: $($_.Exception.Message)"
}
